import json
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from tienda.models import Categoria, Noticia, Producto, Servicio

# Carpeta donde se guardan las fotos de los productos.
CARPETA_FOTOS = Path(settings.BASE_DIR) / 'tienda' / 'Productos'


class Command(BaseCommand):
    help = 'Carga categorías, productos (con sus fotos), servicios y noticias desde data/productos.json'

    def handle(self, *args, **options):
        ruta = Path(settings.BASE_DIR) / 'data' / 'productos.json'
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        self.fotos = 0
        for c in datos['categorias']:
            Categoria.objects.update_or_create(
                slug=c['slug'],
                defaults={'nombre': c['nombre'], 'nombre_en': c.get('nombre_en', '')})
        for p in datos['productos']:
            categoria = Categoria.objects.get(slug=p.pop('categoria'))
            foto = p.pop('imagen', '')          # nombre del archivo dentro de tienda/Productos
            producto, _ = Producto.objects.update_or_create(slug=p['slug'], defaults={**p, 'categoria': categoria})
            self.asignar_foto(producto, foto)
        for sv in datos.get('servicios', []):
            Servicio.objects.update_or_create(nombre=sv['nombre'], defaults=sv)
        for n in datos.get('noticias', []):
            Noticia.objects.update_or_create(slug=n['slug'], defaults=n)
        self.stdout.write(self.style.SUCCESS(
            f'{Categoria.objects.count()} categorías, {Producto.objects.count()} productos, '
            f'{Servicio.objects.count()} servicios y {Noticia.objects.count()} noticias en la base de datos. '
            f'Fotos vinculadas: {self.fotos}.'))

    def asignar_foto(self, producto, nombre):
        """Copia la foto de tienda/Productos a media/productos y la guarda en el campo imagen."""
        if not nombre:
            # Sin "imagen" en el JSON: se busca un archivo que se llame igual que el slug (ej. yamaha-f310.webp).
            for ext in ('webp', 'jpg', 'jpeg', 'png'):
                if (CARPETA_FOTOS / f'{producto.slug}.{ext}').exists():
                    nombre = f'{producto.slug}.{ext}'
                    break
        if not nombre:
            return
        origen = CARPETA_FOTOS / nombre
        if not origen.exists():
            self.stdout.write(self.style.WARNING(f'No se encontró la foto {nombre} en tienda/Productos'))
            return
        destino = Path(settings.MEDIA_ROOT) / 'productos' / nombre
        destino.parent.mkdir(parents=True, exist_ok=True)
        if not destino.exists():
            shutil.copy2(origen, destino)
        producto.imagen = f'productos/{nombre}'
        producto.save(update_fields=['imagen'])
        self.fotos += 1
