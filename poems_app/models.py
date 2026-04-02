from django.db import models


class Poem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Comment(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    poem = models.ForeignKey(
        Poem, on_delete=models.CASCADE, verbose_name="Произведение"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Review(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    poem = models.ForeignKey(
        Poem, on_delete=models.CASCADE, verbose_name="Произведение"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
