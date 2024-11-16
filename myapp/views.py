
from django.http import HttpResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import cliente, Bateria, CarritoItem, Servicio
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
import json   #para leer json
from django.conf import settings #parte para finalizar la compra
#para enviar correos
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
import random #para generar numeros random
import string


# Create your views here.
def index(request):
    return render(request, 'myapp/index.html')

def contacto(request):
    return render(request, 'myapp/contacto.html')

def nosotros(request):
    return render(request, 'myapp/nosotros.html')

def productos(request):
    return render(request, 'myapp/productos.html')

def reservar(request):
    return render(request, 'myapp/reservar.html')

def base(request):
    return render(request, 'myapp/base.html')

def recuperar(request):
    return render(request, 'myapp/recuperar.html')

def perfil(request):
    return render(request, 'myapp/perfil.html')

def modificar(request):
    return render(request, 'myapp/modificar.html')

def eliminar(request):
    return render(request, 'myapp/eliminar.html')


def baterias(request):
    return render(request, 'myapp/baterias.html')


def baterias_vista(request):
    baterias = Bateria.objects.all()
    return render(request, 'myapp/baterias.html', {'baterias': baterias}) #hacer ciclo de productos bateria

def servicios(request):
    return render(request, 'myapp/servicios.html')

def servicios_vista(request):
    servicios = Servicio.objects.all()
    return render(request, 'myapp/servicios.html', {'servicios': servicios}) #hacer ciclo de servicios

def finalizar_compra(request):
    return render(request, 'myapp/finalizar_compra.html')


def cliente_agregar(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        rut = request.POST.get("rut")
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")
        try:
            obj = cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                rut=rut,
                email=email,
                contrasena=contrasena
            )
            mensaje = "Cuenta creada exitosamente"
            return render(request, 'myapp/index.html', {'mensaje': mensaje})
        
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                mensaje = "El rut o correo electrónico ya están en uso."
            else:
                mensaje = "Error al ingresar el cliente."
            
            return render(request, 'myapp/index.html', {'mensaje': mensaje})

    else:
        mensaje = "Error"
        return render(request, 'myapp/index.html')
    

def login_vista(request):


    
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        # Autenticar al cliente manualmente
        try:
            cliente_ = cliente.objects.get(email=correo, contrasena=contrasena)
            request.session['cliente_id'] = cliente_.rut
            return redirect('perfil')  # Redirige a la página de contacto
            
        except cliente.DoesNotExist:
            mensaje = "Correo electrónico o contraseña incorrectos."
            return render(request, 'myapp/index.html', {'mensaje': mensaje})         # Si el cliente no puede ser autenticado, manda un error
    return render(request, 'myapp/index.html')

def logout_vista(request):
    try:
        del request.session['cliente_id']
    except KeyError:
        pass
    return redirect('index')

def eliminar_cuenta(request):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            try:
                cliente_obj = cliente.objects.get(rut=cliente_id)
                contrasena = request.POST.get('contrasena', '')
                if cliente_obj.contrasena == contrasena:
                    cliente_obj.delete()
                    del request.session['cliente_id']
                    mensaje = "Cuenta eliminada exitosamente"
                    return render(request, 'myapp/index.html', {'mensaje': mensaje})  # Redirigir a la página de inicio
    
                else:
                    mensaje = "Contraseña incorrecta. La cuenta no ha sido eliminada."
                    return render(request, 'myapp/eliminar.html', {'mensaje': mensaje})
            except cliente.DoesNotExist:
                messages.error(request, 'No se encontró el cliente.')
        else:
            messages.error(request, 'No hay cliente autenticado.')
    
    return render(request, 'myapp/eliminar.html')  # Renderizar el template para eliminar la cuenta

def agregar_al_carrito(request):
    if request.method == 'POST':
        cliente_rut = request.session.get('cliente_id')
        cantidad = request.POST.get('cantidad')
        product_id = request.POST.get('object_id')
        tipo = request.POST.get('tipo')
        redirigir= tipo.lower()+"s"
        if cliente_rut: # Verificar si el cliente está autenticado
            try:
                cliente_obj= cliente.objects.get(rut=cliente_rut)                 # Obtenemos todos los objetos de cliente
                print(cliente_obj) #contol
                content_type = ContentType.objects.get(model=tipo.lower())  # Obtenemos el tipo de contenido dinámicamente "por tipo"
                ModelClass = content_type.model_class()
                producto = ModelClass.objects.get(id=product_id) #obtenemos el producto de acuerdo al su modelo correspondiente y a su id
                producto = Servicio.objects.get(id=product_id)
                print(producto)
                print(content_type)
                carrito_item, created = CarritoItem.objects.get_or_create(                 # Crear o actualizar el item en el carrito
                    cliente=cliente_obj,
                    content_type=content_type,
                    object_id=producto.id,
                    cantidad=cantidad
                )

                if created:
                    messages.success(request, 'Producto agregado al carrito.')
                else:
                    carrito_item.cantidad += int(cantidad)
                    carrito_item.save()
                    messages.success(request, 'Cantidad actualizada en el carrito.')

                return redirect(redirigir)  # Redirigir a la vista del carrito
            except Bateria.DoesNotExist:
                messages.error(request, 'La batería seleccionada no existe.')
                return redirect(redirigir)  # Redirigir a donde sea necesario en caso de error
            except cliente.DoesNotExist:
                messages.error(request, 'No se encontró el cliente.')
                return redirect('index')  # Redirigir a la página de inicio o a la página de inicio de sesión si no hay cliente autenticado

        else:
            messages.error(request, 'Debe iniciar sesión para agregar productos al carrito.')
            return redirect('index')  # Redirigir a la página de inicio o a la página de inicio de sesión

    return redirect('index')

    
  
