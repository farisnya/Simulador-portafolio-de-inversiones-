class RentaFija:
    def __init__(self, nombre, capital, tasa, dias=0):
        self.nombre = nombre
        self.capital_inicial = capital
        self.capital = capital
        self.tasa = tasa
        self.dias = dias
        self.tasa_diaria = (1 + tasa) ** (1 / 365) - 1

    def liquidar_dia(self):
        self.capital *= (1 + self.tasa_diaria)
        self.dias += 1

    def valor_actual(self):
        return self.capital
