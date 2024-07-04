from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileUpdateViewSet, FollowerViewSet

router = DefaultRouter()
router.register("profile", ProfileViewSet, basename='profile')
router.register(r'profile/(?P<profile_pk>\d+)/update_profile', ProfileUpdateViewSet, basename='profil-update')
router.register(r'profile/(?P<profile_pk>\d+)/follow', FollowerViewSet, basename='follower')


urlpatterns = [
    path('', include(router.urls)),

]