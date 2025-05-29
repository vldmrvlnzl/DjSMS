from django.contrib import admin

from app.models import Student, Teacher, Course, YearLevel, Section, Subject, Quiz, Exam, Activity, QuizResult, \
    ExamResult, ActivityResult

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(YearLevel)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Exam)
admin.site.register(Activity)
admin.site.register(QuizResult)
admin.site.register(ExamResult)
admin.site.register(ActivityResult)