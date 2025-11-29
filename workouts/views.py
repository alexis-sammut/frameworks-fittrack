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
from django.db.models import Avg, Sum, Count

@login_required
def review(request):
    workouts = Workout.objects.filter(user=request.user)
    
    # Overall statistics
    total_workouts = workouts.count()
    total_calories = workouts.aggregate(Sum('calories'))['calories__sum'] or 0
    total_minutes = workouts.aggregate(Sum('duration'))['duration__sum'] or 0
    avg_calories = workouts.aggregate(Avg('calories'))['calories__avg'] or 0
    avg_minutes = workouts.aggregate(Avg('duration'))['duration__avg'] or 0
    
    # Statistics per workout type
    workout_stats = {}
    
    # Distance-based workouts 
    for workout_type in ['Running', 'Walking', 'Cycling']:
        filtered = workouts.filter(workout_type=workout_type)
        count = filtered.count()
        if count > 0:
            workout_stats[workout_type.lower()] = {
                'count': count,
                'avg_calories': filtered.aggregate(Avg('calories'))['calories__avg'] or 0,
                'avg_minutes': filtered.aggregate(Avg('duration'))['duration__avg'] or 0,
                'avg_distance': filtered.aggregate(Avg('distance'))['distance__avg'] or 0,
                'avg_pace': filtered.aggregate(Avg('pace'))['pace__avg'] or 0,
            }
        else:
            workout_stats[workout_type.lower()] = {
                'count': 0,
                'avg_calories': 0,
                'avg_minutes': 0,
                'avg_distance': 0,
                'avg_pace': 0,
            }
    
    # Intensity-based workouts
    intensity_types = {
        'Rowing': 'rowing',
        'Swimming': 'swimming',
        'Hiking': 'hiking',
        'Yoga': 'yoga',
        'Pilates': 'pilates',
        'HIIT': 'hiit',
        'Strength Training': 'strength'
    }
    
    for workout_type, key in intensity_types.items():
        filtered = workouts.filter(workout_type=workout_type)
        count = filtered.count()
        if count > 0:
            # Convert intensity to numeric for averaging
            intensity_map = {'Low': 1, 'Medium': 2, 'High': 3}
            intensities = [intensity_map.get(w.intensity, 0) for w in filtered if w.intensity]
            avg_intensity = sum(intensities) / len(intensities) if intensities else 0
            
            workout_stats[key] = {
                'count': count,
                'avg_calories': filtered.aggregate(Avg('calories'))['calories__avg'] or 0,
                'avg_minutes': filtered.aggregate(Avg('duration'))['duration__avg'] or 0,
                'avg_intensity': round(avg_intensity, 1),
            }
        else:
            workout_stats[key] = {
                'count': 0,
                'avg_calories': 0,
                'avg_minutes': 0,
                'avg_intensity': 0,
            }
    
    context = {
        'workouts': workouts,
        'total_workouts': total_workouts,
        'total_calories': round(total_calories, 1),
        'total_minutes': round(total_minutes, 1),
        'avg_calories': round(avg_calories, 1),
        'avg_minutes': round(avg_minutes, 1),
        'workout_stats': workout_stats,
    }
    
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
    context_object_name = 'workout'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        )  
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.get_object()
        
        # Get previous workout (older date)
        context['previous_workout'] = Workout.objects.filter(
            user=self.request.user,
            date__lt=workout.date
        ).order_by('-date').first()
        
        # Get next workout (newer date)
        context['next_workout'] = Workout.objects.filter(
            user=self.request.user,
            date__gt=workout.date
        ).order_by('date').first()
        
        return context
    
class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    context_object_name = 'workout'
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
    context_object_name = 'workout'
    fields = ["workout_type", "duration", "distance", "pace", "intensity", "calories"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('workout-detail', kwargs={'pk': self.object.pk})

class WorkoutDeleteView(LoginRequiredMixin, DeleteView): 
    model = Workout
    context_object_name = 'workout'
    success_url = reverse_lazy('workouts-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    