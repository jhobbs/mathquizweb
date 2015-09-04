import uuid
import yaml
import mathquiz.questions

from django.contrib.auth.models import User
from django.db import models
from mathquiz.questions import question_name_to_class_name


class QuestionType(models.Model):
    name = models.CharField(max_length=100)
    enabled_users = models.ManyToManyField(
        User, related_name='enabled_questions')

    def __repr__(self):
        return "<QuestionType: %s>" % (self.name)


class QuestionState(models.Model):
    name = models.CharField(max_length=100)


class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    question_type = models.ForeignKey(QuestionType)
    state = models.ForeignKey(QuestionState)
    options = models.TextField()
    properties = models.TextField()
    correct = models.NullBooleanField()

    def get_mq_question(self):
        class_name = question_name_to_class_name(self.question_type.name)
        question_class = getattr(mathquiz.questions, class_name)
        question = question_class({}, yaml.load(self.properties))
        question.uuid = self.uuid
        if self.correct:
            question.result = 1
        elif not self.correct:
            question.result = 0

        return question


class UserQuestionTypeOptions(models.Model):
    user = models.ForeignKey(User)
    question_type = models.ForeignKey(QuestionType)
    options = models.TextField()
