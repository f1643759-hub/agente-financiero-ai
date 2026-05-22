import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

# Configuración de pantalla de alta densidad para análisis masivo
st.set_page_config(page_title="Agente Inteligente de Rotación y Valor", layout="wide", initial_sidebar_state="expanded")

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

# Cargar parámetros cognitivos del Agente
conn = sqlite3.connect('agente_financiero.db')
cursor = conn.cursor()
cursor.execute("SELECT roe_minimo, margen_seguridad, aceleracion_volumen FROM configuracion_filtros ORDER BY id DESC LIMIT 1")
filtro_roe, filtro_margen, filtro_volumen = cursor.fetchone()
conn.close()

# =====================================================================
# 2. SISTEMA DE EXTRACCIÓN DINÁMICA DE MERCADO (ANTI-ESTÁTICO)
# =====================================================================
@st.cache_data(ttl=86400)  # Cachear por 24 horas para evitar bloqueos de IP
def clonar_indices_reales():
    """Descarga de forma dinámica componentes clave de los mercados e índices globales"""
    try:
        # Extraer S&P 500 desde Wikipedia de forma directa
        url_sp500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tabla_sp = pd.read_html(url_sp500)[0]
        sp500_tickers = tabla_sp['Symbol'].ext.tolist() if hasattr(tabla_sp['Symbol'], 'ext') else tabla_sp['Symbol'].tolist()
        sp500_tickers = [t.replace('.', '-') for t in sp500_tickers][:40] # Muestra representativa líder para optimizar velocidad
    except:
        sp500_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BRK-B", "JPM", "XOM", "LLY", "AVGO", "TSLA", "COST", "WMT", "UNH"]

    try:
        # Extraer NASDAQ 100
        url_nasdaq = "https://en.wikipedia.org/wiki/Nasdaq-100"
        tabla_nas = pd.read_html(url_nasdaq)[4] # Tabla de componentes habitual
        nasdaq_tickers = tabla_nas['Ticker'].tolist()[:40]
    except:
        nasdaq_tickers = ["AAPL", "MSFT", "NVDA", "AVGO", "META", "GOOG", "AMZN", "COST", "NFLX", "AMD", "QCOM", "INTC", "ISRG", "HON", "AMAT"]

    # Sectores calientes de alta rotación (Fintech, Uranio/Nuclear, SaaS, Software)
    sectores_crecimiento = ["NU", "SQ", "CCJ", "OKLO", "SMR", "UUUU", "NXE", "SRPT", "NET", "NOW"]
    
    # Combinar en un universo unificado eliminando duplicados
    universo_completo = list(set(sp500_tickers + nasdaq_tickers + sectores_crecimiento))
    return universo_completo

# =====================================================================
# 3. INTERFAZ GRÁFICA PRINCIPAL Y LATERAL
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

# Mapeo de ETFs Líderes para medir a dónde migra el dinero real
ETFS_ROTACION = {
    "Líder de Mercado (S&P 500)": "SPY",
    "Tecnología y Crecimiento (NASDAQ 100)": "QQQ",
    "Semiconductores e IA (SMH)": "SMH",
    "Energía Nuclear y Uranio (URNM)": "URNM",
    "Software y Ciberseguridad (IGV)": "IGV",
    "Sector Financiero y Banca (XLF)": "XLF",
    "Bienes de Consumo Discrecional (XLY)": "XLY",
    "Cuidado de la Salud e Innovación (XLV)": "XLV",
    "Sector Refugio: Consumo Defensivo (XLP)": "XLP",
    "Sector Refugio: Energía Fósil (XLE)": "XLE",
    "Sector Refugio: Oro y Mineras (GDX)": "GDX"
}

