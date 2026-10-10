from django.db import models
from django.templatetags.static import static


class Categoria(models.Model):
    nombre = models.CharField(max_length=60)
    nombre_en = models.CharField('name (English)', max_length=60, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    nombre_en = models.CharField('name (English)', max_length=120, blank=True)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    marca = models.CharField(max_length=60, blank=True)
    descripcion = models.TextField(blank=True)
    descripcion_en = models.TextField('description (English)', blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=10)
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def imagen_url(self):
        # Si no subes foto desde el admin, se usa la imagen de relleno.
        if self.imagen:
            return self.imagen.url
        return static(f'images/products/{self.slug}.svg')


class Mensaje(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    enviado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enviado']

    def __str__(self):
        return f'{self.asunto} - {self.nombre}'


class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    detalle = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.nombre}'


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_en = models.CharField('name (English)', max_length=100, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    descripcion_en = models.CharField('description (English)', max_length=250, blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_min = models.PositiveIntegerField(default=60)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    HORARIOS = [(f'{h:02d}:00', f'{h:02d}:00') for h in range(10, 19)]

    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name='citas')
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    instrumento = models.CharField(max_length=100, help_text='Ej. guitarra acústica Yamaha')
    fecha = models.DateField()
    hora = models.CharField(max_length=5, choices=HORARIOS)
    notas = models.TextField(blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha', 'hora']
        constraints = [models.UniqueConstraint(fields=['fecha', 'hora'], name='cita_unica_por_horario')]

    def __str__(self):
        return f'{self.servicio} - {self.nombre} ({self.fecha} {self.hora})'


class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    titulo_en = models.CharField('title (English)', max_length=150, blank=True)
    slug = models.SlugField(unique=True)
    resumen = models.CharField(max_length=250)
    resumen_en = models.CharField('summary (English)', max_length=250, blank=True)
    contenido = models.TextField()
    contenido_en = models.TextField('content (English)', blank=True)
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='noticias/', blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo

    @property
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return static(f'images/news/{self.slug}.svg')
