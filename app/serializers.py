from rest_framework import serializers
from .models import *


def create_serializer(model_class):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
    return GenericSerializer

StudentSerializer = create_serializer(Student)
TeacherSerializer = create_serializer(Teacher)
CourseSerializer = create_serializer(Course)
YearLevelSerializer = create_serializer(YearLevel)
SectionSerializer = create_serializer(Section)
SubjectSerializer = create_serializer(Subject)
QuizSerializer = create_serializer(Quiz)
ExamSerializer = create_serializer(Exam)
ActivitySerializer = create_serializer(Activity)
QuizResultSerializer = create_serializer(QuizResult)
ExamResultSerializer = create_serializer(ExamResult)
ActivityResultSerializer = create_serializer(ActivityResult)