from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import namedtuple
from mathquiz.quiz import Quiz
from mathquiz.questions import builtin_question_types
from mathquiz.storage import get_current_user_data

defaultoptions = namedtuple('options', [])

def home(request):
    context = RequestContext(request)

    user_data = get_current_user_data('web')
    quiz = Quiz(builtin_question_types, user_data)
    [question] = quiz.questions(1, defaultoptions)

    return render_to_response(
        'index.html',
        {'question': question},
        context_instance=context)
