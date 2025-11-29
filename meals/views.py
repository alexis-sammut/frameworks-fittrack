
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Meal, Ingredient
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
from django.db.models import Sum, Avg, Count
import json

# Function-based view for creating meals (handles API + multi-step form)
@login_required
def log_meal(request):
    if request.method == 'POST':
        # Get the meal data from the hidden input (JSON string from JavaScript)
        meal_data = request.POST.get('mealData')
        
        if meal_data:
            try:
                # Parse the JSON data
                data = json.loads(meal_data)
                
                # Create the Meal object
                meal = Meal.objects.create(
                    user=request.user,
                    name=data['meal_name'],
                    total_weight=data['totals']['weight'],
                    total_total_fat=data['totals']['fat_total_g'],
                    total_saturated_fat=data['totals']['fat_saturated_g'],
                    total_total_carbs=data['totals']['carbohydrates_total_g'],
                    total_fiber=data['totals']['fiber_g'],
                    total_sugar=data['totals']['sugar_g'],
                    total_sodium=data['totals']['sodium_mg'],
                    total_potassium=data['totals']['potassium_mg'],
                    total_cholesterol=data['totals']['cholesterol_mg'],
                )
                
                # Create Ingredient objects for each food item
                for item in data['items']:
                    Ingredient.objects.create(
                        meal=meal,
                        name=item['name'],
                        weight=item['weight'],
                        total_fat=item['fat_total_g'],
                        saturated_fat=item['fat_saturated_g'],
                        total_carbs=item['carbohydrates_total_g'],
                        fiber=item['fiber_g'],
                        sugar=item['sugar_g'],
                        sodium=item['sodium_mg'],
                        potassium=item['potassium_mg'],
                        cholesterol=item['cholesterol_mg'],
                    )
                
                return redirect('meal-detail', pk=meal.pk)
            except Exception as e:
                print(f"Error saving meal: {e}")
                return render(request, 'meals/post_meal.html', {'error': 'Failed to save meal'})
    
    return render(request, 'meals/post_meal.html')

