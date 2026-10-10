from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<slug:slug>/', views.producto, name='producto'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/<slug:slug>/', views.noticia, name='noticia'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('moneda/', views.cambiar_moneda, name='moneda'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar, name='agregar'),
    path('carrito/cambiar/<int:producto_id>/<int:cantidad>/', views.cambiar, name='cambiar'),
    path('carrito/quitar/<int:producto_id>/', views.quitar, name='quitar'),
    path('checkout/', views.checkout, name='checkout'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
