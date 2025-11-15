from django.shortcuts import render
from django.http import HttpResponse


def log(request):
    return render(request, 'workouts/log_workout.html')

def review(request):
    return render(request, 'workouts/review_workouts.html')