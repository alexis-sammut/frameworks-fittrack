from django.shortcuts import render
from .models import Meal, Ingredient

def log(request):
    return render(request, 'meals/log_meal.html')

def review(request):
    context = {
        'meals': Meal.objects.all(),
        'ingredients':Meal.objects.all(),
    }
    return render(request, 'meals/review_meals.html')
