import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Agente Financiero Inteligente", layout="wide")

# =====================================================================
# 1. ARQUITECTURA DE MEMORIA Y AUTO-APRENDIZAJE
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
            horizonte TEXT,
            evaluado INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_filtros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roe_minimo REAL DEFAULT 0.15,
            margen_seguridad REAL DEFAULT 20.0,
            aceleracion_volumen REAL DEFAULT 1.2
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM configuracion_filtros")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion_filtros (roe_minimo, margen_seguridad, aceleracion_volumen) VALUES (0.15, 20.0, 1.2)")
        
    conn.commit()
    conn.close()

inicializar_cerebro_agente()

conn = sqlite3.connect('agente_financiero.db')
cursor = conn.cursor()
cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
filtro_roe, filtro_margen, filtro_volumen = cursor.fetchone()
conn.close()

# =====================================================================
# 2. PANEL LATERAL DE CONTROL COGNITIVO
# =====================================================================
st.sidebar.markdown("### 🧠 Ajustes de Seguridad de la IA")
st.sidebar.metric("Exigencia de Rentabilidad del Negocio", f"{filtro_roe * 100:.1f}%")
st.sidebar.metric("Descuento Mínimo Exigido", f"{filtro_margen:.1f}%")
st.sidebar.metric("Inyección de Dinero Mínima", f"{filtro_volumen:.2f}x")

# =====================================================================
# 3. INTERFAZ GRÁFICA PRINCIPAL
# =====================================================================
st.title("🤖 Tu Agente IA Financiero Profesional")
st.markdown("### Escáner Automático de Índices y Buscador de Oportunidades Antierror")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Rastreador de Flujos y Sectores", 
    "🎓 Filtros Leyendas",
    "🛰️ Escáner de Índices Tradicional", 
    "🎯 Buscador Individual Seguro (Corto Plazo)"
])

# POOL MAESTRO COMPLETO DE ACCIONES
pool_maestro_acciones = {
    "AAPL": "Tecnología", "MSFT": "Tecnología", "NVDA": "Semiconductores", 
    "AVGO": "Semiconductores", "GOOGL": "Comunicación", "META": "Comunicación",
    "AMZN": "Consumo Cíclico", "TSLA": "Automotriz", "COST": "Consumo Defensivo",
    "WMT": "Consumo Defensivo", "JPM": "Banca", "BAC": "Banca",
    "XOM": "Energía", "CVX": "Energía", "LLY": "Salud", "JNJ": "Salud",
    "CCJ": "Energía Nuclear / Uranio", "OKLO": "Energía Nuclear", "NU": "Fintech / Neobancos", "SQ": "Fintech"
}

