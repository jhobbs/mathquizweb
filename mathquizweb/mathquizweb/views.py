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
from mathquizweb.models import (
    Question,
    QuestionType,
    )

from mathquizweb.forms import (
    QuestionForm,
    UserForm,
    )
from mathquizweb.svg import get_shape_svgs

defaultoptions = namedtuple('options', [])


def generate_stats_from_db(user):
    results = {
        'questions': {},
        'question_types': {},
    }

    questions = results['questions']

    questions['total'] = Question.objects.filter(user=user).count()

    if questions['total'] == 0:
        questions['correct'] = 0
        questions['success_rate'] = 0
        return results

    user_questions = Question.objects.filter(
        user=user, correct=True, state__name='answered')
    questions['correct'] = \
        user_questions.count()
    questions['success_rate'] = \
        "%.02f" % (float(questions['correct']) / questions['total'] * 100)

    question_types = results['question_types']

    for question_type in QuestionType.objects.all():
        question_types[question_type.name] = {}
        question_type_entry = question_types[question_type.name]
        questions_of_type = user_questions.filter(
            question_type=question_type)[0:30]
        question_type_entry['total'] = len(questions_of_type)
        correct_of_type = len([
            question for question in questions_of_type
            if question.correct])
        question_type_entry['correct'] = correct_of_type

    return results


def get_default_data(request):
    data = {}
    if request.user.is_authenticated():
        stats = generate_stats_from_db(request.user)
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
                k: v
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
