from django.db import models
from .models import Cliente
#from .models import Producto
# Create your models here.

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion', 'email', 'rut_cliente']



    def __str__(self):
        return self.nombre
