from app.cart.models import Basket


def get_user_basket(user):
    """
    get basket for a user.
    """
    try:
        basket, __ = Basket.open.get_or_create(owner=user)
    except Basket.MultipleObjectsReturned:
        # Not sure quite how we end up here with multiple baskets.
        # We merge them and create a fresh one
        old_baskets = list(Basket.open.filter(owner=user))
        basket = old_baskets[0]
        for other_basket in old_baskets[1:]:
            basket.merge(other_basket, add_quantities=False)
    return basket
