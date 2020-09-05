from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30,blank=False,default='unknown')
    def __str__(self):
        return self.name
class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    hours = models.PositiveIntegerField(default=1)
    interested = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    stages = models.PositiveIntegerField(default=3)
    def __str__(self):
        return self.name
    def discount(self):
        x=self.price
        return x
class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),('CG', 'Calgery'),('MR', 'Montreal'),('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    #username=models.CharField(max_length=50)
    def __str__(self):
        return self.username
class Order(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    book = models.CharField(max_length=60,blank=False,default='unknown')
    levels = models.PositiveIntegerField()
    ORDER_CHOICES = [('0', 'Cancelled'), ('1', 'Confirmed')]
    order_status = models.CharField(max_length=1, choices=ORDER_CHOICES, default='1')
    order_date = models.DateField()
    def __str__(self):
        return self.student.username
    def total_cost(self):
        return Course.objects.aggregate('price')
