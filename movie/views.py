from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin

from .forms import MovieForm
from .models import MovieReview, MovieComment

import requests
import os

baseURL = 'https://api.themoviedb.org/3'
api_key = os.environ.get("MOVIE_DB_API")


class CreateView(View):
    def get(self, request):
        form = MovieForm
        return render(request, "movie/create.html", {"form": form})

    def post(self, request):
        cover = request.FILES.get('cover', False)
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.creator = request.user
            poster_path = request.POST.get("poster_path")
            if poster_path:
                pic_url = "https://image.tmdb.org/t/p/w300"+poster_path
                pic_request = requests.get(pic_url, stream=True)
                if pic_request.status_code == requests.codes.ok:
                    file_name = request.POST.get("movie_name")+".jpg"
                    fp = BytesIO()
                    fp.write(pic_request.content)
                    movie.cover.save(file_name, fp)
            else:
                movie.save()
            id = movie.pk
            return HttpResponseRedirect(reverse('movie:detail', args=(id, )))
        else:
            # messages.warning(request, f'Error: Something Wrong With You Input')
            return render(request, "movie/create.html", {'form': form, 'poster_path': request.POST.get("poster_path")})


class HomeListView(ListView):
    model = MovieReview
    template_name = 'movie/home.html'
    context_object_name = "MovieCollection"
    paginate_by = 3


class MovieDetailView(DetailView, MultipleObjectMixin):
    model = MovieReview
    template_name = 'movie/detail.html'
    context_object_name = "moviereview"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # object_list = MovieComment.objects.filter(comment=self.get_object())
        object_list = self.get_object().comment.all()
        # for obj in object_list:
        #    print(obj.contributor)
        context = super(MovieDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        #print(request.POST.get("comment"))
        cmt = MovieComment(contributor=request.user, comment=request.POST.get("comment"))
        cmt.save()
        self.get_object().comment.add(cmt)
        return HttpResponseRedirect(reverse('movie:detail', args=(self.get_object().id, )))





def popular(request):
    result = GetMovieInfo(route="/movie/popular", max=20)
    return JsonResponse(result)


def search(request):
    queryString = request.GET.dict()
    # print(request.GET)
    result = GetMovieInfo(route="/search/movie", params=queryString)
    return JsonResponse(result)


def GetMovieInfo(route, max=-1, params={}):
    PARAMS = {'api_key': api_key}
    PARAMS.update(params)
    URL = baseURL + route
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    result = {}
    if max != -1:
        length = max
    else:
        length = len(data["results"])
    for i in range(length):
        temp_list = [{
            "release_date": data["results"][i]["release_date"],
            "rating": data["results"][i]["vote_average"],
            "movie_name": data["results"][i]["title"],
            "overview": data["results"][i]["overview"],
            "poster_path": data["results"][i]["poster_path"],
        }]
        result[str(i)] = temp_list
    hashmap = {}
    for key, value in result.items():
        if value[0]["movie_name"] in hashmap:
            hashmap[value[0]["movie_name"]].append(int(key))
        else:
            hashmap[value[0]["movie_name"]] = [int(key)]
    for value in hashmap.values():
        if len(value) > 1:
            for i in value:
                result[str(i)][0]["movie_name"] += " (" + result[str(i)][0]["release_date"] + ")"
    return result
