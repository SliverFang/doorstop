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
    search_fields = ('phone',)

class CheckUserExist(APIView):
    
    def post(self,request,format=None):
        pdata = request.data.get('phone',"")
        count = models.UserProfile.objects.filter(phone=pdata).count()
        if(count!=0):
            return Response({'response':True})
        else:
            return Response({'response':False})

class GetUserDetails(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnData,IsAuthenticated,)
    def post(self,request,format=None):
        pdata = request.data.get('phone',"")
        user = models.UserProfile.objects.filter(phone=pdata)
        if(user):
            return Response({'id':user[0].id,'phone':user[0].phone,'name':user[0].name,'email':user[0].email,'address':user[0].address,'is_worker':user[0].is_worker,'is_staff':user[0].is_staff})
        else:
            return Response({'response':pdata})
    
class UserProfileAddressViewSet(viewsets.ModelViewSet):
    """Handles creating,reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnAddress,
        IsAuthenticated,
        )
    serializer_class = serializers.AddressObjectSerializer
    queryset = models.Address.objects.all()

    def perform_create(self,serializer):
        """sets the user profile to the loged in user"""
        """gets called every time a http post is called"""
        serializer.save(user_profile=self.request.user)

class GetUserAllAddresses(APIView):
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
        

class SearchDatabase(APIView):
    """Api to search database for food and resturants"""
    def get(self,request,format=None):
        query=request.data['query']
        if(query is None):
            return Response({})

        l=[]
        """cuisine = models.Cuisine.objects.filter(name__contains=query)

        for c in cuisine.iterator():
            l.append({'id':c.id,'name':c.name})"""
        
        resturants = models.Resturant.objects.filter(name__contains=query)

        for r in resturants.iterator():
            d={'id':r.id,'name':r.name,'pincode':r.pincode,'address':r.address,'owner':r.owner.id,'discount':r.discount,'isResturant':True}
            if r.photo and hasattr(r.photo, 'url'):
                d['photo']=r.photo.url
            l.append(d)
        
        foods = models.Food.objects.filter(name__contains=query)
        
        for f in foods.iterator():
            d={'id':f.id,'name':f.name,'description':f.description,'category':f.category,'cuisine':f.cuisine,'isFood':True}
            if f.photo and hasattr(f.photo, 'url'):
                d['photo']=f.photo.url
            l.append(d)

        return JsonResponse(l,safe=False)

class ResturantViewSet(viewsets.ModelViewSet):
    """Handles creating,reading and updating resturants"""
    """Listing of all resturants is blocked"""
    """Permission is only granted to creating users to update their resturants"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.IsResturantOwner,
        IsAuthenticated,
        )
    serializer_class = serializers.ResturantObjectSerializer
    queryset = models.Resturant.objects.all()

    def post(self, request, format=None):
        serializer = serializers.ResturantObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if(request.user.is_staff):
            resturant_list=models.Resturant.objects.all()
            serializer = serializers.ResturantObjectSerializer(resturant_list,many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied()
        

class CuisineViewSet(viewsets.ModelViewSet):
    """Handle cuisine objects"""
    """Viewset is only available to admins"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.AdminOnlyApi,
        IsAuthenticated,
        )
    serializer_class = serializers.CuisineObjectSerializer
    queryset = models.Cuisine.objects.all()

class FoodViewSet(viewsets.ModelViewSet):
    """Handles creating,reading and updating foods"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateAdminOnly,
        )
    serializer_class = serializers.FoodObjectSerializer
    queryset = models.Food.objects.all()

    def post(self, request, format=None):
        serializer = serializers.ResturantObjectSerializer(data=request.data)
        cuisine_name= request.POST.get('cuisine')
        req_cuisine=models.Cuisine.objects.filter(name=cuisine_name)
        if serializer.is_valid():
            serializer.save(cuisine=req_cuisine)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetResturantsAfterPincodeFilter(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self,request,format=None):
        pin = request.data['pincode']
        list_response=[]
        resturantslist = models.Resturant.objects.filter(pincode=pin)
        for resturant in resturantslist.iterator():
            list_response.append({'name':resturant.name,'pincode':resturant.pincode,'address':resturant.address,'photo':resturant.photo.url,'id':resturant.id,'discount':resturant.discount})
        
        return JsonResponse(list_response,safe=False)

class GetRestaurantAllFoods(APIView):
    """Api to return details of addresses of all user"""
    def post(self,request,format=None):
        id_data=request.data['id']
        restaurant=models.Resturant.objects.filter(id=id_data)
        l=[]
        if(restaurant.count()==0):
            return JsonResponse(l,safe=False)
        foods=restaurant[0].foods.all()
        for f in foods:
            relation=models.ResturantFood.objects.get(food=f,resturant=restaurant[0])
            l.append({'name':f.name,'description':f.description,'photo':f.photo.url,'category':f.category,'cuisine':f.cuisine.name,'price':relation.price})
        return JsonResponse(l, safe=False)


class FilterResturantByFoodAndPincode(APIView):
    """Api to return details of addresses of all user"""
    def post(self,request,format=None):
        id_data=request.data['id']
        pin=request.data['pincode']
        food=models.Food.objects.filter(id=id_data)
        l=[]
        if(food.count()==0):
            return JsonResponse(l,safe=False)
        resturants=food[0].resturant_set.filter(pincode=pin)
        for resturant in resturants:
            l.append({'name':resturant.name,'pincode':resturant.pincode,'address':resturant.address,'photo':resturant.photo.url,'id':resturant.id,'discount':resturant.discount})
        return JsonResponse(l, safe=False)

