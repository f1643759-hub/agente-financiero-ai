import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Agente Financiero Inteligente", layout="wide")

# =====================================================================
# 1. ARQUITECTURA DE MEMORIA Y AUTO-APRENDIZAJE (SQLite3)
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

def bucle_aprendizaje_autonomo():
    conn = sqlite3.connect('agente_financiero.db')
    cursor = conn.cursor()
    
    df_radar = pd.read_sql_query("SELECT * FROM radar_inversiones WHERE evaluado = 0", conn)
    cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
    roe_act, margen_act, vol_act = cursor.fetchone()
    
    aciertos = 0
    errores = 0
    
    if not df_radar.empty:
        for _, row in df_radar.iterrows():
            ticker = row['ticker']
            p_entrada = row['precio_entrada']
            try:
                t_obj = yf.Ticker(ticker)
                p_actual = t_obj.history(period="1d")['Close'].iloc[-1]
                rendimiento = ((p_actual - p_entrada) / p_entrada) * 100
                
                if rendimiento < -4.0:
                    errores += 1
                elif rendimiento > 4.0:
                    aciertos += 1
                    
                cursor.execute("UPDATE radar_inversiones SET evaluado = 1 WHERE id = ?", (row['id'],))
            except:
                continue
                
    if errores > aciertos:
        nuevo_roe = min(roe_act + 0.02, 0.25)
        nuevo_margen = min(margen_act + 2.5, 35.0)
        nuevo_vol = min(vol_act + 0.1, 1.8)
        cursor.execute("INSERT INTO configuracion_filtros (roe_minimo, margen_seguridad, aceleracion_volumen) VALUES (?, ?, ?)",
                       (nuevo_roe, nuevo_margen, nuevo_vol))
        msg = f"🧠 Optimización Autónoma Completa: Filtros ajustados (ROE Mín: {nuevo_roe*100:.1f}%, Margen Mín: {nuevo_margen:.1f}%)."
    else:
        msg = "✅ El balance de asertividad matemática es óptimo bajo las condiciones actuales de mercado."
        
    conn.commit()
    conn.close()
    return msg

inicializar_cerebro_agente()

conn = sqlite3.connect('agente_financiero.db')
cursor = conn.cursor()
cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
filtro_roe, filtro_margen, filtro_volumen = cursor.fetchone()
conn.close()

# =====================================================================
# 2. PANEL LATERAL DE CONTROL COGNITIVO
# =====================================================================
st.sidebar.markdown("### 🧠 Filtros Calibrados de la IA")
st.sidebar.metric("Exigencia ROE Mínimo", f"{filtro_roe * 100:.1f}%")
st.sidebar.metric("Margen de Seguridad Mín.", f"{filtro_margen:.1f}%")
st.sidebar.metric("Aceleración de Volumen Mín.", f"{filtro_volumen:.2f}x")

# =====================================================================
# 3. INTERFAZ GRÁFICA PRINCIPAL
# =====================================================================
st.title("🤖 Agente IA Financiero Profesional Autónomo")
st.markdown("### Escáner Global, Rotación de Sectores y Rastreo de Flujos Dinámicos")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Rastreador de Flujos y Sectores", "🌍 Escáner de Índices Tradicional", "🔍 Consulta Manual"])

