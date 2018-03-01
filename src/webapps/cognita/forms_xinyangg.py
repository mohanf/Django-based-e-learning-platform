from django import forms
from cognita.models import *

class TestForm(forms.ModelForm):

    title = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control test_title'}))
    description = forms.CharField(required=True, max_length=200,
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}))
    full_score = forms.IntegerField(required=True, min_value=1, max_value=1000,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    expected_hour = forms.FloatField(required=True, min_value=0, max_value=24,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Test
        fields = ['title', 'description', 'full_score', 'expected_hour']

class QuizForm(forms.ModelForm):

    title = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control test_title'}))
    description = forms.CharField(required=True, max_length=200,
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}))
    full_score = forms.IntegerField(required=True, min_value=1, max_value=1000,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    expected_hour = forms.FloatField(required=True, min_value=0, max_value=24,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'full_score', 'expected_hour']

class MCQuestionForm(forms.ModelForm):
    description = forms.CharField(label='Question Description',required=True, max_length=200,
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}))
    weight = forms.IntegerField(label='Question Weight',required=True, min_value=1, max_value=100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MCQuestion
        widget = {'image': forms.ImageField()}
        fields = ['description', 'weight', 'image']

class ChoiceForm(forms.ModelForm):

    content = forms.CharField(label='Choice content',required=True, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control choice_content'}))
    correct = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['content', 'correct']

    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required': '{field_name} is required'.format(
                    field_name=field.label)}


class BFQuestionForm(forms.ModelForm):
    description = forms.CharField(required=True, max_length=200,
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}))
    weight = forms.IntegerField(required=True, min_value=1, max_value=100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BFQuestion
        widget = {'image': forms.ImageField()}
        fields = ['description', 'weight', 'image']

class BFQuestionAnswerForm(forms.ModelForm):
    answer = forms.CharField(label='Correct answer',required=True, max_length=255,
                             widget=forms.TextInput(attrs={'class': 'form-control choice_content'}))
    class Meta:
        model = BFQuestionAnswer
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        super(BFQuestionAnswerForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required': '{field_name} is required'.format(
                    field_name=field.label)}

class UserBFAnswerForm(forms.ModelForm):
    answer = forms.CharField(label='User answer',required=True, max_length=255,
                             widget=forms.TextInput(attrs={'class': 'form-control choice_content'}))
    class Meta:
        model = UserAnswer
        fields = ['answer']
