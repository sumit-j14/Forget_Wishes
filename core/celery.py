from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# celery beat settings
app.conf.beat_schedule = {
    'send_mail_at_00': {
        'task': 'celery_tasks.tasks.send_mail_celery',
        'schedule': crontab(hour=0, minute=0, day_of_week='1-7')
        # 'args' : 'default argument'
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
