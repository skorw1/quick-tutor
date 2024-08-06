from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from .mixins import LanguageMixin
from .models import *
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, View, DetailView, ListView

from notes.models import UserNotes

# Create your views here.

class MainPage(TemplateView):
    template_name = 'main/main_page.html'

class LanguageList(LanguageMixin, ListView):
    model = Category
    template_name = 'main/language_list.html'
    context_object_name = 'cats'  # сокращение от categories

    def get_queryset(self):
        language = self.kwargs.get('language').capitalize()
        return Category.objects.filter(language=language).order_by('difficult')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language'] = self.kwargs.get('language').capitalize()
        return context

class DetailTopic(LanguageMixin, DetailView):
    model = Topic
    template_name = 'main/topic_detail.html'
    context_object_name = 'topic'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Передаем в контекст информацию о том, добавил ли уже пользователь заметку.
        """
        context = super().get_context_data(**kwargs)
        context['usernote'] = False
        if self.request.user.is_authenticated:
            user, topic_pk = self.request.user, self.kwargs.get('pk')
            usernotes = UserNotes.objects.filter(user=user, topic_id=topic_pk)
            if usernotes:
                context['usernote'] = True
        return context

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Topic.objects.filter(pk=pk)

class SearchView(View):
    def get(self, request):
        prompt = request.GET.get('search')
        if prompt:
            categories = Topic.objects.filter(name__icontains=prompt)
            if not categories.exists():
                context = {'no_result_message': 'К сожалению, по вашему запросу ничего не найдено'}
            else:
                context = {'cats': categories}
            return render(request, 'main/search_results.html', context)
        else:
            return render(request, 'main/search_results.html', {'no_result_message': 'Введите поисковый запрос'})

