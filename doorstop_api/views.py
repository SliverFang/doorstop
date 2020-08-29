from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied


from doorstop_api import serializers
from doorstop_api import models
from doorstop_api import permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# Create your views here.

class HelloApiView(APIView):
    """test"""
    def get(self,request,format=None):
        """returns a list of APIView features"""
        return Response({'message':'Hello','data':'ohyeah'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class= serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnData,IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('phone','email',)

    def list(self, request):
        raise PermissionDenied()

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileAdminViewSet(viewsets.ModelViewSet):
    """Handle setting special status to profiles by admin"""
    serializer_class= serializers.UserProfileAdminSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AdminOnlyApi,IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('phone','email',)
    