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

# POOL MAESTRO
pool_maestro_acciones = {
    "AAPL": "Tecnología", "MSFT": "Tecnología", "NVDA": "Semiconductores", 
    "AVGO": "Semiconductores", "GOOGL": "Comunicación", "META": "Comunicación",
    "AMZN": "Consumo Cíclico", "TSLA": "Automotriz", "COST": "Consumo Defensivo",
    "WMT": "Consumo Defensivo", "JPM": "Banca", "BAC": "Banca",
    "XOM": "Energía", "CVX": "Energía", "LLY": "Salud", "JNJ": "Salud",
    "CCJ": "Energía Nuclear", "OKLO": "Energía Nuclear", "NU": "Fintech", "SQ": "Fintech"
}

with tab1:
    st.subheader("📡 Monitor de Flujos de Capital")
    st.write("Muestra dónde se está moviendo el dinero en el mercado hoy.")

with tab2:
    st.subheader("🎓 Filtros Estratégicos")

# =====================================================================
# PESTAÑA 3 RECONSTRUIDA: ESCÁNER DE ÍNDICES TRADUCIDO
# =====================================================================
with tab3:
    st.subheader("🛰️ Escáner Automático de Índices Bursátiles")
    st.write("Selecciona un índice completo. La IA analizará cada una de sus empresas, calculará su valor real y te dirá cuáles tienen las mayores ganancias potenciales.")

    # Diccionario con todos los índices del mercado y sus acciones más importantes
    indices_disponibles = {
        "S&P 500 (Las 15 empresas líderes de EE.UU.)": ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BRK-B", "JPM", "XOM", "LLY", "PG", "JNJ", "TSLA", "WMT", "COST"],
        "NASDAQ 100 (Tecnología e Innovación)": ["AAPL", "MSFT", "NVDA", "AVGO", "META", "GOOG", "AMZN", "COST", "NFLX", "AMD", "INTC", "QCOM", "TXN", "HON", "AMAT"],
        "Dow Jones (Gigantes Industriales Tradicionales)": ["BA", "CAT", "CRM", "CVX", "DIS", "GS", "HD", "HON", "IBM", "JNJ", "JPM", "KO", "MCD", "MMM", "MSFT", "NKE", "PG", "TRV", "UNH", "VZ", "WMT"],
        "Sectores de Alto Crecimiento (Uranio, FinTech y Neobancos)": ["CCJ", "OKLO", "NU", "SQ", "SMR", "UUUU", "URNM", "SRUUF", "NXE", "LEU", "MELI", "SOFI", "UPST"]
    }

    indice_seleccionado = st.selectbox("Elige qué mercado o índice quieres que la IA escanee hoy:", list(indices_disponibles.keys()))
    lista_tickers = indices_disponibles[indice_seleccionado]

    if st.button("⚡ Iniciar Escaneo Automático", key="btn_escanear_indice"):
        resultados_indice = []
        progreso_i = st.progress(0)
        total_i = len(lista_tickers)
        
        with st.spinner(f"Escaneando todas las acciones de {indice_seleccionado}..."):
            for idx, ticker in enumerate(lista_tickers):
                try:
                    acc = yf.Ticker(ticker)
                    inf = acc.info
                    p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                    if p_actual == 0: continue
                    
                    eps = inf.get('trailingEps', 0) or 0
                    roe = inf.get('returnOnEquity', 0) or 0
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    if growth <= 0: growth = 0.05
                    book_value = inf.get('bookValue', 0) or 0
                    peg_ratio = inf.get('pegRatio', 0) or 0
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    aceleracion_vol = vol_hoy / vol_prom
                    
                    # Fórmulas de Valor Real (Internas)
                    v_intrinseco_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                    v_intrinseco_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    v_intrinseco_real = max(v_intrinseco_graham, v_intrinseco_buffett)
                    
                    # Margen de seguridad (Descuento)
                    margen_seguridad = ((v_intrinseco_real - p_actual) / v_intrinseco_real) * 100 if v_intrinseco_real > p_actual else 0.0
                    
                    # Ganancia Futura Largo Plazo
                    ganancia_largo = ((v_intrinseco_real - p_actual) / p_actual) * 100 if v_intrinseco_real > p_actual else 0.0
                    
                    # Ganancia Rápida Corto Plazo
                    v_intrinseco_lynch = p_actual * (1.2 / peg_ratio) if peg_ratio > 0.1 else p_actual
                    ganancia_corto = ((v_intrinseco_lynch - p_actual) / p_actual) * 100 if v_intrinseco_lynch > p_actual else 0.0
                    if aceleracion_vol >= filtro_volumen and ganancia_corto == 0:
                        ganancia_corto = (aceleracion_vol * 5.0) 
                    
                    resultados_indice.append({
                        "Código": ticker,
                        "Nombre de la Empresa": inf.get('shortName', ticker),
                        "Precio Actual": p_actual,
                        "Valor Real Estimado": v_intrinseco_real,
                        "🚨 Descuento de Protección (Margen)": margen_seguridad,
                        "⏳ Ganancia Rápida Estimada (Corto Plazo)": ganancia_corto,
                        "🧱 Ganancia Futura (Largo Plazo)": ganancia_largo,
                        "Rentabilidad Negocio (ROE)": roe
                    })
                except:
                    pass
                progreso_i.progress((idx + 1) / total_i)
                
        if resultados_indice:
            df_res = pd.DataFrame(resultados_indice)
            
            # Formatear la tabla para que sea perfectamente entendible
            df_vista = df_res.copy()
            df_vista["Precio Actual"] = df_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
            df_vista["Valor Real Estimado"] = df_vista["Valor Real Estimado"].map(lambda x: f"${x:,.2f} USD" if x > 0 else "Calculando...")
            df_vista["🚨 Descuento de Protección (Margen)"] = df_vista["🚨 Descuento de Protección (Margen)"].map(lambda x: f"{x:.1f}% de rebaja")
            df_vista["⏳ Ganancia Rápida Estimada (Corto Plazo)"] = df_vista["⏳ Ganancia Rápida Estimada (Corto Plazo)"].map(lambda x: f"+{x:.1f}%" if x > 0 else "0.0%")
            df_vista["🧱 Ganancia Futura (Largo Plazo)"] = df_vista["🧱 Ganancia Futura (Largo Plazo)"].map(lambda x: f"+{x:.1f}%" if x > 0 else "0.0%")
            df_vista["Rentabilidad Negocio (ROE)"] = df_vista["Rentabilidad Negocio (ROE)"].map(lambda x: f"{x*100:.1f}%")
            
            st.markdown("### 📋 Resultados del Análisis de Mercado")
            st.dataframe(df_vista, use_container_width=True)
            
            # --- ZONA DE ALERTAS Y SELECCIÓN DE LAS GANADORAS ---
            st.markdown("---")
            st.markdown("### 🎯 Conclusiones Claras del Asistente")
            
            col_rec1, col_rec2 = st.columns(2)
            
            with col_rec1:
                st.markdown("#### 🔥 Las 3 Mejores Opciones para Ganancias Rápidas (Corto Plazo)")
                df_top_corto = df_res.sort_values(by="⏳ Ganancia Rápida Estimada (Corto Plazo)", ascending=False).head(3)
                for _, r in df_top_corto.iterrows():
                    if r["⏳ Ganancia Rápida Estimada (Corto Plazo)"] > 0:
                        st.success(f"📈 **{r['Nombre de la Empresa']} ({r['Código']})** | Ganancia Rápida: **+{r['⏳ Ganancia Rápida Estimada (Corto Plazo)']:.1f}%** | Precio por acción: ${r['Precio Actual']:.2f} USD")
            
            with col_rec2:
                st.markdown("#### 🧱 Las 3 Mejores Opciones Seguras (Largo Plazo con Descuento)")
                df_top_largo = df_res[df_res["🚨 Descuento de Protección (Margen)"] >= filtro_margen].sort_values(by="🚨 Descuento de Protección (Margen)", ascending=False).head(3)
                if not df_top_largo.empty:
                    for _, r in df_top_largo.iterrows():
                        st.info(f"💎 **{r['Nombre de la Empresa']} ({r['Código']})** | Descuento de Compra: **{r['🚨 Descuento de Protección (Margen)']:.1f}%** | Ganancia Futura: **+{r['🧱 Ganancia Futura (Largo Plazo)']:.1f}%**")
                else:
                    st.write("Ninguna empresa de este índice tiene el descuento de protección mínimo que configuraste en el panel lateral.")
        else:
            st.error("No pudimos conectar con los servidores del mercado. Reintenta el escaneo.")

