from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from appointments.views import AppointmentViewSet, AvailabilityViewSet
from users.views import UserViewSet, register_user, login_user, logout_user

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
    path('api/logout/', logout_user, name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('docs/', include_docs_urls(title='College Appointment System API')),
]