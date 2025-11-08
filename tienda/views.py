from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Producto
import logging

logger = logging.getLogger(__name__)


def tienda(request):
    """Vista de la tienda con productos optimizados y paginados"""
    try:
        # Optimización: select_related para evitar N+1 queries
        productos = Producto.objects.select_related('categorias').filter(
            disponibilidad=True
        ).order_by('-created')

        # Paginación (opcional pero recomendada)
        paginator = Paginator(productos, 12)  # 12 productos por página
        page = request.GET.get('page', 1)

        try:
            productos_paginados = paginator.page(page)
        except PageNotAnInteger:
            productos_paginados = paginator.page(1)
        except EmptyPage:
            productos_paginados = paginator.page(paginator.num_pages)

        return render(request, "tienda/tienda.html", {
            "productos": productos_paginados
        })
    except Exception as e:
        logger.error(f"Error al cargar la tienda: {str(e)}")
        return render(request, "tienda/tienda.html", {
            "productos": []
        })
