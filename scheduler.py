"""
Scheduler service

Import as:
import scheduler
"""
from typing import Callable

import apscheduler.schedulers.background as back_scheduler
import apscheduler.triggers.cron as triggers

scheduler = back_scheduler.BackgroundScheduler()


def add_job(job: Callable, kwargs: dict, cron: str) -> None:
    """
    Add a job to a scheduler.

    :param job: Callable function to add
    :param kwargs: Dict with parameters which passed to the job
    :param cron: Cron string for scheduling period
        Example: '*/2 * * * *' = one time in two minutes
    :return:
    """
    scheduler.add_job(
        job,
        triggers.CronTrigger.from_crontab(cron),
        kwargs=kwargs)


def start() -> None:
    """Helper for starting the scheduler"""
    scheduler.start()
