from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from rest_framework.exceptions import ValidationError

from app.catalogue.models import Product


class Basket(TimeStampedModel):
    """
    Basket object
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name=_("Owner")
    )
    # Basket statuses
    # - Frozen is for when a basket is in the process of being submitted
    #   and we need to prevent any changes to it.
    OPEN, SAVED, FROZEN, SUBMITTED = ("Open", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(_("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)
    date_submitted = models.DateTimeField(_("Date submitted"), null=True, blank=True)

    # Only if a basket is in one of these statuses can it be edited
    editable_statuses = (OPEN, SAVED)

    def __str__(self):
        return _(
            "%(status)s basket (owner: %(owner)s, lines: %(num_lines)d)") \
            % {'status': self.status,
               'owner': self.owner,
               'num_lines': self.num_lines}

    # ============
    # Basket Manipulation
    # ============

    def add_product(self, product, quantity=1):
        """
        Add a product to the basket
        """
        if not self.id:
            self.save()

        if not product.price:
            raise ValidationError("Strategy hasn't found a price for product %s" % product)

        defaults = {
            'quantity': quantity,
            'price': product.price,
            'currency': product.currency,
        }
        try:
            line, created = self.lines.get_or_create(product=product, defaults=defaults)
            if not created:
                line.quantity = max(0, line.quantity + quantity)
                line.save()
                if line.quantity <= 0:
                    line.delete()
        except Exception as e:
            raise ValidationError(str(e))

    def submit(self):
        """
        Mark this basket as submitted
        """
        self.status = self.SUBMITTED
        self.date_submitted = now()
        self.save()

    # =======
    # Helpers
    # =======

    def _get_total(self):
        """
        For executing a named method on each line of the basket
        and returning the total.
        """
        total = Decimal('0.00')
        for line in self.lines.all():
            try:
                total += getattr(line, 'price')*getattr(line, 'quantity')
            except ObjectDoesNotExist:
                # Handle situation where the product may have been deleted
                pass
        return total

    # ==========
    # Properties
    # ==========

    @property
    def total(self):
        """
        Return total line price
        """
        return self._get_total()

    @property
    def is_empty(self):
        """
        Test if this basket is empty.
        """
        return self.id is None or self.num_lines == 0 or self.num_items == 0

    @property
    def num_lines(self):
        """
        Return number of lines.
        """
        return self.lines.all().count()

    @property
    def num_items(self):
        """
        Return number of items.
        """
        return sum(line.quantity for line in self.lines.all())

    @property
    def can_be_edited(self):
        """
        Test if a basket can be edited
        """
        return self.status in self.editable_statuses

    @property
    def currency(self):
        for line in self.lines.all():
            return line.currency


class Line(TimeStampedModel):
    """
    A line of a basket (product and a quantity)
    """
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_("Basket"))

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='basket_lines',
        verbose_name=_("Product"))

    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    currency = models.CharField(_("Currency"), max_length=12, default='INR')
    price = models.DecimalField(_('Price incl. Tax'), decimal_places=2, max_digits=12, null=True)

    class Meta:
        # Enforce sorting by order of creation.
        ordering = ['created', 'pk']

    def __str__(self):
        return _(
            "Basket #%(basket_id)d, Product #%(product_id)d, quantity"
            " %(quantity)d") % {'basket_id': self.basket.pk,
                                'product_id': self.product.pk,
                                'quantity': self.quantity}

    def save(self, *args, **kwargs):
        if not self.basket.can_be_edited:
            raise PermissionDenied(
                _("You cannot modify a %s basket") % (
                    self.basket.status.lower(),))
        return super().save(*args, **kwargs)
