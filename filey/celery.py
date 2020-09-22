from __future__ import absolute_import

import os

from celery import Celery
from filey.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filey.settings')
app = Celery(
    'filey',
    broker=CELERY_BROKER_URL,
    include=['filey.tasks']
)

app.conf.update(
    result_expires=3600,
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
