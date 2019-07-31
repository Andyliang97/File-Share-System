from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User

# Create your models here.


class MovieReview(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=256, verbose_name="Movie Name", default="")
    release_date = models.DateField(default=date.today, verbose_name="Release Date")
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    overview = models.TextField()
    cover = models.ImageField(upload_to="Movie", blank=True)

    class Meta:
        verbose_name = "Movie Information"
        db_table = "Movie Info"

    def __str__(self): # the name we are going to see while query
        return self.movie_name
