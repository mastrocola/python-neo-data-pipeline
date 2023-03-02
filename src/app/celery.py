from celery import Celery
from celery.schedules import crontab
from src.functions import neo
from src.services.logger import Log
from src.settings import PROJECT, REDIS_URL
from src.utils.exec_task import exec_task

app = Celery(PROJECT, broker=REDIS_URL)


@app.on_after_configure.connect
# pylint: disable=unused-argument
def setup_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=12), get_feed_data)

    Log().info('SCHEDULE_TASKS_ADDED', 'Tasks added successfully')


@app.task
def get_feed_data():
    exec_task(neo.get_feed_data)
