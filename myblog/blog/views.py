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
    

    
    
    
    
