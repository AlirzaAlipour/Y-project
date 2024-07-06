from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Follower

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture', 'followers_count', 'followings_count']
        read_only_fields = ['id', 'followers_count', 'followings_count']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.following.count()
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture']
        read_only_fields = ['id', 'user']


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'follower', 'followed']
        read_only_fields = ['id', 'follower', 'followed']

