from django.shortcuts import render
from django.http import HttpResponse
from .models import Workout
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy


@login_required
def review(request):
    context = {"workouts": Workout.objects.all()}
    return render(request, "workouts/review_workouts.html", context)


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    context_object_name = "workouts"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        )  # Filter the queryset to only include objects created by the current user


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        )  # Add a filter to ensure the object also belongs to the current user


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = "workouts/post_workout.html"
    fields = ["workout_type", "duration", "distance", "pace", "intensity", "calories"]

    def form_valid(self, form):
        """Automatically set the user to the logged-in user"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        """
        return reverse("workout-detail", kwargs={"pk": self.object.pk})


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    fields = ["workout_type", "duration", "distance", "pace", "intensity", "calories"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class WorkoutDeleteView(LoginRequiredMixin, DeleteView): 
    model = Workout
    success_url = reverse_lazy('workouts-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    