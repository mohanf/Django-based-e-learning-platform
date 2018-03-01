from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from cognita.models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget

class LoginForm(forms.Form):
    fields = ['username', 'password']
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True,
                                          'autofocus': True}))
    password = forms.CharField(min_length=8, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username__exact=username).count() != 1:
            raise forms.ValidationError("Username doesn't exist")

        return username

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True,
                                          'autofocus': True}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}))
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True}))
    password = forms.CharField(min_length=8, max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True}))
    confirm_password = forms.CharField(min_length=8, max_length=30,
                                       widget=forms.PasswordInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Confirm Password',
                                                  'required': True}))

    def clean_confirm_password(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Passwords must match")
        return cleaned_data

class RegisterCourseForm(forms.Form):
    fields = ['course']
    course = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'take_course_id','required': True}))

    def clean(self):
        cleaned_data = super(RegisterCourseForm, self).clean()
        course = cleaned_data.get('course')

        if Course.objects.filter(id__exact=course).count()!=1:
            raise forms.ValidationError("Invalid courseID")

        return cleaned_data

class ProgressForm(forms.Form):
    fields = ['part']
    part = forms.IntegerField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super(ProgressForm, self).clean()
        print(cleaned_data)
        part = cleaned_data.get('part')
        print(part)
        if Part.objects.filter(id=part).count() != 1:
            print('invalid')
            raise forms.ValidationError("Invalid partID")

        return cleaned_data


class NoteForm(ModelForm):
    class Meta:
        model = StudentNote
        fields = ['note','lecture_id']

    note = forms.CharField(widget=CKEditorUploadingWidget(), min_length=0, required=False)
    lecture_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'lecture_id', 'required': True}))

    def clean(self):
        cleaned_data = super(NoteForm, self).clean()
        lecture_id = cleaned_data.get('lecture_id')
        if Lecture.objects.filter(id=lecture_id).count() != 1:
            print('invalid lectureID')
            raise forms.ValidationError("Invalid lectureID")

        return cleaned_data