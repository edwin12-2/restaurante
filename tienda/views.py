from django.shortcuts import HttpResponse, redirect
from django.http import HttpResponseRedirect

from .models import Producto, Pedido, PedidoActualizar
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from math import ceil
from django.contrib.auth import authenticate, logout, login
import json
from django.views.decorators.csrf import csrf_exempt 

def index(re):
    tProductos = []
    cProductos = Producto.objects.values('categoria', 'id')
    categorias = {item['categoria'] for item in cProductos}
    for categoria in categorias:
        p = Producto.objects.filter(categoria=categoria)
        n = len(p)
        nSlides = n // 4 + ceil((n / 4)-(n // 4))
        tProductos.append([p, range(1, nSlides), nSlides])
    da = {'tProductos': tProductos}
    return render(re, 'tienda/index.html', da)

def handleSalir(re):
    logout(re)
    return HttpResponseRedirect(re.META.get('HTTP_REFERER'))

def handleIngresar(re):
    if re.method == "POST":
        usuario = re.POST['usuario']
        clave = re.POST['clave']

        ingresar = authenticate(username=usuario, password=clave)
        if ingresar is not None:
            login(re, ingresar)
            messages.success(re, '¡Ha ingresado!')
            return HttpResponseRedirect(re.META.get('HTTP_REFERER'))
        else:
            messages.warning(re, '¡No ha ingresado!')
            return HttpResponseRedirect(re.META.get('HTTP_REFERER'))
    return HttpResponse("Error - 404")

def handleRegistro(re):
    if re.method == "POST":
        usuario = re.POST['usuario']
        nombre = re.POST['nombre']
        apellidos = re.POST['apellidos']
        correo = re.POST['correo']
        celular = re.POST['celular']
        clave1 = re.POST['clave1']
        clave2 = re.POST['clave2']
        if (clave2 != clave1):
            messages.warning(re, 'Las contraseñas no son iguales')
            return HttpResponseRedirect(re.META.get('HTTP_REFERER'))
        try:
            usuario = User.objects.get(username=usuario)
            messages.warning(re, 'Ya existe el usuario')
            return HttpResponseRedirect(re.META.get('HTTP_REFERER'))
        except User.DoesNotExist:
            musuario = User.objects.create_user(username=usuario, email=correo, password=clave1)
            musuario.first_name = nombre
            musuario.last_name = apellidos
            musuario.phone = celular
            musuario.save()
            messages.success(re, 'Usuario creado')
            return HttpResponseRedirect(re.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Error - 404")

def verProducto(re, myid):
    pr = Producto.objects.filter(id=myid)
    return render(re, 'tienda/verP.html', {'producto': pr[0]})

def verPedido(re):
    if re.user.is_authenticated:
        c_usuario = re.user
        pedidoH = Pedido.objects.filter()
        if len(pedidoH) == 0:
            messages.info(re, "Ha sido ordenado")
            return render(re, 'tienda/verPedido.html')
        return render(re, 'tienda/verPedido.html', {'pedidoH': pedidoH})
    return render(re, 'tienda/verPedido.html')
        
def buscarMatch(q, item):
    if q in item.descuento.lower() or q in item.p_nombre.lower() or q in item.categoria.lower() or q in item.descuento or q in item.p_nombre or q in item.categoria or q in item.descuento.upper() or q in item.p_nombre.upper() or q in item.categoria.upper():
        return True
    else:
        return False

def buscar(re):
    q = re.GET.get('buscar')
    tProductos = []
    cProductos = Producto.objects.values('categoria', 'id')
    categorias = {item['categoria'] for item in cProductos}
    for categoria in categorias:
        p = Producto.objects.filter(categoria=categoria)
        pr = [item for item in p if buscarMatch(q, item)]
        n = len(pr)
        nSlides = n // 4 + ceil((n / 4)-(n // 4))
        if len(pr) != 0:
            tProductos.append([pr, range(1, nSlides), nSlides])
    da = {'tProductos': tProductos, "msg": ""}
    if len(tProductos) == 0 or len(q) < 3:
        da = {'msg': "No hay productos"}
    return render(re, 'tienda/buscar.html', da)

def verificar(re):
    if re.method == "POST":
        e_json = re.POST.get('itemsJson', '')
        us_id = re.POST.get('user_id', '')
        n = re.POST.get('nombre', '')
        co = re.POST.get('correo', '')
        monto = re.POST.get('monto', '')
        di = re.POST.get('direccion', '') + " " + re.POST.get('direccion2', '')
        ciudad = re.POST.get('ciudad', '')
        es = re.POST.get('estado', '')
        z = re.POST.get('postal', '')
        celular = re.POST.get('celular', '')
        orden = Pedido(e_json=e_json, usuario_id=us_id, monto=monto, nombre=n, correo=co, direccion=di, ciudad=ciudad, estado=es, codigo_z=z, celular=celular)
        orden.save()
        actualizarP = PedidoActualizar(pedido_id=orden.pedido_id, actualizar_de="re")
        actualizarP.save()
        thank = True
        id = orden.pedido_id
        if 'delivery' in re.POST:
            return render(re, 'tienda/verificar.html', {'thank': thank, 'id': id})
    return render(re, 'tienda/verificar.html')
        
def rastreo(re):
    if re.method == "POST":
        id = re.POST.get('id', '')
        correo = re.POST.get('correo', '')
        nombre = re.POST.get('nombre', '')
        clave = re.POST.get('clave')
        usuario = authenticate(username=nombre, password=clave)
        if usuario is not None:
            try:
                orden = Pedido.objects.filter(pedido_id=id, correo=correo)
                if len(orden) > 0:
                    actualiza = PedidoActualizar.objects.filter(pedido_id=id)
                    actualizas = []
                    for item in actualiza:
                        actualizas.append({'text': item.actualizar_de, 'time': item.fecha})
                        response = json.dumps({"status": "comprobado", "actualizas": actualizas, "itemsJson": orden[0].e_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"vacio"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')
        else:
            return HttpResponse('{"status":"fallo"}')
    return render(re, 'tienda/rastreo.html')

