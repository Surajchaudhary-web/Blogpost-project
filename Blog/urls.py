from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Create a router and register our viewsets
router = DefaultRouter()

# Register Post API
router.register('posts', PostViewSet, basename='post')

# Register Comment API
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
