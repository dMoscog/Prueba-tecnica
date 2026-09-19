from django.urls import path
from .views import character_list, character_create, character_edit, character_delete

urlpatterns = [
    path('', character_list, name='character_list'),
    path('character/create/', character_create, name='character_create'),
    path('character/edit/<int:pk>/', character_edit, name='character_edit'),
    path('character/delete/<int:pk>/', character_delete, name='character_delete'),
]