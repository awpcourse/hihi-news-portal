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


