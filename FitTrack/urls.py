from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('workout/', include('workouts.urls')),
    path('meal/', include('meals.urls')),
    path('mood/', include('moods.urls')),
]
