from decimal import Decimal
from .carro import Carro


def importe_total_carro(request):
    """
    Context processor que provee el total del carrito a todos los templates.
    Retorna 0 si el carrito está vacío o el usuario no está autenticado.
    """
    total = Decimal('0')

    if 'carro' in request.session and request.session['carro']:
        carro = Carro(request)
        total = carro.get_total()

    return {'importe_total_carro': total}        