from allauth.account.forms import LoginForm
from django import forms


class CustomLoginForm(LoginForm):
    """
    This CustomLoginForm class created to add some styling
    to 'login' and 'password' fields with the help of provided
    attributes.
    """
    password = forms.CharField(widget=forms.PasswordInput(
               attrs={'placeholder': 'Enter your Password'}))
    
    # This function is mandatory to overwrite few fields like login
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"] = forms.CharField(widget=forms.TextInput(
               attrs={'placeholder': 'Username or Mail ID'}))