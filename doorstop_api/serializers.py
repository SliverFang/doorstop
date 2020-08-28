from rest_framework import serializers
from doorstop_api import models

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
                'read_only':True,
            }
        }
    
    def create(self,validated_data):
        """create and return a new user"""
        user = models.UserProfile.objects.create_user(
            password=validated_data['password'],
            phone = validated_data['phone']
        )

        return user

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





