from django.urls import path
from . import views

app_name = 'crabgame'
urlpatterns = [
    path('', views.index, name='index'),
    path('image/<int:image_id>/', views.detail, name='detail'),
    path('result/<int:session_id>/', views.result, name='result'),
]