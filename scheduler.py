"""Schedules all checker jobs"""
import datetime
from typing import Callable

import apscheduler.schedulers.background as back_scheduler
import apscheduler.triggers.cron as triggers


import db
import db_service
import url_checker

# scheduler = back_scheduler.BlockingScheduler()
scheduler = back_scheduler.BackgroundScheduler()


def test_job(text):
    print(f"{datetime.datetime.now()}: {text}")


def add_job(job: Callable, kwargs: dict, cron: str):
    scheduler.add_job(
        job,
        triggers.CronTrigger.from_crontab(cron),
        kwargs=kwargs)


def start():
    scheduler.start()


def reschedule_all():
    """Delete all jobs and add all it from the DB"""
    conn = db.DBConn.get_conn()
    wesites_list = db_service.read_websites(conn)
    for website in wesites_list:
        scheduler.add_job(test_job,
                          triggers.CronTrigger.from_crontab("* * * * *"),
                          kwargs={"text": "One minute!!!"})

    scheduler.add_job(test_job, triggers.CronTrigger.from_crontab("* * * * *"), kwargs={"text": "One minute!!!"})
    scheduler.add_job(test_job, triggers.CronTrigger.from_crontab("*/2 * * * *"), kwargs={"text": "Two minute!!!"})
    scheduler.start()


# reschedule_all()
