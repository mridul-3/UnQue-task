from rest_framework import serializers
from .models import Availability, Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'student', 'professor', 'date', 'start_time', 'end_time', 'status']
        read_only_fields = ['status']

class StudentAppointmentSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'professor', 'professor_name', 'date', 'start_time', 'end_time', 'status']
        read_only_fields = ['status']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'professor', 'date', 'start_time', 'end_time']