from django.db import models


# Create your models here.

def student_profile_image_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/student_profiles/student_<id>/<filename>
    return f'student_profiles/student_{instance.id}/{filename}'


class Student(models.Model):
    student_id = models.IntegerField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(upload_to=student_profile_image_path, default='default_profile.jpg', blank=True,
                                      null=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    year_level = models.ForeignKey('YearLevel', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='students')
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile_image} {self.last_name} {self.middle_name or ''} {self.last_name} {self.email} {self.date_of_birth}"


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
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Year: {self.year}"


class Section(models.Model):
    section = models.CharField(unique=True ,max_length=10)

    def __str__(self):
        return f"Section {self.section}"


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    students = models.ManyToManyField('Student', related_name='subjects', blank=True)
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
