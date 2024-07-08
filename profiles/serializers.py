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
    followings_list = serializers.HyperlinkedIdentityField(
        view_name='followings_list',
        lookup_field='id',
        lookup_url_kwarg='profile_id'
    )

    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture', 'followers_count', 'followings_count', 'followers_list', "followings_list"]
        read_only_fields = ['id', 'followers_count', 'followings_count', 'followers_list', "followings_list"]

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
    follower = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True,
        lookup_field='id',
        lookup_url_kwarg='pk'
    )
    follower_username = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ['id', 'follower', 'follower_username']

    def get_follower_username(self, obj):
        return obj.follower.user.username
    
class FollowingSerializer(serializers.ModelSerializer):
    followed = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True,
        lookup_field='id',
        lookup_url_kwarg='pk'
    )
    followed_username = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ['id', 'followed', 'followed_username']

    def get_followed_username(self, obj):
        return obj.followed.user.username