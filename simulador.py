import pandas as pd


class Simulador:
    def __init__(self, portafolio, acciones):
        self.portafolio = portafolio
        self.acciones = acciones
        self.fechas = []
        self.ordenes = []

    def programar_orden(self, fecha, tipo, ticker, cantidad):
        self.ordenes.append((pd.Timestamp(fecha).normalize(), tipo, ticker, cantidad))

    def _fechas_comunes(self):
        fechas = None
        for a in self.acciones.values():
            idx = a.data.index.normalize()
            fechas = idx if fechas is None else fechas.intersection(idx)
        return fechas.sort_values()

    def actualizar_precios(self, fecha):
        return {t: a.precio_cierre(fecha) for t, a in self.acciones.items()}

    def _ejecutar_ordenes(self, fecha):
        pendientes = []
        for orden in self.ordenes:
            f, tipo, ticker, cantidad = orden
            if f == fecha.normalize():
                accion = self.acciones.get(ticker) or self.portafolio.acciones.get(ticker)
                if accion is None:
                    print(f"[{fecha.date()}] Ticker {ticker} no disponible")
                    continue
                precio = accion.precio_cierre(fecha)
                if tipo == "compra":
                    self.portafolio.agregar_accion(accion, fecha, precio, cantidad)
                elif tipo == "venta":
                    self.portafolio.vender_accion(ticker, fecha, precio, cantidad)
            else:
                pendientes.append(orden)
        self.ordenes = pendientes

    def simular(self):
        self.fechas = list(self._fechas_comunes())
        for fecha in self.fechas:
            self._ejecutar_ordenes(fecha)
            self.actualizar_precios(fecha)
            self.portafolio.cobrar_dividendos(fecha)
            self.portafolio.liquidar_renta_fija()
            self.portafolio.registrar_hist(fecha)
        return self.fechas

    def calcular_rentabilidad(self):
        if not self.portafolio.historial:
            return 0.0
        inicio = self.portafolio.capital_inicial
        fin = self.portafolio.historial[-1][1]
        return (fin - inicio) / inicio * 100

    def rentabilidad_acumulada_serie(self):
        base = self.portafolio.capital_inicial
        return [(f, (v - base) / base * 100) for f, v in self.portafolio.historial]

    def resumen(self):
        p = self.portafolio
        valor_final = p.historial[-1][1] if p.historial else p.capital_inicial
        return {
            "capital_inicial": p.capital_inicial,
            "valor_final": valor_final,
            "dividendos_cobrados": p.dividendos_totales,
            "comisiones_pagadas": p.comisiones_totales,
            "rentabilidad_%": self.calcular_rentabilidad(),
        }
