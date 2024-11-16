from .models import cliente  

def custom_context(request):
    context = {}
    
    # Verificar si hay un cliente autenticado en la sesión
    if 'cliente_id' in request.session:
        cliente_id = request.session['cliente_id']
        try:
            cliente_obj = cliente.objects.get(rut=cliente_id)
            context['is_authenticated'] = True
            context['cliente'] = cliente_obj
        except cliente.DoesNotExist:
            context['is_authenticated'] = False
            context['cliente'] = None
    else:
        context['is_authenticated'] = False
        context['cliente'] = None
    
    # Manejar el mensaje modal si está en la sesión
    mensaje = None
    if 'mensaje' in request.session:
        mensaje = request.session.pop('mensaje')  # Obtener el mensaje y eliminarlo de la sesión
    context['mensaje_modal'] = mensaje
    
    return context