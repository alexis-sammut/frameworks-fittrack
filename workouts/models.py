from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

class Workout(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='workout',
        help_text="The user who logged this workout."
    )
    date = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time the workout was logged."
    )
    workout_type = models.CharField(
        max_length=50,
        help_text="e.g., Running, Walking, Cycling."
    )
    duration = models.IntegerField(
        help_text="Duration of the workout in minutes."
    )    
    distance = models.FloatField(
        null=True, 
        blank=True,
        help_text="Total distance covered in kilometers."
    )
    pace = models.FloatField(
        null=True, 
        blank=True,
        help_text="Average pace for the workout."
    )
    intensity = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        help_text="Perceived intensity (Low, Medium or High)."
    )
    calories = models.FloatField(
        help_text="Estimated calories burned during the workout."
    )

    # class Meta:
    #     # Define the table name (optional, but good for clarity)
    #     db_table = 'workout_logged'
    #     # Order workouts by the date, descending (most recent first)
    #     ordering = ['-date']

    def __str__(self):
        """String representation for the Django Admin."""
        return f"{self.workout_type} on {self.date.strftime('%d-%m-%Y')} by {self.user.username}"