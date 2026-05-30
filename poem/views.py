# poem/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView, UpdateView as ProfileUpdateView
from django.views.generic.detail import DetailView as ProfileDetailView
from .models import Poem, Poet, Comment
from .forms import PoemForm, CommentForm, UserRegistrationForm, PoetProfileForm


class PoemListView(ListView):
    model = Poem
    template_name = 'poem/poem_list.html'
    context_object_name = 'poems'
    paginate_by = 12

    def get_queryset(self):
        return Poem.objects.filter(is_public=True).select_related('author__user')


class PoemDetailView(DetailView):
    model = Poem
    template_name = 'poem/poem_detail.html'
    context_object_name = 'poem'

    def get_object(self):
        poem = super().get_object()
        poem.views_count += 1
        poem.save(update_fields=['views_count'])
        return poem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('user').all()
        context['comment_form'] = CommentForm()
        context['is_liked'] = self.request.user.is_authenticated and self.object.likes.filter(
            id=self.request.user.id).exists()
        return context


class PoemCreateView(LoginRequiredMixin, CreateView):
    model = Poem
    form_class = PoemForm
    template_name = 'poem/poem_form.html'

    def form_valid(self, form):
        poet, _ = Poet.objects.get_or_create(user=self.request.user)
        form.instance.author = poet
        messages.success(self.request, 'Ваше стихотворение опубликовано!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('poem:detail', kwargs={'pk': self.object.pk})


class PoemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Poem
    form_class = PoemForm
    template_name = 'poem/poem_form.html'

    def test_func(self):
        return self.get_object().author.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Стихотворение обновлено!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('poem:detail', kwargs={'pk': self.object.pk})


class PoemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Poem
    template_name = 'poem/poem_confirm_delete.html'
    success_url = reverse_lazy('poem:list')

    def test_func(self):
        return self.get_object().author.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Стихотворение удалено')
        return super().delete(request, *args, **kwargs)


class MyPoemsListView(LoginRequiredMixin, ListView):
    model = Poem
    template_name = 'poem/my_poems.html'
    context_object_name = 'poems'
    paginate_by = 10

    def get_queryset(self):
        poet = get_object_or_404(Poet, user=self.request.user)
        return Poem.objects.filter(author=poet).select_related('author__user')


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        poem = get_object_or_404(Poem, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.poem = poem
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')

        return redirect('poem:detail', pk=pk)


class LikePoemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        poem = get_object_or_404(Poem, pk=pk)

        if request.user in poem.likes.all():
            poem.likes.remove(request.user)
            liked = False
        else:
            poem.likes.add(request.user)
            liked = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'likes_count': poem.likes.count()
            })

        return redirect('poem:detail', pk=pk)


class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Регистрация успешна! Теперь вы можете войти.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, ProfileDetailView):
    model = Poet
    template_name = 'poem/profile.html'
    context_object_name = 'poet'

    def get_object(self):
        return get_object_or_404(Poet, user=self.request.user)


class ProfileEditView(LoginRequiredMixin, ProfileUpdateView):
    model = Poet
    form_class = PoetProfileForm
    template_name = 'poem/profile_edit.html'
    success_url = reverse_lazy('poem:profile')

    def get_object(self):
        return get_object_or_404(Poet, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлён!')
        return super().form_valid(form)