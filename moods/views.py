from django.shortcuts import render
from django.http import HttpResponse
from .models import Mood
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
from django.db.models import Avg, Count

@login_required
def review(request):
    moods = Mood.objects.filter(user=request.user)
    
    # Calculate statistics
    total_moods = moods.count()
    avg_mood = moods.aggregate(Avg('mood'))['mood__avg'] or 0
    
    context = {
        'moods': moods,
        'total_moods': total_moods,
        'avg_mood': round(avg_mood, 1),
    }
    return render(request, 'moods/review_moods.html', context)



class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    context_object_name = "moods"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        )  # Filter the queryset to only include objects created by the current user
        
class MoodDetailView(LoginRequiredMixin, DetailView):
    model = Mood
    context_object_name = 'mood'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        )  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mood = self.get_object()
        
        # Get previous mood (older date)
        context['previous_mood'] = Mood.objects.filter(
            user=self.request.user,
            date__lt=mood.date
        ).order_by('-date').first()
        
        # Get next mood (newer date)
        context['next_mood'] = Mood.objects.filter(
            user=self.request.user,
            date__gt=mood.date
        ).order_by('date').first()
        
        return context
    
class MoodCreateView(LoginRequiredMixin, CreateView):
    model = Mood
    context_object_name = 'mood'
    template_name = "moods/post_mood.html"
    fields = ["mood", "notes"]

    def form_valid(self, form):
        """Automatically set the user to the logged-in user"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        """
        return reverse("mood-detail", kwargs={"pk": self.object.pk})
    
class MoodUpdateView(LoginRequiredMixin, UpdateView):
    model = Mood
    context_object_name = 'mood'
    fields = ["mood", "notes"]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('mood-detail', kwargs={'pk': self.object.pk})
    
class MoodDeleteView(LoginRequiredMixin, DeleteView): 
    model = Mood
    context_object_name = 'mood'
    success_url = reverse_lazy('moods-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)