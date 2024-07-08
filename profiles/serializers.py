from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Follower

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    followers_list = serializers.HyperlinkedIdentityField(
        view_name='followers_list',
        lookup_field='id',
        lookup_url_kwarg='profile_id'
    )

    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture', 'followers_count', 'followings_count', 'followers_list']
        read_only_fields = ['id', 'followers_count', 'followings_count', 'followers_list']

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
    username = serializers.SerializerMethodField()
    follower = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True,
        lookup_field='id',
        lookup_url_kwarg='pk'
    )
    following = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True,
        lookup_field='id',
        lookup_url_kwarg='pk'
    )

    class Meta:
        model = Follower
        fields = ['id','username', 'follower', 'following']
    def get_username(self, obj):
        return obj.follower.user.username