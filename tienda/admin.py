from django.contrib import admin

from .models import Producto, Contacto, Pedido, PedidoActualizar
from django.contrib.auth.admin import UserAdmin

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('p_nombre', 'categoria', 'precio')
    list_filter = ['categoria']
    search_fields = ['p_nombre']
    
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'desc', 'correo', 'reloj')#tablas
    list_filter = ['reloj']

class PedidoActualizarAdmin(admin.ModelAdmin):
    list_display = ('id', 'actualizar_de', 'fecha')#tablas
    list_filter = ['fecha']
    pass 
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido_id', 'usuario_id', 'nombre', 'correo', 'reloj')#tablas
    list_filter = ['reloj']
    pass

admin.site.register(Producto, ProductoAdmin)#cuadro
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoActualizar, PedidoActualizarAdmin)