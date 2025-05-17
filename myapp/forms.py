from django.forms import ModelForm
from .models import Cliente, DisponibilidadPlato, Plato, CarritoItem
from django import forms
from django.core.exceptions import ValidationError

class Cliente_creacion(ModelForm):
    class Meta:
        model = Cliente
        fields = ['Nombre_Completo', 'descripcion', 'celular', 'dni', 'correo', 'empresa']
        widgets = {
            'Nombre_Completo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su NIE o DNI'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
        }

# --------------- PLATO DISPONIBILIDAD----------

class DisponibilidadPlatoForm(forms.ModelForm):
    class Meta:
        model = DisponibilidadPlato
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        plato = cleaned_data.get('plato')
        dia = cleaned_data.get('dia')

        if DisponibilidadPlato.objects.filter(plato=plato, dia=dia).exists():
            raise ValidationError("Este plato ya está asignado para ese día.")

        return cleaned_data
    



class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Verificamos si el objeto existe y tiene plato asignado
        if self.instance and self.instance.pk and self.instance.plato:
            plato = self.instance.plato
            # Obtenemos los días disponibles para ese plato
            dias_disponibles = DisponibilidadPlato.objects.filter(plato=plato).values_list('dia', flat=True)
            # Filtramos el campo dia_semana para mostrar solo los días disponibles
            self.fields['dia_semana'].choices = [
                (dia, label) for dia, label in self.fields['dia_semana'].choices if dia in dias_disponibles
            ]
        else:
            # Si no hay plato aún, quizás no filtramos o dejamos vacío el campo días
            self.fields['dia_semana'].choices = []





