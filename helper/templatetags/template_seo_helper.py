# coding: utf-8

from django import template
import types
import string
import re

register = template.Library()

tr = string.maketrans(
    'AÁÄBCČDĎEÉĚËFGHIÍJKLĹĽMNŇOÓÔÖPQRŔŘSŠTŤUÚŮÜVWXYÝZŽaáäbcčdďeéěëfghiíjklĺľmnňoóôöpqrŕřsštťuúůüvwxyýzž'.decode('utf-8').encode('cp1250'),
    'AAABCCDDEEEEFGHIIJKLLLMNNOOOOPQRRRSSTTUUUUVWXYYZZaaabccddeeeefghiijklllmnnoooopqrrrssttuuuuvwxyyzz'
)

@register.filter
def to_seo(value):
    if type(value) != types.UnicodeType:
        value = value.decode('utf-8')
    value = value.encode('cp1250')
    value = value.translate(tr)
    value = re.sub(r'([^A-Za-z0-9]+)', r'-', value)
    return value

@register.filter
def to_url(value):
    value = re.sub(
        r'\b(([\w-]+:\/\/?|www[.])[^\s()<>]+(?:([\w\d]+)|([^[:punct:]\s]|\/)))',
        r'<a href="/link/\g<0>" target="_blank">\g<0></a>',
        value
    )
    return value

@register.filter
def to_nl(value):
    value = re.sub(r'(\r\n|\n)', r'\n', value)
    value = re.sub(r'\n', r'<br />', value)
    value = re.sub(r'<br \/><br \/>(?:<br \/>)+', r'<br /><br />', value)
    return value

@register.filter
def to_js(value):
    value = re.sub(r"'", r'&#39;', value)
    return value