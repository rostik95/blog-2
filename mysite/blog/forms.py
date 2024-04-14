from .models import Comment, Post, Tag
from django.forms import ModelForm
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class AddPostForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Тэги', required=False)
    status = forms.ChoiceField(choices=Post.Status.choices, initial=Post.Status.DRAFT, label='Статус')

    class Meta:
        model = Post
        fields = ('title', 'slug', 'image', 'body')
        lables = {'slug': 'URL'}
