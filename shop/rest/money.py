# -*- coding: utf-8 -*-
from django.utils.formats import number_format
from rest_framework import renderers
from rest_framework import serializers
from rest_framework.utils import encoders
from shop.money import AbstractMoney


class JSONEncoder(encoders.JSONEncoder):
    """JSONEncoder subclass that knows how to encode Money."""

    def default(self, obj):
        if isinstance(obj, AbstractMoney):
            return number_format(obj)
        return super(JSONEncoder, self).default(obj)


class JSONRenderer(renderers.JSONRenderer):
    encoder_class = JSONEncoder


class MoneyField(serializers.Field):
    """Money objects are serialized into their readable notation."""

    def __init__(self, *args, **kwargs):
        kwargs.update(read_only=True)
        super(MoneyField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        return number_format(obj)
