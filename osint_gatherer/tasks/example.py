import time

from rq import get_current_job


def sleep_fixed():
    job = get_current_job()
    job.meta["something"] = "foo"
    job.save_meta()
    time.sleep(5)
    return "42"

def sleep_time(t: str):
    time.sleep(int(t))
    return t
