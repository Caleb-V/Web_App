from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Cliente_creacion
from .models import Plato, DisponibilidadPlato, CarritoItem, Cliente,  Recibo, ReciboItem, Empresa, PedidoHistorico
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def helloword(request):
    return render(request, 'home.html')

def register(request):

    if request.method == 'GET':
        return render(request, 'singup.html', {
        'form': UserCreationForm()
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('create_cliente')
            except IntegrityError:
                return render(request, 'singup.html', {
                'form': UserCreationForm(),
                'error': 'El usuario ya existe'
                })
        return render(request, 'singup.html', {
                'form': UserCreationForm(),
                'error': 'Su contraseña no coincide'
                })


def main(request):
    return render(request, 'main.html')    

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html',
                    {'form': AuthenticationForm
                    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',
                    {'form': AuthenticationForm,
                     'error': 'Usuario o Contraseña incorrecta'
                    })
        else:
            login(request, user)
            return redirect('main')

#Asi se hacen todos        
def create_cliente(request):

    if request.method == 'GET':
        return render(request, 'cliente.html', {
            'form': Cliente_creacion
        })
    else:
        try:
            form = Cliente_creacion(request.POST)
            new_cliente = form.save(commit=False)
            new_cliente.usuario =request.user
            new_cliente.save()
            return redirect('main')
        except ValueError:
            return render(request, 'cliente.html', {
                'form': Cliente_creacion,
                'error': 'Ingrese valores validos'
            })


#Continuamos la logica

@login_required(login_url='signin')  # Aquí le dices a dónde ir si no está logueado
def main(request):
    # 1. Diccionario de días para el <select>
    dias_semana = dict(DisponibilidadPlato.DIAS_SEMANA)

    # 2. Día seleccionado (viene en GET ?dia=XXX), si no, 'LUN'
    dia_actual = request.GET.get('dia', 'LUN')

    # 3. Si llega un POST, procesamos el "Agregar al carrito"
    if request.method == 'POST':
        plato_id   = request.POST.get('plato_id')
        cantidad   = int(request.POST.get('cantidad', 1))
        dia_semana = request.POST.get('dia_semana', dia_actual)
        # buscamos el plato, o 404 si no existe
        plato = get_object_or_404(Plato, id=plato_id)

        # agregamos o actualizamos el carrito
        carrito_item, creado = CarritoItem.objects.get_or_create(
            usuario=request.user,
            plato=plato,
            dia_semana=dia_semana,
            defaults={'cantidad': cantidad}
        )
        if not creado:
            carrito_item.cantidad += cantidad
            carrito_item.save()

        # redirigimos de nuevo a la misma url + día para limpiar POST
        return redirect(f"{request.path}?dia={dia_actual}")

    # 4. GET normal: obtenemos los platos disponibles para el día
    disponibles = DisponibilidadPlato.objects.filter(dia=dia_actual).select_related('plato')

    # 5. También traemos el carrito del usuario para mostrarlo
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    total_carrito = sum(item.subtotal() for item in carrito_items)

    # 6. Renderizamos
    return render(request, 'main.html', {
        'dias_semana': dias_semana,
        'dia_actual': dia_actual,
        'dia_actual_nombre': dias_semana.get(dia_actual, ''),
        'disponibles': disponibles,
        'carrito_items': carrito_items,
        'total_carrito': total_carrito,
    })

# ----------PAGO------------
@login_required(login_url='signin')
def pago(request):
    recibo_id = request.session.get('recibo_id')

    if not recibo_id:
        messages.error(request, "No se encontró ningún recibo.")
        return redirect('main')

    recibo = get_object_or_404(Recibo, id=recibo_id, usuario=request.user)
    items = ReciboItem.objects.filter(recibo=recibo)

    return render(request, 'pago.html', {
        'recibo': recibo,
        'items': items,
    })

#----- Eliminar_seleccion -----

@login_required(login_url='signin')
@require_POST
def eliminar_carrito_item(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    item.delete()
    return redirect('main')


# Prueba

@login_required
@transaction.atomic
def procesar_pago(request):
    usuario = request.user
    carrito_items = CarritoItem.objects.filter(usuario=usuario)

    if not carrito_items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('main')

    total = sum(item.plato.precio * item.cantidad for item in carrito_items)

    try:
        cliente = Cliente.objects.get(usuario=usuario)
        empresa = cliente.empresa
    except Cliente.DoesNotExist:
        empresa = None

    recibo = Recibo.objects.create(
        usuario=usuario,
        empresa=empresa,
        total=total
    )

    for item in carrito_items:
        ReciboItem.objects.create(
            recibo=recibo,
            plato=item.plato,
            cantidad=item.cantidad,
            precio_unitario=item.plato.precio
        )

    # Aquí creamos los registros en PedidoHistorico sin pasar fecha_emision
    historico_items = [
        PedidoHistorico(
            usuario=item.usuario,
            plato=item.plato,
            cantidad=item.cantidad,
            dia_semana=item.dia_semana
        ) for item in carrito_items
    ]
    PedidoHistorico.objects.bulk_create(historico_items)

    carrito_items.delete()

    request.session['recibo_id'] = recibo.id

    return redirect('pago')

