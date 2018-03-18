import os
from celery import Celery
from django.conf import settings
from celery.utils.log import get_task_logger
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieRecommendation.settings')

app = Celery('MovieRecommendation')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.formant(self.request))

