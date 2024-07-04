from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Follower
from .serializers import ProfileSerializer, FollowerSerializer
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




class ProfileUpdateViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):  # Separate ViewSet for updates
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] 
    @action(detail=True, methods=['get', 'put', 'patch'], url_path='update_profile')
    def update_profile(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


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
        
