from rest_framework import serializers
from .models import Category , Item

def validate_image_extension(value):
    allowed_extensions = ["jpg", "jpeg", "png", "webp"]
    ext = value.name.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise serializers.ValidationError(
            f"Unsupported file type: {ext}. Allowed types are {', '.join(allowed_extensions)}."
        )
    return value

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','category','name','description','price1','image','discount']

    def validate_image(self, value):
        return validate_image_extension(value)


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  # allow passing an ID
        required=False,
        allow_null=True
    )
    parent_title = serializers.StringRelatedField(source="parent", read_only=True)
    subcategories = serializers.SerializerMethodField()
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title",  "parent", "parent_title", "subcategories", "items"]

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data




