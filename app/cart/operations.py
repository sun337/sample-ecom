from app.cart.models import Basket


def get_user_basket(user):
    """
    get basket for a user.
    """
    basket, __ = Basket.objects.get_or_create(owner=user, status=Basket.OPEN)
    return basket
