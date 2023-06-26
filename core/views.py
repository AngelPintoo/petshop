
from django.shortcuts import render,redirect
from .models import * 
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import *
import requests 
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test


#FUNCION GENERICA VALIDA GRUPOS
#EL USO: @GRUPO_REQUERIDO('cliente')
def GRUPO_REQUERIDO(nombre_grupo):
    def decorator(view_func):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

#from django.contrib.auth.models import Group
#grupo = Group.objects.get(name='cliente')
#user.groups.add(grupo,tuloncio)
#se encarga de mostrar en la lista los datos de datos

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = ProductoSeralizer


class TiposproductoViewset(viewsets.ModelViewSet):
    queryset = TiposProductos.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = TiposProductosSeralizer


class TipoUsuarioViewset(viewsets.ModelViewSet):
    queryset = TipoUsuario.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = TiposUsuarioSeralizer


class UsuarioViewset(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    # queryset = Producto.objets.filter(tipo=1)
    serializer_class = UsuarioSeralizer

#listar productos
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

@GRUPO_REQUERIDO('cliente')
def pagar(request):
    productos = Productos.objects.all()
    carro = Carrito.object.all()
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    valor_carrito = 30000 # aqui en vez de 30000 va el total de compra del carrito
    valor_total = valor_carrito/valor_usd
    datos = {
        'valor' : round(valor_total,2),
        'lp'    : productos,
        'lc'    : carro
}

    return render(request,'core/pagar.html', datos)


@GRUPO_REQUERIDO('cliente')
def contact(request):
    return render(request, 'core/contact.html')

@GRUPO_REQUERIDO('cliente')
def shopdetails(request):
    return render(request, 'core/shop-details.html')

@GRUPO_REQUERIDO('cliente')
def index(request):
    return render(request, 'core/index.html')

@GRUPO_REQUERIDO('cliente')
def despacho(request):
    despacho = Despacho.objects.all()
    estado = Estado.objects.all()
    datos = {
        'despacho'  : despacho,
        'estado' : estado
        
    }
    
    return render(request, 'core/despacho.html',datos)

@GRUPO_REQUERIDO('cliente')
@login_required
def carrito(request):

    carrito = Carrito.objects.all()
    productos = Producto.objects.all()

 
    datos = {
        'lc': carrito,
        'lp': productos,
    }
    if request.method == 'POST':
        producto = request.POST.get('id_producto')
        carrito = Carrito.objects.get(id_producto = producto)
        carrito.delete()
        messages.succes(request, "Producto eliminado correctamente del carrito")
    

    return render(request, 'core/carrito.html', datos)


@GRUPO_REQUERIDO('vendedor')
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
def administrador(request):
    return render(request, 'core/administrador.html')

@GRUPO_REQUERIDO('vendedor')
def admproducto(request):
    productosListados = Producto.objects.all()
    return render(request, 'core/producto/adm-producto.html', {"listado":productosListados})

@GRUPO_REQUERIDO('vendedor')
def admcorreo(request):
    return render(request, 'core/correo/adm-correo.html')

@GRUPO_REQUERIDO('vendedor')
def registro(request):
    return render(request,'registration/registro.html')

#CRUD
@GRUPO_REQUERIDO('vendedor')
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
def delete(request,id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect("producto/admproducto")


#CRUD Empleado
@GRUPO_REQUERIDO('vendedor')
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
def registro_usuario(request):
    datos = {
        'form' : registroUsuarioForm()
    }
    if request.method == 'POST':
        formulario = registroUsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            group = Group.objects.get(name='cliente')
            group.user_set.add(usuario)
            formulario.save()
            messages.success(request,'Usuario guardado correctamente!')
    return render(request,'registration/registro.html',datos) 

def total_carrito(request):
    total = 1
    data = {
        'total' : total

    }
    return render(request, 'core/pagar.html',data)