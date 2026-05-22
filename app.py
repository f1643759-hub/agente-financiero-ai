import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np

# Configuración de pantalla de alta densidad para análisis masivo
st.set_page_config(page_title="Agente Inteligente de Rotación y Valor", layout="wide", initial_sidebar_state="expanded")

# PARCHE DE SEGURIDAD CONTRA BLOQUEOS DE YAHOO FINANCE
import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

# =====================================================================
# 1. ARQUITECTURA DE BASE DE DATOS Y AUTO-APRENDIZAJE
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

# Pool Maestro Diversificado de Acciones (Tecnología, Uranio, Fintech, etc.)
POOL_ACCIONES = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "JPM", "XOM", "LLY", "AVGO", 
    "TSLA", "COST", "WMT", "UNH", "BRK-B", "PG", "JNJ", "HD", "MRK", "ORCL",
    "CCJ", "OKLO", "NU", "SQ", "SMR", "UUUU", "NXE", "NET", "NOW", "AMD"
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
st.sidebar.markdown("### 🧠 Filtros Inteligentes Activos")
st.sidebar.metric("Rentabilidad Mínima (ROE)", f"{filtro_roe * 100:.1f}%")
st.sidebar.metric("Margen de Seguridad Exigido", f"{filtro_margen:.1f}%")
st.sidebar.metric("Inyección de Capital Mínima", f"{filtro_volumen:.2f}x")

st.title("🤖 Agente IA Macro-Fundamental Omnisciente")
st.markdown("### Escaneo Completo de Índices, Flujos de Rotación, Valor Intrínseco y Alertas de Inversión")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🛰️ ESCÁNER MAESTRO: Rotación de Capital Global",
    "🧱 ANÁLISIS VALOR: Radar de Descuento Largo Plazo",
    "🎯 CORTO PLAZO: Impulso, Flujos y Gestión Antierror"
])

# =====================================================================
# PESTAÑA 1: MATRIZ MACRO DE ROTACIÓN DE SECTORES (MIGRACIÓN DEL DINERO)
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
            
            if ganador_macro["Naturaleza"] == "CRECIMIENTO / RIESGO":
                st.success(f"🚀 **ROTACIÓN HACIA EL RIESGO TRABAJANDO (Risk-On):** El capital institucional está migrando con fuerza hacia **{ganador_macro['Índice / Sector']} ({ganador_macro['Ticker']})** con un volumen de **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x**. Buen entorno para buscar compras de momentum.")
            else:
                st.warning(f"⚠️ **ROTACIÓN DEFENSIVA DETECTADA (Risk-Off):** Las grandes ballenas se están protegiendo en **{ganador_macro['Índice / Sector']} ({ganador_macro['Ticker']})**, inyectando **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x** de volumen normal. Reduce riesgos en el corto plazo.")
        else:
            st.error("Error al conectar con los servidores del mercado. Reintenta en unos segundos.")

