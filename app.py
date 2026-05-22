import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

# Configuración de pantalla de alta densidad para análisis masivo
st.set_page_config(page_title="Agente Inteligente de Rotación y Valor", layout="wide", initial_sidebar_state="expanded")

# PARCHE DE SEGURIDAD CONTRA BLOQUEOS DE YAHOO FINANCE
import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

# =====================================================================
# 1. ARQUITECTURA DE BASE DE DATOS Y MEMORIA EVOLUTIVA
# =====================================================================
def inicializar_cerebro_agente():
    conn = sqlite3.connect('agente_financiero.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS radar_inversiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_registro TEXT,
            ticker TEXT,
            precio_entrada REAL,
            stop_loss REAL,
            take_profit REAL,
            tipo_estrategia TEXT,
            resultado TEXT DEFAULT 'PENDIENTE'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_filtros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roe_minimo REAL DEFAULT 0.15,
            margen_seguridad REAL DEFAULT 20.0,
            aceleracion_volumen REAL DEFAULT 1.10
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM configuracion_filtros")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion_filtros (roe_minimo, margen_seguridad, aceleracion_volumen) VALUES (0.15, 20.0, 1.10)")
    conn.commit()
    conn.close()

# =====================================================================
# MOTOR DE APRENDIZAJE AUTÓNOMO: REVISIÓN DE ERRORES Y OPTIMIZACIÓN
# =====================================================================
def optimizar_filtros_autonomo():
    """El agente analiza su historial técnico, detecta fallas y auto-ajusta sus filtros en la DB"""
    conn = sqlite3.connect('agente_financiero.db')
    cursor = conn.cursor()
    
    # 1. Traer operaciones pendientes para evaluar cómo les fue en el mercado real
    cursor.execute("SELECT id, ticker, precio_entrada, stop_loss, take_profit FROM radar_inversiones WHERE resultado = 'PENDIENTE'")
    pendientes = cursor.fetchall()
    
    cambios_realizados = False
    
    for op_id, ticker, entrada, sl, tp in pendientes:
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="5d")
            if hist.empty: continue
            
            precio_maximo = hist['High'].max()
            precio_minimo = hist['Low'].min()
            
            # Verificar si tocó el Stop Loss (Error) o el Take Profit (Acierto)
            if precio_minimo <= sl:
                cursor.execute("UPDATE radar_inversiones SET resultado = 'FALLIDA' WHERE id = ?", (op_id,))
                cambios_realizados = True
            elif precio_maximo >= tp:
                cursor.execute("UPDATE radar_inversiones SET resultado = 'EXITOSA' WHERE id = ?", (op_id,))
                cambios_realizados = True
        except:
            pass
            
    # 2. Analizar métricas de rendimiento para reconfigurar los parámetros algorítmicos
    cursor.execute("SELECT resultado FROM radar_inversiones WHERE resultado IN ('EXITOSA', 'FALLIDA') ORDER BY id DESC LIMIT 10")
    historial = [r[0] for r in cursor.fetchall()]
    
    if len(historial) >= 3: # Necesita una muestra mínima para aprender de sus rachas
        exitosas = historial.count('EXITOSA')
        total = len(historial)
        tasa_acierto = exitosas / total
        
        # Leer filtros actuales
        cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
        curr_roe, curr_margen, curr_vol = cursor.fetchone()
        
        # Bucle de retroalimentación recursivo
        if tasa_acierto < 0.60:
            # APRENDIZAJE POR ERROR: Si el agente está fallando mucho, se vuelve más estricto y defensivo
            nuevo_roe = min(curr_roe + 0.02, 0.25)
            nuevo_margen = min(curr_margen + 2.5, 35.0)
            nuevo_vol = min(curr_vol + 0.1, 1.5)
            cursor.execute("INSERT INTO configuracion_filtros (roe_minimo, margen_seguridad, aceleracion_volumen) VALUES (?, ?, ?)", 
                           (nuevo_roe, nuevo_margen, nuevo_vol))
        elif tasa_acierto >= 0.80:
            # RECOMPENSA DE EFICIENCIA: Si el mercado está limpio y ganando, flexibiliza filtros para capturar más trades
            nuevo_roe = max(curr_roe - 0.01, 0.10)
            nuevo_margen = max(curr_margen - 1.5, 15.0)
            nuevo_vol = max(curr_vol - 0.05, 1.0)
            cursor.execute("INSERT INTO configuracion_filtros (roe_minimo, margen_seguridad, aceleracion_volumen) VALUES (?, ?, ?)", 
                           (nuevo_roe, nuevo_margen, nuevo_vol))
            
    conn.commit()
    conn.close()

