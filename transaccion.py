class Transaccion:
    def __init__(self, tipo, fecha, precio, cantidad, comision=0.01):
        self.tipo = tipo
        self.fecha = fecha
        self.precio = precio
        self.cantidad = cantidad
        self.comision = comision

    def calcular_total(self):
        total = self.precio * self.cantidad
        if self.tipo == "compra":
            return total * (1 + self.comision)
        return total * (1 - self.comision)

    def costo_comision(self):
        return self.precio * self.cantidad * self.comision
