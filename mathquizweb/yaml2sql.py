#!/usr/bin/env python
import os
import sys
import yaml
from mathquiz import storage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mathquizweb.settings")

from mathquizweb.models import (
   QuestionState,
   QuestionType,
   Question)
from django.contrib.auth.models import User


def ensure_question_type(question_type_name):
     try:
         return QuestionType.objects.get(name=question_type_name)
     except QuestionType.DoesNotExist:
         qt = QuestionType(name=question_type_name)
         qt.save()
         return qt

default_properties = ['uuid', 'provided_options']

def migrate_question_result(user, question_result):
    question = question_result.question
    question_type_name = question.name
    question_type = ensure_question_type(question_type_name)
    user = User.objects.get(username=user)
    state = QuestionState.objects.get(name='answered')
    yaml_question = question_result.question
    properties = yaml.dump({
        k: v for k,v in yaml_question.__dict__.iteritems()
        if not k in default_properties})
    question = Question(
        id=yaml_question.uuid,
        user=user,
        question_type=question_type,
        state=state,
        properties=properties,
        options=yaml_question.provided_options,
        correct=question_result.result == 1,
        )
    print question
    question.save()

def migrate_data_for_user(user):
    user_data = storage.get_current_user_data(user)
    for result in user_data['results']:
        for question_result in result.results:
            migrate_question_result(user, question_result)


def main():
    user = sys.argv[1]
    migrate_data_for_user(user)


if __name__ == '__main__':
    main()
