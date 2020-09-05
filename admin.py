from typing import Any, Union

from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'price', 'hours', 'for_everyone')
    actions=['add_50_to_hour']
    def add_50_to_hour(modeladmin, request, queryset):
        for obj in queryset:
            x=obj.hours+50
            obj.hours = x
            print(obj.hours)
            obj.save()
        queryset.update()
    add_50_to_hour.short_description = "Add 50 hours"
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','city')
    actions=['upper_case_name']
    def upper_case_name(modeladmin, request, queryset):
        for obj in queryset:
            obj.first_name=obj.first_name.upper()
            obj.last_name = obj.last_name.upper()
            obj.save()
        queryset.update()
    upper_case_name.short_description = "Student Full Name"
admin.site.register(Topic)
# admin.site.register(Course)
# admin.site.register(Student)
admin.site.register(Order)