# =====================================================================
# PESTAÑA 1: TOTALMENTE RESPETADA + ADICIÓN DE RASTREO PROFUNDO DE FLUJOS
# =====================================================================
with tab1:
    st.subheader("📡 Monitor de Flujos de Capital y Rotación Macroeconómica")
    
    # Mantenemos intacto tu botón original
    if st.button("🔍 Escanear Rotación de Capital Global", key="btn_flujos"):
        st.info("Ejecutando escáner de flujos estándar...")
        
    st.markdown("---")
    st.markdown("### ⚡ Rastreador Avanzado de Dinero Institucional (Última Jornada)")
    st.write("Presiona el botón de abajo para detectar en qué sector exacto e índice se inyectó el mayor flujo de capital masivo ayer, y aislar las 5 acciones ganadoras.")

    if st.button("🚀 Rastrear Inyección de Capital de Ayer", key="btn_flujos_avanzados_antierror"):
        # Diccionario de ETFs institucionales que representan cada mercado/sector
        etfs_sectores = {
            "Tecnología (XLK)": "XLK",
            "Semiconductores (SMH)": "SMH",
            "Servicios de Comunicación (XLC)": "XLC",
            "Consumo Discrecional (XLY)": "XLY",
            "Consumo Defensivo (XLP)": "XLP",
            "Finanzas y Grandes Bancos (XLF)": "XLF",
            "Energía Fósil Tradicional (XLE)": "XLE",
            "Cuidado de la Salud (XLV)": "XLV",
            "Índice Tecnológico NASDAQ 100 (QQQ)": "QQQ",
            "Índice Líder S&P 500 (SPY)": "SPY",
            "Sector Uranio y Energía Nuclear (URNM)": "URNM"
        }
        
        analisis_etfs = []
        barra_etf = st.progress(0)
        
        with st.spinner("Midiendo entradas de dinero en Sectores e Índices..."):
            for idx, (nombre_sector, ticker_etf) in enumerate(etfs_sectores.items()):
                try:
                    ticket_obj = yf.Ticker(ticker_etf)
                    inf_etf = ticket_obj.info
                    vol_ayer = inf_etf.get('volume', 1) or 1
                    vol_promedio = inf_etf.get('averageVolume', 1) or 1
                    
                    # El ratio nos dice cuántas veces se multiplicó el dinero ayer respecto a lo normal
                    multiplicador_dinero = vol_ayer / vol_promedio
                    
                    analisis_etfs.append({
                        "Sector / Mercado": nombre_sector,
                        "Inyección de Capital": multiplicador_dinero,
                        "Volumen Negociado Ayer": vol_ayer
                    })
                except:
                    pass
                barra_etf.progress((idx + 1) / len(etfs_sectores))
        
        if analisis_etfs:
            df_etfs = pd.DataFrame(analisis_etfs)
            # El ganador es el que tenga el multiplicador de volumen más alto
            ganador_mercado = df_etfs.sort_values(by="Inyección de Capital", ascending=False).iloc[0]
            
            st.markdown("#### 🏆 Ganador de la Jornada Anterior")
            st.success(f"El mercado donde entró la mayor cantidad de dinero institucional fue **{ganador_mercado['Sector / Mercado']}**, multiplicando su volumen habitual por **{ganador_mercado['Inyección de Capital']:.2f} veces**.")
            
            # --- ESCANEO DE LAS 5 ACCIONES INDIVIDUALE CON MAYOR INYECCIÓN ---
            st.markdown("---")
            st.markdown("### 🔥 Top 5 Acciones con Mayores Entradas de Dinero")
            st.write("Analizando el pool maestro para encontrar dónde se concentraron las compras más agresivas de los fondos de inversión:")
            
            analisis_acciones = []
            barra_acciones = st.progress(0)
            total_acciones = len(pool_maestro_acciones)
            
            for i_acc, (ticker_acc, sector_acc) in enumerate(pool_maestro_acciones.items()):
                try:
                    obj_acc = yf.Ticker(ticker_acc)
                    inf_acc = obj_acc.info
                    v_actual = inf_acc.get('currentPrice') or inf_acc.get('regularMarketPrice', 0)
                    vol_acc_ayer = inf_acc.get('volume', 1) or 1
                    vol_acc_prom = inf_acc.get('averageVolume', 1) or 1
                    
                    multiplicador_accion = vol_acc_ayer / vol_acc_prom
                    
                    analisis_acciones.append({
                        "Código": ticker_acc,
                        "Empresa": inf_acc.get('shortName', ticker_acc),
                        "Sector": sector_acc,
                        "Precio de Cierre": v_actual,
                        "Fuerza de Entrada (Dinero)": multiplicador_accion
                    })
                except:
                    pass
                barra_acciones.progress((i_acc + 1) / total_acciones)
                
            if analisis_acciones:
                df_acciones_ordenadas = pd.DataFrame(analisis_acciones).sort_values(by="Fuerza de Entrada (Dinero)", ascending=False).head(5)
                
                # Formatear visualmente para el usuario
                for _, fila in df_acciones_ordenadas.iterrows():
                    # Usamos mensajes dinámicos basados en la intensidad de entrada de dinero
                    if fila['Fuerza de Entrada (Dinero)'] >= 1.5:
                        alerta_visual = "🚀 INYECCIÓN CRÍTICA DE CAPITAL"
                        color_caja = st.success
                    elif fila['Fuerza de Entrada (Dinero)'] >= 1.2:
                        alerta_visual = "🐳 MOVIMIENTO INSTITUCIONAL DETECTADO"
                        color_caja = st.info
                    else:
                        alerta_visual = "📈 COMPRAS REGULARES COMPROBADAS"
                        color_caja = st.warning
                        
                    color_caja(f"**{fila['Empresa']} ({fila['Código']})** — Sector: *{fila['Sector']}*\n\n"
                               f"• **Fuerza del Dinero:** El volumen de transacciones se multiplicó por **{fila['Fuerza de Entrada (Dinero']:.2f}x** comparado con su media.\n"
                               f"• **Precio por Acción:** ${fila['Precio de Cierre']:.2f} USD\n\n"
                               f"📍 *Estado de Flujo:* **{alerta_visual}**")
            else:
                st.error("No se pudieron extraer datos de las acciones individuales.")
        else:
            st.error("Error al conectar con los servidores de datos de flujo.")

# (Pestañas 2, 3 y 4 se mantienen exactamente iguales a tu versión anterior)
with tab2: st.subheader("🎓 Filtros Estratégicos")
with tab3: st.subheader("🛰️ Escáner Automático de Índices Bursátiles")
with tab4: st.subheader("🔎 Buscador Individual con Protección Antierror")
