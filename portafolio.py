from transaccion import Transaccion


class Portafolio:
    def __init__(self, capital):
        self.capital_inicial = capital
        self.capital = capital
        self.acciones = {}
        self.renta_fija = []
        self.historial = []
        self.dividendos_totales = 0.0
        self.comisiones_totales = 0.0

    def agregar_accion(self, accion, fecha, precio, cantidad, comision=0.01):
        if not (accion.min_dia(fecha) <= precio <= accion.max_dia(fecha)):
            print(f"[{fecha.date()}] Precio {precio:.2f} fuera del rango "
                  f"[{accion.min_dia(fecha):.2f}, {accion.max_dia(fecha):.2f}] "
                  f"para {accion.ticker}")
            return False

        trans = Transaccion("compra", fecha, precio, cantidad, comision)
        total = trans.calcular_total()

        if self.capital < total:
            print(f"[{fecha.date()}] Capital insuficiente para comprar "
                  f"{cantidad} {accion.ticker}")
            return False

        self.capital -= total
        self.comisiones_totales += trans.costo_comision()
        if accion.ticker in self.acciones:
            self.acciones[accion.ticker].cantidad += cantidad
        else:
            accion.cantidad = cantidad
            self.acciones[accion.ticker] = accion
        print(f"[{fecha.date()}] COMPRA {cantidad} {accion.ticker} @ {precio:.2f}")
        return True

    def vender_accion(self, ticker, fecha, precio, cantidad, comision=0.01):
        if ticker not in self.acciones:
            print(f"[{fecha.date()}] No posee {ticker}")
            return False

        accion = self.acciones[ticker]
        if cantidad > accion.cantidad:
            print(f"[{fecha.date()}] Cantidad a vender excede tenencia de {ticker}")
            return False

        if not (accion.min_dia(fecha) <= precio <= accion.max_dia(fecha)):
            print(f"[{fecha.date()}] Precio {precio:.2f} fuera del rango "
                  f"[{accion.min_dia(fecha):.2f}, {accion.max_dia(fecha):.2f}] "
                  f"para {ticker}")
            return False

        trans = Transaccion("venta", fecha, precio, cantidad, comision)
        self.capital += trans.calcular_total()
        self.comisiones_totales += trans.costo_comision()
        accion.cantidad -= cantidad
        if accion.cantidad == 0:
            del self.acciones[ticker]
        print(f"[{fecha.date()}] VENTA  {cantidad} {ticker} @ {precio:.2f}")
        return True

    def agregar_renta_fija(self, rf):
        if self.capital < rf.capital_inicial:
            print(f"Capital insuficiente para abrir {rf.nombre}")
            return False
        self.capital -= rf.capital_inicial
        self.renta_fija.append(rf)
        print(f"Renta fija abierta: {rf.nombre} "
              f"(capital={rf.capital_inicial}, tasa={rf.tasa*100:.2f}%)")
        return True

    def cobrar_dividendos(self, fecha):
        cobrado = 0.0
        for accion in self.acciones.values():
            div_unit = accion.obtener_dividendos(fecha)
            if div_unit > 0:
                pago = div_unit * accion.cantidad
                self.capital += pago
                accion.dividendos_cobrados += pago
                cobrado += pago
        self.dividendos_totales += cobrado
        return cobrado

    def liquidar_renta_fija(self):
        for rf in self.renta_fija:
            rf.liquidar_dia()

    def valor_total(self, fecha):
        valor_acciones = sum(
            a.precio_cierre(fecha) * a.cantidad for a in self.acciones.values()
        )
        valor_rf = sum(rf.valor_actual() for rf in self.renta_fija)
        return self.capital + valor_acciones + valor_rf

    def registrar_hist(self, fecha):
        self.historial.append((fecha, self.valor_total(fecha)))
