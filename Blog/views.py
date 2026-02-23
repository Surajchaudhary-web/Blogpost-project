from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Pagination class
class SmallPagePagination(PageNumberPagination):
    page_size = 2   # 2 posts per page
    page_size_query_param = 'page_size'  # optional
    max_page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles CRUD operations for Blog Posts.
    - list(): Get all posts
    - retrieve(): Get single post
    - create(): Create new post
    - update(): Update post
    - destroy(): Delete post
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    #  Permissions: anyone can read, only authors can edit
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Pagination
    pagination_class = SmallPagePagination

    # Filters & Search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__name']
    filterset_fields = ['tags', 'created_at']

    # Automatically assign logged-in user as author when creating
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Restrict update to author only
    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You cannot edit this post.")
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
        Automatically assign logged-in user as author.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    # Optional: add pagination for comments
    # pagination_class = SmallPagePagination
