from decimal import Decimal

from django import template
from django.conf import settings
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def precio(context, valor):
    """Convierte un precio en MXN (moneda base) a la moneda elegida."""
    codigo = context.get('moneda_actual') or settings.MONEDA_BASE
    if codigo not in settings.MONEDAS:
        codigo = settings.MONEDA_BASE
    cfg = settings.MONEDAS[codigo]
    convertido = Decimal(valor) * Decimal(str(cfg['tasa']))
    return f"{cfg['simbolo']}{convertido:,.2f} {codigo}"


@register.simple_tag
def traducido(objeto, campo):
    """Devuelve el campo en inglés (campo_en) si el idioma activo es inglés y existe; si no, el original."""
    if (get_language() or '').startswith('en'):
        texto = getattr(objeto, f'{campo}_en', '')
        if texto:
            return texto
    return getattr(objeto, campo)
