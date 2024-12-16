from django.urls import path
from .views import AvailabilityView, AppointmentView, CancelAppointmentView, StudentAppointmentsView

urlpatterns = [
    path('availability/', AvailabilityView.as_view(), name='availability'),
    path('appointments/', AppointmentView.as_view(), name='appointments'),
    path('appointments/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('my-appointments/', StudentAppointmentsView.as_view(), name='my_appointments'),
]