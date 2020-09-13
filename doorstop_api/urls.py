from django.urls import path,include
from rest_framework.routers import DefaultRouter
from doorstop_api import views

router = DefaultRouter()
router.register('user',views.UserProfileViewSet)
router.register('admin_user',views.UserProfileAdminViewSet)
router.register('address',views.UserProfileAddressViewSet)
router.register('resturant',views.ResturantViewSet)
router.register('cuisine',views.CuisineViewSet)
router.register('food',views.FoodViewSet)

urlpatterns = [
    path('getUserDetails/',views.GetUserDetails.as_view()),
    path('checkUserExist/',views.CheckUserExist.as_view()),
    path('getUserAllAddresses/',views.GetUserAllAddresses.as_view()),
    path('search/',views.SearchDatabase.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('filterResturants/',views.GetResturantsAfterPincodeFilter.as_view()),
    path('',include(router.urls))
]