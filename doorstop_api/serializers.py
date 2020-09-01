from rest_framework import serializers
from doorstop_api import models
from django.contrib.auth.hashers import make_password

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name =  serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password','phone','address','is_staff')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            },
            'is_staff':
            {
                'read_only':True
            }
        }
    def create(self,validated_data):
        """create and return a new user"""
        user = models.UserProfile.objects.create_user(
            password=validated_data['password'],
            phone = validated_data['phone']
        )
        return user
    
    def update(self,instance, validated_data):
        if 'password' in validated_data:
            instance.password= make_password(validated_data['password'])
        if 'email' in validated_data:
            instance.email=validated_data['email']
        if 'phone' in validated_data:
            instance.phone=validated_data['phone']
        if 'name' in validated_data:
            instance.name=validated_data['name']
        instance.save()
        return instance


class UserProfileAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin api for user management"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password','phone','address','is_worker','is_staff')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }
    
    def create(self,validated_data):
        """create and return a new user"""
        user = models.UserProfile.objects.create_user(
            password=validated_data['password'],
            phone = validated_data['phone']
        )
        return user

class AddressObjectSerializer(serializers.ModelSerializer):
    """Serialises addressObject"""
    alternate_phone=serializers.CharField(required=False,allow_blank=True,allow_null=True)
    landmark=serializers.CharField(required=False,allow_blank=True,allow_null=True)
    is_home=serializers.BooleanField(required=False)
    class Meta:
        model = models.addressObject
        
        fields = ('id','user_profile','pincode','house_no_building_no'
        ,'road_name_area_colony','city','state','landmark'
        ,'name','phone','alternate_phone','is_home')
        extra_kwargs = {
            'user_profile':{
                'read_only':True
            }
        }
