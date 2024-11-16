# urls.py
from django.urls import path
from . import views
from django.urls import include, path
from .views import baterias_vista
from .views import vista_carrito
urlpatterns = [
    path('myapp/', include('myapp.urls')),
    # ...
]

urlpatterns = [
    path('index', views.index, name='index'),
    path('base', views.base, name='base'),
    path('contacto', views.contacto, name='contacto'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('productos', views.productos, name='productos'),
    path('reservar', views.reservar, name='reservar'),
    path('recuperar', views.recuperar, name='recuperar'),
    path('',views.cliente_agregar,name='cliente_agregar'),
    path('login_vista',views.login_vista,name='login_vista'),
    path('logout_vista',views.logout_vista,name='logout_vista'),
    path('perfil',views.perfil,name='perfil'),
    path('modificar',views.modificar,name='modificar'),
    path('eliminar',views.eliminar,name='eliminar'),
    path('eliminar_cuenta', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('baterias', views.baterias_vista, name='baterias'),  #renderizar los items de bateria en ciclo tomando la funcion
    path('servicios', views.servicios_vista, name='servicios'), #renderizar los items de servicios en ciclo tomando la funcion
    path('agregar_al_carrito', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('finalizar_compra', views.finalizar_compra, name='finalizar_compra'),
    path('carrito', views.vista_carrito, name='carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'), #eliminar items del carrito
    path('actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'), #actualizar items del carrito
    path('finalizar_comprax', views.finalizar_comprax, name='finalizar_comprax'),
    path('actualizar_informacion_cliente',views.actualizar_informacion_cliente,name='actualizar_informacion_cliente'),
    path('recuperar_contrasena',views.recuperar_contrasena,name='recuperar_contrasena'),
    path('confirmar_codigo',views.confirmar_codigo,name='confirmar_codigo'),
    path('contacto_envio',views.contacto_envio,name='contacto_envio'),
    path('reservar_envio',views.reservar_envio,name='reservar_envio'),
] 
