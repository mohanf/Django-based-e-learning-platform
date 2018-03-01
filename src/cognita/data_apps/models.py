# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

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

    published = models.BooleanField(blank=False, null=False, default=False)
    creator = models.ForeignKey(User, blank=False, null=False)
    creator_info = models.TextField()
    description = models.TextField()
    students = models.ManyToManyField(User, related_name='r_course')
    category = models.CharField(blank=False, null=False, max_length=5, choices=Category_CHOICES, default='UCL')

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

class Lecture(Module):
    expected_hour = models.FloatField(null=True, blank=True)


class Part(models.Model):
    Part_CHOICES = (
        ('R', 'Reading'),
        ('V', 'Video'),
    )

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    lecture = models.ForeignKey(Lecture, blank=False, null=False, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(blank=False, null=False)
    expected_hour = models.FloatField(null=False, blank=False)
    part_type = models.CharField(max_length=1, choices=Part_CHOICES, blank=False, null=False, default='R')

class Reading(Part):
    file = models.FileField(upload_to='readings')

class Video(Part):
    link = models.TextField(blank=False,null=False)


class Quiz(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    description = models.TextField(max_length=40000)
    full_score = models.PositiveIntegerField()

class Test(Module):
    full_score = models.PositiveIntegerField()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, blank=True, null=True)
    test = models.ForeignKey(Test, blank=True, null=True)
    index = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    description = models.TextField(max_length=40000)
    image = models.ImageField(blank=True, null=True)

class MCQuestion(Question):
    pass

class Choices(models.Model):
    mcquestion = models.ForeignKey(MCQuestion)
    content = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

class BFQuestion(Question):
    answer = models.CharField(max_length=255)

class UserProgressTotal(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    completed = models.BooleanField(default=False)
    module_completed = models.ManyToManyField(Module, related_name="r_module")


class UserProgressPart(models.Model):
    user = models.ForeignKey(User)
    lecture = models.ForeignKey(Lecture)
    partProgress = models.ManyToManyField(Part, related_name="r_part")


class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    TYPE_CHOICES = (
        ('MC', 'Multiple Choice'),
        ('SR', 'Short Answer'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    answer = models.CharField(max_length=255, blank=True)


class Grade(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, blank=True)
    test = models.ForeignKey(Test, blank=True)
    grade = models.PositiveIntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    bio = models.TextField()


