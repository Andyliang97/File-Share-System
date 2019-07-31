from django import forms
from .models import MovieReview


class MovieForm(forms.ModelForm):

    class Meta:
        model = MovieReview
        fields = ['movie_name', 'release_date', 'rating', 'overview', 'cover']
