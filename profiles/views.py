from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Follower
from .serializers import ProfileSerializer, FollowerSerializer, ProfileUpdateSerializer, FollowingSerializer
from django.conf import settings
from django.db import IntegrityError 
from rest_framework import generics , viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework import status


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):  # Use ReadOnlyModelViewSet
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer




class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = self.get_queryset().get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



class FollowerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def get_queryset(self):
        profile_pk = self.kwargs['profile_pk']
        return Follower.objects.filter(followed__id=profile_pk)

    def perform_create(self, serializer):
        profile_pk = self.kwargs['profile_pk']
        profile = UserProfile.objects.get(id=profile_pk)
        serializer.save(follower=self.request.user.profile, followed=profile)

    def create(self, request, *args, **kwargs):
        profile_pk = self.kwargs['profile_pk']
        profile = UserProfile.objects.get(id=profile_pk)
        follower = request.user.profile

        # Check if the follower-followed relationship already exists
        follower_obj = Follower.objects.filter(follower=follower, followed=profile).first()

        if follower_obj:
            # If the relationship exists, delete it (unfollow)
            follower_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # If the relationship doesn't exist, create it
            serializer = self.get_serializer(data={'follower': follower.id, 'followed': profile.id})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class FollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user_profile = UserProfile.objects.get(id=profile_id)
        return user_profile.followers.all()
    
class FollowingsListView(generics.ListAPIView):
    serializer_class = FollowingSerializer

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user_profile = UserProfile.objects.get(id=profile_id)
        return Follower.objects.filter(follower=user_profile)