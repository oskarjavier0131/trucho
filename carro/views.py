from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tienda.models import Producto
from .carro import Carro
import logging

logger = logging.getLogger(__name__)


def agregar_producto(request, producto_id):
    """Agrega un producto al carrito"""
    try:
        producto = get_object_or_404(Producto, id=producto_id)

        # Verificar que el producto esté disponible
        if not producto.disponibilidad:
            messages.warning(request, f"El producto '{producto.nombre}' no está disponible actualmente.")
            return redirect("Tienda")

        carro = Carro(request)
        carro.agregar(producto=producto)
        messages.success(request, f"'{producto.nombre}' agregado al carrito correctamente.")
    except Exception as e:
        logger.error(f"Error al agregar producto {producto_id} al carrito: {str(e)}")
        messages.error(request, "Hubo un error al agregar el producto al carrito.")

    return redirect("Tienda")


def eliminar_producto(request, producto_id):
    """Elimina un producto del carrito"""
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        carro = Carro(request)
        carro.eliminar(producto=producto)
        messages.success(request, f"'{producto.nombre}' eliminado del carrito.")
    except Exception as e:
        logger.error(f"Error al eliminar producto {producto_id} del carrito: {str(e)}")
        messages.error(request, "Hubo un error al eliminar el producto del carrito.")

    return redirect("Tienda")


def restar_producto(request, producto_id):
    """Reduce la cantidad de un producto en el carrito"""
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        carro = Carro(request)
        carro.restar_producto(producto=producto)
        messages.success(request, f"Cantidad de '{producto.nombre}' actualizada.")
    except Exception as e:
        logger.error(f"Error al restar producto {producto_id} del carrito: {str(e)}")
        messages.error(request, "Hubo un error al actualizar el carrito.")

    return redirect("Tienda")


def limpiar_carro(request):
    """Limpia completamente el carrito"""
    try:
        carro = Carro(request)
        carro.limpiar_carro()
        messages.success(request, "El carrito ha sido vaciado.")
    except Exception as e:
        logger.error(f"Error al limpiar el carrito: {str(e)}")
        messages.error(request, "Hubo un error al vaciar el carrito.")

    return redirect("Tienda")