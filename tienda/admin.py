from django.contrib import admin
from .models import Categoria, Mensaje, Pedido, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'precio', 'stock', 'destacado')
    list_filter = ('categoria', 'destacado')
    search_fields = ('nombre', 'marca')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'nombre', 'correo', 'enviado')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'total', 'creado')


from .models import Cita, Servicio  # noqa: E402


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_min')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'servicio', 'nombre', 'instrumento', 'telefono')
    list_filter = ('servicio', 'fecha')


from .models import Noticia  # noqa: E402


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha')
    prepopulated_fields = {'slug': ('titulo',)}
