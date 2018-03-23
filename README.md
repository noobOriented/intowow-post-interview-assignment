# Intowow post-interview assignment

A Movie Recommendation Website 

## Getting Started
### Prerequisites
  - Python 3.6 https://www.python.org
  - Jupyter Notebook 5.0.0 http://jupyter.readthedocs.io/en/latest/install.html
  - Django 2.0.2 https://docs.djangoproject.com/en/2.0/intro/install/
  - django-extensions https://django-extensions.readthedocs.io/en/latest/
  - Tensorflow 1.0.0 https://www.tensorflow.org/install/
  - Keras 2.1.4 https://keras.io/#installation
  - PostgreSQL 10.3 https://wiki.postgresql.org/wiki/Detailed_installation_guides
  - Redis 2.10.6 https://redis.io/download
  - Celery 4.1.0 http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#installing-celery
### Dataset
  Download the Movie-Lens Full dataset and save it as /ml-latest
  - MovieLens Full: https://grouplens.org/datasets/movielens/latest/
  
### Run
  - Move under /MovieRecommendation:
  - Building database:
    1. Database migration
        ```bash
        $ python manage.py makemigrations
        $ python manage.py migrate
        ```
    2. Data processing, feeding and model training
        ```bash
        $ python manage.py shell_plus --notebook
        ```
  - Run server:
    Run on 4 individual command windows under /MovieRecommendation:
    ```bash
    $ redis-server
    ```
    ```bash
    $ celery -A MovieRecommendation worker -l info
    ```
    ```bash
    $ celery -A MovieRecommendation beat -l info
    ```
    ```bash
    $ python manage.py runserver
    ```
