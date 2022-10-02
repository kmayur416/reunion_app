from rest_framework import serializers
from app.models import *


class ProfileSerializer(serializers.ModelSerializer):
    no_of_following = serializers.SerializerMethodField()
    no_of_followers = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('email', 'username', 'first_name',
                  'last_name', 'no_of_following', 'no_of_followers')

    @classmethod
    def get_no_of_following(self,instance):
        no_of_following = 0
        if instance.following:
            no_of_following = len(instance.following)
        return no_of_following
    
    @classmethod
    def get_no_of_followers(self,instance):
        no_of_followers = 0
        if instance.followers:
            no_of_followers = len(instance.followers)
        return no_of_followers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Profile(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostsSerializer(serializers.ModelSerializer):
    no_of_comments = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        exclude = ('likes', )
    
    @classmethod
    def get_no_of_likes(self,instance):
        no_of_likes = 0
        if instance.likes:
            no_of_likes = len(instance.likes)
        return no_of_likes
    
    @classmethod
    def get_no_of_comments(self,instance):
        no_of_comments = 0
        if instance.comment:
            no_of_comments = len(instance.comment)
        return no_of_comments
