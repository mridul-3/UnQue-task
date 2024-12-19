from django.db import models
from users.models import User

class Availability(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class Appointment(models.Model):
    SCHEDULED = 'scheduled'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (SCHEDULED, 'Scheduled'),
        (CANCELLED, 'Cancelled'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_appointments")
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="professor_appointments")
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SCHEDULED)