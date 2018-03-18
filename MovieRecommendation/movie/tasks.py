from celery import task
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from datetime import timedelta
from .cf_model import init_matrix, cache_recommend_list


logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(seconds=10))
def periodicly_ranking():
	init_matrix()
	cache_recommend_list()
	logger.info('Updated recommend result.')
