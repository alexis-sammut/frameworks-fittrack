from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Mood(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='mood',
        help_text="The user who logged this mood."
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date the mood was logged."
    )
    mood = models.IntegerField(
        help_text="The logged mood, on a scale from 1 to 10."
    )
    notes = models.TextField(
        null=True, 
        blank=True,
        help_text="Optional notes on the mood."
    )
    
    class Meta:
        db_table = 'mood'
        ordering = ['-date']
        unique_together = ('user', 'date')  # One mood per user per day

    def __str__(self):
        return f"Mood {self.mood} for {self.user.username} on {self.date.strftime('%d-%m-%Y')}"
    
    def get_absolute_url(self):
        return reverse('mood-detail', kwargs={'pk': self.pk})