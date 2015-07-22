from mathquizweb.models import (
    Question,
    QuestionType,
    )


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


def get_unanswered_qusetion_from_db(user):
    unanswered_questions = Question.object.filter(
        user=user, state__name='unanswered')

    if len(uanswered_questions) == 0:
        return None

    return unanswered_questions[0]
