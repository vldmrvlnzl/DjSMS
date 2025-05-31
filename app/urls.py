from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    CourseViewSet,
    YearLevelViewSet,
    SectionViewSet,
    SubjectViewSet,
    QuizViewSet,
    ExamViewSet,
    ActivityViewSet,
    QuizResultViewSet,
    ExamResultViewSet,
    ActivityResultViewSet,
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'yearlevels', YearLevelViewSet)
router.register('sections', SectionViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'quiz-results', QuizResultViewSet)
router.register(r'exam-results', ExamResultViewSet)
router.register(r'activity-results', ActivityResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
