import os
import csv
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px

from accion import Accion
from portafolio import Portafolio
from simulador import Simulador
from renta_fija import RentaFija
from transaccion import Transaccion

ARCHIVO_OPERACIONES = "operaciones.csv"
COLUMNAS = ["Timestamp", "Fecha", "Tipo", "Ticker", "Cantidad", "Precio", "Total", "Comision"]


def cargar_operaciones():
    if not os.path.exists(ARCHIVO_OPERACIONES):
        return []
    with open(ARCHIVO_OPERACIONES, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_operacion(registro):
    existe = os.path.exists(ARCHIVO_OPERACIONES)
    with open(ARCHIVO_OPERACIONES, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if not existe:
            writer.writeheader()
        writer.writerow(registro)


st.set_page_config(page_title="Simulador de Portafolio", layout="wide")
st.title("Simulador de Portafolio")

if "portafolio" not in st.session_state:
    st.session_state.portafolio = None
if "acciones" not in st.session_state:
    st.session_state.acciones = {}
if "simulado" not in st.session_state:
    st.session_state.simulado = False
if "log_operaciones" not in st.session_state:
    st.session_state.log_operaciones = cargar_operaciones()

# Sidebar
st.sidebar.header("Configuración")

tickers = st.sidebar.multiselect(
    "Acciones",
    ["AAPL", "TSLA", "MSFT", "AMZN", "GOOG",
     "META", "NVDA", "NFLX", "BABA", "JPM"],
    default=[]
)

capital = st.sidebar.number_input(
    "Capital inicial",
    min_value=1000,
    value=100_000_000,
    step=1000
)

usar_rf = st.sidebar.checkbox("Incluir renta fija", value=True)

if usar_rf:
    capital_rf = st.sidebar.number_input(
        "Capital renta fija",
        min_value=0,
        value=3000,
        step=500
    )
    tasa_rf = st.sidebar.number_input(
        "Tasa anual (%)",
        min_value=0.0,
        value=8.0,
        step=0.5
    ) / 100

simular = st.sidebar.button("Simular")

# Ejecución
if simular:
    try:
        port = Portafolio(capital)
        acciones = {}

        for t in tickers:
            acc = Accion(t)
            try:
                _ = acc.dividendos_serie
            except Exception:
                acc.dividendos_serie = None
            acciones[t] = acc

        fechas = None
        for acc in acciones.values():
            idx = acc.data.index.normalize()
            fechas = idx if fechas is None else fechas.intersection(idx)

        fechas = fechas.sort_values()

        if usar_rf and capital_rf > 0:
            rf = RentaFija("CDT", capital_rf, tasa_rf)
            port.agregar_renta_fija(rf)

        sim = Simulador(port, acciones)
        sim.simular()

        st.session_state.portafolio = port
        st.session_state.acciones = acciones
        st.session_state.simulado = True
        st.session_state.log_operaciones = cargar_operaciones()

    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.simulado:
    port = st.session_state.portafolio
    acciones = st.session_state.acciones

    capital_inicial = port.capital_inicial

    df = pd.DataFrame(port.historial, columns=["Fecha", "Valor"])
    valor_final = df["Valor"].iloc[-1]
    rentabilidad = ((valor_final - capital_inicial) / capital_inicial) * 100
    valor_rf_total = sum(rf.valor_actual() for rf in port.renta_fija)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Capital inicial", f"{capital_inicial:,.0f}")
    col2.metric("Valor final", f"{valor_final:,.0f}")
    col3.metric("Rentabilidad (%)", f"{rentabilidad:.2f}")
    col4.metric("Dividendos", f"{port.dividendos_totales:,.2f}")
    col5.metric("Comisiones", f"{port.comisiones_totales:,.2f}")

    st.metric("Valor renta fija", f"{valor_rf_total:,.2f}")

    st.subheader("Evolución del portafolio")
    fig = px.line(df, x="Fecha", y="Valor")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Precios de acciones")
    precios_df = pd.DataFrame()
    for t, acc in acciones.items():
        precios_df[t] = acc.data["Close"]
    precios_df = precios_df.dropna()

    fig2 = px.line(precios_df)
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Máximos y mínimos diarios")
    hl_df = pd.DataFrame()
    for t, acc in acciones.items():
        hl_df[f"{t}_High"] = acc.data["High"]
        hl_df[f"{t}_Low"] = acc.data["Low"]
    hl_df = hl_df.dropna()
    st.dataframe(hl_df.tail(20), use_container_width=True)

    st.subheader("Rango de precios (High vs Low)")
    for t, acc in acciones.items():
        df_hl = acc.data[["High", "Low"]].dropna()
        fig_hl = px.line(df_hl, title=f"{t} - High vs Low")
        fig_hl.update_layout(template="plotly_dark")
        st.plotly_chart(fig_hl, use_container_width=True)

    st.subheader("Historial")
    st.dataframe(df, use_container_width=True)

    # Trading manual
    st.divider()
    st.header("Trading Manual")

    with st.expander("Estado del portafolio", expanded=True):
        col_cap, col_val = st.columns(2)
        col_cap.metric("Capital disponible", f"${port.capital:,.2f}")
        valor_acciones_actual = sum(
            a.precio_actual() * a.cantidad for a in port.acciones.values()
        )
        col_val.metric("Valor en acciones", f"${valor_acciones_actual:,.2f}")

        if port.acciones:
            tenencia_data = []
            for t, acc in port.acciones.items():
                precio_act = acc.precio_actual()
                tenencia_data.append({
                    "Ticker": t,
                    "Cantidad": acc.cantidad,
                    "Precio actual": f"${precio_act:,.2f}",
                    "Valor total": f"${precio_act * acc.cantidad:,.2f}",
                    "Dividendos cobrados": f"${acc.dividendos_cobrados:,.2f}",
                })
            st.dataframe(pd.DataFrame(tenencia_data), use_container_width=True, hide_index=True)
        else:
            st.info("Sin acciones en el portafolio.")

    st.subheader("Nueva orden")

    tickers_disponibles = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOG", "META", "NVDA", "NFLX", "BABA", "JPM"]
    col_form1, col_form2 = st.columns(2)

    with col_form1:
        tipo_op = st.radio("Tipo de operación", ["Compra", "Venta"], horizontal=True)
        ticker_sel = st.selectbox("Ticker", tickers_disponibles)

        if ticker_sel not in acciones:
            acciones[ticker_sel] = Accion(ticker_sel)
            st.session_state.acciones = acciones
        acc_sel = acciones[ticker_sel]
        fechas_disponibles = acc_sel.data.index.normalize().unique().sort_values()
        fecha_sel = st.selectbox(
            "Fecha",
            fechas_disponibles,
            index=len(fechas_disponibles) - 1,
            format_func=lambda f: f.strftime("%Y-%m-%d"),
        )

    with col_form2:
        try:
            low_dia = acc_sel.min_dia(fecha_sel)
            high_dia = acc_sel.max_dia(fecha_sel)
            cierre_dia = acc_sel.precio_cierre(fecha_sel)

            st.info(
                f"{ticker_sel} — {fecha_sel.strftime('%Y-%m-%d')}\n\n"
                f"Cierre: ${cierre_dia:,.2f} | Rango: ${low_dia:,.2f} – ${high_dia:,.2f}"
            )

            precio_op = st.number_input(
                "Precio por accion ($)",
                min_value=0.01,
                value=round(cierre_dia, 2),
                step=0.01,
                format="%.2f",
            )
        except Exception:
            st.warning("Sin datos para la fecha seleccionada.")
            precio_op = st.number_input("Precio por accion ($)", min_value=0.01, value=100.0, step=0.01)
            low_dia, high_dia = 0.0, float("inf")

        cantidad_op = st.number_input("Cantidad", min_value=1, value=1, step=1)
        comision_op = st.number_input(
            "Comision (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.1
        ) / 100

    trans_preview = Transaccion(tipo_op.lower(), fecha_sel, precio_op, int(cantidad_op), comision_op)
    total_estimado = trans_preview.calcular_total()
    comision_estimada = trans_preview.costo_comision()

    col_est1, col_est2, col_est3 = st.columns(3)
    col_est1.metric("Total estimado", f"${total_estimado:,.2f}")
    col_est2.metric("Comision estimada", f"${comision_estimada:,.2f}")

    if tipo_op == "Compra":
        col_est3.metric("Capital restante", f"${port.capital - total_estimado:,.2f}")
    else:
        col_est3.metric("Capital tras venta", f"${port.capital + total_estimado:,.2f}")

    ejecutar = st.button(
        f"Ejecutar {tipo_op} — {int(cantidad_op)} {ticker_sel}",
        type="primary",
        use_container_width=True,
    )

    if ejecutar:
        if tipo_op == "Compra":
            exito = port.agregar_accion(acc_sel, fecha_sel, precio_op, int(cantidad_op), comision_op)
        else:
            exito = port.vender_accion(ticker_sel, fecha_sel, precio_op, int(cantidad_op), comision_op)

        if exito:
            registro = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Fecha": fecha_sel.strftime("%Y-%m-%d"),
                "Tipo": tipo_op,
                "Ticker": ticker_sel,
                "Cantidad": int(cantidad_op),
                "Precio": f"${precio_op:,.2f}",
                "Total": f"${total_estimado:,.2f}",
                "Comision": f"${comision_estimada:,.2f}",
            }
            guardar_operacion(registro)
            st.session_state.log_operaciones.append(registro)
            st.success(f"{tipo_op} ejecutada: {int(cantidad_op)} {ticker_sel} @ ${precio_op:,.2f}")
        else:
            st.error(f"{tipo_op} fallida. Verifica precio (rango ${low_dia:,.2f}–${high_dia:,.2f}) y capital.")

        st.rerun()

    if st.session_state.log_operaciones:
        st.subheader("Historial de operaciones")

        df_log = pd.DataFrame(st.session_state.log_operaciones)
        st.dataframe(df_log, use_container_width=True, hide_index=True)

        with open(ARCHIVO_OPERACIONES, "rb") as f:
            st.download_button(
                label="Descargar operaciones.csv",
                data=f,
                file_name="operaciones.csv",
                mime="text/csv",
            )

        st.subheader("Resumen")
        col_r1, col_r2, col_r3, col_r4, col_r5, col_r6 = st.columns(6)
        valor_acc_now = sum(a.precio_actual() * a.cantidad for a in port.acciones.values())
        valor_rf_now = sum(rf.valor_actual() for rf in port.renta_fija)
        valor_total_now = port.capital + valor_acc_now + valor_rf_now
        renta_now = ((valor_total_now - capital_inicial) / capital_inicial) * 100

        col_r1.metric("Capital disponible", f"${port.capital:,.2f}")
        col_r2.metric("Valor acciones", f"${valor_acc_now:,.2f}")
        col_r3.metric("Valor renta fija", f"${valor_rf_now:,.2f}")
        col_r4.metric("Dividendos", f"${port.dividendos_totales:,.2f}")
        col_r5.metric("Comisiones", f"${port.comisiones_totales:,.2f}")
        col_r6.metric("Rentabilidad", f"{renta_now:.2f}%")
