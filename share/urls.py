from django.urls import path
from . import views


app_name = "share"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('upload/', views.UploadView.as_view(), name="upload"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('download/<int:videoId>/', views.download, name="download"),
    path('search/', views.ListView.as_view(), name="search"),
    path('delete/<int:videoId>', views.delete, name="delete"),
    path('image/', views.image, name="image"),
    path('checkpagination/', views.check_pagination, name="checkpagination"),
]

