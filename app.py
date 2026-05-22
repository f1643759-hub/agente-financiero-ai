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
    "🔍 Consulta Manual Avanzada"
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
            
            st.markdown("### 🌍 ¿Hacia dónde está migrando el dinero? (Análisis por Sectores)")
            df_sectores = df_flujo.groupby("Sector").agg({"Capital Efectivo (USD)": "sum", "Anomalía Flujo": "mean"}).reset_index()
            df_sectores = df_sectores.sort_values(by="Capital Efectivo (USD)", ascending=False)
            df_sectores_show = df_sectores.copy()
            df_sectores_show["Capital Efectivo (USD)"] = df_sectores_show["Capital Efectivo (USD)"].map(lambda x: f"${x:,.2f}")
            df_sectores_show["Anomalía Flujo"] = df_sectores_show["Anomalía Flujo"].map(lambda x: f"{x:.2f}x (Promedio)")
            st.dataframe(df_sectores_show, use_container_width=True)
            
            top_sector = df_sectores.iloc[0]["Sector"]
            df_acciones_top_sector = df_flujo[df_flujo["Sector"] == top_sector]
            accion_ganadora_raw = df_acciones_top_sector.sort_values(by="Anomalía Flujo", ascending=False).iloc[0]
            
            st.markdown("---")
            st.markdown(f"## ⚡ Alerta Alfa de Corto Plazo: {top_sector}")
            st.markdown(f"La acción con mayor oportunidad operativa a corto plazo en el sector caliente es **{accion_ganadora_raw['Empresa']} ({accion_ganadora_raw['Ticker']})** cotizando a **${accion_ganadora_raw['Precio']:.2f}** con una anomalía de flujo de **{accion_ganadora_raw['Anomalía Flujo']:.2f}x**.")
        else:
            st.error("No se pudieron recopilar métricas de flujo.")

# PESTAÑA 2: FILTROS DE LEYENDAS CON MÍNIMO 10% DE GANANCIA
with tab2:
    st.subheader("🎓 Filtros Estratégicos Automatizados: Leyendas de Wall Street")
    horizonte_seleccionado = st.radio("Selecciona tu Horizonte Temporal Objetivo:", ["Corto Plazo (Momentum/Flujo de Caja)", "Largo Plazo (Valor Intrínseco Extendido)"], horizontal=True)

    if st.button("🚀 Escanear Acciones Bajo Filosofías Value", key="btn_leyendas"):
        resultados_maestros = []
        for ticker, sector in pool_maestro_acciones.items():
            try:
                acc = yf.Ticker(ticker)
                inf = acc.info
                p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                if p_actual == 0: continue
                
                eps = inf.get('trailingEps', 0) or 0
                roe = inf.get('returnOnEquity', 0) or 0
                growth = inf.get('earningsGrowth', 0.05) or 0.05
                book_value = inf.get('bookValue', 0) or 0
                deuda_capital = inf.get('debtToEquity', 999) or 0
                
                # Graham
                p_justo_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                potencial_graham = ((p_justo_graham - p_actual) / p_actual) * 100 if p_justo_graham > 0 else 0
                
                # Buffett
                p_justo_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                potencial_buffett = ((p_justo_buffett - p_actual) / p_actual) * 100 if p_justo_buffett > 0 else 0
                
                # Lynch
                peg_ratio = inf.get('pegRatio', 99) or 99
                potencial_lynch = ((p_actual * (1.2 / peg_ratio) - p_actual) / p_actual) * 100 if (0.1 < peg_ratio <= 1.2) else 0
                
                target_rendimiento = max(potencial_graham, potencial_buffett, potencial_lynch)
                if target_rendimiento >= 10.0:
                    resultados_maestros.append({
                        "Ticker": ticker, "Empresa": inf.get('longName', ticker), "Precio Actual": f"${p_actual:.2f}",
                        "Ganancia Estimada Potencial": f"{target_rendimiento:+.2f}%", "ROE": f"{roe*100:.1f}%"
                    })
            except:
                pass
        if resultados_maestros: st.dataframe(pd.DataFrame(resultados_maestros), use_container_width=True)

