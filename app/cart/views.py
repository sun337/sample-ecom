from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.cart.operations import get_user_basket
from app.cart.serializers import BasketSerializer
from app.catalogue.serializers import AddProductSerializer


class BasketRetrieveCreate(APIView):
    """
    GET: Retrieve your basket.
    POST: Add a certain quantity of a product to the basket.
    POST(url, quantity)
    {
        "product": "id",
        "quantity": 6
    }
    """
    permission_classes = (IsAuthenticated,)
    add_product_serializer_class = AddProductSerializer
    serializer_class = BasketSerializer

    def get(self, request, *args, **kwargs):  # pylint: disable=redefined-builtin
        basket = get_user_basket(request.user)
        ser = self.serializer_class(basket, context={"request": request})
        return Response(ser.data)

    def validate(self, basket, product, quantity):  # pylint: disable=unused-argument
        # if not quantity > 0:
        #     return False, 'Quantity must be a positive integer'
        if not product.is_public:
            return False, 'Product not available for sale'
        return True, None

    def post(self, request, *args, **kwargs):  # pylint: disable=redefined-builtin
        p_ser = self.add_product_serializer_class(
            data=request.data, context={"request": request}
        )
        if p_ser.is_valid():
            basket = get_user_basket(request.user)
            product = p_ser.validated_data["product"]
            quantity = p_ser.validated_data["quantity"]

            basket_valid, message = self.validate(basket, product, quantity)
            if not basket_valid:
                return Response(
                    {"reason": message}, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            basket.add_product(product, quantity=quantity)
            ser = self.serializer_class(basket, context={"request": request})
            return Response(ser.data)
        return Response({"reason": p_ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
