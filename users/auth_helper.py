from rest_framework_simplejwt.tokens import RefreshToken


def get_jwt_with_user(user):
    refresh = RefreshToken.for_user(user)
    print(user.username)
    print(refresh, refresh.access_token)
    token_dict = {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return token_dict

