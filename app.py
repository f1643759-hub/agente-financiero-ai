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
st.markdown("### Escáner Global, Filosofías Value y Rastreo de Flujos")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Rastreador de Flujos y Sectores", 
    "🎓 Filtros Leyendas (Buffett, Lynch, Graham)",
    "🌍 Escáner de Índices Tradicional", 
    "🔍 Consulta Manual"
])

# POOL MAESTRO EXTENDIDO
pool_maestro_acciones = {
    "AAPL": "Tecnología / Hardware", "MSFT": "Tecnología / Software", "NVDA": "Semiconductores", 
    "AVGO": "Semiconductores", "GOOGL": "Servicios de Comunicación", "META": "Servicios de Comunicación",
    "AMZN": "Consumo Cíclico", "TSLA": "Automotriz / Energía", "COST": "Consumo Defensivo",
    "WMT": "Consumo Defensivo", "JPM": "Financiero / Banca", "BAC": "Financiero / Banca",
    "XOM": "Energía / Petróleo", "CVX": "Energía / Petróleo", "LLY": "Salud / Farmacéutica",
    "JNJ": "Salud / Farmacéutica", "CAT": "Industrial", "GE": "Industrial",
    "CCJ": "Energía Nuclear / Uranio", "OKLO": "Energía Nuclear / Innovación", 
    "NU": "Fintech / Neobancos", "SQ": "Fintech / Pagos", "GOOG": "Tecnología",
    "BRK-B": "Conglomerado Financiero", "PG": "Consumo Defensivo", "KO": "Consumo Defensivo",
    "BABA": "Comercio Electrónico", "TROW": "Gestión de Activos", "INTC": "Semiconductores"
}

