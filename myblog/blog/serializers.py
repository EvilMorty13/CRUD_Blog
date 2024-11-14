from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    author = serializers.ReadOnlyField(source='author.id')
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author']


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)
    user = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = Comment
        fields = "__all__"