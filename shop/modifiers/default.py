# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from shop.modifiers.base import PaymentModifier, ShippingModifier


class PayOnDeliveryModifier(PaymentModifier):
    """
    This modifiers has not influence on the cart final. It can be used,
    to enable the customer to pay the products on delivery.
    """
    identifier = 'pay-on-delivery'

    def get_choice(self):
        return (self.identifier, _("Pay on delivery"))


class SelfCollectionModifier(ShippingModifier):
    """
    This modifiers has not influence on the cart final. It can be used,
    to enable the customer to pick up the products in the shop.
    """
    identifier = 'self-collection'

    def get_choice(self):
        return (self.identifier, _("Self collection"))
