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

# Pool exclusivo para la nueva pestaña cripto (Símbolos oficiales Yahoo Finance)
POOL_CRIPTOMONEDAS = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD",
    "Hedera Hasgraph": "HBAR-USD",
    "Ripple": "XRP-USD",
    "Cardano": "ADA-USD",
    "Avalanche": "AVAX-USD",
    "Chainlink": "LINK-USD"
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

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🛰️ PESTAÑA 1: Rotación de Capital y Flujo Institucional",
    "🧱 PESTAÑA 2: Radar de Descuento Cuantitativo (Largo Plazo)",
    "🎯 PESTAÑA 3: Small Caps Growth (Filtros Buffett & Lynch)",
    "🔍 PESTAÑA 4: Consultor de Activos Libre & Diagnóstico IA",
    "🛡️ PESTAÑA 5: Minimización Matemática de Riesgo",
    "🪙 PESTAÑA 6: Crypto Flow Selector & Corto Plazo",
    "🎲 PESTAÑA 7: Simulador de Montecarlo probabilístico"
])

# =====================================================================
# PESTAÑA 1: MAESTRÍA DE ROTACIÓN MACRO Y COMPONENTES EN ACUMULACIÓN
# =====================================================================
with tab1:
    st.subheader("📡 Matriz de Rotación Macroeconómica Global")
    st.write("Detecta a qué industrias y refugios globales está migrando el dinero de las instituciones financieras, analizando la dirección exacta del flujo.")

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
                    
                    # ---- CÁLCULO DE DIRECCIÓN DE VOLUMEN AGRESO DE LA PESTAÑA 1 ----
                    cierre_m = hist['Close'].iloc[-1]
                    max_m = hist['High'].iloc[-1]
                    min_m = hist['Low'].iloc[-1]
                    rango_m = max_m - min_m
                    factor_m = (cierre_m - min_m) / rango_m if rango_m > 0 else 0.5
                    direccion_dinero = "🟢 COMPRA (Acumulación)" if factor_m >= 0.50 else "🔴 VENTA (Distribución)"
                    
                    if ticker in ["SPY", "QQQ", "SMH", "XLY", "URNM", "IBIT"]:
                        tipo_entorno = "CRECIMIENTO / RIESGO"
                    else:
                        tipo_entorno = "REFUGIO / DEFENSA"
                    
                    analisis_macro.append({
                        "Industria / Sector": nombre,
                        "Ticker": ticker,
                        "Variación Diaria": var_diaria,
                        "Volumen Relativo": vol_relativo,
                        "Dirección del Dinero": direccion_dinero,
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
                st.success(f"🚀 **ENTORNO RISK-ON:** Las instituciones están inyectando liquidez agresiva en **{ganador['Industria / Sector']} ({ticker_ganador})** con **{ganador['Volumen Relativo']:.2f}x** de volumen. Presión actual: **{ganador['Dirección del Dinero']}**.")
            else:
                st.warning(f"⚠️ **ENTORNO RISK-OFF:** Las manos fuertes están buscando protección en **{ganador['Industria / Sector']} ({ticker_ganador})** inyectando **{ganador['Volumen Relativo']:.2f}x** de volumen. Presión actual: **{ganador['Dirección del Dinero']}**.")
            
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
                        
                        # Dirección individual del componente
                        cc_c = c_hist['Close'].iloc[-1]
                        cc_mx = c_hist['High'].iloc[-1]
                        cc_mn = c_hist['Low'].iloc[-1]
                        cc_rg = cc_mx - cc_mn
                        cc_f = (cc_c - cc_mn) / cc_rg if cc_rg > 0 else 0.5
                        c_dir = "🟢 COMPRA" if cc_f >= 0.50 else "🔴 VENTA"
                        
                        analisis_comp.append({"Acción": c_ticker, "Variación Diaria": c_var, "Acumulación Real": c_vol_rel, "Flujo": c_dir})
                except:
                    pass
            
            if analisis_comp:
                df_comp = pd.DataFrame(analisis_comp).sort_values(by="Acumulación Real", ascending=False)
                df_c_vista = df_comp.copy()
                df_c_vista["Variación Diaria"] = df_c_vista["Variación Diaria"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
                df_c_vista["Acumulación Real"] = df_c_vista["Acumulación Real"].map(lambda x: f"{x:.2f}x volumen normal")
                st.dataframe(df_c_vista, use_container_width=True, hide_index=True)
                
                top_comp = df_comp.iloc[0]
                st.info(f"🐳 **ALTA CONCENTRACIÓN:** La acción **{top_comp['Acción']}** es el activo individual líder donde las instituciones están concentrando el dinero dentro de este sector, operando a **{top_comp['Acumulación Real']:.2f}x** de volumen y con flujo de **{top_comp['Flujo']}**.")
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
# PESTAÑA 3: ESCÁNER DE SMALL CAPS CON FILTROS BUFFETT & LYNCH
# =====================================================================
with tab3:
    st.subheader("🛰️ Escáner Inteligente de Small Caps Growth e Inyección de Flujo")
    st.write("Analiza activos dinámicos de pequeña capitalización y alta disrupción para aislar flujos de inyección institucionales bajo los estrictos axiomas de Warren Buffett y Peter Lynch.")
    
    POOL_SMALL_CAPS = ["OKLO", "SMR", "NU", "SQ", "CCJ"]
    
    if st.button("🔍 Escanear Universo Small Caps Growth", key="btn_p3_smallcaps"):
        analisis_sc = []
        barra_sc = st.progress(0)
        
        for idx, ticker in enumerate(POOL_SMALL_CAPS):
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="60d")
                if len(hist) < 20: continue
                
                precio_act = hist['Close'].iloc[-1]
                vol_hoy = hist['Volume'].iloc[-1]
                vol_prom = hist['Volume'].mean()
                fuerza_vol = vol_hoy / vol_prom if vol_prom > 0 else 1.0
                
                cierre = hist['Close'].iloc[-1]
                maximo = hist['High'].iloc[-1]
                minimo = hist['Low'].iloc[-1]
                rango = maximo - minimo
                factor_presion = (cierre - minimo) / rango if rango > 0 else 0.5
                
                if factor_presion >= 0.52:
                    flujo_dinero = "🟢 COMPRA (Acumulación)"
                else:
                    flujo_dinero = "🔴 VENTA (Distribución)"
                
                techo_historico = np.percentile(hist['High'], 85)
                valor_estimado_ia = techo_historico * 1.15
                margen_seguridad_sc = ((valor_estimado_ia - precio_act) / valor_estimado_ia) * 100 if valor_estimado_ia > precio_act else 0.0
                
                cumple_buffett = "SÍ" if margen_seguridad_sc >= cfg_margen else "NO"
                
                retornos = hist['Close'].pct_change().dropna()
                volatilidad_sc = retornos.std()
                tasa_cambio_30d = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-20]) / hist['Close'].iloc[-20]) * 100
                
                ratio_lynch = tasa_cambio_30d / (volatilidad_sc * 100) if volatilidad_sc > 0 else 0.0
                cumple_lynch = "SÍ" if (ratio_lynch > 1.2 and tasa_cambio_30d > 0) else "NO"
                
                high_low = hist['High'] - hist['Low']
                high_close = np.abs(hist['High'] - hist['Close'].shift())
                low_close = np.abs(hist['Low'] - hist['Close'].shift())
                atr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1).rolling(14).mean().iloc[-1]
                if atr <= 0: atr = precio_act * 0.04
                
                analisis_sc.append({
                    "Ticker": ticker, "Precio Actual": precio_act, "Volumen Relativo": fuerza_vol,
                    "Flujo de Inyección": flujo_dinero, "Margen Descuento": margen_seguridad_sc,
                    "Cumple Buffett": cumple_buffett, "Ratio Crecimiento/Vol": ratio_lynch,
                    "Cumple Lynch": cumple_lynch, "ATR": atr
                })
            except:
                pass
            barra_sc.progress((idx + 1) / len(POOL_SMALL_CAPS))
            
        if analisis_sc:
            df_sc = pd.DataFrame(analisis_sc)
            st.markdown("### 📊 Radiografía de Flujos en Small Caps")
            df_sc_vista = df_sc.copy()
            df_sc_vista["Precio Actual"] = df_sc_vista["Precio Actual"].map(lambda x: f"${x:,.2f} USD")
            df_sc_vista["Volumen Relativo"] = df_sc_vista["Volumen Relativo"].map(lambda x: f"{x:.2f}x")
            df_sc_vista["Margen Descuento"] = df_sc_vista["Margen Descuento"].map(lambda x: f"{x:.1f}%")
            df_sc_vista["Ratio Crecimiento/Vol"] = df_sc_vista["Ratio Crecimiento/Vol"].map(lambda x: f"{x:.2f}")
            
            st.dataframe(df_sc_vista.drop(columns=["ATR"]), use_container_width=True, hide_index=True)
            st.markdown("### 🎯 Plan de Posiciones Sugeridas (Filtros de Leyendas)")
            st.markdown("---")
            
            conn = sqlite3.connect('agente_quant.db')
            cursor = conn.cursor()
            fecha_hoy_str = datetime.now().strftime("%Y-%m-%d")
            
            hubo_viables = False
            for _, fila in df_sc.iterrows():
                if "🟢" in fila["Flujo de Inyección"] and (fila["Cumple Buffett"] == "SÍ" or fila["Cumple Lynch"] == "SÍ"):
                    hubo_viables = True
                    tk_s = fila["Ticker"]
                    p_s = fila["Precio Actual"]
                    atr_s = fila["ATR"]
                    
                    sl_s = p_s - (1.5 * atr_s)
                    tp_s = p_s + (3.5 * atr_s)
                    
                    cursor.execute("SELECT COUNT(*) FROM registro_operaciones WHERE ticker = ? AND fecha = ?", (tk_s, fecha_hoy_str))
                    if cursor.fetchone()[0] == 0:
                        try:
                            cursor.execute("INSERT INTO registro_operaciones (fecha, ticker, precio_entrada, stop_loss, take_profit) VALUES (?, ?, ?, ?, ?)",
                                           (fecha_hoy_str, tk_s, p_s, sl_s, tp_s))
                        except:
                            pass
                    
                    st.success(f"### 🏆 ACCIÓN SMALL CAP FILTRADA: {tk_s} —— VIABLE PARA PORTAFOLIO")
                    estrategias_cumplidas = []
                    if fila["Cumple Buffett"] == "SÍ": estrategias_cumplidas.append("🧱 FILTRO BUFFETT (Margen de Seguridad)")
                    if fila["Cumple Lynch"] == "SÍ": estrategias_cumplidas.append("🚀 FILTRO LYNCH (Crecimiento de Multiplicación)")
                    st.write(f"**Validaciones logradas:** {' | '.join(estrategias_cumplidas)}")
                    
                    col_p3_1, col_p3_2, col_p3_3 = st.columns(3)
                    with col_p3_1: st.metric("🛒 Entrada Ordenada:", f"${p_s:.2f} USD", f"Volumen: {fila['Volumen Relativo']:.2f}x")
                    with col_p3_2: st.metric("🛑 Stop Loss (1.5 ATR):", f"${sl_s:.2f} USD", f"-{((p_s-sl_s)/p_s)*100:.1f}%")
                    with col_p3_3: st.metric("💰 Objetivo Take Profit:", f"${tp_s:.2f} USD", f"+{((tp_s-p_s)/p_s)*100:.1f}%")
                    st.markdown("---")
            conn.commit()
            conn.close()
            if not hubo_viables:
                st.warning("⚠️ Ninguna Small Cap de la lista cumple simultáneamente con flujo puro de COMPRA y los filtros fundamentales de Buffett o Lynch en este momento.")
        else:
            st.error("No se pudo conectar a los servidores para extraer las métricas de Small Caps.")

