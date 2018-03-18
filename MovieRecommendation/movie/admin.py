from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Movie, Rating

class RatingInline(admin.TabularInline):
	model = Rating
	extra = 3

class MovieAdmin(admin.ModelAdmin):
	fieldsets = [
		(None            , {'fields': ['title']}),
		('IMDB ID'       , {'fields': ['imdb_id']}),
		('Genres'        , {'fields': ['genres']  , 'classes': ['collapse']}),
		('Published Year', {'fields': ['pub_year'], 'classes': ['collapse']}),
		('Latent Factor',  {'fields': ['latent_factor']}),
	]
	inlines = [RatingInline]
	list_display = ('title', 'pub_year', 'get_ave_rating')
	list_filter = ['genres']
	search_fields = ['title']
	ordering = ('-pub_year',)

admin.site.register(Movie, MovieAdmin)