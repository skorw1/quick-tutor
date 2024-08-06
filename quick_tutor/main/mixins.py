# mixins
from django.http import Http404


class LanguageMixin:
    def dispatch(self, request, *args, **kwargs):
        language = self.kwargs.get('language').capitalize()
        if language not in ('Python', 'Javascript', 'Git', 'Html', 'Css ', 'Django'):
            raise Http404('Language not found')
        return super().dispatch(request, *args, **kwargs)