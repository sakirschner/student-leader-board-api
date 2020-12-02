from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions, viewsets, mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import User
from user.serializers import UserSerializer, AuthTokenSerializer
from user import serializers


class GetUsersView(generics.ListAPIView):
    """Lists all users from the database"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Return objects for all user"""
        return self.queryset.order_by('id')


class GetUserByIdView(generics.RetrieveUpdateDestroyAPIView):
    """Lists single user from the database by id"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self, **kwargs):
        """Return object for user"""
        return User.objects.get(id=self.kwargs['pk'])


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authetication user"""
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """Manage user in the database"""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.UserSerializer
        elif self.action == 'upload_image':
            return serializers.UserImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self,request, pk=None):
        """Upload an image to a user"""
        user = self.get_object()
        serializer = self.get_serializer(
            user,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
