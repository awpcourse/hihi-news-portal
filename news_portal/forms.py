from django import forms
from django.contrib.auth.models import User  # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm
from models import SuggestPost


class NewsItemCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
            attrs={'rows': 4, 'cols': 50, 'placeholder': 'Write a comment...'}),
            label='')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=50, label='')


class FilterNewsForm(Form):
    date_from = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}), required=True)
    date_to = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}), required=True)

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}),required=False)

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


class SuggestPostForm(forms.ModelForm):
    description = forms.CharField(required=True)
    link = forms.URLField(required=True)

    class Meta:
        model = SuggestPost
        fields = ('description', 'link')

    def save(self, commit=True):
        post = super(SuggestPostForm, self).save(commit=False)
        post.description=self.cleaned_data['description']
        post.link=self.cleaned_data['link']

        if commit:
            post.save()
        return post