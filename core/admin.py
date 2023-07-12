from django.contrib import admin
from .models import *

# Register your models here.

class EstadoAdmin(admin.ModelAdmin):
    list_display=['id','desc']
    search_fields=['desc']
    list_per_page= 4
    
admin.site.register(Est, EstadoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo']
    search_fields = ['nombre']
    list_per_page = 3
    list_editable = ['precio','stock','descripcion','tipo']
    list_filter = ['tipo','stock']

admin.site.register(TiposProductos)
admin.site.register(Producto,ProductoAdmin)

class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']
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
    list_display = ['codigoCompra','direccion','precio']
    search_fields = ['codigoCompra'] 
    list_per_page = 10

admin.site.register(Historial,HistorialAdmin)




