from datetime import date


class Transaccion:
    
    TIPOS_VALIDOS = ("compra", "venta")
    COMISION_DEFAULT = 0.001  # 0.1% por defecto

    def __init__(
        self,
        tipo: str,
        fecha: date,
        precio: float,
        cantidad: int,
        comision: float = COMISION_DEFAULT,
    ):
        if tipo.lower() not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de transacción inválido: '{tipo}'. Use 'compra' o 'venta'.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")
        if not (0 <= comision < 1):
            raise ValueError("La comisión debe estar entre 0 y 1 (exclusivo).")

        self.tipo = tipo.lower()
        self.fecha = fecha
        self.precio = float(precio)
        self.cantidad = int(cantidad)
        self.comision = float(comision)


    def calcularTotal(self) -> float:

        subtotal = self.precio * self.cantidad
        if self.tipo == "compra":
            return subtotal * (1 + self.comision)
        else:  # venta
            return subtotal * (1 - self.comision)

    def valorComision(self) -> float:
        """Retorna el monto absoluto cobrado por comisión."""
        return self.precio * self.cantidad * self.comision

    def __repr__(self) -> str:
        return (
            f"Transaccion(tipo='{self.tipo}', fecha={self.fecha}, "
            f"precio={self.precio:.4f}, cantidad={self.cantidad}, "
            f"comision={self.comision:.4%}, total={self.calcularTotal():.4f})"
        )