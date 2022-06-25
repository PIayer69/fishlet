from django.forms import ModelForm
from .models import Set, Question


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'description']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'definition', 'question_set']