# =====================================================================
# PESTAÑA 4: COMPONENTES DE MOMENTUM INDIVIDUAL ANTIERROR
# =====================================================================
with tab4:
    st.subheader("🔎 Buscador Individual con Protección Antierror")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        capital_total = st.number_input("Dinero total en tu cuenta (USD):", min_value=10.0, value=2000.0, step=50.0)
    with col_cap2:
        riesgo_maximo = st.slider("¿Qué porcentaje máximo de tu dinero permites arriesgar si sale mal?", 0.5, 5.0, 1.0, 0.5)

    st.markdown("---")
    
    diccionario_empresas = {
        "Nu Holdings (Nubank)": "NU",
        "Nvidia (Inteligencia Artificial)": "NVDA",
        "Microsoft": "MSFT",
        "Apple": "AAPL",
        "Amazon": "AMZN",
        "Cameco (Energía de Uranio)": "CCJ",
        "Tesla": "TSLA",
        "Google": "GOOGL"
    }
    
    empresa_seleccionada = st.selectbox("Selecciona una empresa específica:", list(diccionario_empresas.keys()))
    codigo_accion = diccionario_empresas[empresa_seleccionada]
    
    if st.button("⚡ Analizar Oportunidad Individual", key="btn_auditar_humano"):
        with st.spinner(f"Analizando técnico y riesgo de {empresa_seleccionada}..."):
            try:
                asset = yf.Ticker(codigo_accion)
                hist = asset.history(period="60d")
                inf = asset.info
                precio_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                
                if len(hist) < 20 or precio_actual == 0:
                    st.error("Error al leer datos.")
                else:
                    hist['EMA_9'] = hist['Close'].ewm(span=9, adjust=False).mean()
                    ema_actual = hist['EMA_9'].iloc[-1]
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / (loss + 1e-10)
                    rsi_actual = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    high_low = hist['High'] - hist['Low']
                    high_close = np.abs(hist['High'] - hist['Close'].shift())
                    low_close = np.abs(hist['Low'] - hist['Close'].shift())
                    ranges = pd.concat([high_low, high_close, low_close], axis=1)
                    true_range = ranges.max(axis=1)
                    atr_actual = true_range.rolling(14).mean().iloc[-1]
                    
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    aceleracion_vol = vol_hoy / vol_prom
                    
                    condicion_direccion = precio_actual > ema_actual
                    condicion_fuerza = 45 <= rsi_actual <= 70
                    condicion_grandes_compradores = aceleracion_vol >= 1.2
                    
                    st.markdown(f"## 🏢 {inf.get('longName', empresa_seleccionada)} — `${precio_actual:.2f} USD`")
                    st.markdown("---")
                    
                    st.markdown("### 🚦 Semáforo de Seguridad Instantáneo")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if condicion_direccion: st.success("🟢 **Dirección:** Subiendo de forma constante.")
                        else: st.error("🔴 **Dirección:** Cayendo, peligroso comprar.")
                    with c2:
                        if condicion_fuerza: st.success(f"🟢 **Fuerza:** Interés del público saludable ({rsi_actual:.1f}).")
                        elif rsi_actual > 70: st.warning("⚠️ **Fuerza:** Demasiado inflada hoy.")
                        else: st.error("🔴 **Fuerza:** Sin fuerza ni interés.")
                    with c3:
                        if condicion_grandes_compradores: st.success(f"🟢 **Inversores Grandes:** Dinero fuerte entrando ({aceleracion_vol:.2f}x).")
                        else: st.error("🔴 **Inversores Grandes:** No hay movimientos importantes hoy.")

                    st.markdown("---")
                    st.markdown("### 📋 Tu Plan de Gestión de Riesgo (Evita Errores)")
                    
                    precio_salida_perdida = precio_actual - (1.5 * atr_actual)
                    perdida_porcentaje = ((precio_actual - precio_salida_perdida) / precio_actual) * 100
                    precio_salida_ganancia = precio_actual + (3.0 * atr_actual)
                    ganancia_porcentaje = ((precio_salida_ganancia - precio_actual) / precio_actual) * 100
                    dinero_maximo_a_perder = capital_total * (riesgo_maximo / 100)
                    riesgo_por_accion = precio_actual - precio_salida_perdida
                    
                    cantidad_acciones = int(dinero_maximo_a_perder / riesgo_por_accion) if riesgo_por_accion > 0 else 0
                    dinero_total_compra = cantidad_acciones * precio_actual
                    
                    cp1, cp2, cp3 = st.columns(3)
                    with cp1: st.metric("🛑 Si baja de aquí, VENDE:", f"${precio_salida_perdida:.2f} USD", f"-{perdida_porcentaje:.1f}%")
                    with cp2: st.metric("🎯 Si sube aquí, COBRA GANANCIA:", f"${precio_salida_ganancia:.2f} USD", f"+{ganancia_porcentaje:.1f}%")
                    with cp3: st.metric("📦 Compra máxima permitida:", f"{cantidad_acciones} acciones", f"Usarás: ${dinero_total_compra:,.2f} USD")
                    
                    st.markdown("---")
                    puntos = sum([condicion_direccion, condicion_fuerza, condicion_grandes_compradores])
                    if puntos == 3: st.success("🚀 **¡SEÑAL DE COMPRA CONFIRMADA!** Todo está en verde. Sigue el plan de riesgo de arriba.")
                    elif puntos == 2: st.warning("⚠️ **MEJOR ESPERA:** Riesgo moderado, falta alguna luz verde.")
                    else: st.error("❌ **NO COMPRAR:** Alta probabilidad de perder dinero.")
            except:
                st.error("Error al procesar.")
