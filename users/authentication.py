from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        if not token:
            return None

        try:
            user, _ = self.authenticate_credentials(token)
        except AuthenticationFailed:
            return None

        return (user, token)

