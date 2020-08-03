from django.urls import reverse
from faker import Faker
from nose.tools import eq_
from rest_framework import status
from rest_framework.test import APITestCase

from ...cart.test.factories import BasketFactory
from ...catalogue.test.factories import ProductFactory
from ...users.test.factories import UserFactory

fake = Faker()


class ListCreateOrderTestCase(APITestCase):
    """
    Tests /order get & post operation.
    """

    def setUp(self):
        self.url = reverse('order-list-create')
        self.user = UserFactory()
        self.basket = BasketFactory(user=self.user)
        self.product = ProductFactory()

    def test_place_order_anonymous(self):
        """
        Test if an anonymous user can not place order
        """
        response = self.client.post(
            self.url,
            {}
        )
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_place_order_authenticated(self):
        """
        Test if an authenticated user can add a product to his basket and place order
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        self.basket.add_product(self.product)
        response = self.client.post(
            self.url,
            {"basket": self.basket.id, "total": self.basket.total}
        )
        eq_(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url+str(response.data.get("id"))+"/")
        eq_(response.status_code, status.HTTP_200_OK)

    def test_place_order_authenticated_with_wrong_data(self):
        """
        Test so user can not manipulate data while placing order
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

        # Invalid basket id
        response = self.client.post(
            self.url,
            {"basket": 1, "total": 200}
        )
        eq_(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        # empty basket can not be submitted
        response = self.client.post(
            self.url,
            {"basket": self.basket.id, "total": 0}
        )
        eq_(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        # basket total != total submitted
        self.basket.add_product(self.product)
        response = self.client.post(
            self.url,
            {"basket": self.basket.id, "total": 10}
        )
        eq_(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_list_orders_anonymous(self):
        """
        A user must be logged in to get list of orders.
        """
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_orders_authenticated(self):
        """
        A user can fetch their own orders with the order API.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)
        for order in response.data:
            eq_(order.user, self.user)
