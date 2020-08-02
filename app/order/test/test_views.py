from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import factory
from ..models import Basket
from ...catalogue.models import ProductClass, Product
from ...users.test.factories import UserFactory

fake = Faker()


class ListCreateOrderTestCase(APITestCase):
    """
    Tests /order get & post operation.
    """

    def setUp(self):
        self.url = reverse('order-list-create')
        self.user = UserFactory()
        pc, created = ProductClass.objects.get_or_create(name='XY', slug='xy')
        self.product = Product.objects.create(title='ABC', slug='abc', price=500, product_class=pc)

    def test_place_order_anonymous(self):
        """
        Test if an anonymous user can add a product to his basket
        """
        response = self.client.post(
            self.url,
            {"product": str(self.product.id), "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_place_order_authenticated(self):
        """
        Test if an authenticated user can add a product to his basket
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(
            reverse('basket'),
            {"product": self.product.id, "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            self.url,
            {"basket": response.data.get('id'), "total": response.data.get('total')}
        )
        eq_(response.status_code, status.HTTP_201_CREATED)

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
