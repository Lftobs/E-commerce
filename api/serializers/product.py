from rest_framework import serializers

from store.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""
    class Meta:
        model = Product
        fields = "__all__"
        # extra_kwargs = {'seller': {'read_only': True}}