from django.conf import settings

from .cart import Carrito
from .models import Categoria


def carrito(request):
    c = Carrito(request)
    moneda = request.session.get('moneda', settings.MONEDA_BASE)
    if moneda not in settings.MONEDAS:
        moneda = settings.MONEDA_BASE
    return {
        'carrito_cantidad': len(c),
        'carrito_lineas': list(c.lineas()),
        'carrito_total': c.total(),
        'menu_categorias': Categoria.objects.all(),
        'moneda_actual': moneda,
        'monedas': list(settings.MONEDAS.keys()),
    }
