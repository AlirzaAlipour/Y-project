
from django.conf import settings
from django.db import IntegrityError 
from django.shortcuts import get_object_or_404
from rest_framework import generics , viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Post, Comment, Like
from profiles.models import UserProfile
from .serializers import PostSerializer, CommentSerializer, LikeSerializer




class PostViewset (viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def perform_create(self, serializer):
        user = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(user=user)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        user = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(post_id=post_id, user=user)

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Like.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(UserProfile, user=self.request.user)
        
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            return
        except Like.DoesNotExist:
            serializer.save(post=post, user=user)
        