# Ejecución del núcleo del cerebro antes de renderizar la app
inicializar_cerebro_agente()
optimizar_filtros_autonomo()

# Cargar los filtros inteligentes optimizados de manera dinámica desde la base de datos corregida
conn = sqlite3.connect('agente_financiero.db')
cursor = conn.cursor()
cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
filtro_roe, filtro_margen, filtro_volumen = cursor.fetchone()
conn.close()

# Pool Optimizado y Ultra-Estable (Grandes Líderes, Uranio, Fintech y Crecimiento)
POOL_ACCIONES = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "JPM", "XOM", "LLY", "AVGO", 
    "TSLA", "COST", "WMT", "BRK-B", "PG", "CCJ", "OKLO", "NU", "SQ", "AMD"
]

ETFS_ROTACION = {
    "Líder de Mercado (S&P 500)": "SPY",
    "Tecnología y Crecimiento (NASDAQ 100)": "QQQ",
    "Semiconductores e IA (SMH)": "SMH",
    "Energía Nuclear y Uranio (URNM)": "URNM",
    "Sector Financiero y Banca (XLF)": "XLF",
    "Bienes de Consumo Discrecional (XLY)": "XLY",
    "Cuidado de la Salud e Innovación (XLV)": "XLV",
    "Sector Refugio: Consumo Defensivo (XLP)": "XLP",
    "Sector Refugio: Energía Fósil (XLE)": "XLE"
}

# =====================================================================
# INTERFAZ GRÁFICA PRINCIPAL
# =====================================================================
st.sidebar.markdown("### 🧠 Filtros Inteligentes Dinámicos")
st.sidebar.write("El agente modifica estos valores de forma autónoma analizando sus aciertos y errores históricos.")
st.sidebar.metric("Rentabilidad Mínima (ROE)", f"{filtro_roe * 100:.1f}%")
st.sidebar.metric("Margen de Seguridad Exigido", f"{filtro_margen:.1f}%")
st.sidebar.metric("Inyección de Capital Mínima", f"{filtro_volumen:.2f}x")

# Panel visual de rendimiento de la memoria de la IA
conn = sqlite3.connect('agente_financiero.db')
cursor = conn.cursor()
cursor.execute("SELECT resultado, COUNT(*) FROM radar_inversiones GROUP BY resultado")
res_dict = dict(cursor.fetchall())
conn.close()

st.sidebar.markdown("### 📊 Memoria de Operaciones")
st.sidebar.text(f"✅ Exitosas: {res_dict.get('EXITOSA', 0)}")
st.sidebar.text(f"❌ Fallidas: {res_dict.get('FALLIDA', 0)}")
st.sidebar.text(f"⏳ Pendientes en mercado: {res_dict.get('PENDIENTE', 0)}")

st.title("🤖 Agente IA Macro-Fundamental Omnisciente")
st.markdown("### Escaneo Completo de Índices, Flujos de Rotación, Valor Intrínseco y Alertas de Inversión")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🛰️ ESCÁNER MAESTRO: Rotación de Capital Global",
    "🧱 ANÁLISIS VALOR: Radar de Descuento Largo Plazo",
    "🎯 CORTO PLAZO: Impulso, Flujos y Gestión Antierror"
])

