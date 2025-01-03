import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cweather.settings")

app = Celery("cweather")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-every-15-minutes": {
        "task": "djstorm.tasks.fetch_all",
        "schedule": crontab(minute="*/2"),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@beat_init.connect
def at_start(sender, **kwargs):
    from djstorm.tasks import fetch_all

    fetch_all.delay()
