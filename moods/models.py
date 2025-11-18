from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

class Mood(models.Model):
    """
    Represents a single logged mood entry by a user.
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='mood',
        help_text="The user who logged this mood."
    )
    date = models.DateField(
        default=timezone.now,
        unique=True, # Ensures only one mood log per user per day
        help_text="Date the mood was logged (must be unique for the user)."
    )
    mood = models.IntegerField(
        help_text="The logged mood, on a scale from 1 to 10."
    )
    notes = models.TextField(
        null=True, 
        blank=True,
        help_text="Optional notes on the mood."
    )
    
    # class Meta:
    #     db_table = 'moods_logged'
    #     ordering = ['-date']
    #     # Adding a unique_together constraint to enforce uniqueness per user AND date
    #     unique_together = ('user', 'date')

    def __str__(self):
        """String representation for the Django Admin."""
        return f"Mood {self.mood} for {self.user.username} on {self.date.strftime('%d-%m-%Y')}"