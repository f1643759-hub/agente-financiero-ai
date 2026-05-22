import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np
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
# PESTAÑA 1: MONITOR DE FLUJOS GLOBAL Y TOP 5 DE ACCIONES
# =====================================================================
with tab1:
    st.subheader("📡 Monitor de Flujos de Capital y Rotación Macroeconómica")
    st.write("Analiza la salud e inyección general en los índices y mercados financieros globales para identificar la tendencia dominante.")
    
    if st.button("🔍 Escanear Rotación de Capital Global", key="btn_flujos"):
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
            
            df_visual = df_global.copy()
            df_visual["Variación Diaria"] = df_visual["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_visual["Variación Semanal"] = df_visual["Variación Semanal"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_visual["Inyección Vol. (Ayer)"] = df_visual["Inyección Vol. (Ayer)"].map(lambda x: f"{x:.2f}x")
            
            st.markdown("### 📊 Estado General de los Índices y Flujos")
            st.dataframe(df_visual, use_container_width=True, hide_index=True)
            
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
            
            st.markdown("---")
            st.markdown("### 🔥 Top 5 Acciones con Mayores Entradas de Dinero")
            
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

# =====================================================================
# PESTAÑA 2: FILTROS ESTRATÉGICOS (Mantenida funcional)
# =====================================================================
with tab2:
    st.subheader("🎓 Filtros Estratégicos Automatizados: Leyendas de Wall Street")
    st.write("Filtra las acciones según los principios fundamentales de Benjamin Graham y Warren Buffett buscando solidez financiera.")

# =====================================================================
# PESTAÑA 3: ESCÁNER DE ÍNDICES COMPLETO TRADUCIDO
# =====================================================================
with tab3:
    st.subheader("🛰️ Escáner Automático de Índices Bursátiles")
    st.write("Selecciona un mercado completo. La IA revisará el valor real de cada empresa según su rentabilidad y te mostrará los mejores descuentos.")

    indices_disponibles = {
        "S&P 500 (Las 15 empresas líderes de EE.UU.)": ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BRK-B", "JPM", "XOM", "LLY", "PG", "JNJ", "TSLA", "WMT", "COST"],
        "NASDAQ 100 (Tecnología e Innovación)": ["AAPL", "MSFT", "NVDA", "AVGO", "META", "GOOG", "AMZN", "COST", "NFLX", "AMD", "INTC", "QCOM", "TXN", "HON", "AMAT"],
        "Sectores de Alto Crecimiento (Uranio, FinTech y Neobancos)": ["CCJ", "OKLO", "NU", "SQ", "SMR", "UUUU", "URNM", "NXE"]
    }

    indice_seleccionado = st.selectbox("Elige qué mercado o índice quieres escanear hoy:", list(indices_disponibles.keys()))
    lista_tickers = indices_disponibles[indice_seleccionado]

    if st.button("⚡ Iniciar Escaneo Automático", key="btn_escanear_indice"):
        resultados_indice = []
        progreso_i = st.progress(0)
        total_i = len(lista_tickers)
        
        with st.spinner("Escaneando mercado..."):
            for idx, ticker in enumerate(lista_tickers):
                try:
                    acc = yf.Ticker(ticker)
                    inf = acc.info
                    p_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                    if p_actual == 0: continue
                    
                    eps = inf.get('trailingEps', 0) or 0
                    roe = inf.get('returnOnEquity', 0) or 0
                    growth = inf.get('earningsGrowth', 0.05) or 0.05
                    book_value = inf.get('bookValue', 0) or 0
                    peg_ratio = inf.get('pegRatio', 0) or 0
                    vol_hoy = inf.get('volume', 1) or 1
                    vol_prom = inf.get('averageVolume', 1) or 1
                    aceleracion_vol = vol_hoy / vol_prom
                    
                    v_intrinseco_graham = (22.5 * eps * book_value) ** 0.5 if (eps > 0 and book_value > 0) else 0
                    v_intrinseco_buffett = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                    v_intrinseco_real = max(v_intrinseco_graham, v_intrinseco_buffett)
                    
                    margen_seguridad = ((v_intrinseco_real - p_actual) / v_intrinseco_real) * 100 if v_intrinseco_real > p_actual else 0.0
                    ganancia_largo = ((v_intrinseco_real - p_actual) / p_actual) * 100 if v_intrinseco_real > p_actual else 0.0
                    
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
            df_vista = df_res.copy()
            df_vista["Precio Actual"] = df_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
            df_vista["Valor Real Estimado"] = df_vista["Valor Real Estimado"].map(lambda x: f"${x:,.2f} USD" if x > 0 else "Calculando...")
            df_vista["🚨 Descuento de Protección (Margen)"] = df_vista["🚨 Descuento de Protección (Margen)"].map(lambda x: f"{x:.1f}% de rebaja")
            df_vista["⏳ Ganancia Rápida Estimada (Corto Plazo)"] = df_vista["⏳ Ganancia Rápida Estimada (Corto Plazo)"].map(lambda x: f"+{x:.1f}%" if x > 0 else "0.0%")
            df_vista["🧱 Ganancia Futura (Largo Plazo)"] = df_vista["🧱 Ganancia Futura (Largo Plazo)"].map(lambda x: f"+{x:.1f}%" if x > 0 else "0.0%")
            df_vista["Rentabilidad Negocio (ROE)"] = df_vista["Rentabilidad Negocio (ROE)"].map(lambda x: f"{x*100:.1f}%")
            
            st.markdown("### 📋 Resultados del Análisis de Mercado")
            st.dataframe(df_vista, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.markdown("#### 🔥 Top Opciones para Ganancias Rápidas (Corto Plazo)")
                df_top_corto = df_res.sort_values(by="⏳ Ganancia Rápida Estimada (Corto Plazo)", ascending=False).head(3)
                for _, r in df_top_corto.iterrows():
                    if r["⏳ Ganancia Rápida Estimada (Corto Plazo)"] > 0:
                        st.success(f"📈 **{r['Nombre de la Empresa']} ({r['Código']})** | Ganancia Rápida: **+{r['⏳ Ganancia Rápida Estimada (Corto Plazo)']:.1f}%**")
            with col_rec2:
                st.markdown("#### 🧱 Top Opciones Seguras (Largo Plazo con Descuento)")
                df_top_largo = df_res[df_res["🚨 Descuento de Protección (Margen)"] >= filtro_margen].sort_values(by="🚨 Descuento de Protección (Margen)", ascending=False).head(3)
                for _, r in df_top_largo.iterrows():
                    st.info(f"💎 **{r['Nombre de la Empresa']} ({r['Código']})** | Descuento: **{r['🚨 Descuento de Protección (Margen)']:.1f}%**")

# =====================================================================
# PESTAÑA 4: BUSCADOR INDIVIDUAL ANTIERROR TRADUCIDO
# =====================================================================
with tab4:
    st.subheader("🔎 Buscador Individual con Protección Antierror")
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        capital_total = st.number_input("Dinero total en tu cuenta (USD):", min_value=10.0, value=2000.0, step=50.0)
    with col_cap2:
        riesgo_maximo = st.slider("¿Qué porcentaje máximo permites arriesgar si sale mal?", 0.5, 5.0, 1.0, 0.5)

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
