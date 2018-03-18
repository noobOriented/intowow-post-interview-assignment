from django.contrib import auth
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic
from movie.models import Movie, Rating
from django.db.models import Avg
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from .cf_model import gradient_descent, get_ranking
import json



class HomeView(generic.ListView):
	context_object_name = 'movie_list'
	extra_context = {'omdb_api_url': settings.OMDB_API_URL}

	def get_queryset(self):
		'''
		shows different context to login/guest user.
		'''
		user = self.request.user
		if user.is_authenticated and cache.has_key('ranking__%d' % user.id):
			cache_key = 'ranking__%d' % user.id
			self.template_name = 'home.html'
		else:
			cache_key = 'sorted_rating'
			self.template_name = 'home_guest.html'

		result = cache.get(cache_key)
		return result

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		if user.is_authenticated:
			context['serialized_movie_list']= json.dumps(serialize_movie_model_object(context['movie_list']),
												   cls=DjangoJSONEncoder)
			context['serialized_rated_list'] = json.dumps(serialize_rating_object(user.rating_set.all()),
														  cls=DjangoJSONEncoder)

		return context

def serialize_rating_object(rating_models):
	result = []
	for rating in rating_models:
		elements = {'movie_title': rating.movie.title,
					'score': '%.1f' % rating.score}
		result.append(elements)

	return result

def serialize_movie_model_object(movie_objects):
	result = []
	for movie in movie_objects:
		elements = {'id': movie.id,
					'title': movie.title,
					'imdb_id': '%07d' % movie.imdb_id,
					'ave_rating': '%.1f' % movie.get_ave_rating,}
		result.append(elements)

	return result

def rating(request, movie_id):
	'''
	Update the ranking to models and compute new ranking for users.
	'''
	new_rating = Rating(pub_date=timezone.now(), movie=Movie.objects.get(pk=movie_id),
						user=request.user, score=request.POST['score'])
	print(new_rating)
	gradient_descent(new_rating)
	new_rating.save()

	movie_list = serialize_movie_model_object(get_ranking(request.user))
	rated_list = serialize_rating_object(request.user.rating_set.all())

	context = {'omdb_api_url': settings.OMDB_API_URL,
			   'movie_list': movie_list,
			   'rated_list': rated_list,}
	return JsonResponse(context)