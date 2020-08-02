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


class AddRetrieveBasketTestCase(APITestCase):
    """
    Tests /cart post operation.
    """

    def setUp(self):
        self.url = reverse('basket')
        self.user = UserFactory()
        pc, created = ProductClass.objects.get_or_create(name='XY', slug='xy')
        self.product1 = Product.objects.create(title='ABC', slug='abc', price=500, product_class=pc)
        self.product2 = Product.objects.create(title='ABC', slug='abc', price=500, is_public=False, product_class=pc)

    def test_add_product_anonymous(self):
        """
        Test if an anonymous user can add a product to his basket
        """
        response = self.client.post(
            self.url,
            {"product": str(self.product1.id), "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_product_authenticated(self):
        """
        Test if an authenticated user can add a product to his basket
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(
            self.url,
            {"product": self.product2.id, "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        response = self.client.post(
            self.url,
            {"product": self.product1.id, "quantity": 5}
        )
        eq_(response.status_code, status.HTTP_200_OK)
        line0 = response.data.get('lines')[0]
        eq_(line0["product"], self.product1.id)
        eq_(line0["quantity"], 5)

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
