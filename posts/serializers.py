from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'tags', 'created_at']

    def validate(self, data):
        if 'title' not in data or 'content' not in data:
            raise serializers.ValidationError("Title and content are required.")
        return data
