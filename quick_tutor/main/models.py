from django.db import models
from ckeditor.fields import RichTextField

# Определение выбора уровня сложности
DIFFICULTY_LEVEL_CHOICES = (
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Hard'),
)

class Category(models.Model):
    """
    Модель категории, содержащая название, уровень сложности и язык.
    """
    name = models.CharField(max_length=100, help_text="Название категории")
    difficult = models.IntegerField(
        choices=DIFFICULTY_LEVEL_CHOICES,
        default=1,
        help_text="Уровень сложности"
    )
    language = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Язык категории"
    )

    def __str__(self):
        return f'{self.name}, уровень сложности - {self.get_difficult_display()}'
        # get_difficult_display возвращает уровень сложности Easy/Medium/Hard

class Topic(models.Model):
    """
    Модель темы, связанная с категорией и содержащая название, текст, изображение и дату.
    """
    name = models.CharField(max_length=100, help_text="Название темы")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="Категория"
    )
    difficult = models.IntegerField(
        choices=DIFFICULTY_LEVEL_CHOICES,
        default=1,
        help_text="Уровень сложности"
    )
    text = RichTextField(help_text="Текст темы")
    image = models.ImageField(
        upload_to='main/img/',
        blank=True,
        help_text="Изображение для темы"
    )
    date = models.DateField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Дата создания темы"
    )

    def __str__(self):
        return self.name
