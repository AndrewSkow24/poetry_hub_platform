# poem/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Poem, Comment, Poet


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = ['title', 'content', 'is_public', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название стихотворения'}),
            'content': forms.Textarea(
                attrs={'rows': 15, 'class': 'form-control', 'placeholder': 'Текст стихотворения...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'любовь, природа, философия'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Ваш комментарий...'}),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class PoetProfileForm(forms.ModelForm):
    class Meta:
        model = Poet
        fields = ['bio', 'avatar', 'website', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Расскажите о себе...'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }