
from django.shortcuts import render,redirect
from .models import * 
from .forms import ProductoForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import *
import requests 
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group, User

#FUNCION GENERICA VALIDA GRUPOS
#EL USO: @GRUPO_REQUERIDO('cliente')
def GRUPO_REQUERIDO(nombre_grupo):
    def decorator(view_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(request, *arg, **kwargs):
            return view_fuc(request, *arg, **kwargs)
        return wrapper
    return decorator

#from django.contrib.auth.models import Group
#grupo = Group.objects.get(name='cliente')
#user.groups.add(grupo)
#se encarga de mostrar en la lista los datos de datos

#grupo = Group.objects.get(name='cliente')
#user. groups.add(grupo)

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = ProductoSeralizer


class TiposproductoViewset(viewsets.ModelViewSet):
    queryset = TiposProductos.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = TiposProductosSeralizer




#listar productos

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
@GRUPO_REQUERIDO('cliente')
def tienda(request):
    ProductosAll = Producto.objects.all()

    datos = {
        'lp': ProductosAll
    }

    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        producto = Producto.objects.get(id=id_producto)
        carrito = Carrito()
        carrito.id_producto = producto
        carrito.descripcion = ''
        carrito.save()
    return render(request, 'core/tienda.html', datos)



@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
@GRUPO_REQUERIDO('cliente')
def contact(request):
    return render(request, 'core/contact.html')

@GRUPO_REQUERIDO('cliente')
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
def shopdetails(request):
    
    
    return render(request, 'core/shop-details.html')


@GRUPO_REQUERIDO('cliente')
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
def index(request):
    return render(request, 'core/index.html')

@GRUPO_REQUERIDO('cliente')
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
def seguimiento(request):
    

    return render(request, 'core/seguimiento.html')

@GRUPO_REQUERIDO('cliente')
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
@login_required
def carrito(request):
    carrito = Carrito.objects.all()
    producto = Producto.objects.all()
    a=0
    
    datos = {
        'lc': carrito,
        'lp': producto,
        'a' : a
    }
    

    if request.method == 'POST':
        ab = request.POST.get('id_carro')
        carrito = Carrito.objects.get(id = ab)
        carrito.delete()
        a = request.POST.get('a')
        if a> 0:
            total_carrito(a)
        


    

    return render(request, 'core/carrito.html', datos)


@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')  
@login_required
def eliminar_producto(request, producto_id):
    usuario = request.user
    producto = Producto.objects.get(id=producto_id)

    try:
        item = Carrito.objects.get(usuario=usuario, producto=producto)
        item.delete()
        producto.stock = ('stock') + 1
        producto.save()
    except Carrito.DoesNotExist:
        pass
    
    return redirect('carrito')

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')  
def administrador(request):
    return render(request, 'core/administrador.html')

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')  
def admproducto(request):
    productosListados = Producto.objects.all()
    return render(request, 'core/producto/adm-producto.html', {"listado":productosListados})

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')  
def admcorreo(request):
    return render(request, 'core/correo/adm-correo.html')

@GRUPO_REQUERIDO('cliente')
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def registro(request):
    return render(request,'registration/registro.html')

#CRUD
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def add(request):
    data = {
        'form' : ProductoForm()
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Almacenado Correctamente")

    return render(request, 'core/producto/add-product.html', data)

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def update(request,id):
    producto = Producto.objects.get(id=id)
    data = {
        'form' : ProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(request.POST,instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Actualizado Correctamente")
        data['form'] = formulario
    
    return render(request, 'core/producto/update-product.html', data)
    
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def delete(request,id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect("producto/admproducto")


#CRUD Empleado
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def addEmp(request):
    data = {
        'form': EmpleadoForm()
    }
    
    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Correo almacenado correctamente")
            return redirect('admcorreo')

    return render(request, 'core/correo/add-correo.html', data)

@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def updateEmp(request, id):
    empleado = Empleado.objects.get(id=id)
    data = {
        'form': EmpleadoForm(instance=empleado)
    }
    
    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, instance=empleado, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Correo actualizado correctamente")
            return redirect('admcorreo')
        data['form'] = formulario
    
    return render(request, 'core/correo/update-correo.html', data)
    
@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin')   
def deleteEmp(request, id):
    empleado = Empleado.objects.get(id=id)
    empleado.delete()
    messages.success(request, "Correo eliminado correctamente")
    return redirect('admcorreo')
 

#  API
@GRUPO_REQUERIDO('admin')
def tiendaapi(request):
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    Producto = respuesta.json()

    data = {
        'lp': Producto}
    
    return render(request, 'core/tiendaapi.html',data)


# crud de auth



def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            grupo = Group.objects.get(name='cliente')
            user.groups.add(grupo)
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Te has registrado correctamente")
        else:
            data["form"] = formulario

    return render(request, 'registration/registro.html', data)

def total_carrito(request,totale):
    datos = {
        'total' : totale

    }
    return render(request, 'core/pagar.html',datos)

def historial(request):
    o = Paginator.objects.all()
    data = {
        'lp' : o  
    }

    return render(request, 'core/historial.html',data)


@GRUPO_REQUERIDO('vendedor')
@GRUPO_REQUERIDO('admin') 
@GRUPO_REQUERIDO('cliente')
def pagar(request):
    productos = Producto.objects.all()
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    valor_carrito = 20 
    valor_total = valor_carrito/valor_usd
    datos = {
        'valor' : round(valor_total,2),
        'lp'    : productos

}

    return render(request,'core/pagar.html', datos)
