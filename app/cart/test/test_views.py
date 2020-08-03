from django.urls import reverse
from faker import Faker
from nose.tools import eq_
from rest_framework import status
from rest_framework.test import APITestCase

from ...catalogue.models import Product, ProductClass
from ...catalogue.test.factories import ProductFactory
from ...users.test.factories import UserFactory

fake = Faker()


class AddRetrieveBasketTestCase(APITestCase):
    """
    Tests /cart post operation.
    """

    def setUp(self):
        self.url = reverse('basket')
        self.user = UserFactory()
        self.product1 = ProductFactory()
        self.product2 = ProductFactory(is_public=False)

    def test_add_product_anonymous(self):
        """
        Test if an anonymous user can add a product to his basket
        """
        response = self.client.post(
            self.url,
            {"product": str(self.product1.id), "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_not_public_product_authenticated(self):
        """
        Test if an authenticated user can add a product to his basket
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(
            self.url,
            {"product": self.product2.id, "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_add_product_authenticated(self):
        """
        Test if an authenticated user can add a product to his basket
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(
            self.url,
            {"product": self.product1.id, "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_200_OK)
        line0 = response.data.get('lines')[0]
        eq_(str(line0["product"]), self.product1.id)
        eq_(line0["quantity"], 5)

    def test_add_product_with_wrong_data(self):
        """
        Test if an authenticated user can add a product to his basket
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(
            self.url,
            {"product": self.product1.id, "quantity": -1}
        )
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_basket_anonymous(self):
        """
        A user must be logged in ro get basket.
        """
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_basket_authenticated(self):
        """
        A user can fetch their own basket with the basket API and get's the same basket every time.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)
