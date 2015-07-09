#!/usr/bin/env python
import os
import sys
from mathquiz import storage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mathquizweb.settings")

from mathquizweb.models import QuestionType


def ensure_question_type(question_type_name):
     try:
         QuestionType.objects.get(name=question_type_name)
     except QuestionType.DoesNotExist:
         print("Adding: %s" % (question_type_name))
         qt = QuestionType(name=question_type_name)
         qt.save()


def migrate_question_result(user, question_result):
    question = question_result.question
    question_type = question.name
    print("ensuring type exists: %s" % (question_type))
    ensure_question_type(question_type)



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