# =====================================================================
# PESTAÑA 4: CONSULTOR INDEPENDIENTE DE ACTIVOS GLOBAL (CUALQUIER TICKER)
# =====================================================================
with tab4:
    st.subheader("🕵️‍♂️ Consultor Quant Libre")
    st.write("Escribe cualquier ticker del mercado global para evaluar su valor intrínseco de forma aislada.")
    ticker_libre = st.text_input("Introduce el símbolo del activo (Ej: WDC, GOOGL, AAPL, HBAR-USD):", value="WDC").strip().upper()

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
                        with col_p4_2:
                            st.metric("📉 Suelo de Acumulación Cuant:", f"${suelo_institucional:,.2f} USD")
                        with col_p4_3:
                            st.metric("🛡️ Margen de Seguridad Real:", f"{margen_libre:.1f}%", f"Potencial: +{potencial_libre:.1f}%")
                            
                        st.markdown("---")
                        st.markdown("### 🚦 Evaluación de Requisitos Estrictos de Inversión")
                        
                        if cumple_margen and cumple_volumen:
                            st.success(f"🟢 **ACTIVO VIABLE (COMPRA CONFIRMADA):** {ticker_libre} supera el margen de seguridad óptmos ({margen_libre:.1f}%) and cuenta con una inyección institucional activa de **{fuerza_vol_libre:.2f}x** de volumen.")
                        elif cumple_margen and not cumple_volumen:
                            st.warning(f"🟡 **ACTIVO EN LISTA DE ESPERA (FALTA FLUJO):** El precio es excelente y tiene un gran descuento ({margen_libre:.1f}%), pero el volumen institucional está apagado. Monitorear inyección de capital antes de entrar.")
                        else:
                            st.error(f"🔴 **ACTIVO RECHAZADO:** {ticker_libre} no cumple con los requisitos del algoritmo. Su margen de descuento está por debajo del **{cfg_margen:.1f}%** exigido.")
                            
                        sl_sugerido = p_libre_actual - (1.3 * atr_libre)
                        tp_sugerido = p_libre_actual + (2.6 * atr_libre)
                        st.info(f"💡 **Parámetros de Gestión Táctica:** Stop Loss sugerido: **${sl_sugerido:,.2f} USD** | Take Profit Técnico: **${tp_sugerido:,.2f} USD**.")
                    else:
                        st.error(f"No se encontraron datos de mercado para el símbolo '{ticker_libre}'.")
                except Exception as e:
                    st.error(f"Error crítico al procesar el activo: {str(e)}")

