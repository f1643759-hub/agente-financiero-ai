import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import urllib.request

# --- TU CONFIGURACIÓN ORIGINAL ---
st.set_page_config(page_title="Agente Quant Inteligente", layout="wide", initial_sidebar_state="expanded")
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

# ... [AQUÍ VA TU CÓDIGO ORIGINAL DE LA BASE DE DATOS Y PROCESAR_APRENDIZAJE_AUTONOMO] ...
# (Mantén todo tu código original de la parte 1, 2 y 3 exactamente igual)

# --- AQUÍ ESTÁ EL CAMBIO EN LAS PESTAÑAS ---
# Busca esta línea en tu código y cámbiala por esta:
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🛰️ PESTAÑA 1: Rotación", 
    "🧱 PESTAÑA 2: Descuento", 
    "🎯 PESTAÑA 3: Small Caps", 
    "🔍 PESTAÑA 4: Consultor", 
    "🛡️ PESTAÑA 5: Riesgo", 
    "🪙 PESTAÑA 6: Crypto", 
    "🎲 PESTAÑA 7: Montecarlo"
])

# ... [AQUÍ VA TODO EL CÓDIGO DE TUS PESTAÑAS 1 A 6 EXACTAMENTE COMO LO TENÍAS] ...

# --- AL FINAL, PEGA ESTO ---
with tab7:
    st.subheader("🎲 Proyección Estocástica de Montecarlo")
    st.write("Simula 100 posibles trayectorias futuras del precio basadas en la volatilidad histórica real.")
    
    ticker_mc = st.text_input("Ingresa el Ticker para la Simulación:", value="NVDA", key="mc_input").strip().upper()
    dias_prediccion = st.slider("Días a proyectar:", 30, 365, 100)
    
    if st.button("🚀 Ejecutar Simulación Probabilística"):
        with st.spinner(f"Calculando escenarios para {ticker_mc}..."):
            try:
                data = yf.download(ticker_mc, period="1y", interval="1d")['Close']
                if not data.empty:
                    returns = np.log(1 + data.pct_change().dropna())
                    mu, sigma = returns.mean(), returns.std()
                    
                    last_price = data.iloc[-1]
                    simulations = np.zeros((dias_prediccion, 100))
                    
                    for i in range(100):
                        daily_returns = np.random.normal(mu, sigma, dias_prediccion)
                        simulations[:, i] = last_price * np.exp(np.cumsum(daily_returns))
                    
                    st.line_chart(pd.DataFrame(simulations))
                    
                    final_prices = simulations[-1, :]
                    st.metric("Precio Actual", f"${last_price:,.2f}")
                    c1, c2 = st.columns(2)
                    c1.metric("Escenario Optimista (Percentil 90)", f"${np.percentile(final_prices, 90):,.2f}")
                    c2.metric("Escenario Pesimista (Percentil 10)", f"${np.percentile(final_prices, 10):,.2f}")
                else:
                    st.error("No se encontraron datos.")
            except Exception as e:
                st.error(f"Error en la simulación: {e}")