# PESTAÑA 1: NUEVO ESCÁNER DE ENTRADAS DE CAPITAL Y ROTACIÓN SECTORIAL
with tab1:
    st.subheader("📡 Monitor de Flujos de Capital y Rotación Macroeconómica")
    st.write("El agente analizará los activos institucionales líderes para rastrear el volumen en dólares inyectado hoy y mapear hacia dónde está migrando el dinero.")
    
    if st.button("🔍 Escanear Rotación de Capital Global", key="btn_flujos"):
        # Pool maestro representativo de los principales sectores económicos globales
        pool_maestro = {
            "AAPL": "Tecnología / Hardware", "MSFT": "Tecnología / Software", "NVDA": "Semiconductores", 
            "AVGO": "Semiconductores", "GOOGL": "Servicios de Comunicación", "META": "Servicios de Comunicación",
            "AMZN": "Consumo Cíclico", "TSLA": "Automotriz / Energía", "COST": "Consumo Defensivo",
            "WMT": "Consumo Defensivo", "JPM": "Financiero / Banca", "BAC": "Financiero / Banca",
            "XOM": "Energía / Petróleo", "CVX": "Energía / Petróleo", "LLY": "Salud / Farmacéutica",
            "JNJ": "Salud / Farmacéutica", "CAT": "Industrial", "GE": "Industrial",
            "CCJ": "Energía Nuclear / Uranio", "OKLO": "Energía Nuclear / Innovación", 
            "NU": "Fintech / Neobancos", "SQ": "Fintech / Pagos"
        }
        
        datos_flujo = []
        progreso_f = st.progress(0)
        total_activos = len(pool_maestro)
        
        for idx, (ticker, sector) in enumerate(pool_maestro.items()):
            try:
                acc = yf.Ticker(ticker)
                inf = acc.info
                
                precio = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                vol_hoy = inf.get('volume', 0) or 0
                vol_prom = inf.get('averageVolume', 1) or 1
                
                if precio > 0 and vol_hoy > 0:
                    # Dinero en circulación hoy en este activo (Precio * Volumen)
                    capital_movilizado = precio * vol_hoy
                    anomalia_volumen = vol_hoy / vol_prom
                    
                    datos_flujo.append({
                        "Ticker": ticker,
                        "Empresa": inf.get('longName', ticker),
                        "Sector": sector,
                        "Precio": precio,
                        "Volumen Hoy": vol_hoy,
                        "Anomalía Flujo": anomalia_volumen,
                        "Capital Efectivo (USD)": capital_movilizado
                    })
            except:
                pass
            progreso_f.progress((idx + 1) / total_activos)
            
        if datos_flujo:
            df_flujo = pd.DataFrame(datos_flujo)
            
            # --- 1. ACCIONES CON MAYOR ENTRADA DE CAPITAL ---
            st.markdown("### 🔝 Top Acciones con Mayor Inyección Financiera Directa")
            st.write("Ordenadas por volumen total en dólares transaccionados en la sesión actual:")
            
            df_top_cap = df_flujo.sort_values(by="Capital Efectivo (USD)", ascending=False).head(8)
            
            # Formatear la visualización para el usuario de manera profesional
            df_mostrar_top = df_top_cap.copy()
            df_mostrar_top["Capital Efectivo (USD)"] = df_mostrar_top["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
            df_mostrar_top["Precio"] = df_mostrar_top["Precio"].map(lambda x: f"${x:.2f}")
            df_mostrar_top["Anomalía Flujo"] = df_mostrar_top["Anomalía Flujo"].map(lambda x: f"{x:.2f}x")
            
            st.dataframe(df_mostrar_top[["Ticker", "Empresa", "Sector", "Precio", "Anomalía Flujo", "Capital Efectivo (USD)"]], use_container_width=True)
            
            # --- 2. ACCIONES CON ANOMALÍAS DE VOLUMEN (Corto Plazo / Rupturas) ---
            st.markdown("### 🚨 Alertas de Volumen Súbito (Institucionales Comprando en Masa)")
            st.write(f"Acciones cuyo volumen actual supera el promedio habitual por más de **{filtro_volumen}x**:")
            
            df_anomalias = df_flujo[df_flujo["Anomalía Flujo"] >= filtro_volumen].sort_values(by="Anomalía Flujo", ascending=False)
            
            if not df_anomalias.empty:
                df_mostrar_anom = df_anomalias.copy()
                df_mostrar_anom["Capital Efectivo (USD)"] = df_mostrar_anom["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
                df_mostrar_anom["Precio"] = df_mostrar_anom["Precio"].map(lambda x: f"${x:.2f}")
                df_mostrar_anom["Anomalía Flujo"] = df_mostrar_anom["Anomalía Flujo"].map(lambda x: f"{x:.2f}x")
                st.dataframe(df_mostrar_anom[["Ticker", "Empresa", "Sector", "Precio", "Anomalía Flujo", "Capital Efectivo (USD)"]], use_container_width=True)
            else:
                st.info("Ningún activo presenta una anomalía crítica de volumen en este preciso instante.")
            
            # --- 3. ANÁLISIS DE MIGRACIÓN SECTORIAL ---
            st.markdown("### 🌍 ¿Hacia dónde está migrando el dinero? (Análisis por Sectores)")
            st.write("Consolidación del flujo de dinero institucional agrupado por industrias:")
            
            df_sectores = df_flujo.groupby("Sector").agg({
                "Capital Efectivo (USD)": "sum",
                "Anomalía Flujo": "mean"
            }).reset_index()
            
            df_sectores = df_sectores.sort_values(by="Capital Efectivo (USD)", ascending=False)
            
            # Formatear tabla sectorial
            df_sectores_show = df_sectores.copy()
            df_sectores_show["Capital Efectivo (USD)"] = df_sectores_show["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
            df_sectores_show["Anomalía Flujo"] = df_sectores_show["Anomalía Flujo"].map(lambda x: f"{x:.2f}x (Promedio)")
            
            st.dataframe(df_sectores_show, use_container_width=True)
            
            # Dictamen del agente sobre la rotación
            top_sector = df_sectores.iloc[0]["Sector"]
            st.success(f"🧠 **Dictamen del Agente sobre Flujo Macro:** El dinero institucional está concentrándose con mayor fuerza en el sector **{top_sector}**. Busca oportunidades individuales dentro de este sector en la pestaña de consulta manual.")
        else:
            st.error("No se pudieron recopilar métricas de flujo en este momento. Revisa tu conexión de red.")

# PESTAÑA 2: ESCÁNER TRADICIONAL POR ÍNDICES
with tab2:
    st.subheader("🛰️ Análisis de Índices y Extracción Automatizada")
    if st.button("🚀 Ejecutar Escáner Global por Índices", key="btn_escaneo"):
        mercados_mundiales = {
            "S&P 500 (EE.UU)": {"simbolo": "^GSPC", "pool": ["AAPL", "MSFT", "AMZN", "NVDA", "JPM", "GOOGL"]},
            "NASDAQ 100 (EE.UU)": {"simbolo": "^IXIC", "pool": ["META", "TSLA", "AVGO", "COST", "NFLX"]},
            "EURO STOXX 50 (Europa)": {"simbolo": "^STOXX50E", "pool": ["ASML", "MC.PA", "SAP", "SIE.DE", "OR.PA"]},
            "IBOVESPA (LatAm / Brasil)": {"simbolo": "^BVSP", "pool": ["VALE3.SA", "PETR4.SA", "ITUB4.SA", "ABEV3.SA"]}
        }
        
        tabla_macro = []
        oportunidades_corto = []
        oportunidades_largo = []
        
        progreso = st.progress(0)
        total_mercados = len(mercados_mundiales)
        
        for idx, (nombre_m, config) in enumerate(mercados_mundiales.items()):
            try:
                ind_obj = yf.Ticker(config["simbolo"])
                hist_ind = ind_obj.history(period="5d")
                if len(hist_ind) >= 2:
                    p_cierre = hist_ind['Close'].iloc[-1]
                    var_diaria = ((hist_ind['Close'].iloc[-1] - hist_ind['Close'].iloc[-2]) / hist_ind['Close'].iloc[-2]) * 100
                    tabla_macro.append({
                        "Mercado Global": nombre_m, "Puntos/Nivel": f"{p_cierre:,.2f}",
                        "Variación Diaria": f"{var_diaria:+.2f}%", "Sesgo de Mercado": "🟢 Bullish" if var_diaria > 0 else "🔴 Bearish"
                    })
                
                for ticker in config["pool"]:
                    try:
                        acc_obj = yf.Ticker(ticker)
                        inf = acc_obj.info
                        hist_acc = acc_obj.history(period="5d")
                        px = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                        if px == 0: continue
                        
                        vol_hoy = inf.get('volume', 1) or 1
                        vol_prom = inf.get('averageVolume', 1) or 1
                        ratio_vol = vol_hoy / vol_prom
                        
                        if ratio_vol >= filtro_volumen:
                            ret_5d = ((hist_acc['Close'].iloc[-1] - hist_acc['Close'].iloc[0]) / hist_acc['Close'].iloc[0]) * 100 if len(hist_acc) >= 2 else 0
                            oportunidades_corto.append({
                                "Ticker": ticker, "Empresa": inf.get('longName', ticker), "Precio": f"${px:.2f}",
                                "Aceleración Flujo": f"{ratio_vol:.2f}x", "Rendimiento 5D": f"{ret_5d:+.2f}%"
                            })
                        
                        roe = inf.get('returnOnEquity', 0)
                        eps = inf.get('trailingEps', 0)
                        growth = inf.get('earningsGrowth', 0.05) or 0.05
                        if growth <= 0: growth = 0.05
                        
                        if roe >= filtro_roe and eps > 0:
                            v_intrinseco = eps * (8.5 + (2 * (growth * 100)))
                            margen_s = ((v_intrinseco - px) / v_intrinseco) * 100 if v_intrinseco > 0 else 0
                            if margen_s >= filtro_margen:
                                oportunidades_largo.append({
                                    "Ticker": ticker, "Empresa": inf.get('longName', ticker), "Precio Actual": f"${px:.2f}",
                                    "Valor Estimado": f"${v_intrinseco:.2f}", "Margen Seguridad": f"{margen_s:.1f}%", "ROE": f"{roe*100:.1f}%"
                                })
                    except:
                        continue
            except:
                pass
            progreso.progress((idx + 1) / total_mercados)
            
        st.markdown("#### 📊 Estado de los Índices Mundiales")
        st.dataframe(pd.DataFrame(tabla_macro), use_container_width=True)
        
        c_izq, c_der = st.columns(2)
        with c_izq:
            st.success("⏳ Oportunidades de Corto Plazo (Momentum)")
            if oportunidades_corto: st.dataframe(pd.DataFrame(oportunidades_corto), use_container_width=True)
            else: st.write("Sin anomalías detectadas.")
        with c_der:
            st.info("🧱 Oportunidades de Largo Plazo (Valor)")
            if oportunidades_largo: st.dataframe(pd.DataFrame(oportunidades_largo), use_container_width=True)
            else: st.write("Sin activos infravalorados bajo los filtros actuales.")

    st.markdown("---")
    st.subheader("⚙️ Panel de Auto-Mejoramiento")
    if st.button("🔄 Ejecutar Bucle de Entrenamiento Automático"):
        res_leccion = bucle_aprendizaje_autonomo()
        st.success(res_leccion)

# PESTAÑA 3: CONSULTA MANUAL INDIVIDUAL
with tab3:
    st.subheader("🔍 Auditoría Manual a Demanda")
    ticker_usuario = st.text_input("Ingresa el Ticker del activo:", "NU").strip().upper()
    
    if st.button("⚡ Auditar Activo"):
        with st.spinner(f"Analizando {ticker_usuario}..."):
            try:
                asset = yf.Ticker(ticker_usuario)
                inf = asset.info
                px = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                if px == 0:
                    st.error("No se pudo hallar información de cotización.")
                else:
                    st.markdown(f"### 🏢 {inf.get('longName', ticker_usuario)} — `${px:.2f}`")
                    roe = inf.get('returnOnEquity', 0)
                    eps = inf.get('trailingEps', 0)
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    if growth <= 0: growth = 0.05
                    
                    v_intrinseco = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    margen_s = ((v_intrinseco - px) / v_intrinseco) * 100 if v_intrinseco > 0 else 0
                    
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    ratio_vol = vol_hoy / vol_prom
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("ROE", f"{roe * 100:.2f}%", f"Mín: {filtro_roe*100:.1f}%")
                    col2.metric("Valor Justo", f"${v_intrinseco:.2f}")
                    col3.metric("Margen Seguridad", f"{margen_s:.1f}%", f"Mín: {filtro_margen:.1f}%")
                    col4.metric("Inyección Flujo", f"{ratio_vol:.2f}x", f"Mín: {filtro_volumen:.2f}x")
            except Exception as e:
                st.error(f"Error: {e}")