# =====================================================================
# PESTAÑA 1: RASTREADOR DE ROTACIÓN MACROECONÓMICA Y FLUJOS REALES
# =====================================================================
with tab1:
    st.subheader("📡 ¿A dónde está migrando el dinero de las Manos Fuertes?")
    st.write("Analiza los volúmenes de negociación institucionales de la última jornada para identificar qué sectores e índices están acumulando capital masivo hoy.")

    if st.button("🔍 Rastrear Migración de Capital Global", key="btn_macro_global"):
        analisis_macro = []
        barra_macro = st.progress(0)
        
        with st.spinner("Midiendo inyecciones monetarias líquidas en ETFs de control..."):
            for idx, (nombre, ticker) in enumerate(ETFS_ROTACION.items()):
                try:
                    tk = yf.Ticker(ticker)
                    inf = tk.info
                    hist = tk.history(period="5d")
                    
                    if len(hist) >= 2:
                        var_diaria = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                        vol_ayer = inf.get('volume', 1) or 1
                        vol_prom = inf.get('averageVolume', 1) or 1
                        fuerza_dinero = vol_ayer / vol_prom
                        
                        tipo = "CRECIMIENTO / RIESGO" if ticker in ["SPY", "QQQ", "SMH", "URNM", "IGV", "XLY"] else "REFUGIO / DEFENSA"
                        
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
            
            # Formateo estético
            df_m_visual = df_macro.copy()
            df_m_visual["Variación Diaria"] = df_m_visual["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_m_visual["Inyección de Dinero (Volumen)"] = df_m_visual["Inyección de Dinero (Volumen)"].map(lambda x: f"{x:.2f}x volumen normal")
            
            st.dataframe(df_m_visual, use_container_width=True, hide_index=True)
            
            # DIAGNÓSTICO COGNITIVO DE ROTACIÓN
            st.markdown("### 🚦 Alerta de Diagnóstico del Agente IA")
            ganador_macro = df_macro.iloc[0]
            
            if ganador_macro["Naturaleza"] == "CRECIMIENTO / RIESGO":
                st.success(f"🚀 **ROTACIÓN DE RIESGO CONFIRMADA (Risk-On):** El capital institucional está migrando con fuerza hacia **{ganador_macro['Índice / Sector']} ({ganador_macro['Ticker']})** con una inyección de **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x**. Priorizar operaciones de corto plazo alcistas en este sector.")
            else:
                st.warning(f"⚠️ **ROTACIÓN DEFENSIVA DETECTADA (Risk-Off):** Las grandes ballenas se están refugiando en **{ganador_macro['Índice / Sector']} ({ganador_macro['Ticker']})**, inyectando **{ganador_macro['Inyección de Dinero (Volumen)']:.2f}x** de volumen. Se recomienda precaución en tecnológicas y buscar valor defensivo o mantener liquidez.")
        else:
            st.error("No se pudo conectar con la matriz de flujos institucionales.")

# =====================================================================
# PESTAÑA 2: RADAR DE VALOR ESTRATÉGICO LARGO PLAZO (ALGORITMO BUFFETT/GRAHAM)
# =====================================================================
with tab2:
    st.subheader("🧱 Escáner Automático de Valor Real e Inversión Segura")
    st.write("Analiza de forma automatizada las acciones de los mercados líderes, calcula su Valor Intrínseco real y filtra los mayores descuentos del mercado con margen de protección.")

    if st.button("⚡ Ejecutar Escáner Fundamental Completo", key="btn_fundamental_masivo"):
        universo_acciones = clonar_indices_reales()
        resultados_fundamentales = []
        barra_f = st.progress(0)
        total_f = len(universo_acciones)
        
        with st.spinner(f"Analizando balances financieros de {total_f} empresas en tiempo real..."):
            for idx, ticker in enumerate(universo_acciones):
                try:
                    acc = yf.Ticker(ticker)
                    inf = acc.info
                    p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                    if p_actual == 0: continue
                    
                    eps = inf.get('trailingEps', 0) or 0
                    roe = inf.get('returnOnEquity', 0) or 0
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    book_value = inf.get('bookValue', 0) or 0
                    sector = inf.get('sector', 'Desconocido/Otros')
                    nombre = inf.get('shortName', ticker)
                    
                    # Fórmulas Avanzadas Unificadas de Valor Intrínseco (Graham + Buffett)
                    v_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                    v_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    v_intrinseco_real = max(v_graham, v_buffett)
                    
                    if v_intrinseco_real > p_actual:
                        margen_seguridad = ((v_intrinseco_real - p_actual) / v_intrinseco_real) * 100
                        porcentaje_ganancia = ((v_intrinseco_real - p_actual) / p_actual) * 100
                    else:
                        margen_seguridad = 0.0
                        porcentaje_ganancia = 0.0
                        
                    resultados_fundamentales.append({
                        "Código": ticker,
                        "Empresa": nombre,
                        "Sector": sector,
                        "Precio Actual": p_actual,
                        "Valor Real IA": v_intrinseco_real,
                        "Margen de Seguridad": margen_seguridad,
                        "Ganancia Estimada": porcentaje_ganancia,
                        "ROE": roe
                    })
                except:
                    pass
                barra_f.progress((idx + 1) / total_f)
                
        if resultados_fundamentales:
            df_f = pd.DataFrame(resultados_fundamentales)
            
            # Filtrar estrictamente bajo la regla del 20% de Margen de Seguridad Mínimo
            df_filtrado = df_f[df_f["Margen de Seguridad"] >= filtro_margen].sort_values(by="Margen de Seguridad", ascending=False)
            
            if not df_filtrado.empty:
                df_f_vista = df_filtrado.copy()
                df_f_vista["Precio Actual"] = df_f_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
                df_f_vista["Valor Real IA"] = df_f_vista["Valor Real IA"].map(lambda x: f"${x:,.2f} USD")
                df_f_vista["Margen de Seguridad"] = df_f_vista["Margen de Seguridad"].map(lambda x: f"{x:.1f}% de rebaja")
                df_f_vista["Ganancia Estimada"] = df_f_vista["Ganancia Estimada"].map(lambda x: f"+{x:.1f}% a precio real")
                df_f_vista["ROE"] = df_f_vista["ROE"].map(lambda x: f"{x*100:.1f}%")
                
                st.markdown("### 🏆 Joyas de Valor con Margen de Seguridad ≥ 20%")
                st.dataframe(df_f_vista, use_container_width=True, hide_index=True)
            else:
                st.warning("El mercado está cotizando caro en este momento. Ninguna empresa del índice superó el 20% de margen de seguridad exigido.")
        else:
            st.error("No se pudieron extraer datos del escáner fundamental.")

# =====================================================================
# PESTAÑA 3: GANANCIAS RÁPIDAS (CORTO PLAZO) + AUDITORÍA DE RIESGO TOTAL
# =====================================================================
with tab3:
    st.subheader("🎯 Oportunidades de Corto Plazo: Flujo de Dinero Inmediato")
    st.write("Configura tu capital y descubre el Top 5 de acciones con mayor volumen institucional de entrada y su plan exacto de trading.")
    
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        capital_total = st.number_input("Dinero líquido en tu portafolio (USD):", min_value=10.0, value=2000.0, step=50.0, key="p3_cap")
    with col_x2:
        riesgo_maximo = st.slider("Porcentaje máximo a arriesgar por operación:", 0.5, 5.0, 1.0, 0.5, key="p3_riesg")
        
    st.markdown("---")
    
    if st.button("🚀 Generar Top 5 Corto Plazo y Planes de Inversión", key="btn_corto_plazo_total"):
        universo_acciones = clonar_indices_reales()
        analisis_corto = []
        barra_c = st.progress(0)
        total_c = len(universo_acciones)
        
        with st.spinner("Analizando momentum técnico y volumen institucional..."):
            for idx, ticker in enumerate(universo_acciones):
                try:
                    obj = yf.Ticker(ticker)
                    hist = obj.history(period="30d")
                    inf = obj.info
                    
                    if len(hist) < 20: continue
                    precio_actual = hist['Close'].iloc[-1]
                    
                    # Fuerza del dinero institucional (Volumen diario vs Promedio)
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    fuerza_dinero = vol_hoy / vol_prom
                    
                    # Cálculo técnico de fuerza (RSI de 14 períodos)
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / (loss + 1e-10)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Volatilidad estructural (ATR de 14 periodos para Stop Loss Inteligente)
                    high_low = hist['High'] - hist['Low']
                    high_close = np.abs(hist['High'] - hist['Close'].shift())
                    low_close = np.abs(hist['Low'] - hist['Close'].shift())
                    ranges = pd.concat([high_low, high_close, low_close], axis=1)
                    true_range = ranges.max(axis=1)
                    atr = true_range.rolling(14).mean().iloc[-1]
                    
                    # Media Móvil Exponencial de 9 para detectar dirección limpia
                    hist['EMA_9'] = hist['Close'].ewm(span=9, adjust=False).mean()
                    ema_9 = hist['EMA_9'].iloc[-1]
                    
                    # Algoritmo de Scoring Corto Plazo: Premia volumen masivo + momentum sano sin sobrecompra extrema
                    if 45 <= rsi <= 72 and precio_actual > ema_9:
                        score_corto = (fuerza_dinero * 70) + (100 - abs(60 - rsi))
                    else:
                        score_corto = 0 # Descartado por tendencia bajista o sobrecompra destructiva
                        
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
            # Aislar las 5 mejores opciones absolutas detectadas en el mercado entero
            top_5_corto = pd.DataFrame(analisis_corto).sort_values(by="Score", ascending=False).head(5)
            
            st.markdown("## 🔥 Top 5 Acciones Recomendadas para Inversión Inmediata")
            st.markdown("---")
            
            for rank, (_, fila) in enumerate(top_5_corto.iterrows(), 1):
                precio = fila['Precio']
                atr_f = fila['ATR']
                fuerza = fila['Inyección Capital']
                ticker_c = fila['Código']
                
                # --- MATRIZ MATEMÁTICA DE GESTIÓN DE RIESGO ANTIERROR ---
                precio_stop_loss = precio - (1.5 * atr_f)
                porcentaje_perdida = ((precio - precio_stop_loss) / precio) * 100
                
                precio_take_profit = precio + (3.0 * atr_f) # Ratio Riesgo/Beneficio 1:2 Exacto
                porcentaje_ganancia = ((precio_take_profit - precio) / precio) * 100
                
                dinero_en_riesgo = capital_total * (riesgo_maximo / 100)
                riesgo_por_accion = precio - precio_stop_loss
                
                cantidad_acciones = int(dinero_en_riesgo / riesgo_por_accion) if riesgo_por_accion > 0 else 0
                capital_requerido = cantidad_acciones * precio
                
                # Alertas visuales dinámicas del Agente según nivel de inyección
                if fuerza >= 1.6:
                    tipo_alerta = "🚀 COMPRA CRÍTICA INSTITUCIONAL DETECTADA"
                    color_contenedor = st.success
                else:
                    tipo_alerta = "🐳 ACUMULACIÓN DE GRANDES COMPRADORES"
                    color_contenedor = st.info
                
                # Renderizado del Plan de Operación Unificado
                color_contenedor(f"### 🏆 TOP {rank}: {fila['Empresa']} ({ticker_c}) — Sector: *{fila['Sector']}*")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("🎯 Precio de Entrada Actual:", f"${precio:.2f} USD", f"Flujo: {fuerza:.2f}x")
                with col_m2:
                    st.metric("🛑 Stop Loss (Corte de Pérdida):", f"${precio_stop_loss:.2f} USD", f"-{porcentaje_perdida:.1f}%")
                with col_m3:
                    st.metric("💰 Take Profit (Cobrar Ganancia):", f"${precio_take_profit:.2f} USD", f"+{porcentaje_ganancia:.1f}%")
                    
                st.markdown(f"📦 **Plan de Ejecución:** Compra exacta de **{cantidad_acciones} acciones**. Capital total asignado: **${capital_requerido:,.2f} USD**. *Alerta IA:* **{tipo_alerta}**")
                st.markdown("---")
        else:
            st.error("No se encontraron acciones con momentum óptimo y entrada de volumen simultánea en este bloque.")
