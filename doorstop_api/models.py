from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    
    def create_user(self,phone, email=None, name=None, password=None):
        """Create a new user profile"""
        
        user = self.model(email=email,name=name,phone=phone)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,phone,email,name,password):
        """Create a new super user with given details"""
        user = self.create_user(phone,email,name,password)

        user.is_superuser= True
        user.is_staff=True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""

    email = models.EmailField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=500,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=10,unique=True)

    """Used internally by Django"""
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    """flag for workers to be included later"""
    is_worker = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return string representation of our user"""
        return self.phone
