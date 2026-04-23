# Simulador-portafolio-de-inversiones-

## Descripción

Este proyecto consiste en el desarrollo de un simulador financiero en Python que permite gestionar, analizar y visualizar la rentabilidad de un portafolio de inversión diversificado.

El sistema integra activos de renta variable (acciones) y renta fija (bonos o CDTs), permitiendo simular operaciones de compra y venta, así como analizar la evolución del portafolio a lo largo del tiempo.

El simulador utiliza datos reales del mercado para obtener precios de cierre diarios, e incorpora factores relevantes como dividendos, intereses y comisiones de transacción.

---

## Objetivo

Desarrollar una herramienta que permita:

* Simular decisiones de inversión en distintos tipos de activos
* Evaluar el desempeño de un portafolio financiero
* Analizar la evolución del capital en el tiempo
* Aplicar conceptos financieros en un entorno computacional

---

## Funcionalidades principales

* Consulta de precios reales utilizando la librería `yfinance`
* Compra y venta de acciones con validación de capital disponible
* Cálculo de comisiones por transacción
* Simulación de activos de renta fija con acumulación de interés diario
* Registro histórico del valor del portafolio
* Cálculo de la rentabilidad neta
* Generación de representaciones gráficas del rendimiento

---

## Estructura del proyecto

```id="k92ls1"
proyecto/
│
├── main.py
├── portafolio.py
├── accion.py
├── renta_fija.py
├── transaccion.py
├── simulador.py
├── grafico.py
└── README.md
```

---

## Diseño del sistema

El sistema está desarrollado bajo el paradigma de programación orientada a objetos, donde cada componente del portafolio es representado mediante una clase independiente.

Principales clases:

* `Accion`
* `RentaFija`
* `Portafolio`
* `Transaccion`
* `Simulador`

---

## Metodología de cálculo

La rentabilidad del portafolio se determina considerando:

* Variación en el precio de los activos
* Dividendos generados por acciones
* Intereses acumulados en activos de renta fija
* Costos asociados a comisiones de compra y venta

---

## Visualización

El sistema genera gráficas que permiten analizar:

* La evolución del valor del portafolio
* El comportamiento del rendimiento en el tiempo

---

## Instrucciones de ejecución

1. Clonar el repositorio:

```bash id="p4s2y1"
git clone <url-del-repositorio>
```

2. Instalar dependencias:

```bash id="y7g3a2"
pip install yfinance matplotlib pandas
```

3. Ejecutar el programa:

```bash id="t8h1k9"
python main.py
```

---

## Tecnologías utilizadas

* Python
* yfinance
* pandas
* matplotlib

---

## Ejemplo de uso

* Definir un capital inicial
* Adquirir acciones (por ejemplo, AAPL o MSFT)
* Incorporar activos de renta fija
* Ejecutar la simulación
* Analizar los resultados obtenidos

---

## Consideraciones

* Las operaciones se realizan con base en datos reales del mercado
* Se valida la disponibilidad de capital antes de cada transacción
* El sistema busca representar de manera simplificada el comportamiento de un portafolio real

---

## Autor

Proyecto académico desarrollado como simulador financiero orientado al análisis de inversiones.

---

## Diagrama UML
<img width="1179" height="775" alt="image" src="https://github.com/user-attachments/assets/a999fa60-594b-4eea-929d-2230e180895f" />

---

## Correccón diagrama UML
<img width="1347" height="768" alt="image" src="https://github.com/user-attachments/assets/22922e1c-ac2f-4b13-8a27-bb061694a9f4" />

