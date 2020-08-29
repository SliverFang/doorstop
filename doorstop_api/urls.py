from django.urls import path,include
from rest_framework.routers import DefaultRouter
from doorstop_api import views

router = DefaultRouter()
router.register('user',views.UserProfileViewSet)
router.register('admin_user',views.UserProfileAdminViewSet)

urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view()),
    path('checkUserExist/',views.checkUserExist.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]