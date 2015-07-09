from django.shortcuts import (
    redirect,
    render_to_response,
    )
from django.template import RequestContext
from collections import namedtuple
from mathquiz.quiz import Quiz
from mathquiz.questions import builtin_question_types
from mathquiz.storage import (
    add_answered_question,
    get_current_user_data,
    add_unanswered_question,
    get_unanswered_question,
    remove_unanswered_question,
    )
from mathquiz.stats import generate_stats 

from mathquizweb.forms import (
    QuestionForm,
    UserForm,
    )

defaultoptions = namedtuple('options', [])

import mathquizweb.models


def get_default_data(request):
    data = {}
    if request.user.is_authenticated():
        stats = generate_stats(request.user.username)
        data['stats'] = stats

    return data


def generate_question_response(question, answer):
    response = {}

    if question is None:
        response['headline'] = 'Unknown question!'
        return {'headline': 'Unknown question!'}

    correct = question.check_answer(answer)

    if not correct:
        return {
            'headline': 'Incorrect!',
            'detail': "%s is wrong! %s is the correct answer to '%s'" % (
                answer, question.answer, question.question_string())
        }

    return {
        'headline': 'Correct',
        'detail': "%s is the correct answer to '%s'" % (
            answer, question.question_string())
    }


def answer(request):
    context = RequestContext(request)
    user = request.user.username
    data = get_default_data(request)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            uuid = form.cleaned_data['uuid']
            question = get_unanswered_question(user, uuid)
            data.update(generate_question_response(question, answer))
            if question:
                add_answered_question(
                    user, question, answer, question.check_answer(answer))
                remove_unanswered_question(user, uuid)
                data['stats'] = generate_stats(user)
        else:
            data['headline'] = "Bad data received!"
    else:
        return redirect('question')

    return render_to_response(
        'answer.html',
        data,
        context_instance=context)


def get_next_question(user):
    unanswered = get_unanswered_question(user)
    if unanswered is not None:
        return unanswered

    user_data = get_current_user_data(user)
    quiz = Quiz(builtin_question_types, user_data)
    [question] = quiz.questions(1, defaultoptions)
    add_unanswered_question(user, question)
    return question


def svg_rectangle(width, height):
    # find the longest and scale it to max size
    if width > height:
        scale = height / float(width)
        scaled_width = 150
        scaled_height = int(scale * scaled_width)
    else:
        scale = width / float(height)
        scaled_height = 150
        scaled_width = int(scale * scaled_height)

    y_label_x = scaled_width + 5
    y_label_y = max(15, scaled_height/2)

    x_label_x = int(scaled_width / 2)
    x_label_y = scaled_height + 20

    text = (
    '<svg width="200" height="200">'
      '<rect width="%s" height="%s"></rect>'
      '<text x="%s" y="%s">%s</text>'
      '<text x="%s" y="%s">%s</text>'
    '</svg>') % (
            scaled_width, scaled_height,
            y_label_x, y_label_y, height,
            x_label_x, x_label_y, width)
    return text


shape_to_svg_handlers = {
        'rectangle': svg_rectangle,
    }


def shape_to_svg(shape_type, shape_properties):
    handler = shape_to_svg_handlers[shape_type]
    result = handler(**shape_properties)
    return result


def get_shape_svgs(question):
    return [shape_to_svg(shape_type, shape_properties)
            for shape_type, shape_properties
            in question.graphic_cue.iteritems()]


def question(request):
    context = RequestContext(request)
    user = request.user.username
    data = get_default_data(request)
    data['question'] = get_next_question(user)
    data['shape_svgs'] = get_shape_svgs(data['question'])

    return render_to_response(
        'question.html',
        data,
        context_instance=context)


def home(request):
    context = RequestContext(request)
    data = get_default_data(request)

    if request.user.is_authenticated():
        if data['stats'] is not None:
            data['question_types'] = {
                k.name: v
                for k, v in data['stats']['question_types'].items()
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