# =====================================================================
# PESTAÑA 1: MATRIZ MACRO DE ROTACIÓN + COMPONENTES CON MÁS ACUMULACIÓN
# =====================================================================
with tab1:
    st.subheader("📡 ¿A dónde está migrando el dinero de las Manos Fuertes?")
    st.write("Analiza las variaciones de precio y las inyecciones de volumen en los grandes ETFs para saber en qué industrias están acumulando posiciones las instituciones.")

    if st.button("🔍 Rastrear Migración de Capital Global", key="btn_macro_global"):
        analisis_macro = []
        barra_macro = st.progress(0)
        
        with st.spinner("Midiendo flujos monetarios líquidos..."):
            for idx, (nombre, ticker) in enumerate(ETFS_ROTACION.items()):
                try:
                    tk = yf.Ticker(ticker)
                    hist = tk.history(period="5d")
                    
                    if len(hist) >= 2:
                        var_diaria = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                        vol_ayer = hist['Volume'].iloc[-1]
                        vol_prom = hist['Volume'].mean()
                        fuerza_dinero = vol_ayer / vol_prom if vol_prom > 0 else 1.0
                        
                        tipo = "CRECIMIENTO / RIESGO" if ticker in ["SPY", "QQQ", "SMH", "URNM", "XLY"] else "REFUGIO / DEFENSA"
                        
                        analisis_macro.append({
                            "Índice / Sector": nombre,
                            "Ticker": ticker,
                            "Variación Diaria": var_diaria,
                            "Inyección de Dinero (Volumen)": fuerza_dinero,
                            "Naturaleza": tipo
                        })
                except:
                    pass
                barra_macro.progress((idx + 1) / len(ETFS_ROTACION))
                
        if analisis_macro:
            df_macro = pd.DataFrame(analisis_macro).sort_values(by="Inyección de Dinero (Volumen)", ascending=False)
            
            df_m_visual = df_macro.copy()
            df_m_visual["Variación Diaria"] = df_m_visual["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_m_visual["Inyección de Dinero (Volumen)"] = df_m_visual["Inyección de Dinero (Volumen)"].map(lambda x: f"{x:.2f}x volumen normal")
            
            st.dataframe(df_m_visual, use_container_width=True, hide_index=True)
            
            st.markdown("### 🚦 Alerta de Diagnóstico del Agente IA")
            ganador_macro = df_macro.iloc[0]
            ticker_ganador = ganador_macro["Ticker"]
            
            if ganador_macro["Naturaleza"] == "CRECIMIENTO / RIESGO":
                st.success(f"🚀 **ROTACIÓN HACIA EL RIESGO TRABAJANDO (Risk-On):** El capital institucional está migrando con fuerza hacia **{ganador_macro['Índice / Sector']} ({ticker_ganador})** con un volumen de **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x**. Buen entorno para buscar compras de momentum.")
            else:
                st.warning(f"⚠️ **ROTACIÓN DEFENSIVA DETECTADA (Risk-Off):** Las grandes ballenas se están protegiendo en **{ganador_macro['Índice / Sector']} ({ticker_ganador})**, inyectando **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x** de volumen normal. Reduce riesgos en el corto plazo.")
            
            componentes_etf = {
                "SPY": ["AAPL", "MSFT", "AMZN", "META", "BRK-B"],
                "QQQ": ["AAPL", "MSFT", "NVDA", "AVGO", "META"],
                "SMH": ["NVDA", "AVGO", "AMD", "TSM", "INTC"],
                "URNM": ["CCJ", "UUUU", "NXE", "SMR", "DNN"],
                "XLF": ["JPM", "BRK-B", "GS", "MS", "BAC"],
                "XLY": ["AMZN", "TSLA", "HD", "NKE", "MCD"],
                "XLV": ["LLY", "UNH", "JNJ", "MRK", "ABV"],
                "XLP": ["PG", "COST", "WMT", "KO", "PEP"],
                "XLE": ["XOM", "CVX", "COP", "EOG", "SLB"]
            }
            
            acciones_a_escanear = componentes_etf.get(ticker_ganador, ["AAPL", "MSFT", "NVDA", "BRK-B", "JPM"])
            
            st.markdown(f"### 🔍 Escaneo de Acumulación Interna: Componentes Líderes de {ticker_ganador}")
            
            analisis_componentes = []
            barra_comp = st.progress(0)
            
            for c_idx, c_ticker in enumerate(acciones_a_escanear):
                try:
                    c_tk = yf.Ticker(c_ticker)
                    c_hist = c_tk.history(period="5d")
                    if len(c_hist) >= 2:
                        c_var = ((c_hist['Close'].iloc[-1] - c_hist['Close'].iloc[-2]) / c_hist['Close'].iloc[-2]) * 100
                        c_vol_hoy = c_hist['Volume'].iloc[-1]
                        c_vol_prom = c_hist['Volume'].mean()
                        c_fuerza = c_vol_hoy / c_vol_prom if c_vol_prom > 0 else 1.0
                        
                        analisis_componentes.append({
                            "Acción": c_ticker,
                            "Variación Diaria": c_var,
                            "Fuerza de Acumulación (Volumen)": c_fuerza
                        })
                except:
                    pass
                barra_comp.progress((c_idx + 1) / len(acciones_a_escanear))
                
            if analisis_componentes:
                df_comp = pd.DataFrame(analisis_componentes).sort_values(by="Fuerza de Acumulación (Volumen)", ascending=False)
                df_c_visual = df_comp.copy()
                df_c_visual["Variación Diaria"] = df_c_visual["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
                df_c_visual["Fuerza de Acumulación (Volumen)"] = df_c_visual["Fuerza de Acumulación (Volumen)"].map(lambda x: f"{x:.2f}x volumen normal")
                
                st.dataframe(df_c_visual, use_container_width=True, hide_index=True)
                top_accion = df_comp.iloc[0]
                st.info(f"🐳 **DATO DE ALTA CONCENTRACIÓN:** Dentro del índice líder, la acción **{top_accion['Acción']}** presenta la mayor acumulación institucional activa con **{top_accion['Fuerza de Acumulación (Volumen)']:.2f}x** de volumen.")
