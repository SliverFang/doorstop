from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.http import JsonResponse
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
    permission_classes = (permissions.UpdateOwnData,)
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

class checkUserExist(APIView):
    
    def post(self,request,format=None):
        pdata = request.data['phone']
        count = models.UserProfile.objects.filter(phone=pdata).count()
        if(count!=0):
            return Response({'response':True})
        else:
            return Response({'response':False})

class getUserDetails(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnData,IsAuthenticated,)
    def post(self,request,format=None):
        pdata = request.data['phone']
        user = models.UserProfile.objects.filter(phone=pdata)
        if(user):
            return Response({'id':user[0].id,'phone':user[0].phone,'name':user[0].name,'email':user[0].email,'address':user[0].address,'is_worker':user[0].is_worker,'is_staff':user[0].is_staff})
        else:
            return Response({'response':False})
    
class UserProfileAddressViewSet(viewsets.ModelViewSet):
    """Handles creating,reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnData,
        IsAuthenticated,
        )
    serializer_class = serializers.AddressObjectSerializer
    queryset = models.addressObject.objects.all()

    def perform_create(self,serializer):
        """sets the user profile to the loged in user"""
        """gets called every time a http post is called"""
        serializer.save(user_profile=self.request.user)

class getUserAllAddresses(APIView):
    """Api to return details of addresses of all user"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        data=request.user.all_addresses.all()
        l=[]
        for ao in data.iterator():
            l.append({'id':ao.id,'pincode':ao.pincode,'house_no_building_no':ao.house_no_building_no
            ,'road_name_area_colony':ao.road_name_area_colony,'city':ao.city,'state':ao.state,'landmark':ao.landmark
            ,'name':ao.name,'phone':ao.phone,'alternate_phone':ao.alternate_phone,'is_home':ao.is_home})
        return JsonResponse(l, safe=False)
        