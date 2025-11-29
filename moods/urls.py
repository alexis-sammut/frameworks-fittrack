from django.urls import path
from . import views
from .views import (
    MoodListView,
    MoodDetailView,
    MoodCreateView,
    MoodUpdateView,
    MoodDeleteView,
)

urlpatterns = [
    path("log/", MoodCreateView.as_view(), name="log-mood"),
    path("review/", views.review, name="review-moods"),
    path("list/", MoodListView.as_view(), name="moods-list"),
    path("<int:pk>/", MoodDetailView.as_view(), name="mood-detail"),
    path("<int:pk>/update/", MoodUpdateView.as_view(), name="mood-update"),
    path('<int:pk>/delete/', MoodDeleteView.as_view(), name='mood-delete'),
]

    