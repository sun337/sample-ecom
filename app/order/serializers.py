
from django.db import transaction
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _

from app.cart.models import Basket
from app.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    The order serializer
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "basket", "user", "currency", "total", "status", "created")
        read_only_fields = ("basket", "status")


class CheckoutSerializer(serializers.Serializer):
    basket = serializers.PrimaryKeyRelatedField(queryset=Basket.objects.filter(status=Basket.OPEN))
    total = serializers.DecimalField(decimal_places=2, max_digits=12, required=False)

    def validate(self, attrs):
        request = self.context["request"]

        if request.user.is_anonymous:
            message = _("Anonymous checkout forbidden")
            raise serializers.ValidationError(message)

        basket = attrs.get("basket")

        if basket.num_items <= 0:
            message = _("Cannot checkout with empty basket")
            raise serializers.ValidationError(message)

        posted_total = attrs.get("total")
        total = basket.total
        if posted_total is not None:
            if posted_total != total:
                message = _("Total incorrect %s != %s" % (posted_total, total))
                raise serializers.ValidationError(message)

        # update attrs with validated data.
        attrs["total"] = total
        attrs["basket"] = basket
        return attrs

    def create(self, validated_data):
        try:
            basket = validated_data.get("basket")
            request = self.context["request"]
            user = request.user

            if basket.is_empty:
                raise ValueError(_("Empty baskets cannot be submitted"))
            if not basket.can_be_edited:
                raise ValueError(_("This basket cannot be edited"))

            if Order.objects.filter(basket=basket).exists():
                raise ValueError(_("There is already an order placed with this basket"))

            with transaction.atomic():
                # Ok - everything seems to be in order, let's place the order
                order_data = {
                    'basket': basket,
                    'currency': basket.currency,
                    'total': basket.total
                }
                if user and user.is_authenticated:
                    order_data['user'] = user
                order = Order(**order_data)
                order.save()
                basket.submit()

            return order
        except ValueError as e:
            raise exceptions.NotAcceptable(str(e))
