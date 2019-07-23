from django.urls import path
from . import views

app_name = "share"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('download/<int:videoId>/', views.download, name="download"),
    path('search/', views.ListView.as_view(), name="search"),
    path('delete/<int:videoId>', views.delete, name="delete")
]