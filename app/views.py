from .serializers import *
from rest_framework import viewsets

def create_viewset(model_class, serializer_class):
    return type(
        f'{model_class.__name__}ViewSet',
        (viewsets.ModelViewSet,),
        {
            'queryset': model_class.objects.all(),
            'serializer_class': serializer_class,
        }
    )


StudentViewSet = create_viewset(Student, StudentSerializer)
TeacherViewSet = create_viewset(Teacher, TeacherSerializer)
CourseViewSet = create_viewset(Course, CourseSerializer)
YearLevelViewSet = create_viewset(YearLevel, YearLevelSerializer)
SectionViewSet = create_viewset(Section, SectionSerializer)
SubjectViewSet = create_viewset(Subject, SubjectSerializer)
QuizViewSet = create_viewset(Quiz, QuizSerializer)
ExamViewSet = create_viewset(Exam, ExamSerializer)
ActivityViewSet = create_viewset(Activity, ActivitySerializer)
QuizResultViewSet = create_viewset(QuizResult, QuizResultSerializer)
ExamResultViewSet = create_viewset(ExamResult, ExamResultSerializer)
ActivityResultViewSet = create_viewset(ActivityResult, ActivityResultSerializer)