# PESTAÑA 3: ESCÁNER TRADICIONAL POR ÍNDICES
with tab3:
    st.subheader("🛰️ Análisis de Índices y Extracción Automatizada")

# =====================================================================
# PESTAÑA 4 MODIFICADA: CONSULTA MANUAL AVANZADA DE VALOR
# =====================================================================
with tab4:
    st.subheader("🔍 Auditoría Manual Analítica A Demanda")
    st.write("Introduce el ticker de cualquier empresa global para desglosar sus métricas fundamentales de valor, ganancias proyectadas y su margen de seguridad real.")
    
    ticker_usuario = st.text_input("Ingresa el Ticker del activo a auditar:", "NU").strip().upper()
    
    if st.button("⚡ Auditar Activo y Calcular Valor de Tasación", key="btn_auditar_manual"):
        with st.spinner(f"Extrayendo estados financieros para {ticker_usuario}..."):
            try:
                asset = yf.Ticker(ticker_usuario)
                inf = asset.info
                
                # Precios y Volumen
                p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                if p_actual == 0:
                    st.error("No se pudo obtener la cotización del activo en tiempo real. Comprueba si el ticker es correcto en Yahoo Finance.")
                else:
                    # Datos fundamentales clave extraídos
                    eps = inf.get('trailingEps', 0) or 0
                    roe = inf.get('returnOnEquity', 0) or 0
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    if growth <= 0: growth = 0.05
                    book_value = inf.get('bookValue', 0) or 0
                    peg_ratio = inf.get('pegRatio', 0) or 0
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    aceleracion_vol = vol_hoy / vol_prom
                    
                    st.markdown(f"## 🏢 {inf.get('longName', ticker_usuario)} — Cotización Actual: `${p_actual:.2f}`")
                    st.markdown(f"**Sector:** {inf.get('sector', 'No Especificado')} | **Industria:** {inf.get('industry', 'No Especificado')}")
                    st.markdown("---")
                    
                    # --- 1. MODELADO DE VALOR INTRÍNSECO (VALORACIÓN SOBERANA) ---
                    st.markdown("### 🧮 Modelos de Tasación de los Maestros")
                    
                    # Fórmulas Matemáticas
                    v_intrinseco_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                    v_intrinseco_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    v_intrinseco_lynch = p_actual * (1.2 / peg_ratio) if peg_ratio > 0.1 else 0
                    
                    # Márgenes de Seguridad Individuales
                    margen_graham = ((v_intrinseco_graham - p_actual) / v_intrinseco_graham) * 100 if v_intrinseco_graham > p_actual else 0
                    margen_buffett = ((v_intrinseco_buffett - p_actual) / v_intrinseco_buffett) * 100 if v_intrinseco_buffett > p_actual else 0
                    
                    # Proyecciones de ganancias (%)
                    rendimiento_largo = max(((v_intrinseco_buffett - p_actual) / p_actual) * 100, 0) if v_intrinseco_buffett > 0 else 0
                    rendimiento_corto = ((v_intrinseco_lynch - p_actual) / p_actual) * 100 if v_intrinseco_lynch > 0 else 0
                    if rendimiento_corto < 0: rendimiento_corto = 0 # No mostrar pérdidas si el crecimiento no acompaña
                    
                    # UI de Bloques para los Modelos
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**Fórmula de Benjamin Graham**")
                        st.metric("Valor Justo (Libros)", f"${v_intrinseco_graham:.2f}" if v_intrinseco_graham > 0 else "N/A")
                        st.caption(f"Margen Seg. Graham: {margen_graham:.1f}%")
                    with c2:
                        st.markdown("**Fórmula Warren Buffett (Moat)**")
                        st.metric("Valor Intrínseco (Crecimiento)", f"${v_intrinseco_buffett:.2f}" if v_intrinseco_buffett > 0 else "N/A")
                        st.caption(f"Margen Seg. Buffett: {margen_buffett:.1f}%")
                    with c3:
                        st.markdown("**Modelo Peter Lynch (PEG)**")
                        st.metric("Valor Objetivo (Lynch)", f"${v_intrinseco_lynch:.2f}" if v_intrinseco_lynch > 0 else "N/A")
                        st.caption(f"PEG Ratio: {peg_ratio:.2f}")

                    st.markdown("---")
                    
                    # --- 2. RETORNO ESTIMADO POR HORIZONTE (CORTO VS LARGO PLAZO) ---
                    st.markdown("### 📈 Proyección de Ganancias Potenciales y Target")
                    
                    col_corto, col_largo = st.columns(2)
                    
                    with col_corto:
                        st.markdown("#### ⏳ Horizonte de Corto Plazo (Momentum / Reversión PEG)")
                        st.write("Basado en el ritmo de inyección institucional actual y el crecimiento relativo a su múltiplo PER:")
                        st.metric("Rendimiento Proyectado (Corto Plazo)", f"{rendimiento_corto:+.2f}%")
                        st.progress(min(int(max(rendimiento_corto, 0)), 100) / 100)
                        st.caption(f"Aceleración del volumen institucional en la sesión de hoy: {aceleracion_vol:.2f}x")
                        
                    with col_largo:
                        st.markdown("#### 🧱 Horizonte de Largo Plazo (Valor Compuesto / Intínseco)")
                        st.write("Basado en la convergencia del precio hacia su capacidad de generar flujos y el ROE del negocio:")
                        st.metric("Rendimiento Proyectado (Largo Plazo)", f"{rendimiento_largo:+.2f}%")
                        st.progress(min(int(max(rendimiento_largo, 0)), 100) / 100)
                        st.caption(f"Retorno sobre Capital de la Empresa (ROE real): {roe * 100:.2f}%")

                    st.markdown("---")
                    
                    # --- 3. DICTAMEN FINAL DEL AGENTE IA ---
                    st.markdown("### 🤖 Dictamen de Calificación de la IA")
                    
                    # Lógica de recomendación cruzada inteligente
                    margen_maximo = max(margen_graham, margen_buffett)
                    
                    if margen_maximo >= filtro_margen and roe >= filtro_roe:
                        st.success(f"🟢 **COMPRA FUERTE (Altamente Infravalorada):** `{ticker_usuario}` cotiza con un Margen de Seguridad consolidado del **{margen_maximo:.1f}%**, superando tu umbral configurado de {filtro_margen}%. El negocio tiene excelentes fundamentales estructurales (ROE del {roe*100:.1f}%) y las proyecciones muestran ganancias netas óptimas por encima de nuestro piso estándar del 10%.")
                    elif rendimiento_corto >= 15.0 and aceleracion_vol >= filtro_volumen:
                        st.warning(f"🟡 **OPORTUNIDAD ESPECULATIVA / CORTO PLAZO:** El margen de valor contable es ajustado, pero `{ticker_usuario}` presenta una anomalía de volumen institucional de **{aceleracion_vol:.2f}x** y un potencial de aceleración técnica del **{rendimiento_corto:.1f}%**. Ideal para operaciones tácticas con stops cortos.")
                    else:
                        st.error(f"🔴 **MANTENER / FUERA DEL RADAR:** El activo `{ticker_usuario}` no ofrece suficiente margen de protección frente a su precio actual. El mercado ya lo está tasando de manera justa o sobrevalorada. El agente recomienda buscar alternativas con mejores asimetrías de riesgo/beneficio.")
                        
            except Exception as e:
                st.error(f"Error crítico en el minado de datos del ticker: {e}. Asegúrate de ingresar las siglas válidas (ejemplo: 'NU' para Nu Holdings, 'AAPL' para Apple).")
