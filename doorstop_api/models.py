from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self,phone,email=None,name=None,password=None):
        if not phone:
            raise ValueError('User must have a phone number')
        
        """Normalize email or basically set the second half to lower case"""
        if email:
            email= self.normalize_email(email)
        
        user = self.model(phone=phone,name=name,email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self,email,name,password):
        """create and save a new superuser with given details"""
        user = self.create_user(email,name,password)
        user.is_superuser=True
        user.is_staff =True
        user.is_admin = True
        user.save(using=self.db)
        return user

    def create_worker(self,email,name,password):
        """create and save a new superuser with given details"""
        user = self.create_user(email,name,password)
        user.is_worker=True
        user.save(using=self.db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    phone = models.CharField(max_length=10, blank=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone'
    

    def __str__(self):
        """Return string representation of user"""
        return self.email