from django import forms
from django.forms import inlineformset_factory
from .models import Poem, Comment, Review


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = "__all__"


CommentFormSet = inlineformset_factory(
    Poem,
    Comment,
    fields="__all__",
    extra=1,
    can_delete=3,
)

ReviewFormSet = inlineformset_factory(
    Poem,
    Review,
    fields="__all__",
    extra=1,
    can_delete=3,
)
