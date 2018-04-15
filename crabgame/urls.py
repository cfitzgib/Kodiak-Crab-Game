from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:crab_sample>/', views.playCrabImg, name='playCrabImg'),
]