def vista_carrito(request):
    cliente_id = request.session.get('cliente_id')
    
    if not cliente_id:
        return redirect('index')  # Redirigir al login si el cliente no está autenticado

    try:
        cliente_obj = cliente.objects.get(rut=cliente_id)
        carrito_items = CarritoItem.objects.filter(cliente=cliente_obj)
        if not carrito_items.exists():  #si no hay items en el carrito no pasa a la compra
            return render(request, 'myapp/productos.html', {'mensaje': 'carrito vacio'}) 
        else:
        # Calcular el total de cada ítem y el total general
            for item in carrito_items:
                item.total = item.content_object.precio * item.cantidad
            
            total_general = sum(item.total for item in carrito_items)
            
            return render(request, 'myapp/carrito.html', {  # Asegúrate de que el nombre del archivo sea correcto
                'carrito_items': carrito_items,
                'total_general': total_general
            })
    except cliente.DoesNotExist:
        return redirect('index')  


def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    return redirect('carrito')

def actualizar_carrito(request, item_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))
        try:
            carrito_item = CarritoItem.objects.get(id=item_id)
            carrito_item.cantidad = cantidad
            carrito_item.save()
            messages.success(request, 'Cantidad actualizada en el carrito.')
        except CarritoItem.DoesNotExist:
            messages.error(request, 'El artículo no existe en el carrito.')
    return redirect('carrito')