# =====================================================================
# PESTAÑA 2: RADAR FUNDAMENTAL DE LARGO PLAZO (BUFFETT & GRAHAM PURAS)
# =====================================================================
with tab2:
    st.subheader("🧱 Escáner de Valor Intrínseco y Descuento Fundamental (Largo Plazo)")
    st.write("Analiza balances financieros reales de las empresas para calcular su valor real estimado por algoritmos tradicionales de valor.")

    if st.button("⚡ Ejecutar Escáner Fundamental Completo", key="btn_fundamental_masivo"):
        resultados_fundamentales = []
        barra_f = st.progress(0)
        total_f = len(POOL_ACCIONES)
        
        with st.spinner("Procesando Estados de Resultados e Info Financiera..."):
            for idx, ticker in enumerate(POOL_ACCIONES):
                try:
                    acc = yf.Ticker(ticker)
                    inf = acc.info
                    p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                    if p_actual == 0: continue
                    
                    eps = inf.get('trailingEps', 0) or 0
                    roe = inf.get('returnOnEquity', 0) or 0
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    book_value = inf.get('bookValue', 0) or 0
                    sector = inf.get('sector', 'Otros')
                    
                    # Fórmulas Clásicas de Valor Intrínseco
                    v_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                    v_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    v_intrinseco_real = max(v_graham, v_buffett)
                    
                    if v_intrinseco_real > p_actual:
                        margen_seguridad = ((v_intrinseco_real - p_actual) / v_intrinseco_real) * 100
                        porcentaje_ganancia = ((v_intrinseco_real - p_actual) / p_actual) * 100
                    else:
                        margen_seguridad = 0.0
                        porcentaje_ganancia = 0.0
                        
                    # Filtro exigente: Solo pasa si tiene ROE positivo y margen de seguridad óptimo
                    if margen_seguridad >= filtro_margen and roe >= filtro_roe:
                        resultados_fundamentales.append({
                            "Código": ticker,
                            "Empresa": inf.get('shortName', ticker),
                            "Sector": sector,
                            "Precio Actual": p_actual,
                            "Valor Real IA": v_intrinseco_real,
                            "Margen de Seguridad": margen_seguridad,
                            "Ganancia Potencial": porcentaje_ganancia,
                            "Rentabilidad ROE": roe
                        })
                except:
                    pass
                barra_f.progress((idx + 1) / total_f)
                
        if resultados_fundamentales:
            df_f = pd.DataFrame(resultados_fundamentales).sort_values(by="Margen de Seguridad", ascending=False)
            
            df_f_vista = df_f.copy()
            df_f_vista["Precio Actual"] = df_f_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
            df_f_vista["Valor Real IA"] = df_f_vista["Valor Real IA"].map(lambda x: f"${x:,.2f} USD")
            df_f_vista["Margen de Seguridad"] = df_f_vista["Margen de Seguridad"].map(lambda x: f"{x:.1f}% de descuento")
            df_f_vista["Ganancia Potencial"] = df_f_vista["Ganancia Potencial"].map(lambda x: f"+{x:.1f}% al objetivo")
            df_f_vista["Rentabilidad ROE"] = df_f_vista["Rentabilidad ROE"].map(lambda x: f"{x*100:.1f}%")
            
            st.markdown("### 🏆 Empresas en Liquidación Fundamental (Margen ≥ 20%)")
            st.dataframe(df_f_vista, use_container_width=True, hide_index=True)
        else:
            st.warning("Ninguna de las acciones del pool cuenta actualmente con un margen de seguridad del 20% o más y un ROE saludable en sus balances actuales.")

