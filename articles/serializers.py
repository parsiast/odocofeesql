from rest_framework import serializers
from .models import Article ,Notification

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title','content','image']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title','content']
