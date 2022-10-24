from datetime import datetime

import redis
from flask import render_template, redirect, url_for, flash, request
from rq import Queue
from rq.job import Job
from rq_scheduler import Scheduler

from . import app
from .forms import JobForm, ScheduledJobForm
from .tasks import example

r = redis.Redis()
q = Queue(connection=r)
sched = Scheduler(connection=r)


@app.route("/")
def index():
    finished = [
        Job.fetch(i, connection=r) for i in q.finished_job_registry.get_job_ids()
    ]
    scheduled = list(sched.get_jobs())
    return render_template(
        "index.jinja2", queued=q.jobs, finished=finished, scheduled=scheduled
    )


@app.route("/example")
def example_job():
    job = q.enqueue(example.sleep_fixed)
    flash(f"Job ({job.id}) added to queue at {job.enqueued_at}")
    return redirect(url_for("index"))


@app.route("/simple", methods=["GET", "POST"])
def simple_job():
    form = JobForm(request.form)
    if request.method == "POST" and form.validate():
        if form.args.data:
            job = q.enqueue(eval(form.job.data), form.args.data)
        else:
            job = q.enqueue(eval(form.job.data))
        flash(f"Job ({job.id}) added to queue at {job.enqueued_at}")
    return render_template("simple_job.jinja2", form=form)


@app.route("/simple/cancel/<job_id>")
def simple_job_cancel(job_id: str):
    job = Job.fetch(job_id, connection=r)
    job.cancel()
    flash("job canceled")
    return redirect(url_for("index"))


@app.route("/scheduled", methods=["GET", "POST"])
def scheduled_job():
    form = ScheduledJobForm(request.form)
    if request.method == "POST" and form.validate():
        job = sched.schedule(
            scheduled_time=datetime.utcnow(),
            func=eval(form.job.data),
            args=[form.args.data] if form.args.data else [],
            interval=form.interval.data * 60,
            repeat=None if form.repeat.data == 0 else form.repeat.data,
        )
        flash(f"Job ({job.id}) added to queue at {job.enqueued_at}")
    return render_template("scheduled_job.jinja2", form=form)


@app.route("/scheduled/cancel/<job_id>")
def scheduled_job_cancel(job_id: str):
    sched.cancel(job_id)
    flash("scheduled job canceled")
    return redirect(url_for("index"))
