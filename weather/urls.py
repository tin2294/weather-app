from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.weather_view, name="weather"),
    path('create/', views.create_weather_data, name='create_weather'),
    path('list/', views.list_weather_data, name='list_weather'),
    path('update/<int:pk>/', views.update_weather_data, name='update_weather_data'),
    path('delete/<int:pk>/', views.delete_weather_data, name='delete_weather_data'),
]
