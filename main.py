import yfinance as yf
class Activo:
    def __init__(self, ticker, cantidad):
        self.ticker = ticker
        self.cantidad = cantidad

    def valor(self):
        raise NotImplementedError("Debe implementarse en la subclase")
    

class Accion(Activo):
    def __init__(self, ticker, cantidad):
        self.ticker = ticker.upper()
        self.cantidad = cantidad
        self.data = yf.download(self.ticker, period="1y", progress=False)

    def precio_actual(self):
        return float(self.data["Close"].iloc[-1])

    def precio_dia(self, index):
        return float(self.data["Close"].iloc[index])

    def valor(self, index=None):
        if index is None:
            return self.precio_actual() * self.cantidad
        else:
            return self.precio_dia(index) * self.cantidad

    def dividendos(self):
        ticker = yf.Ticker(self.ticker)
        return float(ticker.dividends.sum())



class RentaFija(Activo):
    def __init__(self, capital, tasa_anual):
        self.capital = capital
        self.tasa_anual = tasa_anual

    def valor_actual(self, dias):
        tasa_diaria = self.tasa_anual / 365
        return self.capital * (1 + tasa_diaria) ** dias

    def valor(self):
        return self.capital
    