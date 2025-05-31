from rest_framework import serializers

from .models import (
    Student, Course, YearLevel, Section, Subject,
    Quiz, Exam, Activity,
    QuizResult, ExamResult, ActivityResult
)


def create_serializer(model_class):
    serializer_name = f"{model_class.__name__}Serializer"

    serializer_class = type(
        serializer_name,
        (serializers.ModelSerializer,),
        {
            "Meta": type("Meta", (), {
                "model": model_class,
                "fields": "__all__"
            })
        }
    )
    return serializer_class


StudentSerializer = create_serializer(Student)
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
