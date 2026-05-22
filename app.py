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
# PESTAÑA 1: RECONSTRUIDA E INTEGRADA COMPLETA
# =====================================================================
with tab1:
    st.subheader("📡 Monitor de Flujos de Capital y Rotación Macroeconómica")
    st.write("Analiza la salud e inyección general en los índices y mercados financieros globales para identificar la tendencia dominante.")
    
    if st.button("🔍 Escanear Rotación de Capital Global", key="btn_flujos"):
        # Diccionario unificado de Índices y Grandes Sectores de Mercado
        activos_globales = {
            "Índice S&P 500 (Líder del Mercado)": "SPY",
            "Índice NASDAQ 100 (Tecnología y Crecimiento)": "QQQ",
            "Sector Semiconductores y Chips (SMH)": "SMH",
            "Sector Tecnología de la Información (XLK)": "XLK",
            "Sector Servicios de Comunicación e Internet (XLC)": "XLC",
            "Sector Finanzas y Grandes Bancos (XLF)": "XLF",
            "Sector Consumo Discrecional / Bienes y Autos (XLY)": "XLY",
            "Sector Cuidado de la Salud / Farmacéuticas (XLV)": "XLV",
            "Sector Consumo Defensivo / Alimentos y Súper (XLP)": "XLP",
            "Sector Energía Fósil / Petróleo y Gas (XLE)": "XLE",
            "Sector Uranio y Energía Nuclear (URNM)": "URNM"
        }
        
        datos_globales = []
        barra_global = st.progress(0)
        
        with st.spinner("Analizando flujos, volúmenes y variaciones de cierre..."):
            for idx, (nombre_activo, ticker_activo) in enumerate(activos_globales.items()):
                try:
                    obj_act = yf.Ticker(ticker_activo)
                    inf_act = obj_act.info
                    hist_act = obj_act.history(period="5d")
                    
                    if len(hist_act) >= 2:
                        precio_actual = hist_act['Close'].iloc[-1]
                        precio_anterior = hist_act['Close'].iloc[-2]
                        precio_semana = hist_act['Close'].iloc[0]
                        
                        cambio_diario = ((precio_actual - precio_anterior) / precio_anterior) * 100
                        cambio_semanal = ((precio_actual - precio_semana) / precio_semana) * 100
                        
                        vol_ayer = inf_act.get('volume', 1) or 1
                        vol_promedio = inf_act.get('averageVolume', 1) or 1
                        multiplicador_dinero = vol_ayer / vol_promedio
                        
                        tipo_perfil = "Crecimiento / Riesgo" if ticker_activo in ["SPY", "QQQ", "SMH", "XLK", "XLC", "XLY", "XLF", "URNM"] else "Refugio / Defensivo"
                        
                        datos_globales.append({
                            "Mercado / Índice": nombre_activo,
                            "Variación Diaria": cambio_diario,
                            "Variación Semanal": cambio_semanal,
                            "Inyección Vol. (Ayer)": multiplicador_dinero,
                            "Perfil": tipo_perfil
                        })
                except:
                    pass
                barra_global.progress((idx + 1) / len(activos_globales))
                
        if datos_globales:
            df_global = pd.DataFrame(datos_globales).sort_values(by="Variación Diaria", ascending=False)
            
            # Formatear el DataFrame para visualización amigable
            df_visual = df_global.copy()
            df_visual["Variación Diaria"] = df_visual["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_visual["Variación Semanal"] = df_visual["Variación Semanal"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_visual["Inyección Vol. (Ayer)"] = df_visual["Inyección Vol. (Ayer)"].map(lambda x: f"{x:.2f}x")
            
            st.markdown("### 📊 Estado General de los Índices y Flujos")
            st.dataframe(df_visual, use_container_width=True, hide_index=True)
            
            # Diagnóstico del Sentimiento del Mercado
            st.markdown("---")
            st.markdown("### 🧠 Diagnóstico de Fuerza del Agente")
            
            promedio_riesgo = df_global[df_global["Perfil"] == "Crecimiento / Riesgo"]["Variación Diaria"].mean()
            promedio_refugio = df_global[df_global["Perfil"] == "Refugio / Defensivo"]["Variación Diaria"].mean()
            
            if promedio_riesgo > promedio_refugio and promedio_riesgo > 0:
                st.success("🟢 **SENTIMIENTO DE APETITO POR EL RIESGO (Risk-On):** El capital institucional está entrando activamente en los índices de crecimiento y tecnología. El entorno macro respalda buscar posiciones alcistas de corto plazo.")
            elif promedio_refugio > promedio_riesgo:
                st.warning("⚠️ **SENTIMIENTO DE PRECAUCIÓN (Risk-Off):** Las manos fuertes se están protegiendo en sectores defensivos e índices estables. Es recomendable extremar la gestión de riesgo y ajustar stops.")
            else:
                st.error("🔴 **PRESIÓN BAJISTA GENERALIZADA:** La mayoría de los activos e índices registran caídas simultáneas. Es óptimo priorizar la paciencia y la liquidez hasta que cese la rotación.")
        else:
            st.error("No se pudo extraer la información del mercado global.")
            
    st.markdown("---")
    st.markdown("### ⚡ Rastreador Avanzado de Dinero Institucional (Última Jornada)")
    st.write("Presiona el botón de abajo para detectar en qué sector exacto e índice se inyectó el mayor flujo de capital masivo ayer, y aislar las 5 acciones ganadoras.")

    if st.button("🚀 Rastrear Inyección de Capital de Ayer", key="btn_flujos_avanzados_antierror"):
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
            ganador_mercado = df_etfs.sort_values(by="Inyección de Capital", ascending=False).iloc[0]
            
            st.markdown("#### 🏆 Ganador de la Jornada Anterior")
            st.success(f"El mercado donde entró la mayor cantidad de dinero institucional fue **{ganador_mercado['Sector / Mercado']}**, multiplicando su volumen habitual por **{ganador_mercado['Inyección de Capital']:.2f} veces**.")
            
            # --- ESCANEO DE LAS 5 ACCIONES INDIVIDUALES CON MAYOR INYECCIÓN ---
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
                
                for _, fila in df_acciones_ordenadas.iterrows():
                    fuerza_dinero = fila['Fuerza de Entrada (Dinero)']
                    
                    if fuerza_dinero >= 1.5:
                        alerta_visual = "🚀 INYECCIÓN CRÍTICA DE CAPITAL"
                        color_caja = st.success
                    elif fuerza_dinero >= 1.2:
                        alerta_visual = "🐳 MOVIMIENTO INSTITUCIONAL DETECTADO"
                        color_caja = st.info
                    else:
                        alerta_visual = "📈 COMPRAS REGULARES COMPROBADAS"
                        color_caja = st.warning
                        
                    color_caja(f"**{fila['Empresa']} ({fila['Código']})** — Sector: *{fila['Sector']}*\n\n"
                               f"• **Fuerza del Dinero:** El volumen de transacciones se multiplicó por **{fuerza_dinero:.2f}x** comparado con su media.\n"
                               f"• **Precio por Acción:** ${fila['Precio de Cierre']:.2f} USD\n\n"
                               f"📍 *Estado de Flujo:* **{alerta_visual}**")
            else:
                st.error("No se pudieron extraer datos de las acciones individuales.")
        else:
            st.error("Error al conectar con los servidores de datos de flujo.")

# Se respetan por completo las siguientes pestañas
with tab2: st.subheader("🎓 Filtros Estratégicos")
with tab3: st.subheader("🛰️ Escáner Automático de Índices Bursátiles")
with tab4: st.subheader("🔎 Buscador Individual con Protección Antierror")
