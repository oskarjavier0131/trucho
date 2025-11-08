from decimal import Decimal


class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}

        self.carro = carro

    def agregar(self, producto):
        """Agrega un producto al carrito o incrementa su cantidad"""
        producto_id = str(producto.id)
        if producto_id not in self.carro:
            self.carro[producto_id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio_unitario": str(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url if producto.imagen else ""
            }
        else:
            self.carro[producto_id]["cantidad"] += 1

        self.guardar()

    def guardar(self):
        """Guarda el carrito en la sesión"""
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        """Elimina un producto del carrito completamente"""
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar()

    def restar_producto(self, producto):
        """Reduce la cantidad de un producto en 1 o lo elimina si llega a 0"""
        producto_id = str(producto.id)
        if producto_id in self.carro:
            self.carro[producto_id]["cantidad"] -= 1
            if self.carro[producto_id]["cantidad"] <= 0:
                del self.carro[producto_id]
            self.guardar()

    def limpiar_carro(self):
        """Vacía completamente el carrito"""
        self.session["carro"] = {}
        self.session.modified = True

    def get_total(self):
        """Calcula el total del carrito"""
        total = Decimal('0')
        for item in self.carro.values():
            precio_unitario = Decimal(item["precio_unitario"])
            cantidad = item["cantidad"]
            total += precio_unitario * cantidad
        return total

    def get_cantidad_total(self):
        """Obtiene la cantidad total de productos en el carrito"""
        return sum(item["cantidad"] for item in self.carro.values())

    def __iter__(self):
        """Permite iterar sobre los items del carrito"""
        for item in self.carro.values():
            item['precio_unitario'] = Decimal(item['precio_unitario'])
            item['subtotal'] = item['precio_unitario'] * item['cantidad']
            yield item

    def __len__(self):
        """Retorna la cantidad de productos diferentes en el carrito"""
        return len(self.carro)    


