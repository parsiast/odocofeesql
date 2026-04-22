from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from django.shortcuts import get_object_or_404
from dashboard.permissions import IsSuperUser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article , Notification
from .serializers import ArticleSerializer,NotificationSerializer


@extend_schema(
    tags=["articles for admin (IsSuperUser)"]
)
class ArticleDetail(APIView):


    permission_classes = [IsSuperUser]

    @extend_schema(
        summary="Get article by id",
        responses={200: ArticleSerializer, 404: None},
    )
    def get(self,request,pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)



    @extend_schema(
        summary="Update article",
        request=ArticleSerializer,
        responses={200: ArticleSerializer, 404: None},
    )
    def put (self,request,pk):
        article = get_object_or_404(Article, pk=pk)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Delete article",
        responses={204: None, 404: None},
    )
    def delete (self,request,pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
        summary="Get all articles",
        responses={200: ArticleSerializer(many=True)},
        tags=["get all article (AllowAny)"]
)
class ArticleView(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["articles post for admin (IsSuperUser)"]
)
class ArticlePostView(APIView):
    permission_classes = [IsSuperUser]

    @extend_schema(
        summary="Create article",
        request=ArticleSerializer,
        responses={201: ArticleSerializer},
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['notifications for admin (IsSuperUser)']
)
class NotificationDetail(APIView):
    permission_classes = [IsSuperUser]

    @extend_schema(
        summary="Get notification by id",
        responses={200: NotificationSerializer, 404: None},
    )
    def get(self,request,pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer=NotificationSerializer(notification)
        return Response(serializer.data)

    @extend_schema(
        summary="Update notification",
        request=NotificationSerializer,
        responses={200: NotificationSerializer, 404: None},
    )
    def put(self,request,pk):
        notification = get_object_or_404(Notification, pk=pk)

        serializer=NotificationSerializer(notification,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Delete notification",
        responses={204: None, 404: None},
    )
    def delete (self,request,pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@extend_schema(
    summary="Get all notifications",
    responses={200: NotificationSerializer(many=True)},
    tags=['get all notifications (AllowAny)']
)
class NotificationView(APIView):
    permission_classes = [AllowAny]


    def get(self,request):
        notification=Notification.objects.all()
        serializer=NotificationSerializer(notification,many=True)
        return Response(serializer.data)

@extend_schema(
    tags=['notifications post admin (IsSuperUser)']
)
class NotificationPostView(APIView):
    permission_classes = [IsSuperUser]

    @extend_schema(
        summary="Create notification",
        request=NotificationSerializer,
        responses={201: NotificationSerializer},
    )
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)