# PESTAÑA 1: RASTREADOR DE FLUJOS, SECTORES Y SELECCIÓN DE MOMENTUM
with tab1:
    st.subheader("📡 Monitor de Flujos de Capital y Rotación Macroeconómica")
    st.write("El agente analizará los activos institucionales líderes para rastrear el volumen en dólares inyectado hoy y mapear hacia dónde está migrando el dinero.")
    
    if st.button("🔍 Escanear Rotación de Capital Global", key="btn_flujos"):
        datos_flujo = []
        progreso_f = st.progress(0)
        total_activos = len(pool_maestro_acciones)
        
        for idx, (ticker, sector) in enumerate(pool_maestro_acciones.items()):
            try:
                acc = yf.Ticker(ticker)
                inf = acc.info
                
                precio = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                vol_hoy = inf.get('volume', 0) or 0
                vol_prom = inf.get('averageVolume', 1) or 1
                
                if precio > 0 and vol_hoy > 0:
                    capital_movilizado = precio * vol_hoy
                    anomalia_volumen = vol_hoy / vol_prom
                    
                    datos_flujo.append({
                        "Ticker": ticker, "Empresa": inf.get('longName', ticker), "Sector": sector,
                        "Precio": precio, "Volumen Hoy": vol_hoy, "Anomalía Flujo": anomalia_volumen,
                        "Capital Efectivo (USD)": capital_movilizado
                    })
            except:
                pass
            progreso_f.progress((idx + 1) / total_activos)
            
        if datos_flujo:
            df_flujo = pd.DataFrame(datos_flujo)
            
            st.markdown("### 🔝 Top Acciones con Mayor Inyección Financiera Directa")
            df_top_cap = df_flujo.sort_values(by="Capital Efectivo (USD)", ascending=False).head(8)
            df_mostrar_top = df_top_cap.copy()
            df_mostrar_top["Capital Efectivo (USD)"] = df_mostrar_top["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
            df_mostrar_top["Precio"] = df_mostrar_top["Precio"].map(lambda x: f"${x:.2f}")
            df_mostrar_top["Anomalía Flujo"] = df_mostrar_top["Anomalía Flujo"].map(lambda x: f"{x:.2f}x")
            st.dataframe(df_mostrar_top[["Ticker", "Empresa", "Sector", "Precio", "Anomalía Flujo", "Capital Efectivo (USD)"]], use_container_width=True)
            
            st.markdown("### 🚨 Alertas de Volumen Súbito (Institucionales Comprando en Masa)")
            df_anomalias = df_flujo[df_flujo["Anomalía Flujo"] >= filtro_volumen].sort_values(by="Anomalía Flujo", ascending=False)
            if not df_anomalias.empty:
                df_mostrar_anom = df_anomalias.copy()
                df_mostrar_anom["Capital Efectivo (USD)"] = df_mostrar_anom["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
                df_mostrar_anom["Precio"] = df_mostrar_anom["Precio"].map(lambda x: f"${x:.2f}")
                df_mostrar_anom["Anomalía Flujo"] = df_mostrar_anom["Anomalía Flujo"].map(lambda x: f"{x:.2f}x")
                st.dataframe(df_mostrar_anom[["Ticker", "Empresa", "Sector", "Precio", "Anomalía Flujo", "Capital Efectivo (USD)"]], use_container_width=True)
            else:
                st.info("Ningún activo presenta una anomalía crítica de volumen en este preciso instante.")
            
            # --- ANÁLISIS DE MIGRACIÓN SECTORIAL ---
            st.markdown("### 🌍 ¿Hacia dónde está migrando el dinero? (Análisis por Sectores)")
            df_sectores = df_flujo.groupby("Sector").agg({"Capital Efectivo (USD)": "sum", "Anomalía Flujo": "mean"}).reset_index()
            df_sectores = df_sectores.sort_values(by="Capital Efectivo (USD)", ascending=False)
            df_sectores_show = df_sectores.copy()
            df_sectores_show["Capital Efectivo (USD)"] = df_sectores_show["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
            df_sectores_show["Anomalía Flujo"] = df_sectores_show["Anomalía Flujo"].map(lambda x: f"{x:.2f}x (Promedio)")
            st.dataframe(df_sectores_show, use_container_width=True)
            
            # EXTRAER EL SECTOR LÍDER Y SU ACCIÓN DE MEJOR MOMENTUM DE CORTO PLAZO
            top_sector = df_sectores.iloc[0]["Sector"]
            
            # Filtrar el dataframe original para quedarnos solo con las acciones del sector ganador
            df_acciones_top_sector = df_flujo[df_flujo["Sector"] == top_sector]
            
            # Identificar la acción con la mayor Anomalía de Flujo (mayor presión compradora/volumen relativo)
            accion_ganadora_raw = df_acciones_top_sector.sort_values(by="Anomalía Flujo", ascending=False).iloc[0]
            
            st.markdown("---")
            st.markdown(f"## ⚡ Alerta Alfa de Corto Plazo: {top_sector}")
            
            col_info, col_metric = st.columns([2, 1])
            with col_info:
                st.markdown(f"""
                El dinero institucional está concentrándose con mayor fuerza en el sector **{top_sector}**. 
                Evaluando las métricas internas de liquidez y velocidad de transacciones, la acción con la **mayor oportunidad operativa a corto plazo** dentro del sector caliente es:
                
                *   **Compañía:** {accion_ganadora_raw['Empresa']} (`{accion_ganadora_raw['Ticker']}`)
                *   **Precio de Cotización:** ${accion_ganadora_raw['Precio']:.2f}
                *   **Volumen Negociado Hoy:** {accion_ganadora_raw['Volumen Hoy']:,} acciones
                """)
            
            with col_metric:
                st.metric(
                    label=f"Presión de Flujo en {accion_ganadora_raw['Ticker']}", 
                    value=f"{accion_ganadora_raw['Anomalía Flujo']:.2f}x",
                    delta="Volumen Superior al Promedio"
                )
                
            st.success(f"🎯 **Sugerencia del Agente:** `{accion_ganadora_raw['Ticker']}` está liderando la carga de volumen en el sector más fuerte de la sesión. Es el candidato ideal para estrategias de trading de ruptura o momentum de corto plazo.")
        else:
            st.error("No se pudieron recopilar métricas de flujo.")

# PESTAÑA 2: FILTROS DE LEYENDAS CON MÍNIMO 10% DE GANANCIA
with tab2:
    st.subheader("🎓 Filtros Estratégicos Automatizados: Leyendas de Wall Street")
    st.write("Escanea activos bajo las métricas matemáticas exactas de tres de los inversores más exitosos del mundo, exigiendo un potencial de rendimiento del 10% en adelante.")
    
    horizonte_seleccionado = st.radio("Selecciona tu Horizonte Temporal Objetivo:", ["Corto Plazo (Momentum/Flujo de Caja)", "Largo Plazo (Valor Intrínseco Extendido)"], horizontal=True)

    if st.button("🚀 Escanear Acciones Bajo Filosofías Value", key="btn_leyendas"):
        resultados_maestros = []
        progreso_m = st.progress(0)
        total_m = len(pool_maestro_acciones)
        
        for idx, (ticker, sector) in enumerate(pool_maestro_acciones.items()):
            try:
                acc = yf.Ticker(ticker)
                inf = acc.info
                
                p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                if p_actual == 0: continue
                
                eps = inf.get('trailingEps', 0) or 0
                roe = inf.get('returnOnEquity', 0) or 0
                growth = inf.get('earningsGrowth', 0.05) or 0.05
                pe_ratio = inf.get('trailingPE', 999) or 999
                book_value = inf.get('bookValue', 0) or 0
                deuda_capital = inf.get('debtToEquity', 999) or 0
                
                # ALGORITMO 1: BENJAMIN GRAHAM
                es_graham = False
                p_justo_graham = 0
                potencial_graham = 0
                if eps > 0 and book_value > 0:
                    p_justo_graham = (22.5 * eps * book_value) ** 0.5
                    potencial_graham = ((p_justo_graham - p_actual) / p_actual) * 100
                    if potencial_graham >= 10.0 and deuda_capital < 150:
                        es_graham = True
                
                # ALGORITMO 2: WARREN BUFFETT
                es_buffett = False
                p_justo_buffett = 0
                potencial_buffett = 0
                if roe >= 0.15 and eps > 0:
                    p_justo_buffett = eps * (8.5 + (2 * (growth * 100)))
                    potencial_buffett = ((p_justo_buffett - p_actual) / p_actual) * 100
                    if potencial_buffett >= 10.0 and deuda_capital < 100:
                        es_buffett = True
                        
                # ALGORITMO 3: PETER LYNCH
                es_lynch = False
                potencial_lynch = 0
                peg_ratio = inf.get('pegRatio', 99) or 99
                if 0.1 < peg_ratio <= 1.2 and growth > 0:
                    p_objetivo_lynch = p_actual * (1.2 / peg_ratio)
                    potencial_lynch = ((p_objetivo_lynch - p_actual) / p_actual) * 100
                    if potencial_lynch >= 10.0:
                        es_lynch = True

                hist = acc.history(period="5d")
                vol_hoy = inf.get('volume', 1) or 1
                vol_prom = inf.get('averageVolume', 1) or 1
                aceleracion_vol = vol_hoy / vol_prom
                
                aplica_filtro = False
                target_rendimiento = 0
                maestro_asignado = []
                
                if es_graham: maestro_asignado.append("Benjamin Graham (Margen Neto)")
                if es_buffett: maestro_assigned.append("Warren Buffett (Moat / ROE)")
                if es_lynch: maestro_asignado.append("Peter Lynch (Crecimiento PEG)")
                
                if maestro_asignado:
                    target_rendimiento = max(potencial_graham, potencial_buffett, potencial_lynch)
                    
                    if "Corto Plazo" in horizonte_seleccionado:
                        var_5d = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100 if len(hist) >= 2 else 0
                        if aceleracion_vol > 1.0 or var_5d > 0:
                            aplica_filtro = True
                    else:
                        aplica_filtro = True
                        
                if aplica_filtro:
                    resultados_maestros.append({
                        "Ticker": ticker, "Empresa": inf.get('longName', ticker),
                        "Maestro Coincidente": ", ".join(maestro_asignado), "Precio Actual": f"${p_actual:.2f}",
                        "Ganancia Estimada Potencial": f"{target_rendimiento:+.2f}%", "PER": f"{pe_ratio:.1f}" if pe_ratio != 999 else "N/A",
                        "ROE": f"{roe*100:.1f}%", "Aceleración Flujo": f"{aceleracion_vol:.2f}x"
                    })
            except:
                pass
            progreso_m.progress((idx + 1) / total_m)
            
        if resultados_maestros:
            df_maestros = pd.DataFrame(resultados_maestros)
            st.success(f"🎯 Se encontraron {len(df_maestros)} acciones que cumplen las reglas de las leyendas.")
            st.dataframe(df_maestros, use_container_width=True)
        else:
            st.warning("Ninguna acción del pool califica bajo los filtros en esta sesión.")

# PESTAÑA 3: ESCÁNER TRADICIONAL POR ÍNDICES
with tab3:
    st.subheader("🛰️ Análisis de Índices y Extracción Automatizada")
    if st.button("🚀 Ejecutar Escáner Global por Índices", key="btn_escaneo"):
        mercados_mundiales = {
            "S&P 500 (EE.UU)": {"simbolo": "^GSPC", "pool": ["AAPL", "MSFT", "AMZN", "NVDA", "JPM", "GOOGL"]},
            "NASDAQ 100 (EE.UU)": {"simbolo": "^IXIC", "pool": ["META", "TSLA", "AVGO", "COST", "NFLX"]},
        }
        tabla_macro = []
        for nombre_m, config in mercados_mundiales.items():
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
            except:
                pass
        st.dataframe(pd.DataFrame(tabla_macro), use_container_width=True)

# PESTAÑA 4: CONSULTA MANUAL INDIVIDUAL
with tab4:
    st.subheader("🔍 Auditoría Manual a Demanda")
    ticker_usuario = st.text_input("Ingresa el Ticker del activo:", "NU").strip().upper()
    if st.button("⚡ Auditar Activo"):
        try:
            asset = yf.Ticker(ticker_usuario)
            inf = asset.info
            px = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
            st.markdown(f"### 🏢 {inf.get('longName', ticker_usuario)} — `${px:.2f}`")
        except Exception as e:
            st.error(f"Error: {e}")
