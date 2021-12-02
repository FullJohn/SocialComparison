from rest_framework import serializers
from SocialComp.models import PostModel, QueryModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('PostId', 'url', 'title', 'description', 'thumbnail', 'channel', 'date', 'views', 'comments', 'likes')


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryModel
        fields = ('QueryId', 'platform', 'brand1', 'brand2', 'brand3', 'startDate', 'endDate')
