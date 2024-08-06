from django.db import models
from django.contrib.auth.models import User
from main.models import Topic
# Create your models here.

class UserNotes(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)