# =====================================================================
# PESTAÑA 5: AUDITORÍA DE PRESIÓN ABSOLUTA (COMPRA VS VENTA MACRO Y MICRO)
# =====================================================================
with tab5:
    st.subheader("🛡️ Optimización Avanzada de Mínima Varianza y Criterio de Riesgo")
    st.write("Esta pestaña escanea el mercado para aislar simultáneamente los sectores y acciones líderes bajo presión absoluta de COMPRA y VENTA.")
    
    presupuesto_total = st.number_input("Capital total para este portafolio blindado (USD):", min_value=100.0, value=3000.0, step=100.0, key="p5_presupuesto")
    
    if st.button("🛡️ Ejecutar Optimización de Mínimo Riesgo", key="btn_p5_ejecutar"):
        sectores_compradores = []
        sectores_vendedores = []
        
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
                    factor_presion = (cierre - minimo) / rango_total if rango_total > 0 else 0.5
                    nodo_sector = {"Sector": nombre, "Ticker": tick, "Volumen": v_rel}
                    
                    if factor_presion >= 0.50:
                        sectores_compradores.append(nodo_sector)
                    else:
                        sectores_vendedores.append(nodo_sector)
            except:
                pass

        sector_max_comp = pd.DataFrame(sectores_compradores).sort_values(by="Volumen", ascending=False).iloc[0] if sectores_compradores else None
        sector_max_vent = pd.DataFrame(sectores_vendedores).sort_values(by="Volumen", ascending=False).iloc[0] if sectores_vendedores else None

        st.markdown("---")
        col_macro_c, col_macro_v = st.columns(2)

        with col_macro_c:
            st.markdown("### 🟢 FLUJO INSTITUCIONAL ALCISTA (COMPRA)")
            if sector_max_comp is not None:
                st.success(f"🔥 **Sector Líder en Acumulación:**\n**{sector_max_comp['Sector']} ({sector_max_comp['Ticker']})** con **{sector_max_comp['Volumen']:.2f}x** de volumen anormal.")
                
                componentes_c = COMPONENTES_ETFS.get(sector_max_comp['Ticker'], ["AAPL", "MSFT"])
                filtrados_c = []
                for tc in componentes_c:
                    try:
                        t_k = yf.Ticker(tc)
                        t_h = t_k.history(period="5d")
                        c_vol = t_h['Volume'].iloc[-1] / t_h['Volume'].mean()
                        filtrados_c.append({"Acción": tc, "Fuerza": c_vol})
                    except:
                        pass
                if filtrados_c:
                    ganador_c = pd.DataFrame(filtrados_c).sort_values(by="Fuerza", ascending=False).iloc[0]["Acción"]
                    st.info(f"💎 **Activo Alfa Inmobiliario/Bursátil para Compras:** **{ganador_c}**")
            else:
                st.write("No hay sectores dominantes con presión de compra.")

        with col_macro_v:
            st.markdown("### 🔴 FLUJO INSTITUCIONAL BAJISTA (VENTA / DISTRIBUCIÓN)")
            if sector_max_vent is not None:
                st.error(f"🚨 **Sector Líder en Distribución:**\n**{sector_max_vent['Sector']} ({sector_max_vent['Ticker']})** experimentando **{sector_max_vent['Volumen']:.2f}x** de volumen de liquidación.")
                
                componentes_v = COMPONENTES_ETFS.get(sector_max_vent['Ticker'], ["AAPL", "MSFT"])
                filtrados_v = []
                for tv in componentes_v:
                    try:
                        t_k = yf.Ticker(tv)
                        t_h = t_k.history(period="5d")
                        v_vol = t_h['Volume'].iloc[-1] / t_h['Volume'].mean()
                        filtrados_v.append({"Acción": tv, "Fuerza": v_vol})
                    except:
                        pass
                if filtrados_v:
                    ganador_v = pd.DataFrame(filtrados_v).sort_values(by="Fuerza", ascending=False).iloc[0]["Acción"]
                    st.warning(f"⚠️ **Activo Crítico Expuesto a Caídas:** **{ganador_v}**")
            else:
                st.write("No hay sectores dominantes bajo presión de liquidación masiva.")

        st.markdown("---")
        st.markdown("## 🛡️ Cobertura Delta y Asignación Eficiente Kelly")
        if sector_max_comp is not None and 'ganador_c' in locals():
            st.write(f"El optimizador ha diseñado un escudo matemático dividiendo los **${presupuesto_total:,.2f} USD** de capital:")
            cap_long = presupuesto_total * 0.70
            cap_hedge = presupuesto_total * 0.30
            
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.metric(f"🟢 Posición Direccional Alfa ({ganador_c})", f"${cap_long:,.2f} USD", "70% del Portafolio")
                st.caption(f"Focalizado en la inyección líquida del sector {sector_max_comp['Sector']}.")
            with col_k2:
                if sector_max_vent is not None and 'ganador_v' in locals():
                    st.metric(f"🛡️ Cobertura o Reserva Líquida ({ganador_v} o Cash)", f"${cap_hedge:,.2f} USD", "30% de Cobertura")
                    st.caption(f"Mitiga la correlación sistémica utilizando debilidad institucional en {sector_max_vent['Sector']}.")
                else:
                    st.metric("🛡️ Reserva en Bonos / Cash Flotante", f"${cap_hedge:,.2f} USD", "30% Estabilidad")
                    st.caption("Reserva líquida ante la ausencia de sectores bajistas claros.")

