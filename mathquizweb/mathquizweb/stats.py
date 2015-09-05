import random
import yaml

from mathquiz.questions import question_name_to_class_name
import mathquiz.questions

from mathquizweb.models import (
    Question,
    QuestionState,
    QuestionType,
    UserQuestionTypeOptions,
    )

MASTERY_COUNT = 30
MASTERY_PERCENT = 0.9
UNMASTERED_MULTIPLIER = 5


def generate_stats_from_db(user):
    results = {
        'questions': {},
        'question_types': {},
    }

    questions = results['questions']

    user_questions = Question.objects.filter(user=user, state__name='answered')
    questions['total'] = user_questions.count()

    if questions['total'] == 0:
        questions['correct'] = 0
        questions['success_rate'] = 0
        return results

    correct_questions = user_questions.filter(correct=True)
    questions['correct'] = \
        correct_questions.count()
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
        if len(questions_of_type) >= 30 and \
                float(correct_of_type) / len(questions_of_type) >= 0.9:
            question_type_entry['mastery'] = True
        else:
            question_type_entry['mastery'] = False

    return results


def get_unanswered_question_from_db(user):
    unanswered_questions = Question.objects.filter(
        user=user, state__name='unanswered')

    if len(unanswered_questions) == 0:
        return None

    return unanswered_questions[0].get_mq_question()

default_properties = ['uuid', 'provided_options']


def add_unanswered_question(user, question, question_type):
    properties = yaml.dump({
        k: v for k, v in question.__dict__.iteritems()
        if k not in default_properties})
    question_instance = Question(
        uuid=question.uuid,
        user=user,
        question_type=question_type,
        state=QuestionState.objects.get(name='unanswered'),
        properties=properties,
        options=question.options,
        correct=None,
        )
    question_instance.save()


def question_type_is_mastered(user, question_type):
    user_questions = Question.objects.filter(user=user, state__name='answered')
    questions_of_type = user_questions.filter(
        question_type=question_type)[0:30]
    num_questions = len(questions_of_type)
    if num_questions < MASTERY_COUNT:
        return False
    num_correct = len([
        question for question in questions_of_type
        if question.correct])
    percent_correct = float(num_correct) / num_questions
    if percent_correct >= MASTERY_PERCENT:
        return True
    return False


def get_next_question_from_db(user):
    """FIXME: random for now, not based on mastery."""
    if user.enabled_questions.count() > 0:
        question_types = user.enabled_questions.all()
    else:
        question_types = QuestionType.objects.all()
    adjusted_question_types = []
    # Make unmastered questions more likely to appear.
    for question_type in question_types:
        if question_type_is_mastered(user, question_type):
            adjusted_question_types.append(question_type)
        else:
            adjusted_question_types.extend(
                [question_type] * UNMASTERED_MULTIPLIER)

    question_type = random.choice(adjusted_question_types)
    question_options_query = UserQuestionTypeOptions.objects.filter(
            user=user, question_type=question_type)
    if question_options_query.exists():
        [question_options_object] = question_options_query.all()
        question_options = yaml.load(question_options_object.options)
    else:
        question_options = None
    class_name = question_name_to_class_name(question_type.name)
    question_class = getattr(mathquiz.questions, class_name)
    question = question_class(options=question_options)
    add_unanswered_question(user, question, question_type)
    return question
