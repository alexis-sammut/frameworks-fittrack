from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log, name='log-workout'),
    path('review/',views.review, name='review-workouts'),
]