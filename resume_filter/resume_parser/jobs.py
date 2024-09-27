"""
This script helps to schedule your backend tasks.
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import (DjangoJobStore,
                                          register_events)
from django_apscheduler.models import DjangoJobExecution
from .views import process_documents


# Set up logger
logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age: int = 86400) -> None:
    """
    This function helps to all the job execution records which
    are older than one day

    :param max_age: seconds
    :type  max_age: int

    :rtype : None
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start_scheduler() -> None:
    """
    Schedule the jobs
    """
    scheduler = BackgroundScheduler()

    # Use Django job store to store the jobs in the database
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Example of adding a job with a cron trigger
    scheduler.add_job(
        process_documents,
        trigger=CronTrigger(minute="*/5"),  # Runs at every two minutes
        id="process_documents",
        # only one instance of the job can run at any given time.
        # If the job is still running when its next scheduled run
        # time comes around, the next instance of the job will be skipped.
        # Keep one is good if you are writing something to databse
        # to avoid conflicts
        max_instances=1,
        # does not stop or interrupt a job that is already running.
        # It only updates the job's configuration for future executions.
        replace_existing=True,
        args=[None,]
    )

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(minute=0),  # Runs at every every hour
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    # Start the scheduler
    scheduler.start()

    logger.info("Scheduler started...")
