from django.urls import path
from . import views

urlpatterns = [
    path('log', views.log, name='log-workouts'),
    path('review/',views.review, name='review-workouts'),
]