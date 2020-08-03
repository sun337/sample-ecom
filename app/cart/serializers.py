from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.cart.models import Basket, Line

User = get_user_model()


class BasketLineSerializer(serializers.ModelSerializer):
    """
    This serializer computes the prices of this line by using the basket
    strategy.
    """

    class Meta:
        model = Line
        fields = (
            "id",
            "product",
            "quantity",
            "currency",
            "price",
            "basket",
            "created",
        )


class BasketSerializer(serializers.ModelSerializer):
    lines = BasketLineSerializer(many=True, read_only=True)
    total = serializers.DecimalField(decimal_places=2, max_digits=12, required=False)
    currency = serializers.CharField(required=False)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Basket
        fields = (
            "id",
            "owner",
            "status",
            "lines",
            "total",
            "currency",
        )
