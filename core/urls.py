from django.urls import path, include
from .views import *
from rest_framework import routers
from django.contrib.auth.decorators import login_required

#RUTAS DEL API

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tiposproductos', TiposproductoViewset)


urlpatterns = [
    path('api/', include(router.urls)),
    #index
    path('', index, name="index"),
    path('tiendaapi/',tiendaapi, name="tiendaapi"),
    # Despacho 
    path('seguimiento', login_required(seguimiento), name="seguimiento"),
    #tienda
    path('pagar/', login_required(pagar), name="pagar"),
    path('shopdetails/', shopdetails, name="shopdetails"),
    path('tienda/', tienda, name="tienda"),
    path('carrito/', login_required(carrito), name="carrito"),
    path('historial', login_required(historial), name="historial"),
    #adms
    path('producto/adm-producto/', login_required(admproducto), name="admproducto"),
    path('admcorreo/', login_required(admcorreo), name="admcorreo"),
    path('administrador/',login_required(administrador), name="administrador"),

    #otros
    path('contact/', contact, name="contact"),
    path('registration/registro/', registro, name="registro" ),
    
    #CRUD producto

    path('add/' , login_required(add), name="add"),
    path('update/<id>/', login_required(update), name="update"),
    path('delete/<id>/', login_required(delete), name="delete"),
  
   
    #Crud Empleado
    path('correo/addEmp' , login_required(addEmp), name="addEmp"),
    path('correo/updateEmp/<id>/', login_required(updateEmp), name="updateEmp"),
    path('correo/deleteEmp/<id>/', login_required(deleteEmp), name="deleteEmp"),

    #admin
    path('', include('admin_argon.urls')),
    path('total_carrito/', total_carrito, name='total_carrito'),

]