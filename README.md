# Intowow post-interview assignment

A Movie Recommendation Website 

## Getting Started
### Prerequisites
  - Python 3.6
  - Django 2.0.2 https://github.com/django/django
  - Tensorflow 1.0.0
  - Keras 2.1.4
  - PostgreSQL 10.3
  - Redis 2.10.6
  - Celery 4.1.0
  
### Dataset
  Download the Movie-Lens Full dataset and save it as /ml-latest
  - MovieLens Full: https://grouplens.org/datasets/movielens/latest/
  
### Run
  Run four shell script under /MovieRecommandetion directory:
  '''
    redis-server
  '''
  '''
    celery -A MovieRecommendation worker -l info
  '''
  '''
    celery -A MovieRecommendation beat -l info
  '''
  '''
    python manage.py runserver
  '''
