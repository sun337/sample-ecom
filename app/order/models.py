from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from app.cart.models import Basket


class Order(TimeStampedModel):
    """
    The main order model
    """
    basket = models.ForeignKey(
        Basket,
        verbose_name=_("Basket"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    currency = models.CharField(_("Currency"), max_length=12, default='INR')
    total = models.DecimalField(_("Order total"), decimal_places=2, max_digits=12)
    # Use the status field to indicate that an order is processing / cancelled
    CREATED, PROCESSING, CLOSED, CANCELLED = ("Created", "Processing", "Delivered", "Cancelled")
    STATUS_CHOICES = (
        (CREATED, _("Created - order placed")),
        (PROCESSING, _("Processing - order is being processed")),
        (CLOSED, _("Delivered - order has been successfully delivered")),
        (CANCELLED, _("Cancelled - order has been cancelled"))
    )
    status = models.CharField(
        _("Status"),
        default=CREATED,
        max_length=100,
        blank=True,
        choices=STATUS_CHOICES
    )
