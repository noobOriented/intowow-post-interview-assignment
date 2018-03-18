from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
User = get_user_model()

class Genre(models.Model):
	genre_text = models.CharField(max_length=32, unique=True)

	def __str__(self):
		return self.genre_text

	class Meta:
		ordering = ('genre_text',)

class Movie(models.Model):
	title = models.TextField()
	genres = models.ManyToManyField(Genre)
	imdb_id = models.IntegerField(blank=True, null=True)
	tmdb_id = models.IntegerField(blank=True, null=True)
	rated_by = models.ManyToManyField(User,
		through='Rating',
		through_fields=('movie', 'user')
	)
	pub_year = models.IntegerField(blank=True, null=True)
	latent_factor = JSONField(blank=True, null=True)

	def __str__(self):
		return self.title

	@property
	def get_ave_rating(self):
		return self.rating_set.all().aggregate(models.Avg('score'))['score__avg']

	class Meta:
		ordering = ('id',)

class Rating(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	score = models.DecimalField(max_digits=2, decimal_places=1)
	pub_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return 'User#%s -> Movie#%s: %.2f' % (self.user_id, self.movie_id, float(self.score))

