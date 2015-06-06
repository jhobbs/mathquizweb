from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import namedtuple
from mathquiz.quiz import Quiz
from mathquiz.questions import builtin_question_types
from mathquiz.storage import get_current_user_data
from mathquiz.stats import generate_stats 

from mathquizweb.forms import UserForm

defaultoptions = namedtuple('options', [])

def question(request):
    context = RequestContext(request)

    user_data = get_current_user_data(request.user.username)
    quiz = Quiz(builtin_question_types, user_data)
    [question] = quiz.questions(1, defaultoptions)

    return render_to_response(
        'index.html',
        {'question': question},
        context_instance=context)


def home(request):
    context = RequestContext(request)

    stats = generate_stats(request.user.username)
    question_types = {k.name: v for k, v in stats['question_types'].items()}

    return render_to_response(
        'index.html',
        {
            'stats': stats,
            'question_types': question_types
        },
        context_instance=context)

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if not user_form.is_valid():
            return render_to_response(
                'registration/register.html',
                {'user_form': user_form, 'registered': registered},
                context)

        user = user_form.save()
        user.set_password(user.password)
        user.save()
        registered = True
    else:
        user_form = UserForm()

    return render_to_response(
        'registration/register.html',
        {'user_form': user_form, 'registered': registered},
        context)
