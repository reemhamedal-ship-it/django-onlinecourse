from django.contrib import admin
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')


class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Submission)
