from django.contrib import admin
from .models import Test, Question, Answer, Result
# Register your models here.

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)