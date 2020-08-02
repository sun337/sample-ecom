from rest_framework import generics, response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from app.base.permissions import IsOwner
from app.cart.models import Basket
from app.order.models import Order
from app.order.serializers import OrderSerializer, CheckoutSerializer


# class OrderList(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = (IsOwner,)
#
#     def get_queryset(self):
#         qs = Order.objects.all()
#         return qs.filter(user=self.request.user)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)


class OrderListCreate(APIView):
    order_serializer_class = OrderSerializer
    serializer_class = CheckoutSerializer

    def get(self, request):
        qs = Order.objects.filter(user=request.user)
        # paginator = PageNumberPagination()
        # paginator.page_size = 10
        # result_page = paginator.paginate_queryset(qs, request)
        # orders_data = self.order_serializer_class(result_page, many=True).data
        # return paginator.get_paginated_response(orders_data)
        orders_data = self.order_serializer_class(qs, many=True).data
        return response.Response(orders_data)

    def post(self, request, format=None, *args, **kwargs):
        c_ser = self.serializer_class(data=request.data, context={"request": request})

        if c_ser.is_valid():
            order = c_ser.save()
            o_ser = self.order_serializer_class(order, context={"request": request})
            return response.Response(o_ser.data, status.HTTP_201_CREATED)

        return response.Response(c_ser.errors, status.HTTP_406_NOT_ACCEPTABLE)
