from django.urls import path
from .views import PoemListView, PoemDetailView, PoemCreateView

from .apps import PoemsAppConfig

app_name = PoemsAppConfig.name

urlpatterns = [
    path("", PoemListView.as_view(), name="list"),
    path("create/", PoemCreateView.as_view(), name="create"),
]
