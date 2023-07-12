from django.db import models


# Create your models here.

class TiposProductos(models.Model):
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=300)
    tipo = models.ForeignKey(TiposProductos, on_delete=models.CASCADE)
    imagen = models.ImageField(null=True,blank=True)
    fecha = models.DateField()
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre
      
class Subscripcion(models.Model):
    nombreSubs = models.CharField(max_length=100)
    correo = models.CharField(max_length=100) 
    rut = models.CharField(max_length=11)

    def __str__(self):
        return self.nombreSubs
    
class Historial(models.Model):
    codigoCompra = models.IntegerField()
    direccion = models.CharField(max_length=100) 
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre_Producto  
      
class Carrito(models.Model):
    descripcion = models.CharField(max_length=100)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Est(models.Model):
    desc = models.CharField(max_length=100)
    def __str__(self):
        return self.desc

class Seguimiento(models.Model):
    estado = models.ForeignKey(Est, on_delete=models.CASCADE)

    def __str__(self):
        return self.estado
