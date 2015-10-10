import uuid
import yaml
import mathquiz.questions

from django.contrib.auth.models import User
from django.db import models
from mathquiz.questions import question_name_to_class_name


class QuestionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    enabled_users = models.ManyToManyField(
        User, related_name='enabled_questions')

    def __repr__(self):
        return "<QuestionType: %s>" % (self.name)

    @property
    def mathquiz_class(self):
        class_name = question_name_to_class_name(self.name)
        question_class = getattr(mathquiz.questions, class_name)
        return question_class


class QuestionState(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User)
    question_type = models.ForeignKey(QuestionType)
    state = models.ForeignKey(QuestionState)
    options = models.TextField()
    properties = models.TextField()
    correct = models.NullBooleanField()
    answered_at = models.DateTimeField(blank=True, null=True)
    given_answer = models.CharField(
        max_length=100, blank=True, null=True)

    def get_mq_question(self):
        question_class = self.question_type.mathquiz_class
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

    class Meta:
        unique_together = ("user", "question_type")
