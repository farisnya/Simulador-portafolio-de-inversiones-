from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portafolio import Portafolio


class Simulador:


    def __init__(self, portafolio: "Portafolio"):
        self.portafolio = portafolio
        self.fechas: list[date] = []

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def simular(self, fecha_inicio: date, fecha_fin: date) -> None:
        
        if fecha_inicio > fecha_fin:
            raise ValueError("fecha_inicio debe ser anterior o igual a fecha_fin.")

        self.fechas = self._generar_fechas(fecha_inicio, fecha_fin)

        capital_inicial = self.portafolio.valorTotal()
        print(f"\n{'='*55}")
        print(f"  Inicio de simulación: {fecha_inicio}  →  {fecha_fin}")
        print(f"  Días de trading : {len(self.fechas)}")
        print(f"  Capital inicial : ${capital_inicial:,.2f}")
        print(f"{'='*55}\n")

        for fecha in self.fechas:
            self.actualizarPrecios(fecha)
            self._acumularInteresesRentaFija(fecha)
            self.portafolio.registrarHist(fecha)

        print(f"\n{'='*55}")
        print("  Simulación finalizada.")
        print(f"  Capital final   : ${self.portafolio.valorTotal():,.2f}")
        rentabilidad = self.calcularRentabilidad()
        signo = "+" if rentabilidad >= 0 else ""
        print(f"  Rentabilidad    : {signo}{rentabilidad:.2f}%")
        print(f"{'='*55}\n")

    def actualizarPrecios(self, fecha: date) -> None:
        
        import yfinance as yf

        if not self.portafolio.acciones:
            return

        tickers = [a.ticker for a in self.portafolio.acciones]
        fecha_str = fecha.strftime("%Y-%m-%d")
        # yfinance requiere un rango; pedimos fecha ± 1 día para asegurar el dato.
        fecha_siguiente = (fecha + timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            datos = yf.download(
                tickers,
                start=fecha_str,
                end=fecha_siguiente,
                progress=False,
                auto_adjust=True,
            )

            if datos.empty:
                return  # No hay datos para esa fecha (festivo, etc.)

            for accion in self.portafolio.acciones:
                try:
                    if len(tickers) == 1:
                        # Con un solo ticker yfinance no crea MultiIndex
                        precio_serie = datos["Close"]
                    else:
                        precio_serie = datos["Close"][accion.ticker]

                    if not precio_serie.empty:
                        nuevo_precio = float(precio_serie.iloc[-1])
                        if nuevo_precio > 0:
                            # Añadimos la fila al DataFrame interno de la acción
                            accion._registrar_precio(fecha, nuevo_precio)
                except (KeyError, IndexError):
                    pass  # Ticker sin datos en esa fecha → conserva último precio

        except Exception as exc:
            print(f"  [Advertencia] No se pudo actualizar precios para {fecha}: {exc}")

    def calcularRentabilidad(self) -> float:
    
        historial = self.portafolio.historial
        if not historial:
            raise ValueError(
                "El historial está vacío. Ejecute simular() antes de calcular la rentabilidad."
            )

        valor_inicial = historial[0]["valor"]
        valor_final = historial[-1]["valor"]

        if valor_inicial == 0:
            raise ZeroDivisionError("El valor inicial del portafolio es cero; no se puede calcular rentabilidad.")

        return ((valor_final - valor_inicial) / valor_inicial) * 100


    
    def _generar_fechas(inicio: date, fin: date) -> list[date]:
    
        fechas = []
        actual = inicio
        while actual <= fin:
            if actual.weekday() < 5:  # 0=Lunes … 4=Viernes
                fechas.append(actual)
            actual += timedelta(days=1)
        return fechas

    def _acumularInteresesRentaFija(self, fecha: date) -> None:  # noqa: N802
        
        for rf in self.portafolio.rentaFija:
            interes_diario = rf.capital * (rf.tasa / 365)
            rf.capital += interes_diario
            rf.dias += 1

    def __repr__(self) -> str:
        rango = (
            f"{self.fechas[0]} → {self.fechas[-1]}" if self.fechas else "sin ejecutar"
        )
        return (
            f"Simulador(portafolio='{self.portafolio}', "
            f"fechas={len(self.fechas)} días [{rango}])"
        )