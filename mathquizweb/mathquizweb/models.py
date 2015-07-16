import uuid

from django.contrib.auth.models import User
from django.db import models
from yamlfield.fields import YAMLField


class QuestionType(models.Model):
    name = models.CharField(max_length=100)


class QuestionState(models.Model):
    name = models.CharField(max_length=100)
    

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    question_type = models.ForeignKey(QuestionType)
    state = models.ForeignKey(QuestionState)
    options = models.TextField()
    properties = models.TextField()
