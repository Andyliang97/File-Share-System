from django import forms
from .models import MovieReview


class MovieForm(forms.ModelForm):

    class Meta:
        model = MovieReview
        fields = ['movie_name', 'release_date', 'rating', 'overview', 'cover']

    def clean_rating(self):
        rating=self.cleaned_data['rating']
        if rating > 10 or rating < 0:
            raise forms.ValidationError("This is not a valid rating")
        return rating
