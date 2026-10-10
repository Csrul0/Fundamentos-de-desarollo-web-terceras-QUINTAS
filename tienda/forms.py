import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Cita, Mensaje, Pedido
from .templatetags.tienda_extras import traducido

CAMPO = 'w-full p-2 border border-gray-300 rounded'


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['nombre', 'correo', 'asunto', 'mensaje']
        labels = {
            'nombre': _('Nombre'), 'correo': _('Correo'),
            'asunto': _('Asunto'), 'mensaje': _('Mensaje'),
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CAMPO}),
            'correo': forms.EmailInput(attrs={'class': CAMPO}),
            'asunto': forms.TextInput(attrs={'class': CAMPO}),
            'mensaje': forms.Textarea(attrs={'class': CAMPO, 'rows': 5}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'correo', 'direccion']
        labels = {'nombre': _('Nombre'), 'correo': _('Correo'), 'direccion': _('Dirección')}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': CAMPO}),
            'correo': forms.EmailInput(attrs={'class': CAMPO}),
            'direccion': forms.TextInput(attrs={'class': CAMPO}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Correo'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = CAMPO


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['servicio', 'instrumento', 'fecha', 'hora', 'nombre', 'correo', 'telefono', 'notas']
        labels = {
            'servicio': _('Servicio'), 'instrumento': _('Instrumento'), 'fecha': _('Fecha'),
            'hora': _('Hora'), 'nombre': _('Nombre'), 'correo': _('Correo'),
            'telefono': _('Teléfono'), 'notas': _('Notas'),
        }
        widgets = {
            'servicio': forms.Select(attrs={'class': CAMPO}),
            'instrumento': forms.TextInput(attrs={'class': CAMPO}),
            'fecha': forms.DateInput(attrs={'class': CAMPO, 'type': 'date'}),
            'hora': forms.Select(attrs={'class': CAMPO}),
            'nombre': forms.TextInput(attrs={'class': CAMPO}),
            'correo': forms.EmailInput(attrs={'class': CAMPO}),
            'telefono': forms.TextInput(attrs={'class': CAMPO}),
            'notas': forms.Textarea(attrs={'class': CAMPO, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs['min'] = datetime.date.today().isoformat()
        # El nombre del servicio se muestra en el idioma activo.
        self.fields['servicio'].label_from_instance = lambda s: traducido(s, 'nombre')

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < datetime.date.today():
            raise forms.ValidationError(_('Elige una fecha de hoy en adelante.'))
        if fecha.weekday() == 6:
            raise forms.ValidationError(_('Los domingos no abrimos. Elige otro día.'))
        return fecha

    def clean(self):
        datos = super().clean()
        fecha, hora = datos.get('fecha'), datos.get('hora')
        if fecha and hora and Cita.objects.filter(fecha=fecha, hora=hora).exists():
            self.add_error('hora', _('Ese horario ya está ocupado. Elige otro.'))
        return datos
