from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, View
from .models import UserNotes
from main.models import Topic

class NotesListView(LoginRequiredMixin, ListView):
    model = UserNotes
    template_name = 'main/notes.html'
    context_object_name = 'cats'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CreateNoteView(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    def post(self, request, pk):
        user = request.user
        topic = get_object_or_404(Topic, pk=pk)
        if not UserNotes.objects.filter(user=user, topic=topic).exists():
            UserNotes.objects.create(user=user, topic=topic)
        return JsonResponse({'success': True})

class DeleteNoteView(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    def post(self, request, pk):
        user = request.user
        topic = get_object_or_404(Topic, pk=pk)
        UserNotes.objects.filter(user=user, topic=topic).delete()
        return JsonResponse({'success': True})
