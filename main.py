from accion import Accion
from renta_fija import RentaFija
from portafolio import Portafolio
from simulador import Simulador
from grafico import Grafico


def main():
    port = Portafolio(80000)

    tickers = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOG",
               "META", "NVDA", "NFLX", "BABA", "JPM"]

    acciones = {t: Accion(t) for t in tickers}

    # Primer día común de datos
    fechas_iniciales = None
    for a in acciones.values():
        idx = a.data.index.normalize()
        fechas_iniciales = idx if fechas_iniciales is None else fechas_iniciales.intersection(idx)
    fechas_ord = fechas_iniciales.sort_values()
    fecha0 = fechas_ord[0]

    # Compra inicial: 5 unidades de cada acción
    for t, acc in acciones.items():
        precio = acc.precio_cierre(fecha0)
        port.agregar_accion(acc, fecha0, precio, cantidad=5)

    # Renta fija diversificada
    port.agregar_renta_fija(RentaFija("CDT-90d",    5000, 0.075))
    port.agregar_renta_fija(RentaFija("CDT-360d",   8000, 0.095))
    port.agregar_renta_fija(RentaFija("Bono-Corp",  6000, 0.11))

    # Simulador con órdenes intercaladas
    sim = Simulador(port, acciones)

    if len(fechas_ord) > 60:
        sim.programar_orden(fechas_ord[30],  "venta",  "TSLA", 2)
        sim.programar_orden(fechas_ord[60],  "compra", "NVDA", 3)
    if len(fechas_ord) > 150:
        sim.programar_orden(fechas_ord[120], "venta",  "NFLX", 5)
        sim.programar_orden(fechas_ord[150], "compra", "AAPL", 4)
    if len(fechas_ord) > 200:
        sim.programar_orden(fechas_ord[200], "venta",  "BABA", 3)

    sim.simular()

    resumen = sim.resumen()
    print("\n--- RESULTADOS ---")
    for k, v in resumen.items():
        if isinstance(v, float):
            print(f"{k}: {v:,.2f}")
        else:
            print(f"{k}: {v}")

    Grafico(port.historial, sim.rentabilidad_acumulada_serie()).graficar()


if __name__ == "__main__":
    main()
