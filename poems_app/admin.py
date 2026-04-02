from django.contrib import admin

from .models import Poem, Comment, Review

# Register your models here.
admin.site.register(Poem)
admin.site.register(Comment)
admin.site.register(Review)
