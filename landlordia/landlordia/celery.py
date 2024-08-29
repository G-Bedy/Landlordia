from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landlordia.settings')

app = Celery('landlordia')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-and-send-payment-reminders': {
        'task': 'realestate.tasks.check_and_send_payment_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
}

app.conf.timezone = settings.CELERY_TIMEZONE
