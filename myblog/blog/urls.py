from django.urls import path
from blog.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    
    path('posts/<int:fk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),  
    path('posts/<int:fk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),  
]
