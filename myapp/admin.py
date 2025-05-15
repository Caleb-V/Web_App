from django.contrib import admin
from .models import Cliente, Empresa, Plato, DisponibilidadPlato, CarritoItem, Recibo, ReciboItem
from .forms import DisponibilidadPlatoForm, CarritoItemForm

class DisponibilidadPlatoAdmin(admin.ModelAdmin):
    form = DisponibilidadPlatoForm
    list_display = ('plato', 'display_dias_semana')
    list_filter = ('plato',)
    search_fields = ('plato__nombre',)

    def display_dias_semana(self, obj):
        return obj.get_dia_display()
    display_dias_semana.short_description = "Día disponible"

class CarritoItemAdmin(admin.ModelAdmin):
    form = CarritoItemForm
    list_display = ('usuario', 'plato', 'cantidad', 'dia_semana')

class myappAdmin(admin.ModelAdmin):
    readonly_fields = ("Creacion_cuenta",)

# Registros estándar
admin.site.register(Cliente, myappAdmin)
admin.site.register(Empresa)
admin.site.register(Plato)
admin.site.register(DisponibilidadPlato, DisponibilidadPlatoAdmin)  # Usando el admin personalizado
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(Recibo)
admin.site.register(ReciboItem)