@login_required
def update_meal(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        meal_data = request.POST.get('mealData')
        
        if meal_data:
            try:
                data = json.loads(meal_data)
                
                # Update the Meal object
                meal.name = data['meal_name']
                meal.total_weight = data['totals']['weight']
                meal.total_total_fat = data['totals']['fat_total_g']
                meal.total_saturated_fat = data['totals']['fat_saturated_g']
                meal.total_total_carbs = data['totals']['carbohydrates_total_g']
                meal.total_fiber = data['totals']['fiber_g']
                meal.total_sugar = data['totals']['sugar_g']
                meal.total_sodium = data['totals']['sodium_mg']
                meal.total_potassium = data['totals']['potassium_mg']
                meal.total_cholesterol = data['totals']['cholesterol_mg']
                meal.save()
                
                # Delete old ingredients and create new ones
                meal.ingredients.all().delete()
                for item in data['items']:
                    Ingredient.objects.create(
                        meal=meal,
                        name=item['name'],
                        weight=item['weight'],
                        total_fat=item['fat_total_g'],
                        saturated_fat=item['fat_saturated_g'],
                        total_carbs=item['carbohydrates_total_g'],
                        fiber=item['fiber_g'],
                        sugar=item['sugar_g'],
                        sodium=item['sodium_mg'],
                        potassium=item['potassium_mg'],
                        cholesterol=item['cholesterol_mg'],
                    )
                
                return redirect('meal-detail', pk=meal.pk)
            except Exception as e:
                print(f"Error updating meal: {e}")
    
    # Prepare meal data for pre-population
    # Convert ingredients to a list of dictionaries
    ingredients_list = []
    for ingredient in meal.ingredients.all():
        ingredients_list.append({
            'name': ingredient.name,
            'weight': float(ingredient.weight),
            'fat_total_g': float(ingredient.total_fat),
            'fat_saturated_g': float(ingredient.saturated_fat),
            'carbohydrates_total_g': float(ingredient.total_carbs),
            'fiber_g': float(ingredient.fiber),
            'sugar_g': float(ingredient.sugar),
            'sodium_mg': float(ingredient.sodium),
            'potassium_mg': float(ingredient.potassium),
            'cholesterol_mg': float(ingredient.cholesterol),
        })
    
    context = {
        'meal': meal,
        'ingredients': meal.ingredients.all(),
        'ingredients_json': json.dumps(ingredients_list),
        'is_update': True,
    }
    
    return render(request, 'meals/meal_form.html', context)

@login_required
def review(request):
    meals = Meal.objects.filter(user=request.user)
    
    # Calculate total and average statistics
    total_weight = meals.aggregate(Sum('total_weight'))['total_weight__sum'] or 0
    total_fat = meals.aggregate(Sum('total_total_fat'))['total_total_fat__sum'] or 0
    total_saturated_fat = meals.aggregate(Sum('total_saturated_fat'))['total_saturated_fat__sum'] or 0
    total_carbs = meals.aggregate(Sum('total_total_carbs'))['total_total_carbs__sum'] or 0
    total_fiber = meals.aggregate(Sum('total_fiber'))['total_fiber__sum'] or 0
    total_sugar = meals.aggregate(Sum('total_sugar'))['total_sugar__sum'] or 0
    total_sodium = meals.aggregate(Sum('total_sodium'))['total_sodium__sum'] or 0
    total_potassium = meals.aggregate(Sum('total_potassium'))['total_potassium__sum'] or 0
    total_cholesterol = meals.aggregate(Sum('total_cholesterol'))['total_cholesterol__sum'] or 0
    
    avg_weight = meals.aggregate(Avg('total_weight'))['total_weight__avg'] or 0
    avg_fat = meals.aggregate(Avg('total_total_fat'))['total_total_fat__avg'] or 0
    avg_saturated_fat = meals.aggregate(Avg('total_saturated_fat'))['total_saturated_fat__avg'] or 0
    avg_carbs = meals.aggregate(Avg('total_total_carbs'))['total_total_carbs__avg'] or 0
    avg_fiber = meals.aggregate(Avg('total_fiber'))['total_fiber__avg'] or 0
    avg_sugar = meals.aggregate(Avg('total_sugar'))['total_sugar__avg'] or 0
    avg_sodium = meals.aggregate(Avg('total_sodium'))['total_sodium__avg'] or 0
    avg_potassium = meals.aggregate(Avg('total_potassium'))['total_potassium__avg'] or 0
    avg_cholesterol = meals.aggregate(Avg('total_cholesterol'))['total_cholesterol__avg'] or 0
    
    context = {
        'meals': meals.order_by('-date'),
        'total_weight': round(total_weight, 1),
        'total_fat': round(total_fat, 1),
        'total_saturated_fat': round(total_saturated_fat, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fiber': round(total_fiber, 1),
        'total_sugar': round(total_sugar, 1),
        'total_sodium': round(total_sodium, 1),
        'total_potassium': round(total_potassium, 1),
        'total_cholesterol': round(total_cholesterol, 1),
        'avg_weight': round(avg_weight, 1),
        'avg_fat': round(avg_fat, 1),
        'avg_saturated_fat': round(avg_saturated_fat, 1),
        'avg_carbs': round(avg_carbs, 1),
        'avg_fiber': round(avg_fiber, 1),
        'avg_sugar': round(avg_sugar, 1),
        'avg_sodium': round(avg_sodium, 1),
        'avg_potassium': round(avg_potassium, 1),
        'avg_cholesterol': round(avg_cholesterol, 1),
    }
    return render(request, 'meals/review_meals.html', context)

class MealListView(LoginRequiredMixin, ListView):
    model = Meal
    context_object_name = "meals"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class MealDetailView(LoginRequiredMixin, DetailView):
    model = Meal
    context_object_name = 'meal'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = self.object 

        # Add ingredients
        context['ingredients'] = meal.ingredients.all()

        # Previous meal (older date)
        context['previous_meal'] = Meal.objects.filter(
            user=self.request.user,
            date__lt=meal.date
        ).order_by('-date').first()

        # Next meal (newer date)
        context['next_meal'] = Meal.objects.filter(
            user=self.request.user,
            date__gt=meal.date
        ).order_by('date').first()

        return context



class MealDeleteView(LoginRequiredMixin, DeleteView):
    model = Meal
    context_object_name = 'meal'
    success_url = reverse_lazy('meals-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)