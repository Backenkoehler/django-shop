# -*- coding: utf-8 -*-
from decimal import Decimal
from shop.cart.cart_modifiers_base import BaseCartModifier, ExtraEntryLine


class TenPercentGlobalTaxModifier(BaseCartModifier):
    """
    A basic Tax calculator: it simply adds a taxes field to the *order*,
    and makes it a fixed percentage of the subtotal (10%)

    Obviously, this is only provided as an example, and anything serious should
    use a more dynamic configuration system, such as settings or models to
    hold the tax values...
    """
    modifier_name = 'ten_percent_global_tax'
    TAX_PERCENTAGE = Decimal('10')

    def get_extra_cart_line(self, cart, state):
        """
        Add a field on cart.extra_entry_line:
        """
        taxes = (self.TAX_PERCENTAGE / 100) * cart.current_total
        return ExtraEntryLine(label='Taxes total', value=taxes)


class TenPercentPerItemTaxModifier(BaseCartModifier):
    """
    This adds a 10% tax cart modifier, calculated on the item's base price,
    plus any modifier applied to the cart item *so far* (order matters!).

    Make sure the moment you apply taxes comply with your local regulations!
    Some countries insist that taxes are calculated after/before discounts, and
    so forth
    """
    modifier_name = 'ten_percent_per_item_tax'
    TAX_PERCENTAGE = Decimal("10")

    def get_extra_cart_item_line(self, cart_item, state):
        tax_amount = (self.TAX_PERCENTAGE / 100) * cart_item.current_total

        return ExtraEntryLine(label='Taxes (10%)', value=tax_amount)
