from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_view, name='login'),
    path('register/', views.auth_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  
    path('update/', views.update_account, name='update-account'),
    path('delete/', views.delete_account, name='delete-account'),
    path('account/',views.account,name='account'),
    ]