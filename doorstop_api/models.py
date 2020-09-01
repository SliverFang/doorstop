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
        user.is_staff = True
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
    REQUIRED_FIELDS = ['email','name']

    def __str__(self):
        """Return string representation of our user"""
        return self.phone

class addressObject(models.Model):
    """User Address objects"""
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='all_addresses'
    )

    pincode = models.CharField(max_length=6,blank=False,null=False)
    house_no_building_no=models.CharField(max_length=250,blank=False,null=False)
    road_name_area_colony=models.CharField(max_length=250,blank=False,null=False)
    city=models.CharField(max_length=250,blank=False,null=False)
    state=models.CharField(max_length=250,blank=False,null=False)
    landmark=models.CharField(max_length=250,blank=True,null=True)
    name=models.CharField(max_length=250,blank=False,null=False)
    phone = models.CharField(max_length=10,blank=False,null=False)
    alternate_phone=models.CharField(max_length=10,blank=True,null=True)
    is_home=models.BooleanField(default=False)

    def _str_self(self):
        return self.status_text

    def as_json(self):
        return dict(
            pincode = self.pincode,
            house_no_building_no=self.house_no_building_no,
            road_name_area_colony=self.road_name_area_colony,
            city=self.city,
            state=self.state,
            landmark=self.landmark,
            name=self.name,
            phone = self.phone,
            alternate_phone=self.alternate_phone,
            is_home=self.is_home)