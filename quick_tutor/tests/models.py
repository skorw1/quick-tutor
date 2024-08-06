from django.db import models
from main.models import Category
from django.contrib.auth.models import User
# Create your models here.

TYPE_ANSWERS = (
    (1, 'Одиночный выбор'),
    (2, 'Множественный выбор')
)

class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    quantity_questions = models.PositiveIntegerField(default=1)

    def get_user_result(self, user):
        return Result.objects.filter(user=user, test=self).first()

    def __str__(self):
        return self.name



class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    number = models.PositiveIntegerField(unique=True)
    type = models.IntegerField(choices=TYPE_ANSWERS, default=1)

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'ответ: {self.answer}, на вопрос: {self.question}'

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    quantity_correct_answers = models.PositiveIntegerField(default=0)
    completion_percentage = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def calculate_completion_percentage(self):
        if self.test.quantity_questions == 0:
            self.completion_percentage = 0
        else:
            self.completion_percentage = round((self.quantity_correct_answers / self.test.quantity_questions) * 100, 2)
        self.save(update_fields=['completion_percentage'])
