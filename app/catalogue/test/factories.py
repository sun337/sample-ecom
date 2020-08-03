import factory


class ProductClassFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'catalogue.ProductClass'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'testname{n}')
    slug = factory.Sequence(lambda n: f'testslug{n}')


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'catalogue.Product'
        django_get_or_create = ('id',)

    id = factory.Faker('uuid4')
    title = factory.Sequence(lambda n: f'testtitle{n}')
    currency = 'INR'
    price = 100
    product_class = factory.SubFactory(ProductClassFactory)
    is_public = True
