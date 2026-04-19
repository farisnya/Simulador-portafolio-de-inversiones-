import matplotlib.pyplot as plt


class Grafico:
    def __init__(self, datos, rentabilidad_serie=None):
        self.datos = datos
        self.fechas = [d[0] for d in datos]
        self.valores = [d[1] for d in datos]
        self.rent_serie = rentabilidad_serie

    def graficar(self):
        if self.rent_serie is not None:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            ax1.plot(self.fechas, self.valores, color="steelblue",
                     label="Valor del portafolio")
            ax1.set_title("Evolución histórica del portafolio")
            ax1.set_ylabel("Valor (USD)")
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            rf = [r[0] for r in self.rent_serie]
            rv = [r[1] for r in self.rent_serie]
            ax2.plot(rf, rv, color="seagreen", label="Rentabilidad acumulada (%)")
            ax2.axhline(0, color="gray", linewidth=0.8, linestyle="--")
            ax2.set_title("Rendimiento del portafolio")
            ax2.set_xlabel("Fecha")
            ax2.set_ylabel("Rentabilidad (%)")
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            plt.tight_layout()
        else:
            plt.figure(figsize=(10, 5))
            plt.plot(self.fechas, self.valores, label="Valor del portafolio")
            plt.title("Evolución histórica del portafolio")
            plt.xlabel("Fecha")
            plt.ylabel("Valor (USD)")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
        plt.show()
