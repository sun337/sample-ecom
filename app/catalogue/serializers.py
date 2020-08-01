from rest_framework import serializers

from app.catalogue.models import Product


class AddProductSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializes and validates an add to basket request.
    """

    quantity = serializers.IntegerField(required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects)
