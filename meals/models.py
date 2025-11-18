from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

# --- MEAL MODEL (Parent Model) ---
class Meal(models.Model):
    """
    Table for logging meals. Each meal is linked to one user and can contain many ingredients.
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # If the parent user is deleted, this meal is also deleted.
        related_name='meal',
        help_text="The user who logged this meal."
    )
    name = models.CharField(
        max_length=100, 
        help_text="Name of the meal (e.g., 'Breakfast', 'Chicken Salad')."
    )
    date = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time the meal was logged."
    )
    total_weight = models.FloatField(help_text="Total weight of the meal (g).")
    total_total_fat = models.FloatField(verbose_name='Total Fat', help_text="Total fat (g).")
    total_saturated_fat = models.FloatField(verbose_name='Saturated Fat', help_text="Saturated fat (g).")
    total_total_carbs = models.FloatField(verbose_name='Total Carbs', help_text="Total carbohydrates (g).")
    total_fiber = models.FloatField(verbose_name='Fiber', help_text="Dietary fiber (g).")
    total_sugar = models.FloatField(verbose_name='Sugar', help_text="Sugar (g).")
    total_sodium = models.FloatField(verbose_name='Sodium', help_text="Sodium (mg).")
    total_potassium = models.FloatField(verbose_name='Potassium', help_text="Potassium (mg).")
    total_cholesterol = models.FloatField(verbose_name='Cholesterol', help_text="Cholesterol (mg).")
    
    # class Meta:
    #     db_table = 'meals_logged'
    #     ordering = ['-date']
    #     verbose_name = 'Meal Log'
    #     verbose_name_plural = 'Meal Logs'
    
    def __str__(self):
        return f"Meal '{self.name}' by {self.user.username} on {self.date.strftime('%d-%m-%Y')}"
    
# --- INGREDIENT MODEL (Child Model) ---
class Ingredient(models.Model):
    """
    Table for storing individual ingredient entries linked to a meal (One-to-Many relationship).
    """
    
    # Foreign Key linking back to Meal
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE, # If the parent meal is deleted, this ingredient is also deleted.
        related_name='ingredients',
        help_text="The meal this ingredient belongs to."
    )
    name = models.CharField(
        max_length=100, 
        help_text="Name of the ingredient."
    )
    weight = models.FloatField(help_text="Weight of the ingredient used (g).")
    total_fat = models.FloatField(verbose_name='Total Fat', help_text="Fat content (g).")
    saturated_fat = models.FloatField(verbose_name='Saturated Fat', help_text="Saturated fat content (g).")
    total_carbs = models.FloatField(verbose_name='Total Carbs', help_text="Carbohydrate content (g).")
    fiber = models.FloatField(verbose_name='Fiber', help_text="Fiber content (g).")
    sugar = models.FloatField(verbose_name='Sugar', help_text="Sugar content (g).")
    sodium = models.FloatField(verbose_name='Sodium', help_text="Sodium content (mg).")
    potassium = models.FloatField(verbose_name='Potassium', help_text="Potassium content (mg).")
    cholesterol = models.FloatField(verbose_name='Cholesterol', help_text="Cholesterol content (mg).")
    
    # class Meta:
    #     db_table = 'logged_ingredients'
    #     ordering = ['name']
    #     verbose_name = 'Logged Ingredient'
    #     verbose_name_plural = 'Logged Ingredients'

    def __str__(self):
        return f"Ingredient '{self.name}' in Meal: {self.meal.name}"