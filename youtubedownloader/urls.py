from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('download/start/', views.start_download, name='start_download'),
    path('download/cancel/', views.stop_download, name='stop_download'),
]