from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import *
from blog.tasks import *

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
    
    def create(self, validated_data):
        post = super().create(validated_data)

        # Trigger the email sending task asynchronously
        send_post_creation_email.delay(post.title, post.author.email)

        return post


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        """
        Override the create method to trigger the Celery email task after saving a new comment.
        """
        comment = super().create(validated_data)  # Create the comment instance

        # Get the necessary data from the comment and related models
        post = comment.post
        post_title = post.title  # Post title
        comment_author = comment.user.username  # Comment author's username
        comment_content = comment.content  # Comment content
        post_author_email = post.author.email  # Post author's email

        # Trigger the Celery task to send the email notification
        send_comment_notification_email.delay(post_title, comment_author, comment_content, post_author_email)

        return comment