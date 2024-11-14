from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from blog.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import NotAuthenticated,PermissionDenied

class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the currently logged-in user as the author
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)  # Set the 'author' to the current user
        else:
            raise NotAuthenticated("You must be logged in to create a post.")

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Check if the user is the author of the post before updating
        if self.request.user == self.get_object().author:
            serializer.save(author=self.request.user)  # Only allow updating if the user is the author
        else:
            raise PermissionDenied("You do not have permission to edit this post.")

    def perform_destroy(self, instance):
        # Check if the user is the author of the post before deleting
        if self.request.user == instance.author:
            instance.delete()  # Only allow deleting if the user is the author
        else:
            raise PermissionDenied("You do not have permission to delete this post.")


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs.get('fk')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
            # Automatically assign the currently logged-in user as the user and the fk as post
            post_id = self.kwargs.get('fk')  # Get the post ID from the URL
            post = Post.objects.get(id=post_id)  # Retrieve the post object
            
            # Automatically set the logged-in user and the post foreign key
            serializer.save(user=self.request.user, post=post)
            

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user == self.request.user:
            # Allow the update and add a success message
            serializer = self.get_serializer(comment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Comment successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You do not have permission to edit this comment.")

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user == self.request.user:
            # Allow deletion and return a success message
            comment.delete()
            return Response({"message": "Comment successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You do not have permission to delete this comment.")
