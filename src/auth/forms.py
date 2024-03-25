from django import forms

from users.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password_again = forms.CharField(
        label='Password again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username',
                  'password', 'password_again',)
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            error = 'Passwords don\'t match'
            raise forms.ValidationError(error)
        return password_again


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    token = forms.CharField(label='Token', max_length=6)
