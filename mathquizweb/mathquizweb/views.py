from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import namedtuple
from mathquiz.quiz import Quiz
from mathquiz.questions import builtin_question_types
from mathquiz.storage import (
    get_current_user_data,
    add_unanswered_question,
    )
from mathquiz.stats import generate_stats 

from mathquizweb.forms import (
    QuestionForm,
    UserForm,
    )


defaultoptions = namedtuple('options', [])

def question(request):
    context = RequestContext(request)

    data = {}

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            data['response'] = "Answer received!"
        else:
            data['response'] = "BAD"
    else:
        data['response'] = 'Welcome!'

    user = request.user.username
    user_data = get_current_user_data(user)
    quiz = Quiz(builtin_question_types, user_data)
    [question] = quiz.questions(1, defaultoptions)
    add_unanswered_question(user, question)
    data['question'] = question


    return render_to_response(
        'question.html',
        data,
        context_instance=context)


def home(request):
    context = RequestContext(request)
    data = {}

    if request.user.is_authenticated():
        stats = generate_stats(request.user.username)
        data['stats'] = stats
        data['question_types'] = {
            k.name: v
            for k, v in stats['question_types'].items()
        }

    return render_to_response(
        'index.html',
        data,
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
