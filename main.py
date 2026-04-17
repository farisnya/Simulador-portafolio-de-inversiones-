import yfinance as yf
class Activo:
    def valor(self):
        raise NotImplementedError("Debe implementarse en la subclase")


class Accion(Activo):
    def __init__(self, ticker, cantidad):
        self.ticker = ticker.upper()
        self.cantidad = cantidad
        self.precios = yf.download(self.ticker, period="1y", progress=False)

    def precioActual(self):
        return self.precios["Close"].iloc[-1]

    def precioDia(self, fecha):
        return self.precios.loc[fecha]["Close"]

    def minDia(self, fecha):
        return self.precios.loc[fecha]["Low"]

    def maxDia(self, fecha):
        return self.precios.loc[fecha]["High"]

    def valor(self):
        return self.precioActual() * self.cantidad

    def obtenerDividendos(self):
        ticker = yf.Ticker(self.ticker)
        return ticker.dividends.sum()

class RentaFija(Activo):
    def __init__(self, capital, tasa, dias):
        self.capital = capital
        self.tasa = tasa
        self.dias = dias

    def valorActual(self):
        tasa_diaria = self.tasa / 365
        return self.capital * (1 + tasa_diaria) ** self.dias

    def valor(self):
        return self.valorActual()
    