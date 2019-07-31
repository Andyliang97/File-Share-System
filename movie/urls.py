from django.urls import path
from . import views as movie_views


app_name = "movie"
urlpatterns = [
    path('create/', movie_views.CreateView.as_view(), name="create"),
    path('popular/', movie_views.popular, name="popular"),
    path('search/', movie_views.search, name="search"),
    path('detail/<pk>/', movie_views.MovieDetailView.as_view(), name="detail"),
    path('', movie_views.HomeListView.as_view(), name="home"),
]
