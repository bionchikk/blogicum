from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'pub_date':forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)