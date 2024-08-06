from django.urls import path
from .views import *
urlpatterns = [
    path('notes/', NotesListView.as_view(), name='notes-list'),
    path('add_note/<int:pk>/', CreateNoteView.as_view(), name='add-note'),
    path('delete_note/<int:pk>/', DeleteNoteView.as_view(), name='delete-note'),
]
