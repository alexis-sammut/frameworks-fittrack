from django.shortcuts import render
from .models import Workout

def log(request):
    return render(request, 'workouts/log_workout.html')

def review(request):
    context = {
       'workouts': Workout.objects.all()
    }
    return render(request, 'workouts/review_workouts.html', context) 