#-*- coding: utf-8 -*-
from django.conf import settings
from django.core import exceptions
from django.utils.importlib import import_module


class CartModifiersPool(object):

    USE_CACHE = True

    def __init__(self):
        self._modifiers_list = []

    def get_modifiers_list(self):
        if not self.USE_CACHE or not self._modifiers_list:
            self._modifiers_list = self._load_modifiers_list()
        return self._modifiers_list

    def _load_modifiers_list(self):
        """
        Heavily inspired by django.core.handlers.base...
        """
        result = []
        modifier_names = []
        if not getattr(settings, 'SHOP_CART_MODIFIERS', None):
            return result

        for modifier_path in settings.SHOP_CART_MODIFIERS:
            try:
                mod_module, mod_classname = modifier_path.rsplit('.', 1)
            except ValueError:
                raise exceptions.ImproperlyConfigured(
                    '%s isn\'t a price modifier module' % modifier_path)
            try:
                mod = import_module(mod_module)
            except ImportError, e:
                raise exceptions.ImproperlyConfigured(
                    'Error importing modifier %s: "%s"' % (mod_module, e))
            try:
                mod_class = getattr(mod, mod_classname)
            except AttributeError:
                raise exceptions.ImproperlyConfigured(
                    'Price modifier module "%s" does not define a "%s" class' %
                        (mod_module, mod_classname))
            mod_instance = mod_class()
            if not hasattr(mod_instance, 'modifier_name'):
                raise exceptions.ImproperlyConfigured(
                    'The price modifier class "%s" does not define any "modifier_name"' %
                        mod_classname
                )
            class_identifier = getattr(mod_instance, 'modifier_name')
            if type(class_identifier) != str:
                raise exceptions.ImproperlyConfigured(
                    'The price modifier class "%s" contains an invalid modifier_name' %
                        mod_classname
                )
            if class_identifier in modifier_names:
                raise exceptions.ImproperlyConfigured(
                    'The price modifier class "%s" contains modifier_name "%s" '
                    'which is used by another modifier class' %
                    (mod_classname, class_identifier)
                )
            modifier_names.append(class_identifier)
            result.append(mod_instance)

        return result


cart_modifiers_pool = CartModifiersPool()
