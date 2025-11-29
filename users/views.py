from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserDeleteForm
from django.contrib import messages
from django.contrib.auth import login, logout

# One view to manage both Login and Register forms as they are on the same template
def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    initial_mode = request.path

    if initial_mode == '/users/register/': # Register view
        if request.method == 'POST':
            form_register = UserRegisterForm(request.POST)
            form_login = UserLoginForm()
            if form_register.is_valid():
                user = form_register.save()
                username = form_register.cleaned_data.get('username')
                login(request, user)
                messages.success(request, f'Account created for {username}!')
                return redirect('home')
        else:
            form_login = UserLoginForm()
            form_register = UserRegisterForm()
            
    else : # Login view
        if request.method == 'POST':
            form_login = UserLoginForm(request, data=request.POST)
            form_register = UserRegisterForm()
            if form_login.is_valid():
                user = form_login.get_user()
                login(request, user)
                return redirect('home')
    
        else:
            form_login = UserLoginForm()
            form_register = UserRegisterForm()
    
    context = {
        'form_login': form_login,
        'form_register': form_register,
        'initial_mode': initial_mode,
    }
    
    return render(request, 'users/authentification.html', context)

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def account(request):
    form_update = UserUpdateForm(instance=request.user)
    form_delete = UserDeleteForm()
    
    context = {
        'form_update': form_update,
        'form_delete': form_delete,
    }
    
    return render(request, 'users/account.html', context)

@login_required
def update_account(request):
    """Handle account update"""
    if request.method == 'POST':
        form_update = UserUpdateForm(request.POST, instance=request.user)
        if form_update.is_valid():
            form_update.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')
        else:
            # If form is invalid, show errors
            form_delete = UserDeleteForm()
            context = {
                'form_update': form_update,
                'form_delete': form_delete,
            }
            return render(request, 'users/account.html', context)
    
    return redirect('account')

@login_required
def delete_account(request):
    """Handle account deletion"""
    if request.method == 'POST':
        form_delete = UserDeleteForm(request.POST)
        if form_delete.is_valid():
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
        else:
            # If form is invalid, show errors
            form_update = UserUpdateForm(instance=request.user)
            context = {
                'form_update': form_update,
                'form_delete': form_delete,
            }
            return render(request, 'users/account.html', context)
    
    return redirect('account')