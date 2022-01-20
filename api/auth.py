from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        if not user.is_superuser:
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response({'Error': 'Not found'})
