from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Question, Test

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Question

@receiver(post_save, sender=Question)
def update_quantity_questions_on_save(sender, instance, **kwargs):
    test = instance.test
    test.quantity_questions = test.question_set.count()
    test.save()
@receiver(post_delete, sender=Question)
def update_quantity_questions_on_delete(sender, instance, **kwargs):
    test = instance.test
    test.quantity_questions = test.question_set.count()
    test.save()



