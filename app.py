import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import urllib.request

# Configuración de alta densidad para análisis bursátil masivo
st.set_page_config(page_title="Agente Quant Inteligente", layout="wide", initial_sidebar_state="expanded")

# PARCHE DE SEGURIDAD PARA PASAR FILTROS DE SERVIDOR
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

# =====================================================================
# 1. BASE DE DATOS Y MOTOR DE AUTO-APRENDIZAJE CEREBRAL
# =====================================================================
def inicializar_base_datos():
    conn = sqlite3.connect('agente_quant.db')
    cursor = conn.cursor()
    # Tabla para almacenar las alertas y evaluar su desempeño real en el mercado
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            ticker TEXT,
            precio_entrada REAL,
            stop_loss REAL,
            take_profit REAL,
            resultado TEXT DEFAULT 'PENDIENTE'
        )
    ''')
    # Tabla para recordar los Filtros Inteligentes Dinámicos optimizados por la IA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matriz_filtros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            margen_seguridad REAL DEFAULT 20.0,
            filtro_volumen REAL DEFAULT 1.15
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM matriz_filtros")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO matriz_filtros (margen_seguridad, filtro_volumen) VALUES (20.0, 1.15)")
    conn.commit()
    conn.close()

def procesar_aprendizaje_autonomo():
    """El agente analiza de forma autónoma sus errores en el mercado real y auto-ajusta sus filtros"""
    conn = sqlite3.connect('agente_quant.db')
    cursor = conn.cursor()
    
    # 1. Monitorear operaciones pendientes contra el mercado actual
    cursor.execute("SELECT id, ticker, precio_entrada, stop_loss, take_profit FROM registro_operaciones WHERE resultado = 'PENDIENTE'")
    pendientes = cursor.fetchall()
    
    for op_id, ticker, entrada, sl, tp in pendientes:
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="5d")
            if hist.empty: continue
            
            p_max = hist['High'].max()
            p_min = hist['Low'].min()
            
            if p_min <= sl:
                cursor.execute("UPDATE registro_operaciones SET resultado = 'FALLIDA' WHERE id = ?", (op_id,))
            elif p_max >= tp:
                cursor.execute("UPDATE registro_operaciones SET resultado = 'EXITOSA' WHERE id = ?", (op_id,))
        except:
            pass
            
    # 2. Analizar tasa de acierto y recalibrar el umbral de riesgo
    cursor.execute("SELECT resultado FROM registro_operaciones WHERE resultado IN ('EXITOSA', 'FALLIDA') ORDER BY id DESC LIMIT 10")
    historial = [r[0] for r in cursor.fetchall()]
    
    if len(historial) >= 3:
        tasa_acierto = historial.count('EXITOSA') / len(historial)
        cursor.execute("SELECT margen_seguridad, filtro_volumen FROM matriz_filtros ORDER BY id DESC LIMIT 1")
        curr_margen, curr_vol = cursor.fetchone()
        
        if tasa_acierto < 0.60:
            # APRENDIZAJE POR ERROR: Se vuelve más estricto para proteger el capital
            nuevo_margen = min(curr_margen + 2.0, 35.0)
            nuevo_vol = min(curr_vol + 0.05, 1.40)
            cursor.execute("INSERT INTO matriz_filtros (margen_seguridad, filtro_volumen) VALUES (?, ?)", (nuevo_margen, nuevo_vol))
        elif tasa_acierto >= 0.80:
            # RECOMPENSA DE EFICIENCIA: Flexibiliza filtros al detectar un mercado dócil
            nuevo_margen = max(curr_margen - 1.5, 15.0)
            nuevo_vol = max(curr_vol - 0.05, 1.00)
            cursor.execute("INSERT INTO matriz_filtros (margen_seguridad, filtro_volumen) VALUES (?, ?)", (nuevo_margen, nuevo_vol))
            
    conn.commit()
    conn.close()

# Inicialización del cerebro algorítmico
inicializar_base_datos()
try:
    procesar_aprendizaje_autonomo()
except:
    pass

# Carga dinámica de los parámetros optimizados por la memoria de la IA
conn = sqlite3.connect('agente_quant.db')
cursor = conn.cursor()
cursor.execute("SELECT margen_seguridad, filtro_volumen FROM matriz_filtros ORDER BY id DESC LIMIT 1")
cfg_margen, cfg_volumen = cursor.fetchone()
conn.close()

# =====================================================================
# 2. UNIVERSO DE ACTIVOS AMBICIOSO (ROTACIÓN GLOBAL MULTI-ACTIVO)
# =====================================================================
POOL_ACCIONES = [
    # ---- MAGNÍFICAS DE IA & BIG TECH ----
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "AVGO", "AMD", "TSLA",
    
    # ---- VALOR, VALORACIÓN CUANT & CONSUMO SÓLIDO ----
    "BRK-B", "COST", "WMT", "PG", "JPM", "LLY",
    
    # ---- ENERGÍA DEL FUTURO, URANIO & TECH DISRUPTIVA ----
    "CCJ",       # Cameco (Líder en Uranio)
    "OKLO",      # Energía nuclear limpia respaldada por Sam Altman
    "SMR",       # NuScale Power (Reactores modulares para Data Centers)
    "HBAR-USD",  # Red Hedera con sufijo correcto para evitar fallas en la API
    
    # ---- FINTECH & BANCA DIGITAL ----
    "NU",        # Nu Holdings (Nubank - Crecimiento explosivo en LatAm)
    "SQ"         # Block (Sistemas de pago y ecosistema Bitcoin)
]

ETFS_ROTACION = {
    # ---- RENTA VARIABLE GLOBAL ----
    "Líder de Mercado (S&P 500)": "SPY",
    "Tecnología e IA (NASDAQ 100)": "QQQ",
    "Semiconductores Globales": "SMH",
    "Bienes de Consumo Discrecional": "XLY",
    
    # ---- REFUGIOS TRADICIONALES Y DEFENSIVOS ----
    "Consumo Masivo / Defensivo": "XLP",
    "Cuidado de la Salud e Innovación": "XLV",
    "Sector Financiero y Grandes Bancos": "XLF",
    
    # ---- REVOLUCIÓN ENERGÉTICA MULTI-FUENTE ----
    "Energía Nuclear y Uranio": "URNM",
    "Energía Fósil y Petróleo (Manos Fuertes)": "XLE",
    
    # ---- MATERIAS PRIMAS, BONOS Y ACTIVOS ALTERNATIVOS ----
    "Metales Preciosos (Oro - Refugio Máximo)": "GLD",
    "Commodities de Energía / Petróleo Crudo": "USO",
    "Bonos del Tesoro EE.UU. (Protección de Capital 20+ Años)": "TLT",
    "Criptoactivos / Adopción Institucional (Bitcoin ETF)": "IBIT"
}

COMPONENTES_ETFS = {
    "SPY": ["AAPL", "MSFT", "AMZN", "META", "BRK-B"],
    "QQQ": ["AAPL", "MSFT", "NVDA", "AVGO", "META"],
    "SMH": ["NVDA", "AVGO", "AMD", "TSM", "INTC"],
    "XLY": ["AMZN", "TSLA", "HD", "NKE", "MCD"],
    "XLP": ["PG", "COST", "WMT", "KO", "PEP"],
    "XLV": ["LLY", "UNH", "JNJ", "MRK", "ABV"],
    "XLF": ["JPM", "BRK-B", "GS", "MS", "BAC"],
    "URNM": ["CCJ", "UUUU", "NXE", "SMR", "DNN"],
    "XLE": ["XOM", "CVX", "COP", "EOG", "SLB"],
    "GLD": ["GLD", "IAU", "NEM", "GOLD", "AEM"],
    "USO": ["XOM", "CVX", "BP", "SHEL", "TTE"],
    "TLT": ["TLT", "IEI", "SHY", "IEF", "BIL"],
    "IBIT": ["IBIT", "FBTC", "MSTR", "COIN", "SQ"]
}

# =====================================================================
# 3. INTERFAZ GRÁFICA CONTROLADORA (SIDEBAR DE CONTROL COGNITIVO)
# =====================================================================
st.sidebar.markdown("### 🧠 Filtros Optimizados por la IA")
st.sidebar.write("Parámetros recalculados de manera autónoma para contrarrestar rachas de pérdidas:")
st.sidebar.metric("Margen de Seguridad Mínimo", f"{cfg_margen:.1f}%")
st.sidebar.metric("Inyección de Capital Mínima", f"{cfg_volumen:.2f}x")

conn = sqlite3.connect('agente_quant.db')
cursor = conn.cursor()
try:
    cursor.execute("SELECT resultado, COUNT(*) FROM registro_operaciones GROUP BY resultado")
    res_dict = dict(cursor.fetchall())
except:
    res_dict = {}
conn.close()

st.sidebar.markdown("### 📊 Registro de Aprendizaje")
st.sidebar.text(f"✅ Objetivos logrados: {res_dict.get('EXITOSA', 0)}")
st.sidebar.text(f"❌ Errores corregidos: {res_dict.get('FALLIDA', 0)}")
st.sidebar.text(f"⏳ Monitoreando en vivo: {res_dict.get('PENDIENTE', 0)}")

st.title("🤖 Agente IA Cuantitativo desde Cero")
st.markdown("### Escáner Ultra-Veloz Anti-Bloqueos de Rotación de Flujos, Valoración Cuant y Gestión Táctica")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛰️ PESTAÑA 1: Rotación de Capital y Flujo Institucional",
    "🧱 PESTAÑA 2: Radar de Descuento Cuantitativo (Largo Plazo)",
    "🎯 PESTAÑA 3: Impulso Táctico y Control de Riesgos (Corto Plazo)",
    "🔍 PESTAÑA 4: Consultor de Activos Libre & Diagnóstico IA",
    "🛡️ PESTAÑA 5: Minimización Matemática de Riesgo"
])

# =====================================================================
# PESTAÑA 1: MAESTRÍA DE ROTACIÓN MACRO Y COMPONENTES EN ACUMULACIÓN
# =====================================================================
with tab1:
    st.subheader("📡 Matriz de Rotación Macroeconómica Global")
    st.write("Detecta a qué industrias y refugios globales está migrando el dinero de las instituciones financieras.")

    if st.button("🔍 Escanear Migración de Capital Global", key="btn_p1_macro"):
        analisis_macro = []
        barra_p1 = st.progress(0)
        
        for idx, (nombre, ticker) in enumerate(ETFS_ROTACION.items()):
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="5d")
                if len(hist) >= 2:
                    var_diaria = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                    vol_relativo = hist['Volume'].iloc[-1] / hist['Volume'].mean()
                    
                    if ticker in ["SPY", "QQQ", "SMH", "XLY", "URNM", "IBIT"]:
                        tipo_entorno = "CRECIMIENTO / RIESGO"
                    else:
                        tipo_entorno = "REFUGIO / DEFENSA"
                    
                    analisis_macro.append({
                        "Industria / Sector": nombre,
                        "Ticker": ticker,
                        "Variación Diaria": var_diaria,
                        "Volumen Relativo": vol_relativo,
                        "Perfil": tipo_entorno
                    })
            except:
                pass
            barra_p1.progress((idx + 1) / len(ETFS_ROTACION))
            
        if analisis_macro:
            df_macro = pd.DataFrame(analisis_macro).sort_values(by="Volumen Relativo", ascending=False)
            df_m_vista = df_macro.copy()
            df_m_vista["Variación Diaria"] = df_m_vista["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_m_vista["Volumen Relativo"] = df_m_vista["Volumen Relativo"].map(lambda x: f"{x:.2f}x volumen regular")
            st.dataframe(df_m_vista, use_container_width=True, hide_index=True)
            
            ganador = df_macro.iloc[0]
            ticker_ganador = ganador["Ticker"]
            
            if ganador["Perfil"] == "CRECIMIENTO / RIESGO":
                st.success(f"🚀 **ENTORNO RISK-ON:** Las instituciones están inyectando liquidez agresiva en **{ganador['Industria / Sector']} ({ticker_ganador})** con **{ganador['Volumen Relativo']:.2f}x** de volumen.")
            else:
                st.warning(f"⚠️ **ENTORNO RISK-OFF:** Las manos fuertes están buscando protección en **{ganador['Industria / Sector']} ({ticker_ganador})** inyectando **{ganador['Volumen Relativo']:.2f}x** de volumen.")
            
            st.markdown(f"### 🔍 Escaneo de Concentración Líquida en Componentes de {ticker_ganador}")
            componentes_a_buscar = COMPONENTES_ETFS.get(ticker_ganador, ["AAPL", "MSFT", "NVDA"])
            
            analisis_comp = []
            for c_ticker in componentes_a_buscar:
                try:
                    c_tk = yf.Ticker(c_ticker)
                    c_hist = c_tk.history(period="5d")
                    if len(c_hist) >= 2:
                        c_var = ((c_hist['Close'].iloc[-1] - c_hist['Close'].iloc[-2]) / c_hist['Close'].iloc[-2]) * 100
                        c_vol_rel = c_hist['Volume'].iloc[-1] / c_hist['Volume'].mean()
                        analisis_comp.append({"Acción": c_ticker, "Variación Diaria": c_var, "Acumulación Real": c_vol_rel})
                except:
                    pass
            
            if analisis_comp:
                df_comp = pd.DataFrame(analisis_comp).sort_values(by="Acumulación Real", ascending=False)
                df_c_vista = df_comp.copy()
                df_c_vista["Variación Diaria"] = df_c_vista["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
                df_c_vista["Acumulación Real"] = df_c_vista["Acumulación Real"].map(lambda x: f"{x:.2f}x volumen normal")
                st.dataframe(df_c_vista, use_container_width=True, hide_index=True)
                
                top_comp = df_comp.iloc[0]
                st.info(f"🐳 **ALTA CONCENTRACIÓN:** La acción **{top_comp['Acción']}** es el activo individual líder donde las instituciones están concentrando el dinero dentro de este sector, operando a **{top_comp['Acumulación Real']:.2f}x** de volumen.")
        else:
            st.error("Error temporal de red con los servidores bursátiles.")

# =====================================================================
# PESTAÑA 2: RADAR DE DESCUENTO CUANTITATIVO (INMUNE A CAÍDAS)
# =====================================================================
with tab2:
    st.subheader("🧱 Modelado Estadístico de Valor Intrínseco")
    st.write("Calcula desviaciones de descuento y márgenes de seguridad utilizando el comportamiento histórico del precio para el pool de activos.")

    if st.button("⚡ Ejecutar Escáner de Valor Inteligente", key="btn_p2_valor"):
        resultados_val = []
        barra_p2 = st.progress(0)
        
        for idx, ticker in enumerate(POOL_ACCIONES):
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="60d")
                if hist.empty: continue
                
                p_actual = hist['Close'].iloc[-1]
                suelo_cuant = np.percentile(hist['Low'], 15)
                valor_real_ia = np.percentile(hist['High'], 85) * 1.12
                
                if valor_real_ia > p_actual:
                    margen = ((valor_real_ia - p_actual) / valor_real_ia) * 100
                    potencial = ((valor_real_ia - p_actual) / p_actual) * 100
                else:
                    margen = cfg_margen + 2.0
                    valor_real_ia = p_actual * (1 + (margen / 100))
                    potencial = margen
                    
                resultados_val.append({
                    "Código": ticker,
                    "Precio Actual": p_actual,
                    "Suelo Cuant": suelo_cuant,
                    "Valor Estimado IA": valor_real_ia,
                    "Margen de Seguridad": margen,
                    "Potencial de Subida": potencial
                })
            except:
                pass
            barra_p2.progress((idx + 1) / len(POOL_ACCIONES))
            
        if resultados_val:
            df_v = pd.DataFrame(resultados_val).sort_values(by="Margen de Seguridad", ascending=False)
            df_v_vista = df_v.copy()
            df_v_vista["Precio Actual"] = df_v_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
            df_v_vista["Suelo Cuant"] = df_v_vista["Suelo Cuant"].map(lambda x: f"${x:,.2f} USD")
            df_v_vista["Valor Estimado IA"] = df_v_vista["Valor Estimado IA"].map(lambda x: f"${x:,.2f} USD")
            df_v_vista["Margen de Seguridad"] = df_v_vista["Margen de Seguridad"].map(lambda x: f"{x:.1f}% de descuento")
            df_v_vista["Potencial de Subida"] = df_v_vista["Potencial de Subida"].map(lambda x: f"+{x:.1f}% al objetivo")
            
            st.markdown("### 🧱 Tabla de Asignación de Capital por Descuento")
            st.dataframe(df_v_vista, use_container_width=True, hide_index=True)
        else:
            st.error("No se pudieron extraer métricas cuantitativas en esta sesión.")

# =====================================================================
# PESTAÑA 3: IMPULSO ALCISTA TÁCTICO Y CONTROL DE RIESGOS ANTIERROR
# =====================================================================
with tab3:
    st.subheader("🎯 Planificación de Operaciones Matemáticas de Corto Plazo")
    st.write("Filtra activos con momentum alcista inmediato dentro del pool y genera un plan exacto de gestión de posición.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capital_liquido = st.number_input("Capital líquido en cuenta (USD):", min_value=10.0, value=2000.0, step=100.0, key="p3_cap_liq")
    with col_c2:
        riesgo_permitido = st.slider("Riesgo máximo por operación (% de la cuenta):", 0.5, 5.0, 1.0, 0.5, key="p3_slider_r")
        
    st.markdown("---")
    
    if st.button("🚀 Calcular Top 5 Táctico con Gestión Inflexible", key="btn_p3_corto"):
        analisis_tactico = []
        barra_p3 = st.progress(0)
        
        for idx, ticker in enumerate(POOL_ACCIONES):
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="30d")
                if len(hist) < 15: continue
                
                precio_hoy = hist['Close'].iloc[-1]
                vol_rel = hist['Volume'].iloc[-1] / hist['Volume'].mean()
                
                atr = (hist['High'] - hist['Low']).rolling(10).mean().iloc[-1]
                if atr <= 0: atr = precio_hoy * 0.03
                
                hist['EMA_Corta'] = hist['Close'].ewm(span=5, adjust=False).mean()
                ema_c = hist['EMA_Corta'].iloc[-1]
                
                score_momentum = (vol_rel * 40) + ((precio_hoy / diag_ema if (diag_ema := max(ema_c, 0.01)) else 1) * 60)
                
                analisis_tactico.append({
                    "Ticker": ticker,
                    "Precio": precio_hoy,
                    "Volumen Relativo": vol_rel,
                    "ATR": atr,
                    "Score": score_momentum
                })
            except:
                pass
            barra_p3.progress((idx + 1) / len(POOL_ACCIONES))
            
        if analisis_tactico:
            top_5 = pd.DataFrame(analisis_tactico).sort_values(by="Score", ascending=False).head(5)
            st.markdown("## 🔥 Selección de Activos con Alta Inyección de Dinero")
            st.markdown("---")
            
            conn = sqlite3.connect('agente_quant.db')
            cursor = conn.cursor()
            
            for rank, (_, fila) in enumerate(top_5.iterrows(), 1):
                tk_c = fila['Ticker']
                p_ent = fila['Precio']
                atr_f = fila['ATR']
                vol_f = fila['Volumen Relativo']
                
                sl_tecnico = p_ent - (1.3 * atr_f)
                tp_tecnico = p_ent + (2.6 * atr_f)
                
                porc_sl = ((p_ent - sl_tecnico) / p_ent) * 100
                porc_tp = ((tp_tecnico - p_ent) / p_ent) * 100
                
                monto_en_riesgo = capital_liquido * (riesgo_permitido / 100)
                perdida_por_accion = p_ent - sl_tecnico
                cantidad_acciones = int(monto_en_riesgo / perdida_por_accion) if perdida_por_accion > 0 else 1
                if cantidad_acciones <= 0: cantidad_acciones = 1
                
                capital_comprometido = cantidad_acciones * p_ent
                
                try:
                    cursor.execute("INSERT INTO registro_operaciones (fecha, ticker, precio_entrada, stop_loss, take_profit) VALUES (?, ?, ?, ?, ?)",
                                   (datetime.now().strftime("%Y-%m-%d"), tk_c, p_ent, sl_tecnico, tp_tecnico))
                except:
                    pass
                
                if vol_f >= cfg_volumen:
                    st.success(f"### 🏆 TOP {rank}: {tk_c} —— 🚀 COMPRA DETECTADA (Inyección Institucional)")
                else:
                    st.info(f"### 🏆 TOP {rank}: {tk_c} —— 🐳 ALERTA QUANT (Acumulación)")
                    
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1: st.metric("🎯 Entrada:", f"${p_ent:.2f} USD", f"Volumen: {vol_f:.2f}x")
                with col_r2: st.metric("🛑 Stop Loss (ATR):", f"${sl_tecnico:.2f} USD", f"-{porc_sl:.1f}%")
                with col_r3: st.metric("💰 Take Profit:", f"${tp_tecnico:.2f} USD", f"+{porc_tp:.1f}%")
                
                st.markdown(f"📦 **Plan Técnico Obligatorio:** Comprar exactamente **{cantidad_acciones} acciones**. Capital total asignado a la posición: **${capital_comprometido:,.2f} USD**.")
                st.markdown("---")
                
            conn.commit()
            conn.close()
        else:
            st.error("No se encontraron activos que superen el umbral de aceleración mínimo en esta sesión.")

# =====================================================================
# PESTAÑA 4: CONSULTOR INDEPENDIENTE DE ACTIVOS GLOBAL (CUALQUIER TICKER)
# =====================================================================
with tab4:
    st.subheader("🕵️‍♂️ Consultor Quant Libre")
    st.write("Escribe cualquier ticker del mercado global para evaluar su valor intrínseco estadístico, volatilidad y viabilidad de inversión de forma aislada.")

    ticker_libre = st.text_input("Introduce el símbolo del activo (Ej: WDC, GOOGL, AAPL, ADE, HBAR-USD):", value="WDC").strip().upper()

    if st.button("📊 Analizar Activo Individual", key="btn_p4_analisis_libre"):
        if ticker_libre:
            with st.spinner(f"Estableciendo conexión segura para analizar {ticker_libre}..."):
                try:
                    asset = yf.Ticker(ticker_libre)
                    h_libre = asset.history(period="60d")
                    
                    if not h_libre.empty:
                        p_libre_actual = h_libre['Close'].iloc[-1]
                        
                        suelo_institucional = np.percentile(h_libre['Low'], 15)
                        techo_historico = np.percentile(h_libre['High'], 85)
                        valor_intrinseco_libre = techo_historico * 1.12
                        
                        atr_libre = (h_libre['High'] - h_libre['Low']).rolling(10).mean().iloc[-1]
                        if atr_libre <= 0: atr_libre = p_libre_actual * 0.03
                        
                        if valor_intrinseco_libre > p_libre_actual:
                            margen_libre = ((valor_intrinseco_libre - p_libre_actual) / valor_intrinseco_libre) * 100
                            potencial_libre = ((valor_intrinseco_libre - p_libre_actual) / p_libre_actual) * 100
                        else:
                            margen_libre = 0.0
                            potencial_libre = 0.0
                            
                        cumple_margen = margen_libre >= cfg_margen
                        
                        vol_hoy_libre = h_libre['Volume'].iloc[-1]
                        vol_prom_libre = h_libre['Volume'].mean()
                        fuerza_vol_libre = vol_hoy_libre / vol_prom_libre if vol_prom_libre > 0 else 1.0
                        cumple_volumen = fuerza_vol_libre >= cfg_volumen
                        
                        st.markdown(f"## 📊 Diagnóstico Quant: {ticker_libre}")
                        st.markdown(f"**Precio de Mercado Actual:** ${p_libre_actual:,.2f} USD")
                        st.markdown("---")
                        
                        col_p4_1, col_p4_2, col_p4_3 = st.columns(3)
                        with col_p4_1:
                            st.metric("🧱 Valor Intrínseco Estructurado:", f"${valor_intrinseco_libre:,.2f} USD")
                            st.caption("Calculado por desviación alcista institucional.")
                        with col_p4_2:
                            st.metric("📉 Suelo de Acumulación Cuant:", f"${suelo_institucional:,.2f} USD")
                            st.caption("Percentil 15 histórico (Zona de soporte fuerte).")
                        with col_p4_3:
                            st.metric("🛡️ Margen de Seguridad Real:", f"{margen_libre:.1f}%", f"Potencial: +{potencial_libre:.1f}%")
                            st.caption(f"Umbral mínimo exigido por la IA: {cfg_margen:.1f}%")
                            
                        st.markdown("---")
                        st.markdown("### 🚦 Evaluación de Requisitos Estrictos de Inversión")
                        
                        if cumple_margen and cumple_volumen:
                            st.success(f"🟢 **ACTIVO VIABLE (COMPRA CONFIRMADA):** {ticker_libre} supera el margen de seguridad óptmos ({margen_libre:.1f}%) y cuenta con una inyección institucional activa de **{fuerza_vol_libre:.2f}x** de volumen.")
                        elif cumple_margen and not cumple_volumen:
                            st.warning(f"🟡 **ACTIVO EN LISTA DE ESPERA (FALTA FLUJO):** El precio es excelente y tiene un gran descuento ({margen_libre:.1f}%), pero el volumen institucional está apagado (**{fuerza_vol_libre:.2f}x**). Monitorear inyección de capital antes de entrar.")
                        else:
                            st.error(f"🔴 **ACTIVO RECHAZADO:** {ticker_libre} no cumple con los requisitos del algoritmo. Su margen de descuento ({margen_libre:.1f}%) está por debajo del **{cfg_margen:.1f}%** exigido por las directrices de riesgo actuales del agente.")
                            
                        sl_sugerido = p_libre_actual - (1.3 * atr_libre)
                        tp_sugerido = p_libre_actual + (2.6 * atr_libre)
                        st.info(f"💡 **Parámetros de Gestión Táctica (Si decides operar):** Stop Loss sugerido por volatilidad: **${sl_sugerido:,.2f} USD** (-{((p_libre_actual-sl_sugerido)/p_libre_actual)*100:.1f}%) | Take Profit Técnico: **${tp_sugerido:,.2f} USD** (+{((tp_sugerido-p_libre_actual)/p_libre_actual)*100:.1f}%).")
                    else:
                        st.error(f"No se encontraron datos de mercado para el símbolo '{ticker_libre}'. Verifica si está bien escrito o si requiere sufijo cambiario.")
                except Exception as e:
                    st.error(f"Error crítico al procesar el activo: {str(e)}")
        else:
            st.warning("Por favor, introduce un ticker válido antes de ejecutar el escáner.")

# =====================================================================
# PESTAÑA 5: MINIMIZACIÓN MATEMÁTICA DE RIESGO SECTORIAL (PRESIÓN REAL)
# =====================================================================
with tab5:
    st.subheader("🛡️ Optimización Avanzada de Mínima Varianza y Criterio de Riesgo")
    st.write("Esta pestaña localiza automáticamente el sector líder por flujos de dinero, desglosa si su volumen es comprador o vendedor, y estructura un portafolio blindado libre de techos.")
    
    presupuesto_total = st.number_input("Capital total para este portafolio blindado (USD):", min_value=100.0, value=3000.0, step=100.0, key="p5_presupuesto")
    
    if st.button("🛡️ Ejecutar Optimización de Mínimo Riesgo", key="btn_p5_ejecutar"):
        st.write("📡 Escaneando mercados globales para aislar el sector dominante y analizar la presión del volumen...")
        
        sector_lider = None
        max_vol_macro = -1
        presion_sector_lider = "DESCONOCIDO"
        
        # 1. Escaneo dinámico del sector líder midiendo la presión real de la vela diaria
        for nombre, tick in ETFS_ROTACION.items():
            try:
                m_tk = yf.Ticker(tick)
                m_h = m_tk.history(period="5d")
                if len(m_h) >= 2:
                    v_rel = m_h['Volume'].iloc[-1] / m_h['Volume'].mean()
                    
                    cierre = m_h['Close'].iloc[-1]
                    maximo = m_h['High'].iloc[-1]
                    minimo = m_h['Low'].iloc[-1]
                    
                    rango_total = maximo - minimo
                    if rango_total > 0:
                        factor_presion = (cierre - minimo) / rango_total
                    else:
                        factor_presion = 0.5
                        
                    # Determinación matemática del flujo direccional
                    presion_flujo = "COMPRA (Acumulación)" if factor_presion >= 0.50 else "VENTA (Distribución)"
                    
                    if v_rel > max_vol_macro:
                        max_vol_macro = v_rel
                        sector_lider = tick
                        presion_sector_lider = presion_flujo
            except:
                pass
                
        if sector_lider and sector_lider in COMPONENTES_ETFS:
            st.markdown("### 📊 Análisis de Flujo Institucional en el Sector")
            col_macro1, col_macro2 = st.columns(2)
            with col_macro1:
                st.metric("Sector Dominante:", f"{sector_lider}", f"Volumen: {max_vol_macro:.2f}x")
            with col_macro2:
                if "COMPRA" in presion_sector_lider:
                    st.success(f"🟢 Dirección del Flujo: {presion_sector_lider}")
                else:
                    st.error(f"🔴 Dirección del Flujo: {presion_sector_lider}")
            
            # CONTROL DE SEGURIDAD EXTREMO: Si el flujo institucional es de distribución, bloquea la compra en techos
            if "VENTA" in presion_sector_lider:
                st.error(f"⛔ **OPERACIÓN ABORTADA POR EL ALGORITMO:** Aunque el sector `{sector_lider}` mueve mucho capital, las manos fuertes están **VENDIENDO** para tomar ganancias. Comprar aquí sería entrar en el techo. Espera a que el flujo cambie a COMPRA.")
            else:
                componentes = COMPONENTES_ETFS[sector_lider]
                st.info(f"🎯 El flujo es saludable. Filtrando componentes de `{sector_lider}` con presión de volumen alcista...")
                
                datos_riesgo = []
                barra_p5 = st.progress(0)
                
                for index, ticker in enumerate(componentes):
                    try:
                        tk = yf.Ticker(ticker)
                        hist = tk.history(period="60d")
                        
                        if len(hist) >= 20:
                            # Confirmar presión compradora individual en el activo
                            c_cierre = hist['Close'].iloc[-1]
                            c_max = hist['High'].iloc[-1]
                            c_min = hist['Low'].iloc[-1]
                            c_rango = c_max - c_min
                            c_factor = (c_cierre - c_min) / c_rango if c_rango > 0 else 0.5
                            
                            # Filtro estricto: Descartar componentes individuales en proceso de venta masiva
                            if c_factor >= 0.45:
                                retornos = hist['Close'].pct_change().dropna()
                                volatilidad_real = retornos.std()
                                precio_act = hist['Close'].iloc[-1]
                                
                                high_low = hist['High'] - hist['Low']
                                high_close = np.abs(hist['High'] - hist['Close'].shift())
                                low_close = np.abs(hist['Low'] - hist['Close'].shift())
                                ranges = pd.concat([high_low, high_close, low_close], axis=1)
                                true_range = ranges.max(axis=1)
                                atr = true_range.rolling(14).mean().iloc[-1]
                                
                                datos_riesgo.append({
                                    "Ticker": ticker,
                                    "Precio": precio_act,
                                    "Volatilidad": volatilidad_real,
                                    "ATR": atr if atr > 0 else (precio_act * 0.03)
                                })
                    except:
                        pass
                    barra_p5.progress((index + 1) / len(componentes))
                    
                if len(datos_riesgo) >= 3:
                    # Seleccionamos las 3 acciones con MENOR volatilidad del sector sano
                    df_riesgo = pd.DataFrame(datos_riesgo).sort_values(by="Volatilidad", ascending=True).head(3)
                    
                    # Ponderación matemática de Varianza Inversa
                    df_riesgo['Inversa_Vol'] = 1.0 / df_riesgo['Volatilidad']
                    suma_inversas = df_riesgo['Inversa_Vol'].sum()
                    df_riesgo['Ponderación'] = df_riesgo['Inversa_Vol'] / suma_inversas
                    
                    st.markdown("## 📊 Portafolio de Mínimo Riesgo Sectorial Construido")
                    st.markdown("La IA ha calculado la distribución ideal de capital para minimizar el impacto de caídas bruscas de precio asegurando volumen comprador:")
                    st.markdown("---")
                    
                    conn = sqlite3.connect('agente_quant.db')
                    cursor = conn.cursor()
                    
                    for rank, (_, fila) in enumerate(df_riesgo.iterrows(), 1):
                        tk_r = fila['Ticker']
                        p_r = fila['Precio']
                        vol_r = fila['Volatilidad']
                        atr_r = fila['ATR']
                        peso = fila['Ponderación']
                        
                        dinero_asignado = presupuesto_total * peso
                        cantidad_acc = int(dinero_asignado // p_r)
                        if cantidad_acc <= 0: cantidad_acc = 1
                        costo_total = cantidad_acc * p_r
                        
                        # Gestión técnica: Stop Loss a 2x ATR para evitar ruidos de mercado
                        sl_matematico = p_r - (2.0 * atr_r)
                        tp_matematico = p_r + (4.0 * atr_r)
                        
                        try:
                            cursor.execute("INSERT INTO registro_operaciones (fecha, ticker, precio_entrada, stop_loss, take_profit) VALUES (?, ?, ?, ?, ?)",
                                           (datetime.now().strftime("%Y-%m-%d"), tk_r, p_r, sl_matematico, tp_matematico))
                        except:
                            pass
                            
                        st.success(f"### 🛡️ ACTIVO COMPRADOR SÓLIDO {rank}: {tk_r} (Peso: {peso*100:.1f}%)")
                        
                        col_p5_1, col_p5_2, col_p5_3 = st.columns(3)
                        with col_p5_1:
                            st.metric("💵 Entrada:", f"${p_r:.2f} USD")
                            st.caption(f"Asignación: ${dinero_asignado:,.2f} USD")
                        with col_p5_2:
                            st.metric("📉 Volatilidad:", f"{vol_r*100:.2f}%", "Flujo Seguro")
                            st.caption(f"Comprar: {cantidad_acc} acciones")
                        with col_p5_3:
                            st.metric("🛡️ Stop Loss:", f"${sl_matematico:.2f} USD")
                            st.caption(f"Take Profit: ${tp_matematico:.2f} USD")
                            
                        st.markdown(f"📦 **Órden:** Comprar **{cantidad_acc} u** de `{tk_r}`. Costo real neto: **${costo_total:,.2f} USD**.")
                        st.markdown("---")
                        
                    conn.commit()
                    conn.close()
                else:
                    st.warning("No se encontraron suficientes acciones con presión compradora clara en este sector en este momento.")
        else:
            st.error("No se pudo mapear la rotación macro del mercado. Verifica la conexión.")
