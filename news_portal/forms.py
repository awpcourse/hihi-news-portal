from django import forms
from django.contrib.auth.models import User  # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, CharField, Textarea, PasswordInput, TextInput

class NewsItemCommentForm(Form):
    text = CharField(widget=Textarea(
        attrs={'rows': 4, 'cols': 50, 'placeholder': 'Write a comment...'}),
        label='')

class UserLoginForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)

class SearchForm(Form):
    text = CharField(max_length=50, label='')

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birthday = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birthday = self.cleaned_data['birthday']

        if commit:
            user.save()

        return user