# =====================================================================
# PESTAÑA 3: TOP 5 ACCIONES CORTO PLAZO + ALERTAS + GESTIÓN ANTIERROR
# =====================================================================
with tab3:
    st.subheader("🎯 Escáner de Corto Plazo e Impulso (Inyección Inmediata)")
    st.write("Calcula de forma automática qué acciones tienen momentum alcista y diseña un plan exacto de gestión de riesgo.")
    
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        capital_total = st.number_input("Dinero líquido disponible (USD):", min_value=10.0, value=2000.0, step=50.0, key="p3_cap")
    with col_x2:
        riesgo_maximo = st.slider("Porcentaje de cuenta que permites arriesgar (%):", 0.5, 5.0, 1.0, 0.5, key="p3_riesg")
        
    st.markdown("---")
    
    if st.button("🚀 Generar Top 5 Táctico Corto Plazo", key="btn_corto_plazo_total"):
        analisis_corto = []
        barra_c = st.progress(0)
        total_c = len(POOL_ACCIONES)
        
        with st.spinner("Escaneando gráficos y medias móviles..."):
            for idx, ticker in enumerate(POOL_ACCIONES):
                try:
                    obj = yf.Ticker(ticker)
                    hist = obj.history(period="30d")
                    inf = obj.info
                    
                    if len(hist) < 20: continue
                    precio_actual = hist['Close'].iloc[-1]
                    
                    # Fuerza del volumen institucional diario vs promedio de su mes
                    vol_hoy = hist['Volume'].iloc[-1]
                    vol_prom = hist['Volume'].mean()
                    fuerza_dinero = vol_hoy / vol_prom if vol_prom > 0 else 1.0
                    
                    # Cálculo técnico del RSI (Índice de Fuerza Relativa)
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / (loss + 1e-10)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Cálculo de volatilidad real (ATR de 14 periodos para Stops Seguros)
                    high_low = hist['High'] - hist['Low']
                    high_close = np.abs(hist['High'] - hist['Close'].shift())
                    low_close = np.abs(hist['Low'] - hist['Close'].shift())
                    ranges = pd.concat([high_low, high_close, low_close], axis=1)
                    true_range = ranges.max(axis=1)
                    atr = true_range.rolling(14).mean().iloc[-1]
                    
                    # Media Móvil Exponencial de 9 días para asegurar dirección alcista
                    hist['EMA_9'] = hist['Close'].ewm(span=9, adjust=False).mean()
                    ema_9 = hist['EMA_9'].iloc[-1]
                    
                    # Condición técnica estricta: Tendencia alcista y RSI sin burbuja destructiva
                    if precio_actual > ema_9 and 45 <= rsi <= 72:
                        score_corto = (fuerza_dinero * 70) + (100 - abs(60 - rsi))
                    else:
                        score_corto = 0
                        
                    if score_corto > 0:
                        analisis_corto.append({
                            "Código": ticker,
                            "Empresa": inf.get('shortName', ticker),
                            "Sector": inf.get('sector', 'Otros'),
                            "Precio": precio_actual,
                            "Inyección Capital": fuerza_dinero,
                            "RSI": rsi,
                            "ATR": atr,
                            "Score": score_corto
                        })
                except:
                    pass
                barra_c.progress((idx + 1) / total_c)
                
        if analisis_corto:
            top_5_corto = pd.DataFrame(analisis_corto).sort_values(by="Score", ascending=False).head(5)
            st.markdown("## 🔥 Los 5 Candidatos con Mayor Fuerza Inmediata")
            st.markdown("---")
            
            for rank, (_, fila) in enumerate(top_5_corto.iterrows(), 1):
                precio = fila['Precio']
                atr_f = fila['ATR']
                fuerza = fila['Inyección Capital']
                ticker_c = fila['Código']
                
                # --- MATEMÁTICA DE GESTIÓN DE RIESGO ANTIERROR ---
                precio_stop_loss = precio - (1.5 * atr_f)
                porcentaje_perdida = ((precio - precio_stop_loss) / precio) * 100
                precio_take_profit = precio + (3.0 * atr_f)
                porcentaje_ganancia = ((precio_take_profit - precio) / precio) * 100
                
                dinero_en_riesgo = capital_total * (riesgo_maximo / 100)
                riesgo_por_accion = precio - precio_stop_loss
                cantidad_acciones = int(dinero_en_riesgo / riesgo_por_accion) if riesgo_por_accion > 0 else 0
                capital_requerido = cantidad_acciones * precio
                
                if fuerza >= 1.4:
                    tipo_alerta = "🚀 COMPRA CRÍTICA: Inyección Institucional Masiva"
                    color_contenedor = st.success
                else:
                    tipo_alerta = "🐳 ALERTA IA: Acumulación Silenciosa de Manos Fuertes"
                    color_contenedor = st.info
                
                color_contenedor(f"### 🏆 TOP {rank}: {fila['Empresa']} ({ticker_c}) — Sector: {fila['Sector']}")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1: st.metric("🎯 Precio de Entrada Actual:", f"${precio:.2f} USD", f"Fuerza: {fuerza:.2f}x")
                with col_m2: st.metric("🛑 Stop Loss Obligatorio:", f"${precio_stop_loss:.2f} USD", f"-{porcentaje_perdida:.1f}%")
                with col_m3: st.metric("💰 Objetivo Take Profit:", f"${precio_take_profit:.2f} USD", f"+{porcentaje_ganancia:.1f}%")
                
                st.markdown(f"📦 **Plan Antierror de Trading:** Adquirir exactamente **{cantidad_acciones} acciones**. Capital comprometido: **${capital_requerido:,.2f} USD**. *Estado:* **{tipo_alerta}**")
                st.markdown("---")
        else:
            st.error("No se detectaron acciones en tendencia limpia alcista con volumen fuerte en este bloque.")
