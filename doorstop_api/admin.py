from django.contrib import admin
from doorstop_api import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Address)
admin.site.register(models.Cuisine)
admin.site.register(models.Food)
admin.site.register(models.ResturantFood)
admin.site.register(models.Resturant)