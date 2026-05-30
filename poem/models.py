# poem/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Poet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='poet_profile')
    bio = models.TextField('биография', max_length=1000, blank=True)
    avatar = models.ImageField('аватар', upload_to='avatars/', blank=True, null=True)
    website = models.URLField('личный сайт', blank=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True)
    created_at = models.DateTimeField('дата регистрации', auto_now_add=True)

    def __str__(self):
        return f"Поэт: {self.user.username}"

    class Meta:
        verbose_name = 'поэт'
        verbose_name_plural = 'поэты'

class Poem(models.Model):
    title = models.CharField('название', max_length=200)
    content = models.TextField('текст стихотворения')
    author = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='poems')
    created_at = models.DateTimeField('дата создания', default=timezone.now)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    is_public = models.BooleanField('опубликовано', default=True)
    likes = models.ManyToManyField(User, related_name='liked_poems', blank=True)
    views_count = models.PositiveIntegerField('просмотры', default=0)
    tags = models.CharField('теги', max_length=200, blank=True, help_text='Введите теги через запятую')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'стихотворение'
        verbose_name_plural = 'стихотворения'

class Comment(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('текст комментария', max_length=500)
    created_at = models.DateTimeField('дата комментария', auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'