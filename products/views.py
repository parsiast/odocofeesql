from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Category, Item
from .serializers import ItemSerializer ,CategorySerializer
from rest_framework.response import Response
from dashboard.permissions import IsSuperUser
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Create category",
    request=CategorySerializer,
    responses={201: CategorySerializer},
    tags=["category (isSuperuser)"],
)
class CategoryView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @extend_schema(
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=204)




@extend_schema(
    summary="Update item",
    request=ItemSerializer,
    responses={200: ItemSerializer},
    tags=["item (isSuperuser)"],
)
class ItemView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=204)



class CategoryGets(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get category",
        responses={200: CategorySerializer},
        tags=["showcategory (AllowAny)"],
    )
    def get(self, request, pk=None):
        if pk:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ItemGets(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get item(s)",
        responses={200: ItemSerializer},
        tags=["Itemshow (AllowAny)"],
    )
    def get(self, request, pk=None):
        if pk:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


