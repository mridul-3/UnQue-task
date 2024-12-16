import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appointments.models import User, Appointment, Availability
from datetime import datetime, timedelta
from rest_framework.exceptions import PermissionDenied

class AppointmentE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            username='student1', 
            password='password123', 
            email='student1@example.com',
            first_name='John',
            last_name='Doe',
            user_type='student',
            roll_number='S12345',
            branch='Computer Science',
            graduation_year=2024
        )
        self.professor = User.objects.create_user(
            username='professor1', 
            password='password123', 
            email='professor1@example.com',
            first_name='Jane',
            last_name='Smith',
            user_type='professor',
            professor_id='P12345',
            branch='Computer Science'
        )

    def test_full_appointment_flow(self):
        # 1. Professor logs in and creates availability
        self.login('professor1', 'password123')
        
        # Create availability
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        availability_data = {
            'date': tomorrow,
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'professor': self.professor.id
        }
        response = self.client.post(reverse('availability-list'), availability_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        availability_id = response.data['id']

        # 2. Student logs in and books appointment
        self.login('student1', 'password123')
        
        # Book appointment
        appointment_data = {
            'professor': self.professor.id,
            'date': tomorrow,
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'availability': availability_id
        }
        response = self.client.post(reverse('appointment-list'), appointment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Continue with rest of the flow
        self.view_filter_student_appointments()

        # Professor views and cancels
        self.login('professor1', 'password123')
        self.view_filter_professor_appointments()
        self.cancel_appointment()

        # Student verifies cancellation
        self.login('student1', 'password123')
        self.verify_cancelled_appointment()

    def login(self, username, password):
        response = self.client.post(reverse('login'), {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def create_availability(self):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        availability_data = {
            'date': tomorrow,
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'professor': self.professor.id
        }
        response = self.client.post(reverse('availability-list'), availability_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def view_filter_availabilities(self):
        response = self.client.get(reverse('availability-list') + '?ordering=-date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def view_professor_availabilities(self):
        response = self.client.get(reverse('availability-list') + f'?professor={self.professor.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def view_filter_student_appointments(self):
        response = self.client.get(reverse('appointment-list') + '?ordering=-date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def view_filter_professor_appointments(self):
        response = self.client.get(reverse('appointment-list') + '?ordering=-date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def cancel_appointment(self):
        appointment = Appointment.objects.filter(professor=self.professor).first()
        response = self.client.post(reverse('appointment-cancel', kwargs={'pk': appointment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def verify_cancelled_appointment(self):
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_student_cannot_create_availability(self):
        self.login('student1', 'password123')
        availability_data = {
            'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'start_time': '10:00:00',
            'end_time': '11:00:00'
        }
        response = self.client.post(reverse('availability-list'), availability_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_professor_cannot_book_appointment(self):
        self.login('professor1', 'password123')
        
        # Create availability first
        availability_id = self.create_availability()
        
        appointment_data = {
            'professor': self.professor.id,
            'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'availability': availability_id,
            'student': self.student.id
        }
        response = self.client.post(reverse('appointment-list'), appointment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def book_appointment(self):
        # First create availability and get its ID
        availability_id = self.create_availability()
        
        # Get the availability object to use its date and times
        availability = Availability.objects.get(id=availability_id)
        
        appointment_data = {
            'professor': self.professor.id,
            'date': availability.date,
            'start_time': availability.start_time,
            'end_time': availability.end_time,
            'availability': availability_id
        }
        response = self.client.post(reverse('appointment-list'), appointment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

