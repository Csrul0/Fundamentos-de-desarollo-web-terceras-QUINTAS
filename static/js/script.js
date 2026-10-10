/* Carrito desplegable del menú */
document.addEventListener('DOMContentLoaded', function () {
  const cartIcon = document.querySelector('.cart-wrapper');
  if (!cartIcon) return;
  const cartDropdown = cartIcon.querySelector('.group-hover\\:block');
  const ocultar = () => { cartIcon.__timer = setTimeout(() => cartDropdown.classList.add('hidden'), 1300); };
  cartIcon.addEventListener('mouseenter', () => { clearTimeout(cartIcon.__timer); cartDropdown.classList.remove('hidden'); });
  cartIcon.addEventListener('mouseleave', ocultar);
  cartDropdown.addEventListener('mouseenter', () => clearTimeout(cartIcon.__timer));
  cartDropdown.addEventListener('mouseleave', ocultar);
});

/* Menú móvil */
document.addEventListener('DOMContentLoaded', function () {
  const boton = document.getElementById('hamburger');
  const menu = document.querySelector('.mobile-menu');
  if (boton && menu) boton.addEventListener('click', () => menu.classList.toggle('hidden'));
});

/* Slider de portada */
document.addEventListener('DOMContentLoaded', function () {
  if (typeof Swiper !== 'undefined' && document.querySelector('.main-slider')) {
    new Swiper('.main-slider', {
      slidesPerView: 1,
      loop: true,
      autoplay: { delay: 5000 },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
    });
  }
});

/* Buscador del menú */
document.addEventListener('DOMContentLoaded', function () {
  const icono = document.getElementById('search-icon');
  const campo = document.getElementById('search-field');
  if (!icono || !campo) return;
  icono.addEventListener('click', function () {
    campo.classList.toggle('hidden');
    campo.classList.toggle('search-slide-down');
    if (!campo.classList.contains('hidden')) campo.querySelector('input').focus();
  });
});

/* Cantidad en la página del producto */
document.addEventListener('DOMContentLoaded', function () {
  const menos = document.getElementById('decrease');
  const mas = document.getElementById('increase');
  const cantidad = document.getElementById('quantity');
  if (!menos || !mas || !cantidad) return;
  const actualizar = () => { menos.disabled = parseInt(cantidad.value) <= 1; };
  menos.addEventListener('click', () => { cantidad.value = Math.max(1, parseInt(cantidad.value) - 1); actualizar(); });
  mas.addEventListener('click', () => { cantidad.value = parseInt(cantidad.value) + 1; actualizar(); });
});

/* Animaciones con jQuery */
$(function () {

  /* 1. Las tarjetas de producto aparecen con fade y subiendo al hacer scroll */
  var $tarjetas = $('.tarjeta-anim').css({ opacity: 0, position: 'relative', top: 30 });
  function mostrarVisibles() {
    var limite = $(window).scrollTop() + $(window).height() - 60;
    $tarjetas.each(function (i) {
      var $t = $(this);
      if (!$t.data('visto') && $t.offset().top < limite) {
        $t.data('visto', true).delay((i % 4) * 120).animate({ opacity: 1, top: 0 }, 500);
      }
    });
  }
  $(window).on('scroll resize', mostrarVisibles);
  mostrarVisibles();

  /* 2. Los mensajes se despliegan con slideDown y se ocultan solos con slideUp */
  $('.mensaje-flash').hide().slideDown(300).delay(4000).slideUp(400);
  $('.mensaje-flash').on('click', function () { $(this).stop(true).slideUp(200); });

  /* 3. Botón "Volver arriba": aparece con fadeIn y sube con animate */
  var etiqueta = $('html').attr('lang') === 'en' ? 'Back to top' : 'Volver arriba';
  var $subir = $('<button id="volver-arriba" type="button"></button>')
    .attr('aria-label', etiqueta).html('&uarr;').appendTo('body').hide();
  var visible = false;
  $(window).on('scroll', function () {
    var debeVerse = $(window).scrollTop() > 300;
    if (debeVerse === visible) return;
    visible = debeVerse;
    if (visible) { $subir.stop(true, true).fadeIn(200); } else { $subir.stop(true, true).fadeOut(200); }
  });
  $subir.on('click', function () { $('html, body').animate({ scrollTop: 0 }, 600); });
});
