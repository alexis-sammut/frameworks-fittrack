from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'name',
            'required': True
        })
        self.fields['email'].widget.attrs.update({
            'id': 'create-account-email',
            'autocomplete': 'email',
            'required': True
        })
        self.fields['password1'].widget.attrs.update({
            'id': 'signup-password',
            'autocomplete': 'new-password',
            'required': True
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'required': True
        })
        
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'login-email',
            'type': 'text',  
            'autocomplete': 'username', 
            'required': True
        })
        self.fields['password'].widget.attrs.update({
            'id': 'login-password',
            'autocomplete': 'current-password',
            'required': True
        })
        self.fields['username'].label = "Email or Username"
        
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Check if username is actually an email
            if '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    username = user_obj.username
                except User.DoesNotExist:
                    pass
            
            # Authenticate with the username
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username/email and password.",
                    code='invalid_login',
                )
        
        return self.cleaned_data    
    
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'name',
            'required': True
        })
        self.fields['email'].widget.attrs.update({
            'id': 'update-email',
            'autocomplete': 'email',
            'required': True
        })
        self.fields['first_name'].widget.attrs.update({
            'id': 'first-name',
        })
        self.fields['last_name'].widget.attrs.update({
            'id': 'last-name',
        })

class UserDeleteForm(forms.Form):
    # Confirmation field to prevent accidental deletion
    confirm = forms.BooleanField(
        required=True,
        label="I understand this action cannot be undone"
    )