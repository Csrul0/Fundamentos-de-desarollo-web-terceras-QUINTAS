# SoundBazaarBytes
ESTE ES UN PROYECTO PIA DE MATERIA FUDAMENTOS DE DESAROLLO WEB TERCERAS & QUINTAS

Tienda de música hecha con Django (proyecto PIA). El diseño parte de la plantilla Tailstore (Tailwind CSS, licencia MIT).

## Cómo correrlo en tu computadora

```
pip install -r requirements.txt
py manage.py migrate
py manage.py cargar_productos
py manage.py createsuperuser
py manage.py runserver
```

Abre http://127.0.0.1:8000/ para ver la tienda y http://127.0.0.1:8000/admin/ para administrarla.
La página necesita internet para cargar las fuentes, los íconos, Alpine y Swiper desde CDN.

## Qué incluye

- Inicio con slider y productos destacados, catálogo con búsqueda, filtro por categoría y orden por precio.
- Página de producto, carrito (guardado en la sesión) y checkout que registra el pedido.
- Idioma (español / inglés) y moneda (MXN / USD) desde la barra superior. La moneda base es el peso mexicano: los precios de la base de datos y los pedidos se guardan en MXN, y el dólar es solo una conversión de referencia.
- Noticias: listado y página de detalle, cargadas desde `data/productos.json` o desde el admin. Las últimas tres aparecen en el inicio.
- Servicios y citas: ajuste de guitarra, cambio de cuerdas, afinación y más. El formulario agenda la cita (lunes a sábado, 10:00 a 18:00) y no permite fechas pasadas, domingos ni un horario ya ocupado. Las citas se ven en el admin.
- Quiénes somos (con misión y visión) y página de contacto con datos de la tienda y formulario (los mensajes se ven en el admin).
- Registro, login y logout con el sistema de usuarios de Django.
- Datos dinámicos: los productos se cargan del archivo `data/productos.json` con `python manage.py cargar_productos`, y también se pueden agregar o editar desde el admin.
- Animaciones con jQuery (en `static/js/script.js`): las tarjetas de producto aparecen al hacer scroll, los mensajes se despliegan y se ocultan solos, y un botón "Volver arriba" sube la página con animación.

## Estructura

- `config/`: configuración del proyecto y URLs principales.
- `tienda/`: modelos, vistas, formularios, carrito y templates.
- `static/`: CSS, JS e imágenes. Las imágenes de productos son de relleno (`static/images/products/`); para usar fotos reales sube la imagen desde el admin en cada producto.
- `data/productos.json`: catálogo inicial.

## Si cambias el diseño con Tailwind

El CSS ya está compilado en `static/css/styles.css`. Si agregas clases nuevas en los templates: `npm install` y luego `npm run build`.

## Fotos de productos

Las fotos están en `tienda/Productos/`. Cada producto de `data/productos.json` puede llevar el campo `"imagen"` con el nombre del archivo (por ejemplo `"imagen": "316EmWDalaL.webp"`). Al correr `py manage.py cargar_productos`, el comando copia la foto a `media/productos/` y la vincula al producto. Si un producto no tiene `"imagen"`, el comando busca un archivo que se llame igual que su `slug` (por ejemplo `yamaha-f310.webp`). Para agregar un producto con foto: ponle su entrada en el JSON, guarda la imagen en `tienda/Productos/` y vuelve a correr el comando.

## Idioma y moneda

- **Idioma:** usa el sistema de traducciones de Django. Los textos en español están en los templates y el inglés está en `locale/en/LC_MESSAGES/django.po` (ya compilado en `django.mo`). Los productos, servicios, categorías y noticias tienen campos `_en` (por ejemplo `nombre_en`) que se llenan desde `data/productos.json` o desde el admin. Si un campo `_en` está vacío, se muestra el texto en español.
- **Moneda:** en `config/settings.py`, el diccionario `MONEDAS` tiene la tasa de cada moneda (cuánto vale 1 MXN). La tasa del dólar es una referencia (1 USD = 17.62 MXN, 26 de septiembre de 2026) y se actualiza a mano. Para agregar otra moneda, añade una línea con su símbolo y su tasa.

## Para contraseña de DJANGO:
user: admin
password: Panzer#4

## INSTRUCCIONES PARA INICIAR:
py manage.py migrate
py manage.py cargar_productos
py manage.py runserver

## Django admin
 http://127.0.0.1:8000/admin/
