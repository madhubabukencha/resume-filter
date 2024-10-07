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
        trigger=CronTrigger(minute="*/1"),  # Runs at every one minutes
        id="process_documents",
        max_instances=1,  # Only one instance can run at a time
        replace_existing=True,  # Replace existing job if already exists
        misfire_grace_time=300,  # Allow a grace period of 5 minutes
        coalesce=True,  # If multiple triggers missed, only run once
        args=[None,]
    )

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(minute="*/25"),  # Runs in every 25 minutes
        id="delete_old_job_executions",
        max_instances=1,  # Only one instance can run at a time
        replace_existing=True,  # Replace existing job if already exists
        misfire_grace_time=300,  # Allow a grace period of 5 minutes
        coalesce=True,  # If multiple triggers missed, only run once
    )
    register_events(scheduler)
    # Start the scheduler
    scheduler.start()

    logger.info("Scheduler started...")