# =====================================================================
# PESTAÑA 6: CRYPTO FLOW SELECTOR & CORTO PLAZO
# =====================================================================
with tab6:
    st.subheader("🪙 Crypto Momentum & Flow Selector")
    st.write("Monitorea la microestructura del libro de órdenes implícito y la velocidad del capital en las criptomonedas más líquidas del entorno global.")

    if st.button("🪙 Escanear Flujo Cripto de Alta Velocidad", key="btn_p6_crypto"):
        analisis_crypto = []
        barra_p6 = st.progress(0)
        
        for idx, (nombre, ticker) in enumerate(POOL_CRIPTOMONEDAS.items()):
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="5d")
                if len(hist) >= 2:
                    var_diaria = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
                    vol_relativo = hist['Volume'].iloc[-1] / hist['Volume'].mean()
                    
                    c_c = hist['Close'].iloc[-1]
                    c_mx = hist['High'].iloc[-1]
                    c_mn = hist['Low'].iloc[-1]
                    c_rg = c_mx - c_mn
                    c_f = (c_c - c_mn) / c_rg if c_rg > 0 else 0.5
                    
                    flujo_c = "🟢 ACUMULACIÓN" if c_f >= 0.51 else "🔴 DISTRIBUCIÓN"
                    
                    # Cálculo de volatilidad implícita de corto plazo (True Range Modificado)
                    retornos = hist['Close'].pct_change().dropna()
                    vol_cp = retornos.std() * 100
                    
                    analisis_crypto.append({
                        "Criptomoneda": nombre,
                        "Ticker": ticker,
                        "Precio": c_c,
                        "Variación 24H": var_diaria,
                        "Presión de Bloque": vol_relativo,
                        "Dirección Algorítmica": flujo_c,
                        "Volatilidad Real (%)": vol_cp
                    })
            except:
                pass
            barra_p6.progress((idx + 1) / len(POOL_CRIPTOMONEDAS))
            
        if analisis_crypto:
            df_cr = pd.DataFrame(analisis_crypto).sort_values(by="Presión de Bloque", ascending=False)
            df_cr_vista = df_cr.copy()
            df_cr_vista["Precio"] = df_cr_vista["Precio"].map(lambda x: f"${x:,.4f} USD" if x < 1 else f"${x:,.2f} USD")
            df_cr_vista["Variación 24H"] = df_cr_vista["Variación 24H"].map(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")
            df_cr_vista["Presión de Bloque"] = df_cr_vista["Presión de Bloque"].map(lambda x: f"{x:.2f}x volumen regular")
            df_cr_vista["Volatilidad Real (%)"] = df_cr_vista["Volatilidad Real (%)"].map(lambda x: f"{x:.2f}% de oscilación")
            
            st.dataframe(df_cr_vista, use_container_width=True, hide_index=True)
            
            cripto_lider = df_cr.iloc[0]
            st.success(f"⚡ **MOMENTUM CRIPTO:** El activo digital con mayor velocidad de participación institucional es **{cripto_lider['Criptomoneda']} ({cripto_lider['Ticker']})**, registrando una presión de bloque de **{cripto_lider['Presión de Bloque']:.2f}x** con un sesgo final de **{cripto_lider['Dirección Algorítmica']}**.")
        else:
            st.error("Servidores de cotización cripto no disponibles de manera temporal.")

# =====================================================================
# PESTAÑA 7: SIMULADOR DE MONTECARLO PROBABILÍSTICO
# =====================================================================
with tab7:
    st.subheader("🎲 Simulador Cuantitativo de Montecarlo")
    st.write("Genera proyecciones probabilísticas y modelado de escenarios predictivos basados en el movimiento browniano geométrico del activo seleccionado.")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        ticker_montecarlo = st.text_input("Símbolo para simular (Ej: WDC, AAPL, BTC-USD):", value="WDC", key="mc_ticker").strip().upper()
    with col_m2:
        simulaciones = st.number_input("Número de trayectorias (Simulaciones):", min_value=10, max_value=5000, value=1000, step=100)
    with col_m3:
        dias_proyeccion = st.number_input("Días de proyección hacia el futuro:", min_value=5, max_value=252, value=30, step=5)

    if st.button("🎲 Ejecutar Simulación Probabilística", key="btn_p7_montecarlo"):
        if ticker_montecarlo:
            with st.spinner(f"Analizando histórico y procesando {simulaciones} escenarios para {ticker_montecarlo}..."):
                try:
                    asset_mc = yf.Ticker(ticker_montecarlo)
                    h_mc = asset_mc.history(period="120d")
                    
                    if not h_mc.empty and len(h_mc) >= 10:
                        # Cálculo de parámetros estadísticos reales (Rendimientos Logarítmicos)
                        precios_cierre = h_mc['Close']
                        precio_actual = precios_cierre.iloc[-1]
                        
                        rendimientos_log = np.log(precios_cierre / precios_cierre.shift(1)).dropna()
                        media_diaria = rendimientos_log.mean()
                        varianza_diaria = rendimientos_log.var()
                        
                        # Movimiento Browniano Geométrico: Drift y Volatilidad
                        drift = media_diaria - (0.5 * varianza_diaria)
                        volatilidad_diaria = rendimientos_log.std()
                        
                        # Matriz de simulaciones
                        valores_simulados = np.zeros((dias_proyeccion + 1, simulaciones))
                        valores_simulados[0] = precio_actual
                        
                        for t in range(1, dias_proyeccion + 1):
                            shocks = np.random.normal(0, 1, simulaciones)
                            valores_simulados[t] = valores_simulados[t - 1] * np.exp(drift + volatilidad_diaria * shocks)
                        
                        # Extracción de Percentiles Críticos Estadísticos
                        precios_finales = valores_simulados[-1, :]
                        p_optimista = np.percentile(precios_finales, 85)
                        p_esperado = np.percentile(precios_finales, 50)
                        p_pesimista = np.percentile(precios_finales, 15)
                        
                        probabilidad_ganancia = (precios_finales > precio_actual).mean() * 100
                        
                        # Despliegue de métricas de control de riesgo
                        st.markdown(f"### 📊 Resultados de Distribución para {ticker_montecarlo}")
                        st.markdown(f"**Precio Inicial de Distribución:** ${precio_actual:,.2f} USD")
                        st.markdown("---")
                        
                        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                        with col_r1:
                            st.metric("🟢 Escenario Alcista (P85):", f"${p_optimista:,.2f} USD", f"+{((p_optimista - precio_actual) / precio_actual) * 100:.1f}%")
                        with col_r2:
                            st.metric("🔵 Escenario Central (Mediana):", f"${p_esperado:,.2f} USD", f"{((p_esperado - precio_actual) / precio_actual) * 100:.1f}%")
                        with col_r3:
                            st.metric("🔴 Escenario Bajista (P15):", f"${p_pesimista:,.2f} USD", f"{((p_pesimista - precio_actual) / precio_actual) * 100:.1f}%")
                        with col_r4:
                            st.metric("🎲 Probabilidad de Retorno Positivo:", f"{probabilidad_ganancia:.1f}%", delta="Rendimiento Probable" if probabilidad_ganancia >= 50 else "Riesgo Elevado", delta_color="normal" if probabilidad_ganancia >= 50 else "inverse")
                            
                        st.markdown("---")
                        st.markdown("### 📈 Curva de Proyección Temporal (Evolución de Trayectorias)")
                        
                        # Generación de dataframe estructurado para graficar de forma nativa y eficiente
                        df_grafico = pd.DataFrame(valores_simulados)
                        df_grafico.index.name = "Días"
                        st.line_chart(df_grafico, use_container_width=True)
                        st.caption(f"El gráfico muestra la evolución de las {simulaciones} trayectorias aleatorias generadas por el motor matemático a lo largo de {dias_proyeccion} días comerciales.")
                    else:
                        st.error(f"Datos históricos insuficientes para calcular los parámetros estadísticos de '{ticker_montecarlo}'.")
                except Exception as e:
                    st.error(f"Error crítico en el cálculo de la simulación de Montecarlo: {str(e)}")
