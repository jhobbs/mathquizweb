import yaml

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from mathquizweb.models import (
    QuestionType,
    UserQuestionTypeOptions,
)
from django.core.exceptions import ObjectDoesNotExist


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
            field_name = "%s.enabled" % (question_type.name)
            self.fields[field_name] = forms.BooleanField(
                label="%s: enabled" % (question_type.name),
                initial=is_question_type_enabled(question_type, user),
                required=False)

            try:
                user_options_object = UserQuestionTypeOptions.objects.get(
                    user=user, question_type=question_type)
                user_options = yaml.load(user_options_object.options)
            except ObjectDoesNotExist:
                user_options = {}
            builtin_options = question_type.mathquiz_class.options
            for option_name, option_details in builtin_options.iteritems():
                if option_details['type'] != int:
                    raise Exception("Unknown option type!")
                global_option_name = "%s.%s" % (question_type.name, option_name)
                field_label = "%s: %s" % (question_type.name, option_name)
                if option_name in user_options:
                    initial_value = user_options[option_name]
                else:
                    initial_value = option_details['default']
                self.fields[global_option_name] = forms.IntegerField(
                    label=field_label,
                    initial=initial_value,
                    required=False)

    def save(self, user):
        if len(self.changed_data) == 0:
            return

        if user.enabled_questions.count() == 0:
            initialize_question_types(user)

        modified_question_types = []
        for field_name in self.changed_data:
            data = self.cleaned_data[field_name]
            question_type_name, setting = field_name.split(".")
            question_type = QuestionType.objects.get(name=question_type_name)
            if setting == 'enabled':
                enabled = data
                if enabled:
                    question_type.enabled_users.add(user)
                else:
                    question_type.enabled_users.remove(user)
                question_type.save()
            elif setting in question_type.mathquiz_class.options:
                options = {setting: data}
                try:
                    uqto = UserQuestionTypeOptions.objects.get(
                        user=user, question_type=question_type)
                except ObjectDoesNotExist:
                    options_string = yaml.dump(options)
                    uqto = UserQuestionTypeOptions(
                        user, question_type, options=options_string)
                    uqto.save()
                    continue
                existing = yaml.load(uqto.options)
                existing.update(options)
                uqto.options = yaml.dump(existing)
                uqto.save()
