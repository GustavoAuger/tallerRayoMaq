from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(cliente)
admin.site.register(Bateria)
admin.site.register(Categoria)
admin.site.register(CarritoItem)
admin.site.register(Servicio)