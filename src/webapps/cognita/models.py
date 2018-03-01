# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Tag(models.Model):
    tag_content = models.CharField(max_length=20, blank=False)

    def __unicode__(self):
        return self.tag_content


class Course(models.Model):
    Category_CHOICES = (
        ('CS', 'Computer Science'),
        ('MATH', 'Mathematics'),
        ('ART', 'Art'),
        ('BUS', 'Business'),
        ('SCI', 'Natural Science'),
        ('SSCI', 'Social Science'),
        ('LIT', 'Literature'),
        ('UCL', 'Unclassified'),
    )

    title = models.CharField(max_length=255, blank=False, null=False)
    published = models.BooleanField(blank=False, null=False, default=False)
    creator = models.ForeignKey(User, blank=False, null=False, related_name='course_created')
    creator_info = models.TextField()
    description = models.TextField()
    students = models.ManyToManyField(User, related_name='course_taking', blank=True)
    category = models.CharField(blank=False, null=False, max_length=5, choices=Category_CHOICES, default='UCL')
    course_image = models.ImageField(blank=True, upload_to="course_image")
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tagged_course')

    def __unicode__(self):
        return self.title


class Module(models.Model):
    Module_CHOICES = (
        ('L', 'Lecture'),
        ('T', 'Test'),
    )
    module_type = models.CharField(max_length=1, blank=False, null=False, choices=Module_CHOICES, default='L')
    course = models.ForeignKey(Course, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    index = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.module_type + ' ' + self.title


class Lecture(Module):
    expected_hour = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Part(models.Model):
    Part_CHOICES = (
        ('R', 'Reading'),
        ('V', 'Video'),
        ('Q', 'Quiz'),
    )

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    lecture = models.ForeignKey(Lecture, blank=False, null=False, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(blank=False, null=False)
    expected_hour = models.FloatField(null=False, blank=False)
    part_type = models.CharField(max_length=1, choices=Part_CHOICES, blank=False, null=False, default='R')

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.part_type + ' ' + self.title


class Reading(Part):
    Reading_CHOICES = (
        ('P', 'PDF'),
        ('M', 'material'),
    )

    file = models.FileField(upload_to='readings', blank=True, null=True)
    material = RichTextUploadingField(blank=True)
    reading_type = models.CharField(max_length=1, choices=Reading_CHOICES, blank=False, null=False, default='P')

    def __unicode__(self):
        return self.title


class Video(Part):
    link = models.TextField(blank=False,null=False)

    def __unicode__(self):
        return self.title


class Quiz(Part):
    full_score = models.PositiveIntegerField()

class Test(Module):
    expected_hour = models.FloatField(null=False, blank=False)
    full_score = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

class Question(models.Model):
    QUESTION_CHOICES = (
        ('MC', 'Multiple Choice'),
        ('BF', 'Blank Filled'),
    )
    quiz = models.ForeignKey(Quiz, blank=True, null=True, related_name='questions')
    test = models.ForeignKey(Test, blank=True, null=True, related_name='questions')
    index = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='question_image',blank=True, null=True)
    type = models.CharField(max_length=2, choices=QUESTION_CHOICES, blank=False, null=False, default='MC')

    def __unicode__(self):
        return self.description

    def delete(self):
        if self.quiz:
            upper_index = Question.objects.filter(quiz_id__exact=self.quiz_id, index__gt=self.index)
            if upper_index:
                for question in upper_index:
                    question.index = question.index - 1
                    question.save()
        if self.test:
            upper_index = Question.objects.filter(test_id__exact=self.test_id, index__gt=self.index)
            if upper_index:
                for question in upper_index:
                    question.index = question.index - 1
                    question.save()
        super(Question, self).delete()

class MCQuestion(Question):
    pass

class Choice(models.Model):
    mcquestion = models.ForeignKey(MCQuestion, related_name='choices')
    content = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

class BFQuestion(Question):
    pass

class BFQuestionAnswer(models.Model):
    bfquestion = models.ForeignKey(BFQuestion)
    answer = models.CharField(max_length=255)

    def __unicode__(self):
        return self.answer

class UserProgressCourse(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    completed = models.BooleanField(default=False)
    module_completed = models.ManyToManyField(Module, related_name="completed_module")


class UserProgressModule(models.Model):
    user = models.ForeignKey(User)
    lecture = models.ForeignKey(Lecture)
    completed = models.BooleanField(default=False)
    part_completed = models.ManyToManyField(Part, related_name="completed_part")


class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    TYPE_CHOICES = (
        ('MC', 'Multiple Choice'),
        ('BF', 'Blank Filled'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    answer = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.answer

class UserAnswerUnsubmit(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, blank=True, null=True)
    test = models.ForeignKey(Test, blank=True, null=True)
    unsubmit = models.BooleanField(default=False)

class Grade(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, blank=True, null=True)
    test = models.ForeignKey(Test, blank=True, null=True)
    grade = models.IntegerField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    bio = models.TextField()

class StudentNote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, blank=True, null=True)
    note = RichTextUploadingField(blank=True, null=True, default='')