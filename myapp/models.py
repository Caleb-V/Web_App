from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# -------------------- MODELO CLIENTE --------------------
class Cliente(models.Model):
    Nombre_Completo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    Creacion_cuenta = models.DateTimeField(auto_now_add=True)
    importante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
         return f"{self.Nombre_Completo} - {self.empresa.nombre}"

# -------------------- MODELO EMPRESA --------------------
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    nit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------- MODELO PLATO --------------------
class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class DisponibilidadPlato(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    dia = models.CharField(max_length=3, choices=DIAS_SEMANA, default='LUN')

    class Meta:
        unique_together = ('plato', 'dia')

    def __str__(self):
        return f"{self.plato.nombre} disponible el {self.get_dia_display()}"

class CarritoItem(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA, default='LUN')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.cantidad * self.plato.precio

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} - {self.usuario.username} ({self.get_dia_semana_display()})"


# -------------------- RECIBO --------------------
class Recibo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Recibo #{self.id} - {self.usuario.username} - {self.fecha_compra.strftime('%Y-%m-%d')}"

# -------------------- DETALLE DE RECIBO --------------------
class ReciboItem(models.Model):
    recibo = models.ForeignKey(Recibo, related_name='items', on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"
