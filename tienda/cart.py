from decimal import Decimal
from .models import Producto


class Carrito:
    """Carrito guardado en la sesión: {id_producto: cantidad}."""

    def __init__(self, request):
        self.session = request.session
        self.datos = self.session.setdefault('carrito', {})

    def _guardar(self):
        self.session.modified = True

    def agregar(self, producto, cantidad=1):
        clave = str(producto.id)
        nueva = self.datos.get(clave, 0) + cantidad
        self.datos[clave] = max(1, min(nueva, producto.stock or 1))
        self._guardar()

    def cambiar(self, producto, cantidad):
        if cantidad <= 0:
            self.quitar(producto)
        else:
            self.datos[str(producto.id)] = min(cantidad, producto.stock or 1)
            self._guardar()

    def quitar(self, producto):
        self.datos.pop(str(producto.id), None)
        self._guardar()

    def vaciar(self):
        self.session['carrito'] = {}
        self._guardar()

    def lineas(self):
        productos = Producto.objects.filter(id__in=self.datos.keys())
        for p in productos:
            cantidad = self.datos[str(p.id)]
            yield {'producto': p, 'cantidad': cantidad, 'subtotal': p.precio * cantidad}

    def total(self):
        return sum((l['subtotal'] for l in self.lineas()), Decimal('0'))

    def __len__(self):
        return sum(self.datos.values())
