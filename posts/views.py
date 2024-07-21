from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST)
