from django.contrib import admin
from .models import *

# Register your models here.


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo']
    search_fields = ['nombre']
    list_per_page = 3
    list_editable = ['precio','stock','descripcion','tipo']
    list_filter = ['tipo','stock']

admin.site.register(TiposProductos)
admin.site.register(Producto,ProductoAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_usuario','edad','rut','direccion','correo']
    search_fields = ['nombre']
    list_per_page = 10
    list_editable = ['edad','rut','direccion','correo']

admin.site.register(TipoUsuario)
admin.site.register(Usuario,UsuarioAdmin)

class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ['estado']
    search_fields = ['estado']
    list_per_page = 4

admin.site.register(Seguimiento, SeguimientoAdmin)

class SubscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombreSubs','correo','rut']
    search_fields = ['correo']
    list_per_page = 10
    list_editable = ['correo']   

admin.site.register(Subscripcion,SubscripcionAdmin)


class CarritoAdmin(admin.ModelAdmin):
    list_display = ['descripcion','id_producto'] 
    search_fields = ['id_producto']
    list_per_page = 10

admin.site.register(Carrito,CarritoAdmin)


class HistorialAdmin(admin.ModelAdmin):
    list_display = ['nombre_Producto','direccion','precio','pago']
    search_fields = ['nombre_Producto'] 
    list_per_page = 10

admin.site.register(Historial,HistorialAdmin)