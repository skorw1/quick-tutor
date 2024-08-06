from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.views.generic import ListView, DetailView, View
from .models import *

# Create your views here.

class Tests(ListView):
    """
    Представление списка тестов.
    """
    model = Test
    template_name = 'tests/test_list.html'
    context_object_name = 'tests'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tests_with_results = []

        for test in context['tests']:
            result = test.get_user_result(user)
            tests_with_results.append((test, result))

        context['tests_with_results'] = tests_with_results
        return context
class DetailTest(DetailView):
    """
    Представление для просмотра детальной информации о тесте и, и при необходимости старта тестирования.
    """
    model = Test
    template_name = 'tests/detail_test.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quantity = self.object.quantity_questions

        # Вычисляем последнюю цифру и последние две цифры количества вопросов
        last_digit = quantity % 10
        last_two_digits = quantity % 100

        # Обновляем контекст, добавляя необходимые переменные для шаблона
        context.update({
            'last_digit': last_digit,
            'last_two_digits': last_two_digits,
            'between_2_and_4': 2 <= quantity <= 4,  # Переменная для проверки диапазона от 2 до 4
            'is_1': quantity == 1,
            'in_exception_range': last_two_digits in [12, 13, 14],  # Переменная для проверки исключительных чисел 12, 13, 14
            'is_2_3_4': last_digit in [2, 3, 4]
        })
        return context


class BeforeTesting(View):
    """
    Представление для обработки действий перед началом тестирования.
    Удаляет предыдущие результаты и создает новый результат для текущего пользователя.
    """
    @method_decorator(login_required)
    def post(self, request):
        test = Test.objects.get(pk=request.POST.get('test_pk'))
        user = request.user
        # Удаляет предыдущие результаты теста для данного пользователя
        Result.objects.filter(test=test, user=user).delete()
        # Создает новый результат теста для данного пользователя
        Result.objects.create(test=test, user=user)

        # Устанавливаем сессию для того, чтобы понять, какой вопрос идет по счету
        request.session['current_question'] = 1
        return redirect('test-run', pk_test=test.pk)

class RunTest(View):
    """
    Представление для прохождения теста.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk_test):
        test: Test = get_object_or_404(Test, pk=pk_test)
        current_question: int = request.session.get('current_question', 1)
        question: Question = get_object_or_404(Question, test=test, number=current_question)
        answers = Answer.objects.filter(question=question)
        result: Result = get_object_or_404(Result, user=request.user, test=test)

        context = {
            'test': test,
            'question': question,
            'current_question': current_question,
            'answers': answers,
            'result': result,

        }
        return render(request, 'tests/test.html', context=context)

    def post(self, request, pk_test):
        try:
            answer_id: int = request.POST.get('answer')
            answer: Answer = get_object_or_404(Answer, pk=answer_id)
            test: Test = get_object_or_404(Test, pk=request.POST.get('test_pk'))
            result: Result = get_object_or_404(Result, user=request.user, test=test)

            current_question: int = request.session.get('current_question', 1)
            # Если тест не завершен, проверяем ответ
            if not result.is_finished:
                if answer.is_correct:
                    result.quantity_correct_answers += 1
                result.save()

            # Проверка, завершен ли тест
            if current_question >= test.quantity_questions:
                result.is_finished = True
                result.save()
                result.calculate_completion_percentage()
                return JsonResponse({'status': 'finished', 'result': result.quantity_correct_answers})

            request.session['current_question'] += 1
            return JsonResponse({'status': 'next_question'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error'})




