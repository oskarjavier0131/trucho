from django.db import models
from django.contrib.auth import get_user_model
from tienda.models import Producto
from django.db.models import Sum, F, DecimalField 

# Create your models here.

User = get_user_model()

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Representación más descriptiva
        return f"Pedido {self.id} - Usuario: {self.user.username} - Fecha: {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def total(self):
        # Calcula el total del pedido
        return self.lineapedido_set.aggregate(
            total=Sum(F('precio') * F('cantidad'), output_field=DecimalField())
        )['total'] or 0

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

class LineaPedido(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Precio unitario al momento de la compra
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto.nombre}'

    @property
    def subtotal(self):
        """Calcula el subtotal de esta línea de pedido"""
        return self.precio * self.cantidad

    class Meta:
        db_table = 'lineas_pedido'
        verbose_name = 'Linea de Pedido'
        verbose_name_plural = 'Lineas de Pedidos'
        ordering = ['id']

