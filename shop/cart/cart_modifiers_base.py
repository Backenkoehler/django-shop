# -*- coding: utf-8 -*-


class ExtraEntryLine(object):
    """
    This object holds all the data which is added to an item as extra line when
    the cart is transformed into an order.
    """
    def __init__(self, label, value, data=None):
        """
        @param label: A descriptive text about this line.
        @param value: The decimal should be the amount that should get added to
            the current subtotal. It can be a negative value.
        The price difference for this item.
        @param data: A dictionary created by the modifier to store custom data.
        """
        self.label = label
        self.value = value
        self.data = data


class BaseCartModifier(object):
    """
    Price modifiers are the cart's counterpart to backends.
    It allows to implement Taxes and rebates / bulk prices in an elegant
    manner:

    Every time the cart is refreshed (via it's update() method), the cart will
    call all subclasses of this class registered with their full path in the
    settings.SHOP_CART_MODIFIERS setting, calling methods defined here are
    in the following sequence:

    1. pre_process_cart: Totals are not computed, the cart is "rough": only
        relations and quantities are available
    2. process_cart_item: Called for each cart_item in the cart. The current
       total for this item is available as current_total
    (2.a). get_extra_entry_line: A helper method provided for simple
           use cases. It returns an object of type ExtraEntryLine containing
           extra information about the current cart_item. It is OK to return
           None here.
    3. process_cart: Called once for the whole cart. Here, all fields relative
       to cart items are filled, as well as the cart subtotal. The current
       total is available as Cart.current_total (it includes modifications from
       previous calls to this method, in other modifiers)
    (3.a). get_extra_entry_line: A helper method for simple use cases. It
           shall return an object of type ExtraEntryLine containing extra
           information about the current cart It is OK to return
           None here.
    4. post_process_cart: all totals are up-to-date, the cart is ready to be
       displayed. Any change you make here must be consistent!
    """

    #==========================================================================
    # Processing hooks
    #==========================================================================

    def pre_process_cart(self, cart, state):
        """
        This method will be called before the cart starts being processed.
        Totals are not updated yet (obviously), but this method can be useful
        to gather some information on products in the cart.

        The `state` parameter is further passed to process_cart_item,
        process_cart, and post_process_cart, so it can be used as a way to
        store per-request arbitrary information.
        """
        pass

    def post_process_cart(self, cart, state):
        """
        This method will be called after the cart was processed.
        The Cart object is "final" and all the fields are computed. Remember
        that anything changed at this point should be consistent: if updating
        the price you should also update all relevant totals (for example).
        """
        pass

    def process_cart_item(self, cart_item, state):
        """
        This will be called for every line item in the Cart:
        Line items typically contain: product, unit_price, quantity...

        Subtotal for every line (unit price * quantity) is already computed,
        but the line total is 0, and is expected to be calculated in the Cart's
        update() method. Subtotal and total should NOT be written by this.

        Overrides of this method should however update cart_item.current_total,
        since it will potentially be used by other modifiers.

        The state parameter is only used to let implementations store temporary
        information to pass between cart_item_modifers and cart_modifiers
        """
        field = self.get_extra_cart_item_line(cart_item, state)
        if field != None:
            price = field.value
            cart_item.current_total = cart_item.current_total + price
            cart_item.extra_entry_lines[self.modifier_name] = field
        return cart_item

    def process_cart(self, cart, state):
        """
        This will be called once per Cart, after every line item was treated
        The subtotal for the cart is already known, but the Total is 0.
        Like for the line items, total is expected to be calculated in the
        cart's update() method.

        Line items should be complete by now, so all of their fields are
        accessible.

        Subtotal is accessible, but total is still 0.0. Overrides are expected
        to update cart.current_total.

        The state parameter is only used to let implementations store temporary
        information to pass between cart_item_modifers and cart_modifiers
        """
        field = self.get_extra_entry_line(cart, state)
        if field != None:
            price = field.value
            cart.current_total = cart.current_total + price
            cart.extra_entry_lines[self.modifier_name] = field
        return cart

    #==========================================================================
    # Simple methods
    #==========================================================================

    def get_extra_cart_item_line(self, cart_item, state):
        """
        Get an extra item line for the current cart_item:

        This allows to modify the price easily, simply return an object of
        type ExtraEntryLine or None if no extra line shall be added.

        In case your modifier is based on the current price (for example in
        order to compute value added tax for this cart item only) your
        override can access that price via ``cart_item.current_total``.

        A tax modifier would do something like this:
        >>> data = { 'foo': 'bar' }
        >>> return ExtraEntryLine(label='taxes', value=Decimal(9), data=data)

        And a rebate modifier would do something along the lines of:
        >>> data = { 'foo': 'bar' }
        >>> return ExtraEntryLine(label='rebate', value=Decimal(-9), data=data)

        More examples can be found in shop.cart.modifiers.*
        """
        return None  # Does nothing by default

    def get_extra_entry_line(self, cart, state):
        """
        Get an extra line for the current cart:

        This allows to modify the price easily, simply return an object of
        type ExtraEntryLine or None if no extra line shall be added.

        In case your modifier is based on the current price (for example in
        order to compute value added tax for the whole current price) your
        override can access that price via ``cart.current_total``. That is the
        subtotal, updated with all cart modifiers so far)

        >>> data = { 'foo': 'bar' }
        >>> return ExtraEntryLine(label='Taxes total', Decimal(19.00), data=data)
        """
        return None
