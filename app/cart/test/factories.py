import factory

from app.cart.models import Basket
from app.catalogue.test.factories import ProductFactory
from app.users.test.factories import UserFactory


class BasketFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'cart.Basket'
        django_get_or_create = ('user', 'status')

    user = factory.SubFactory(UserFactory)
    status = Basket.OPEN


class LineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'cart.Line'
        django_get_or_create = ('id',)

    currency = 'INR'
    price = 100
    product = factory.SubFactory(ProductFactory)
    basket = factory.SubFactory(BasketFactory)
    quantity = 5
