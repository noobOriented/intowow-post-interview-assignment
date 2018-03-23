import numpy as np
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Avg
from .models import Movie, Rating

User = get_user_model()

cf_model_config = {'k_factors': 30,
				   'user_weight_learning_rate': 0.3,
				   'user_bias_learning_rate': 0.1,
				   'movie_learning_rate': 0.01,
				   'rating_mean': 3.5533,}

def gradient_descent(new_rating):
	'''
	Update the Matrix Factorization Model.
	'''
	user_weight_learning_rate = cf_model_config['user_weight_learning_rate']
	user_bias_learning_rate = cf_model_config['user_bias_learning_rate']
	movie_learning_rate = cf_model_config['movie_learning_rate']
	rating_mean  = cf_model_config['rating_mean']

	user = new_rating.user
	movie = new_rating.movie
	v_u = np.array(user.latent_factor, dtype='float64')
	movie_matrix = cache.get('movie_latent_matrix')
	v_m = movie_matrix[movie.id, :]

	pred_score = np.dot(v_u[1:], v_m[1:]) + v_u[0] + v_m[0] + rating_mean 
	error = pred_score - float(new_rating.score)

	# weights update
	v_u[1:] -= user_weight_learning_rate * error * v_m[1:]
	v_m[1:] -= movie_learning_rate * error * v_u[1:]

	# bias update
	v_u[0] -= user_bias_learning_rate * error
	v_m[0] -= movie_learning_rate * error

	movie_matrix[movie.id, :] = v_m
	cache.set('movie_latent_matrix', movie_matrix)
	user.latent_factor = v_u.tolist()
	movie.latent_factor = v_m.tolist()
	user.save(update_fields=['latent_factor'])
	movie.save(update_fields=['latent_factor'])

def get_ranking(user, movie_set=None):
	'''
	Compute the recommending rank for user.
	'''
	movie_matrix = cache.get('movie_latent_matrix')
	v_u = np.array(user.latent_factor)
	score = np.dot(movie_matrix[:, 1:], v_u[1:]) + movie_matrix[:, 0] + v_u[0]
	has_rated = list(user.movie_set.values_list('id', flat=True))
	# remove the rated
	score[has_rated] = -100.0
	result_index = np.argpartition(score, -5)[-5:]
	if movie_set is None:
		movie_set = cache.get('movie_set_with_ave_rating')
	result = movie_set.filter(id__in=result_index)
	return result

def cache_movie_set():
	'''
	Preload movie latent factors to numpy matrix to reduce DB accessing.
	'''
	k_factors = cf_model_config['k_factors']
	movie_matrix = np.array([[0] * (1 + k_factors)] + list(Movie.objects.values_list('latent_factor', flat=True)))
	cache.set('movie_latent_matrix', movie_matrix)

	movie_set_with_ave_rating = Movie.objects.annotate(ave_rating=Avg('rating__score'))
	cache.set('movie_set_with_ave_rating', movie_set_with_ave_rating)

def cache_recommend_list():
	'''
	Compute the recommending rank for guest by average rating score.
	'''
	cache_time = 30
	movie_set_with_ave_rating = cache.get('movie_set_with_ave_rating')
	top_5 = movie_set_with_ave_rating.order_by('-ave_rating', '-pub_year')[:5]
	cache.set('sorted_rating', top_5, cache_time)
	for user in User.objects.all():
		cache_key = 'ranking__%d' % user.id
		result = get_ranking(user, movie_set_with_ave_rating)
		cache.set(cache_key, result)
