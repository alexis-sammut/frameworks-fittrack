from django.urls import path
from . import views
from .views import (
    WorkoutListView,
    WorkoutDetailView,
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
)

urlpatterns = [
    path("log/", WorkoutCreateView.as_view(), name="log-workout"),
    path("review/", views.review, name="review-workouts"),
    path("list/", WorkoutListView.as_view(), name="workouts-list"),
    path("<int:pk>/", WorkoutDetailView.as_view(), name="workout-detail"),
    path("<int:pk>/update/", WorkoutUpdateView.as_view(), name="workout-update"),
    path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout-delete'),
]