#finalizar la compra:
def finalizar_comprax(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('index')
    try:
        cliente_obj = cliente.objects.get(rut=cliente_id)
        carrito_items = CarritoItem.objects.filter(cliente=cliente_obj)
        if not carrito_items.exists():  #si no hay items en el carrito no pasa a la compra
            return render(request, 'myapp/finalizar_compra.html', {'mensaje': 'carrito vacio'}) 
        else:     
            if request.method == 'POST':
                numero_tarjeta = request.POST.get('numero_tarjeta')
                cvv = request.POST.get('cvv')
                contrasena = request.POST.get('contrasena')
                with open(settings.BASE_DIR / 'myapp/tarjetas.json', 'r') as file:
                    tarjetas = json.load(file)
                    print(tarjetas)
                tarjeta_valida = False
                for tarjeta in tarjetas:
                    print(tarjeta['numero_tarjeta'])
                    print(tarjeta['cvv'])
                    print(tarjeta['contrasena'])
                    if (tarjeta['numero_tarjeta'] == numero_tarjeta and tarjeta['cvv'] == cvv and tarjeta['contrasena'] == contrasena):
                        print("bandera pasa tarjeta")
                        tarjeta_valida = True
                        total_compra = sum(item.content_object.precio * item.cantidad for item in carrito_items)
                        if tarjeta['monto'] < total_compra:
                            return render(request, 'myapp/finalizar_compra.html', {'mensaje': 'Dinero insufuciente'})      
                        else:
                            for item in carrito_items:
                                item.content_object.cantidad -= item.cantidad
                                item.content_object.save()
                            tarjeta['monto'] = int(tarjeta['monto'] - total_compra)#descuenta dinero de la tarjeta
                            with open(settings.BASE_DIR / 'myapp/tarjetas.json', 'w') as file: #abre la tarjeta y descuenta el dinero de la tarjeta
                                json.dump(tarjetas, file)  
                            carrito_items.delete() #elimina los items del carrito
                            print("ok pagado") # a modo de control interno por consola
                            return render(request, 'myapp/finalizar_compra.html', {'mensaje': 'Compra finalizada con éxito'})  # se puede depurar, muestra mensaje de compra ok     
                if not tarjeta_valida:

                    return render(request, 'myapp/finalizar_compra.html', {'mensaje': 'Datos de tarjeta incorrectos'})                      
        return render(request, 'myapp/finalizar_compra.html')
    except cliente.DoesNotExist:
        return redirect('index')

def actualizar_informacion_cliente(request):
    cliente_id = request.session.get('cliente_id')
    print("test")
    if not cliente_id:
        return redirect('index')
    try:
        cliente_obj = cliente.objects.get(rut=cliente_id)
        print("test2")
        if request.method == 'POST':
            print("test3")
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            contrasena = request.POST.get('contrasena')
            print("hola")
            if nombre != '':
                cliente_obj.nombre = nombre
            if apellido != '':
                cliente_obj.apellido = apellido
            if email != '':
                cliente_obj.email = email
            if contrasena != '':
                cliente_obj.contrasena = contrasena   
            cliente_obj.save()
            return render(request, 'myapp/perfil.html',{'mensaje': 'Datos modificados correctamente'})
        else:
            return render(request, 'myapp/modificar.html', {'mensaje': 'Error intente nuevamente'})
    except cliente.DoesNotExist:

        return redirect('index')
def generar_codigo():
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
    codigo = ''.join(random.choices(caracteres, k=10))  # Genera una cadena de 10 caracteres aleatorios
    return codigo    

#recuperar contraseña - envio de codigo de recupereación
def recuperar_contrasena(request):   #falta validar si existe el objeto con un try
    if request.method == 'POST':
        email= request.POST.get('email')
        cliente_obj = cliente.objects.get(email=email)
        cliente_obj.codigo = generar_codigo()
        print(cliente_obj.codigo)
        cliente_obj.save()
        subject = 'Recuperar contraseña taller mecanico rayomakween'
        message = 'CODIGO PROVISORIO:\n'+cliente_obj.codigo
        from_email = 'conmiscotusca2@gmail.com'  # correo de prueba que tenemos
        send_correo = [email]  # envía al correo que tiene asociado
        try:
            send_mail(subject, message, from_email, send_correo)
            messages.success(request, 'Correo enviado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

        return render(request, 'myapp/index.html', {'mensaje': 'Envío exitoso, favor revise su correo'})

    return redirect('index')

#recuperar contraseña
def confirmar_codigo(request):
    if request.method == 'POST':
        codigo=  request.POST.get('codigo')
        try:
            cliente_obj = cliente.objects.get(codigo=codigo)
        except:
            return render(request, 'myapp/index.html', {'mensaje': 'Código ingresado no es válido o a caducado'})  
        contrasena= request.POST.get('contrasena')
        if cliente_obj != '':
            cliente_obj.contrasena = contrasena   
            print("hola")
            print(cliente_obj.codigo)
            cliente_obj.save()
            print(cliente_obj)
            return render(request, 'myapp/index.html', {'mensaje': 'Contraseña modificada con éxito'})
            
        else:
            return render(request, 'myapp/index.html', {'mensaje': 'Código ingresado no es válido o a caducado'})  

    return redirect('index')

#funcion form contacto
def contacto_envio(request):
    if request.method == 'POST':
        nombre = request.POST.get("nombre") #nombre y apellido
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje_ = request.POST.get("mensaje")
        motivo =  request.POST.get("motivo")
        subject = 'Mensaje a través de contacto, seleccioón: '+motivo
        message = "La persona: "+nombre+" ha enviado el siguiente mensaje:\n\n"+mensaje_+"\n\n"+"Telefono: "+telefono+"\n"+"Email: "+email
        from_email = 'conmiscotusca2@gmail.com'  # correo de prueba que tenemos desde ahi salen los correos
        recipient_list = ['gu.auger@duocuc.cl']  # correo aqui llegan los correos de contacto & reserva

        try:
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Correo enviado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

        return render(request, 'myapp/index.html', {'mensaje': 'Envío exitoso, favor revise su correo'})

    return redirect('index')

def reservar_envio(request):
    if request.method == 'POST':
        nombre = request.POST.get("nombre") #nombre y apellido
        apellido = request.POST.get("apellido")
        rut = request.POST.get("rut")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        marca = request.POST.get("marca")
        anno =  request.POST.get("anno")
        fecha = request.POST.get("fecha")
        diagnostico = request.POST.get("diagnostico")
        subject = 'Reserva, selección: '+ diagnostico
        message = "Reserva:\n\nNombre: "+nombre+" "+apellido+"\nRut: "+rut+"\nEmail: "+email+"\nTelefono: "+telefono+"\nAuto: "+marca +"\nAño: "+anno+"\nFecha reserva: "+fecha
        from_email = 'conmiscotusca2@gmail.com'  # correo de prueba que tenemos desde ahi salen los correos
        recipient_list = ['gu.auger@duocuc.cl']  # correo aqui llegan los correos de contacto & reserva
 
        try:
            send_mail(subject, message, from_email, recipient_list)
            print(message)
            messages.success(request, 'Correo enviado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

        return render(request, 'myapp/reservar.html', {'mensaje': 'Envío exitoso, favor revise su correo'})

    return redirect(request,'myapp/reservar.html', {'mensaje': 'Error al enviar mensaje, intente más tarde'}) 