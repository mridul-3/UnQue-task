from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Availability, Appointment
from .serializers import AvailabilitySerializer, AppointmentSerializer, StudentAppointmentSerializer
from .permissions import IsProfessor, IsOwnerOrProfessor
from django_filters.rest_framework import DjangoFilterBackend

# View for Professor to add availability
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrProfessor]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'status']
    ordering_fields = ['date', 'start_time']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'professor':
            return Appointment.objects.filter(professor=user)
        elif user.user_type == 'student':
            return Appointment.objects.filter(
                student=user,
                status=Appointment.SCHEDULED  # Only show scheduled appointments
            )
        return Appointment.objects.none()

    def get_serializer_class(self):
        if self.request.user.user_type == 'student':
            return StudentAppointmentSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        if self.request.user.user_type != 'student':
            raise PermissionDenied("Only students can book appointments.")
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.professor == request.user:
            appointment.status = Appointment.CANCELLED
            appointment.save()
            return Response({"message": "Appointment cancelled successfully"})
        return Response({"error": "You don't have permission to cancel this appointment"}, status=status.HTTP_403_FORBIDDEN)

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'professor']
    ordering_fields = ['date', 'start_time']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsProfessor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'professor':
            return Availability.objects.filter(professor=user)
        return Availability.objects.all()

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)