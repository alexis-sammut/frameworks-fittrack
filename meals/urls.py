from django.urls import path
from . import views
from .views import (
    MealListView,
    MealDetailView,
    MealDeleteView,
)

urlpatterns = [
    path("log/", views.log_meal, name="log-meal"),
    path("review/", views.review, name="review-meals"),
    path("list/", MealListView.as_view(), name="meals-list"),
    path("<int:pk>/", MealDetailView.as_view(), name="meal-detail"),
    path("<int:pk>/update/", views.update_meal, name="meal-update"),
    path('<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),
]