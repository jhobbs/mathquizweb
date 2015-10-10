from collections import defaultdict
from datetime import datetime
from django.shortcuts import (
    redirect,
    render_to_response,
    )
from django.template import RequestContext
from collections import namedtuple
from mathquizweb.models import (
    Question,
    QuestionState,
    QuestionType,
    )
from mathquizweb.stats import (
    generate_stats_from_db,
    get_next_question_from_db,
    get_unanswered_question_from_db,
    )
from mathquizweb.forms import (
    QuestionForm,
    SettingsForm,
    UserForm,
    )
from mathquizweb.svg import get_shape_svgs

defaultoptions = namedtuple('options', [])


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
    data = get_default_data(request)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            uuid = form.cleaned_data['uuid']
            questions = Question.objects.filter(
                user=request.user, uuid=uuid)
            if len(questions) == 0:
                question = None
            else:
                question_instance = questions[0]
                question = question_instance.get_mq_question()

            data.update(generate_question_response(question, answer))
            if question is not None:
                question_instance.state = QuestionState.objects.get(
                    name='answered')
                question_instance.correct = question.check_answer(answer)
                question_instance.answered_at = datetime.now()
                question_instance.given_answer = answer
                question_instance.save()
                data['stats'] = generate_stats_from_db(request.user)
        else:
            data['headline'] = "Bad data received!"
    else:
        return redirect('home')

    return render_to_response(
        'answer.html',
        data,
        context_instance=context)


def get_next_question(user):
    unanswered = get_unanswered_question_from_db(user)
    if unanswered is not None:
        return unanswered

    return get_next_question_from_db(user)


def question(request):
    context = RequestContext(request)
    data = get_default_data(request)
    if request.user.is_authenticated():
        data['question'] = get_next_question(request.user)
        data['shape_svgs'] = get_shape_svgs(data['question'])

    return render_to_response(
        'question.html',
        data,
        context_instance=context)


def question_detail(request, question_id):
    if not request.user.is_authenticated():
        return redirect('home')
    context = RequestContext(request)
    data = get_default_data(request)
    base_question = Question.objects.get(
        id=question_id, user=request.user)
    data['question'] = base_question.get_mq_question()
    data['question'].correct = base_question.correct
    data['shape_svgs'] = get_shape_svgs(data['question'])

    return render_to_response(
        'question_detail.html',
        data,
        context_instance=context)


def stats(request):
    context = RequestContext(request)
    data = get_default_data(request)

    if request.user.is_authenticated():
        if data['stats'] is not None:
            data['question_types'] = {
                k: v
                for k, v in data['stats']['question_types'].items()
            }

    return render_to_response(
        'stats.html',
        data,
        context_instance=context)


def history(request):
    context = RequestContext(request)
    data = get_default_data(request)

    if request.user.is_authenticated():
        if data['stats'] is not None:
            data['stats']['question_history'] = Question.objects.filter(
                    state__name='answered',
                    user=request.user).order_by('-id')[:100]

    return render_to_response(
        'history.html',
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


def settings(request):
    context = RequestContext(request)
    data = get_default_data(request)

    if not request.user.is_authenticated():
        return redirect('home')

    settings_form = SettingsForm(request.POST or None, user=request.user)
    data['form'] = settings_form
    if settings_form.is_valid():
        settings_form.save(request.user)
        data['saved'] = True

    all_enabled = request.user.enabled_questions.count() == 0
    data['question_types'] = defaultdict(dict)
    for question_type in QuestionType.objects.all():
        if all_enabled:
            data['question_types'][question_type.name]['enabled'] = True
        else:
            data['question_types'][question_type.name]['enabled'] = \
                question_type in request.user.enabled_questions.all()
    data['question_types'] = dict(data['question_types'])
    return render_to_response(
        'settings.html',
        data,
        context_instance=context)
