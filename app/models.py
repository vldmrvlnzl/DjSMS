from django.db import models


# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.code}"


class YearLevel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='year_levels')
    year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('course', 'year')

    def __str__(self):
        return f"Course:{self.course} Year:{self.year}"


class Section(models.Model):
    year_level = models.ForeignKey(YearLevel, on_delete=models.CASCADE, related_name='sections')
    section = models.CharField(max_length=10)

    class Meta:
        unique_together = ('year_level', 'section')

    def __str__(self):
        return f"Section {self.section} ({self.year_level})"


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} {self.name} {self.code}"


class BaseAssessment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    date = models.DateField()

    class Meta:
        abstract = True


class Quiz(BaseAssessment):
    pass


class Exam(BaseAssessment):
    pass


class Activity(BaseAssessment):
    description = models.TextField()


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'student')

    def __str__(self):
        return f"{self.student} {self.quiz.title} {self.score}"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student} {self.exam.title} {self.score}"


class ActivityResult(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'student')

    def __str__(self):
        return f"{self.student} {self.activity.title} {self.score}"
