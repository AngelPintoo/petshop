##se encarga de convertir la data
from .models import *
from rest_framework import serializers

class TiposProductosSeralizer(serializers.ModelSerializer):
    class Meta:
        model = TiposProductos
        fields = '__all__'
        
class ProductoSeralizer(serializers.ModelSerializer):
    tipo = TiposProductosSeralizer(read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'


