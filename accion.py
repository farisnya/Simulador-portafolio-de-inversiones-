import yfinance as yf
import pandas as pd


class Accion:
    def __init__(self, ticker, cantidad=0):
        self.ticker = ticker
        self.cantidad = cantidad
        tk = yf.Ticker(ticker)
        self.data = tk.history(period="1y", auto_adjust=False)
        self.dividendos_serie = tk.dividends
        self.dividendos_cobrados = 0.0

    def precio_cierre(self, fecha):
        return float(self.data.loc[fecha, "Close"])

    def min_dia(self, fecha):
        return float(self.data.loc[fecha, "Low"])

    def max_dia(self, fecha):
        return float(self.data.loc[fecha, "High"])

    def precio_actual(self):
        return float(self.data["Close"].iloc[-1])

    def valor(self, fecha=None):
        precio = self.precio_cierre(fecha) if fecha is not None else self.precio_actual()
        return precio * self.cantidad

    def obtener_dividendos(self, fecha=None):
        serie = self.dividendos_serie
        if serie is None or serie.empty:
            return 0.0
        if fecha is None:
            return float(serie.sum())
        idx = serie.index
        if getattr(idx, "tz", None) is not None:
            try:
                idx = idx.tz_convert(None)
            except TypeError:
                idx = idx.tz_localize(None)
        mask = idx.normalize() == pd.Timestamp(fecha).normalize()
        if mask.any():
            return float(serie[mask].sum())
        return 0.0
