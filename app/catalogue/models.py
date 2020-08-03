import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from model_utils.models import TimeStampedModel
from rest_framework.exceptions import ValidationError


class ProductClass(models.Model):
    """
    Used for defining options and attributes for a subset of products.
    E.g. Books, DVDs and Toys. A product can only belong to one product class.
    At least one product class must be created when setting up a new deployment.
    Not necessarily equivalent to top-level categories but usually will be.
    """
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Slug'), max_length=128, unique=True)

    class Meta:
        app_label = 'catalogue'
        ordering = ['name']
        verbose_name = _("Product class")
        verbose_name_plural = _("Product classes")

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
    The base product object
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_public = models.BooleanField(
        _('Is public'),
        default=True,
        db_index=True,
        help_text=_("Show this product in search results and catalogue listings."))

    # Title is mandatory
    title = models.CharField(pgettext_lazy('Product title', 'Title'), max_length=255, blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=False)
    description = models.TextField(_('Description'), blank=True)
    currency = models.CharField(_("Currency"), max_length=12, default='INR')
    price = models.DecimalField(_('Price incl. Tax'), decimal_places=2, max_digits=12, null=True)
    #: "Kind" of product, e.g. T-Shirt, Book, etc.
    product_class = models.ForeignKey(
        ProductClass,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('Product type'), related_name="products",
        help_text=_("Choose what type of product this is"))

    # objects = ProductQuerySet.as_manager()

    class Meta:
        app_label = 'catalogue'
        ordering = ['-created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.id

    def clean(self):
        """
        Validate a product.
        """
        if not self.title:
            raise ValidationError(_("Your product must have a title."))
        if not self.product_class:
            raise ValidationError(_("Your product must have a product class."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
