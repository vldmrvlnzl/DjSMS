import uuid

from django.db import models


# Utility
def student_profile_image_path(instance, filename):
    return f'student_profiles/student_{instance.id}/{filename}'


# =========================
# Core Academic Structures
# =========================

class Course(models.Model):
    """Represents a degree or program."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class YearLevel(models.Model):
    """Represents a year level in a course."""
    year = models.PositiveSmallIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Year Levels"
        ordering = ['year']

    def __str__(self):
        return f"Year {self.year}"


class Section(models.Model):
    """Represents a section within a year level."""
    section = models.CharField(unique=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sections"
        ordering = ['section']

    def __str__(self):
        return f"Section {self.section}"


class Subject(models.Model):
    """
    Represents a subject taught in a course.
    - Each subject belongs to a course.
    - Subject code is unique within a course.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subjects',
        help_text="Course to which this subject belongs."
    )
    name = models.CharField(max_length=100, help_text="Name of the subject.")
    code = models.CharField(max_length=10, help_text="Subject code (unique within course).")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this subject was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this subject was last updated.")

    class Meta:
        verbose_name_plural = "Subjects"
        unique_together = ('course', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.course.code}"


# =========================
# Student Model
# =========================

class Student(models.Model):
    """Represents a student."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(upload_to=student_profile_image_path, default='default_profile.jpg', blank=True,
                                      null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True, blank=True, related_name='students')
    year_level = models.ForeignKey(YearLevel, on_delete=models.PROTECT, null=True, blank=True, related_name='students')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, null=True, blank=True, related_name='students')
    subject = models.ManyToManyField(Subject, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name} ({self.email})"


# =========================
# Assessments
# =========================

class BaseAssessment(models.Model):
    """Abstract base for assessments."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    total_marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.total_marks <= 0:
            raise ValueError("Total marks must be greater than zero.")

    def __str__(self):
        return f"{self.title} ({self.subject})"


class Quiz(BaseAssessment):
    """Quiz assessment."""
    pass


class Exam(BaseAssessment):
    """Exam assessment."""
    pass


class Activity(BaseAssessment):
    """Activity assessment."""
    description = models.TextField(blank=True, help_text="Description of the activity.")

    def __str__(self):
        return f"{self.title} ({self.subject})"


# =========================
# Assessment Results
# =========================

class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'student')
        ordering = ['-graded_at']

    def clean(self):
        if self.score > self.quiz.total_marks:
            raise ValueError("Score cannot exceed total marks of the quiz total marks")

    def __str__(self):
        return f"{self.student} - {self.quiz.title}: {self.score}"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['-graded_at']

    def clean(self):
        if self.score > self.exam.total_marks:
            raise ValueError("Score cannot exceed total marks of the exam.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam.title}: {self.score}"


class ActivityResult(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'student')
        ordering = ['-graded_at']

    def clean(self):
        if self.score > self.activity.total_marks:
            raise ValueError("Score cannot exceed total marks of the activity.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.activity.title}: {self.score}"
