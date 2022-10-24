import csv
from rq_scheduler import Scheduler
from redis import Redis
from rq import Queue
from datetime import datetime
from osint_gatherer.tasks.twitter import get_names_update


scheduler = Scheduler(connection=Redis())

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=get_names_update,
    interval=3 * 86400,
    repeat=None,
)

# scheduler.schedule(
#     scheduled_time=datetime.utcnow(),
#     func=get_names_first,
#     repeat=1,
# )
