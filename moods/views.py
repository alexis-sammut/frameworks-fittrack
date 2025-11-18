from django.shortcuts import render
from .models import Mood

def log(request):
    return render(request, 'moods/log_mood.html')

def review(request):
    context = {
       'moods': Mood.objects.all()
    }
    return render(request, 'moods/review_moods.html', context)