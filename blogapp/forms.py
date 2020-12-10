from django import forms
from .models import Article, Author, Comment, Category


class CreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category',
        ]


class CrateAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'profile_pic',
            'email',
            'details',
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment',
        ]


class CommentFormAgain(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'post_comment',
        ]