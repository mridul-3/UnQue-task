from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model to include roles
class User(AbstractUser):
    STUDENT = 'student'
    PROFESSOR = 'professor'
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    professor_id = models.CharField(max_length=20, blank=True, null=True)
    branch = models.CharField(max_length=50)
    graduation_year = models.IntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def is_professor(self):
        return self.user_type == self.PROFESSOR