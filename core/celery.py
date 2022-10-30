from celery import Celery
from celery.schedules import crontab
from settings import settings

celery_app = Celery(
    'weather_worker',
    broker=settings.broker,
    backend=settings.broker
)


celery_app.conf.beat_schedule = {
    'send_mail_every_hour': {
        'task': 'Send_mail_every_hour',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'send_mail_three_hours': {
        'task': 'Send_mail_every_three_hours',
        'schedule': crontab(minute=0, hour='*/3'),
    },
    'send_mail_five_hours': {
        'task': 'Send_mail_every_five_hours',
        'schedule': crontab(minute=0, hour='*/5'),
    },
    'update_weather': {
        'task': 'Update_weather',
        'schedule': crontab(minute=0, hour='*/1')
    }

}