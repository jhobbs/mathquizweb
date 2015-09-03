from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from mathquizweb.models import QuestionType


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class QuestionForm(forms.Form):
    answer = forms.CharField(label='Answer')
    uuid = forms.CharField(label='uuid', widget=forms.widgets.HiddenInput)


def is_question_type_enabled(question_type, user):
    if user.enabled_questions.count() == 0:
        return True

    return question_type.enabled_users.filter(id=user.id).exists()


def initialize_question_types(user):
    for question_type in QuestionType.objects.all():
        question_type.enabled_users.add(user)
        question_type.save()


class SettingsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SettingsForm, self).__init__(*args, **kwargs)

        for question_type in QuestionType.objects.all():
            self.fields[question_type.name] = forms.BooleanField(
                label=question_type.name,
                initial=is_question_type_enabled(question_type, user),
                required=False)

    def save(self, user):
        if len(self.changed_data) == 0:
            return

        if user.enabled_questions.count() == 0:
            initialize_question_types(user)

        for question_type_name in self.changed_data:
            question_type = QuestionType.objects.get(name=question_type_name)
            enabled = self.cleaned_data[question_type_name]
            if enabled:
                question_type.enabled_users.add(user)
            else:
                question_type.enabled_users.remove(user)
            question_type.save()
