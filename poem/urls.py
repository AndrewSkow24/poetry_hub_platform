# poem/urls.py
from django.urls import path
from . import views

app_name = 'poem'

urlpatterns = [
    path('', views.PoemListView.as_view(), name='list'),
    path('<int:pk>/', views.PoemDetailView.as_view(), name='detail'),
    path('create/', views.PoemCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.PoemUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PoemDeleteView.as_view(), name='delete'),
    path('my-poems/', views.MyPoemsListView.as_view(), name='my_poems'),
    path('<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/like/', views.LikePoemView.as_view(), name='like'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]