# Intowow post-interview assignment
(two-week project)
A Movie Recommendation Website providing the following features:
1) For guest users (user not logged in), the website recommend movies with highest average ratings
2) Users can sign-up for a new account, providing his/her
   * email
   * password
3) Users can sign-in with his/her (email, password) pair
4) After signing-in, the website will 
   1) Show movies which have been rated by the user.
   2) Recommend a list of movies, which have not been rated by the user.
5) For each recommended movie, user can rate it on a 1 star-5 stars scale.
6) After the movie is rated, it is removed from the recommendation list.
7) The website will remember these ratings, combine them with existing movie rating data,
   and recompute the recommendation model on a periodical basis.
8) The recommendation list will dynamically reloads itself based on the up-to-date model.
   

![home](https://raw.githubusercontent.com/noobOriented/intowow-post-interview-assignment/master/images/home.png)

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
