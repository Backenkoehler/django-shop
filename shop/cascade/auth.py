# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from shop import settings as shop_settings
from shop.models.auth import get_customer
from .plugin_base import ShopPluginBase


class ShopLoginPlugin(ShopPluginBase):
    """
    A placeholder plugin which provides a login box to be added to any placeholder.
    """
    name = _("Login Form")
    parent_classes = ('BootstrapColumnPlugin',)
    cache = False

    def get_render_template(self, context, instance, placeholder):
        template_names = [
            '{}/auth/login.html'.format(shop_settings.APP_LABEL),
            'shop/auth/login.html',
        ]
        return select_template(template_names)

    def render(self, context, instance, placeholder):
        user = get_customer(context['request'])
        if not user.is_authenticated():
            return super(ShopLoginPlugin, self).render(context, instance, placeholder)

plugin_pool.register_plugin(ShopLoginPlugin)
