from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .cart import Carrito
from .forms import CheckoutForm, CitaForm, ContactoForm, RegistroForm
from .models import Categoria, Noticia, Pedido, Producto, Servicio
from .templatetags.tienda_extras import traducido


def inicio(request):
    return render(request, 'tienda/inicio.html', {
        'destacados': Producto.objects.filter(destacado=True)[:8],
        'categorias': Categoria.objects.all()[:3],
        'noticias': Noticia.objects.all()[:3],
    })


def catalogo(request):
    productos = Producto.objects.select_related('categoria')
    categoria = request.GET.get('categoria', '')
    q = request.GET.get('q', '').strip()
    orden = request.GET.get('orden', '')
    if categoria:
        productos = productos.filter(categoria__slug=categoria)
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(nombre_en__icontains=q) | Q(marca__icontains=q))
    if orden == 'precio':
        productos = productos.order_by('precio')
    elif orden == '-precio':
        productos = productos.order_by('-precio')
    return render(request, 'tienda/catalogo.html', {
        'productos': productos, 'categoria_actual': categoria, 'q': q, 'orden': orden,
    })


def producto(request, slug):
    p = get_object_or_404(Producto, slug=slug)
    relacionados = Producto.objects.filter(categoria=p.categoria).exclude(id=p.id)[:4]
    return render(request, 'tienda/producto.html', {'p': p, 'relacionados': relacionados})


def noticias(request):
    return render(request, 'tienda/noticias.html', {'noticias': Noticia.objects.all()})


def noticia(request, slug):
    n = get_object_or_404(Noticia, slug=slug)
    otras = Noticia.objects.exclude(id=n.id)[:3]
    return render(request, 'tienda/noticia.html', {'n': n, 'otras': otras})


def nosotros(request):
    return render(request, 'tienda/nosotros.html')


def contacto(request):
    form = ContactoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mensaje = form.save()
        send_mail(
            subject=f'Nuevo mensaje: {mensaje.asunto}',
            message=mensaje.mensaje,
            from_email=mensaje.correo,
            recipient_list=['contacto@soundbazaarbytes.local'],
        )
        messages.success(request, _('Recibimos tu mensaje. Te respondemos pronto.'))
        return redirect('contacto')
    return render(request, 'tienda/contacto.html', {'form': form})


def servicios(request):
    inicial = {}
    if request.user.is_authenticated:
        inicial = {'nombre': request.user.get_full_name() or request.user.username,
                   'correo': request.user.email}
    if request.GET.get('servicio'):
        inicial['servicio'] = request.GET['servicio']
    form = CitaForm(request.POST or None, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        cita = form.save()
        messages.success(request, _('Tu cita quedó para el %(fecha)s a las %(hora)s. Te esperamos.') % {
            'fecha': date_format(cita.fecha, 'SHORT_DATE_FORMAT'), 'hora': cita.hora})
        return redirect('servicios')
    return render(request, 'tienda/servicios.html', {
        'servicios': Servicio.objects.all(), 'form': form,
    })


def ver_carrito(request):
    return render(request, 'tienda/carrito.html')


@require_POST
def agregar(request, producto_id):
    p = get_object_or_404(Producto, id=producto_id)
    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except ValueError:
        cantidad = 1
    Carrito(request).agregar(p, cantidad)
    messages.success(request, _('Agregaste "%(nombre)s" al carrito.') % {'nombre': traducido(p, 'nombre')})
    return redirect(request.POST.get('next') or 'carrito')


def cambiar(request, producto_id, cantidad):
    Carrito(request).cambiar(get_object_or_404(Producto, id=producto_id), cantidad)
    return redirect('carrito')


def quitar(request, producto_id):
    Carrito(request).quitar(get_object_or_404(Producto, id=producto_id))
    return redirect('carrito')


def checkout(request):
    carrito = Carrito(request)
    if len(carrito) == 0:
        messages.info(request, _('Tu carrito está vacío.'))
        return redirect('catalogo')
    inicial = {}
    if request.user.is_authenticated:
        inicial = {'nombre': request.user.get_full_name() or request.user.username,
                   'correo': request.user.email}
    form = CheckoutForm(request.POST or None, initial=inicial)
    if request.method == 'POST' and form.is_valid():
        pedido = form.save(commit=False)
        pedido.total = carrito.total()
        pedido.detalle = '\n'.join(
            f"{l['cantidad']} x {l['producto'].nombre} (${l['subtotal']})" for l in carrito.lineas())
        pedido.save()
        carrito.vaciar()
        return render(request, 'tienda/gracias.html', {'pedido': pedido})
    return render(request, 'tienda/checkout.html', {'form': form})


def registro(request):
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, _('Tu cuenta está lista.'))
        return redirect('inicio')
    return render(request, 'registration/registro.html', {'form': form})


@require_POST
def cambiar_moneda(request):
    codigo = request.POST.get('moneda', '')
    if codigo in settings.MONEDAS:
        request.session['moneda'] = codigo
    destino = request.POST.get('next', '')
    if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        destino = reverse('inicio')
    return redirect(destino)


def error_404(request, exception):
    return render(request, '404.html', status=404)