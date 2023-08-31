from django.db import models
from django.utils import timezone

class Producto(models.Model):
    id = models.AutoField
    p_nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50, default="")
    subcategoria = models.CharField(max_length=50, default="")
    precio = models.IntegerField(default=0)
    descuento = models.CharField(max_length=200)
    publicacion = models.DateField()
    imagen = models.ImageField(upload_to="", default="")
    def __str__(self):
        return self.p_nombre

class Contacto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=70, default="")
    celular = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")
    reloj = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    pedido_id = models.AutoField(primary_key=True)
    e_json = models.CharField(max_length=5000)
    usuario_id = models.IntegerField(default=0)
    monto = models.IntegerField(default=0)
    nombre = models.CharField(max_length=90)
    correo = models.CharField(max_length=111)
    direccion = models.CharField(max_length=111)
    ciudad = models.CharField(max_length=111)
    estado = models.CharField(max_length=111)
    codigo_z = models.CharField(max_length=111)
    celular = models.CharField(max_length=111, default="")
    reloj = models.DateTimeField(default=timezone.now)

class PedidoActualizar(models.Model):
    id = models.AutoField(primary_key=True)
    pedido_id = models.IntegerField(default="")
    actualizar_de = models.CharField(max_length=5000)
    fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.actualizar_de