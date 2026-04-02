from sys import prefix

from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)
from django.shortcuts import redirect
from .models import Poem

from .forms import PoemForm, CommentFormSet, ReviewFormSet


class PoemListView(ListView):
    model = Poem


class PoemDetailView(DetailView):
    model = Poem


class PoemCreateView(CreateView):
    model = Poem
    form_class = PoemForm
    success_url = reverse_lazy("poems_app:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import PoemForm, CommentFormSet, ReviewFormSet

        if self.request.POST:
            context["comment_formset"] = CommentFormSet(
                self.request.POST, prefix="comment"
            )
            context["review_formset"] = ReviewFormSet(
                self.request.POST, prefix="review"
            )
        else:
            context["comment_formset"] = CommentFormSet(prefix="comment")
            context["review_formset"] = ReviewFormSet(prefix="review")

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        comment_formset = context["comment_formset"]

        if comment_formset.is_valid():
            self.object = form.save()
            comment_formset.instance = self.object
            comment_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("poem_appls:list")

    def get_success_url(self):
        return reverse_lazy("poems_app:list")
