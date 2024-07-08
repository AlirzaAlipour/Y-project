from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileUpdateView, FollowerViewSet, FollowersListView, FollowingsListView

router = DefaultRouter()
router.register("profiles", ProfileViewSet, basename='profile')
router.register(r'profiles/(?P<profile_pk>\d+)/follow', FollowerViewSet, basename='follower')


urlpatterns = [
    path('', include(router.urls)),
    path('profiles/<int:pk>/update_profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/<int:profile_id>/followers/', FollowersListView.as_view(), name='followers_list'),
    path('profiles/<int:profile_id>/followings/', FollowingsListView.as_view(), name='followings_list'),
]