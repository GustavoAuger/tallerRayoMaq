from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class cliente(models.Model):  
    rut = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=50)
    codigo = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.email
    
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_categoria

class Bateria(models.Model):
    marca = models.CharField(max_length=30)
    nombre = models.CharField(max_length=100, db_column='descripcion')
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField(default=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='baterias')
    icono = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.marca
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=400)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField(default=1)
    icono = models.CharField(max_length=100, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='servicios')
    

    def __str__(self):
        return self.nombre
    
class CarritoItem(models.Model):
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') #cruce entre tipo de objeto y id de objeto
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.content_object} ({self.cantidad})'

