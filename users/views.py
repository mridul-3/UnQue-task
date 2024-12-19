from rest_framework.response import Response
from rest_framework import status

from .auth_helper import get_jwt_with_user
from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token_dict = get_jwt_with_user(user)
        # token, _ = Token.objects.create(user=user, key=token_dict['access'])
        return Response({
            'token': token_dict['access'],
            'user_id': user.pk,
            'email': user.email,
            'user_type': user.user_type
        })
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    response = Response({"detail": "Successfully logged out."})
    response.delete_cookie('auth_token')
    return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]