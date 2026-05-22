import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

# =====================================================================
# 1. MOTOR DE MEMORIA E INTELIGENCIA (100% GRATUITO Y PERSISTENTE)
# =====================================================================
def inicializar_base_datos():
    """Crea la base de datos local si no existe en la carpeta"""
    conn = sqlite3.connect('agente_memoria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portafolio_radar (
            ticker TEXT PRIMARY KEY,
            empresa TEXT,
            fecha_registro TEXT,
            precio_entrada REAL,
            valor_intrinseco REAL,
            plazo_sugerido TEXT,
            margen_seguridad REAL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_accion_en_memoria(ticker, empresa, precio, valor_int, plazo, margen):
    """Guarda una oportunidad seleccionada por el usuario sin perder los datos"""
    conn = sqlite3.connect('agente_memoria.db')
    cursor = conn.cursor()
    try:
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT OR REPLACE INTO portafolio_radar 
            (ticker, empresa, fecha_registro, precio_entrada, valor_intrinseco, plazo_sugerido, margen_seguridad)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (ticker, empresa, fecha_hoy, precio, valor_int, plazo, margen))
        conn.commit()
        st.success(f"💾 {ticker} guardada en la memoria del archivo local con éxito.")
    except Exception as e:
        st.error(f"Error al escribir en la base de datos: {e}")
    finally:
        conn.close()

# Inicializar almacenamiento de la base de datos al arrancar
inicializar_base_datos()

# Inicializar la memoria temporal de Streamlit para evitar el 'efecto olvido'
if "resultados_radar" not in st.session_state:
    st.session_state.resultados_radar = None
if "indices_radar" not in st.session_state:
    st.session_state.indices_radar = None
if "total_analizadas" not in st.session_state:
    st.session_state.total_analizadas = 0
if "descartadas" not in st.session_state:
    st.session_state.descartadas = 0

# =====================================================================
# 2. CONFIGURACIÓN DE LA INTERFAZ
# =====================================================================
st.set_page_config(page_title="Agente IA: Terminal Macro & Memoria", layout="wide")

st.title("🤖 Agente IA: Terminal Macro Global & Sistema de Aprendizaje")
st.markdown("### Inteligencia de Capitales: Radar de Flujos, Horizontes Temporales y Bitácora de Auto-Corrección Asertiva.")
st.markdown("---")

# Barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

# Pestañas principales
tab1, tab2, tab3 = st.tabs([
    "🔍 Auditoría Manual", 
    "🛰️ Radar Macroeconómico e Índices del Mundo",
    "🧱 Rotación de Sectores y Flujo de Capital"
])

# =====================================================================
# PESTAÑA 1: AUDITORÍA MANUAL
# =====================================================================
with tab1:
    st.subheader("Auditoría personalizada de activos")
    tickers_input = st.text_input("Introduce los tickers clave (ej: GOOGL, V, NKE, TGT):", "GOOGL, V, NKE, TGT")
    lista_tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if st.button("🚀 Ejecutar Análisis de Confluencia", key="btn_manual"):
        if not lista_tickers:
            st.warning("Introduce tickers válidos.")
        else:
            resultados = []
            with st.spinner("Agente procesando métricas fundamentales..."):
                for t in lista_tickers:
                    try:
                        ticker = yf.Ticker(t)
                        info = ticker.info
                        precio = info.get('currentPrice', 0)
                        eps = info.get('trailingEps', 0)
                        crecimiento = info.get('earningsGrowth', 0.05) or 0.05
                        if crecimiento <= 0: crecimiento = 0.05
                        
                        if eps and eps > 0:
                            valor_intrinseco = eps * (8.5 + (2 * (crecimiento * 100)))
                            if valor_intrinseco > precio:
                                desc = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                                op = f"SÍ ({desc:.1f}% Desc.) 🔥"
                                det = "Infravalorada. Buen punto de entrada estratégico."
                            else:
                                op = "NO ❌"
                                det = "Cotiza a precio justo o sobrevalorada."
                        else:
                            valor_intrinseco = 0
                            op = "N/D"
                            det = "EPS ausente o negativo."

                        resultados.append({
                            "Ticker": t, "Empresa": info.get('longName', t), "Precio": f"${precio:.2f}",
                            "Valor Intrínseco": f"${valor_intrinseco:.2f}" if valor_intrinseco > 0 else "N/D",
                            "¿Oportunidad?": op, "Dictamen": det
                        })
                    except:
                        pass
            if resultados:
                st.dataframe(pd.DataFrame(resultados), use_container_width=True)

# =====================================================================
# PESTAÑA 2: RADAR MACRO + ESCANEO PERSISTENTE AMPLIO
# =====================================================================
with tab2:
    st.subheader("🛰️ Sistema de Rastreo Global y Filtro Fundamental en Tiempo Real")
    
    enfoque_mercado = st.selectbox(
        "Selecciona el universo de mercado a auditar hoy:",
        [
            "S&P 500 (Grandes Monopolios y Consumo) 🏢", 
            "NASDAQ / NASDAQ 100 (Tecnología, Semiconductores e IA) 🚀", 
            "Dow Jones (Aristócratas e Industria Pesada) 🏗️", 
            "Russell 2000 (Joyas y Small Caps de Crecimiento Estricto) 🌱",
            "Escanear Todo el Mercado Integrado (Espectro Completo) 🌍"
        ], key="sb_p2"
    )
    
    margen_exigido = st.slider("Margen de Seguridad Mínimo Exigido (%)", 5, 40, 20, key="slider_macro_p2")

    if st.button("🛰️ Lanzar Algoritmo de Búsqueda Global", key="btn_auto"):
        # 1. Escaneo de Índices de Referencia (Añadido Dow Jones)
        indices_dict = {"S&P 500": "^GSPC", "NASDAQ 100": "^NDX", "Russell 2000": "^RUT", "Dow Jones": "^DJI"}
        analisis_indices = []
        for nombre_ind, ticker_ind in indices_dict.items():
            try:
                ind = yf.Ticker(ticker_ind)
                hist = ind.history(period="2d")
                if len(hist) >= 2:
                    precio_actual = hist['Close'].iloc[-1]
                    precio_previo = hist['Close'].iloc[-2]
                    cambio_diario = ((precio_actual - precio_previo) / precio_previo) * 100
                    analisis_indices.append({"Índice": nombre_ind, "Cierre": round(precio_actual, 2), "Cambio": f"{cambio_diario:+.2f}%"})
            except: pass
        st.session_state.indices_radar = analisis_indices

        # 2. Pools Ampliados de Tickers
        dict_sp500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "MA", "JPM", "BAC", "PG", "KO", "NKE", "TGT", "WMT", "JNJ", "PFE", "UNH", "XOM", "CVX", "HD", "COST", "PEP", "PM"]
        dict_nasdaq = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "AMD", "QCOM", "INTC", "TSM", "ASML", "NFLX", "ADBE", "PANW", "SNPS", "CDNS", "MAR", "ORCL", "TXN"]
        dict_dowjones = ["AAPL", "MSFT", "AMZN", "V", "JPM", "AXP", "PG", "KO", "WMT", "HD", "CAT", "DIS", "CVX", "BA", "HON", "IBM", "MMM", "GS", "UNH", "VZ"]
        dict_russell2000 = ["CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "PDFS", "CEVA", "AEIS", "COHR", "UFPI", "AIT", "FIX", "AMN", "SPSC", "EGBN", "KNSL", "MEDP"]

        if "Espectro Completo" in enfoque_mercado:
            pool_dinamico = list(set(dict_sp500 + dict_nasdaq + dict_dowjones + dict_russell2000))
        elif "S&P 500" in enfoque_mercado:
            pool_dinamico = dict_sp500
        elif "NASDAQ" in enfoque_mercado:
            pool_dinamico = dict_nasdaq
        elif "Dow Jones" in enfoque_mercado:
            pool_dinamico = dict_dowjones
        else:
            pool_dinamico = dict_russell2000

        oportunidades = []
        descartadas_por_filtro = 0
        progress = st.progress(0)
        
        for idx, t in enumerate(pool_dinamico):
            progress.progress((idx + 1) / len(pool_dinamico))
            try:
                ticker = yf.Ticker(t)
                info = ticker.info
                precio = info.get('currentPrice', 0)
                eps = info.get('trailingEps', 0)
                nombre = info.get('longName', t)
                cap_mercado = info.get('marketCap', 0)
                crecimiento_ganancias = info.get('earningsGrowth', 0.05) or 0.05
                vol_actual = info.get('volume', 1)
                vol_prom = info.get('averageVolume', 1)
                ratio_vol = vol_actual / vol_prom
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento_ganancias * 100)))
                    descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                    
                    if valor_intrinseco > precio and descuento >= margen_exigido:
                        if cap_mercado < 6000000000 and crecimiento_ganancias <= 0.02: 
                            continue
                        
                        # --- NUEVA LÓGICA DE PLAZO SUGERIDO (MOMENTUM Y VOLATILIDAD) ---
                        max_52 = info.get('fiftyTwoWeekHigh', precio)
                        min_52 = info.get('fiftyTwoWeekLow', precio)
                        
                        rango_total = max_52 - min_52 if (max_52 - min_52) > 0 else 1
                        posicion_precio = (precio - min_52) / rango_total
                        
                        # Si tiene volumen alto, está cerca de máximos o es una Small Cap volátil -> Corto Plazo
                        if ratio_vol >= 1.05 or posicion_precio >= 0.75 or cap_mercado < 10000000000:
                            horizonte_sugerido = "⏳ Corto Plazo"
                        else:
                            horizonte_sugerido = "📈 Largo Plazo"
                        # --------------------------------------------------------------

                        oportunidades.append({
                            "Ticker": t, "Empresa": nombre, "Plazo Sugerido": horizonte_sugerido, 
                            "Precio Actual": precio, "Valor Intrínseco": round(valor_intrinseco, 2), 
                            "Margen de Seguridad": round(descuento, 1)
                        })
                    else:
                        descartadas_por_filtro += 1
                else:
                    descartadas_por_filtro += 1
            except: 
                descartadas_por_filtro += 1
        
        st.session_state.resultados_radar = oportunidades
        st.session_state.total_analizadas = len(pool_dinamico)
        st.session_state.descartadas = descartadas_por_filtro

    # --- MOSTRAR RESULTADOS GUARDADOS EN LA SESIÓN ---
    if st.session_state.indices_radar:
        st.markdown("#### 🌍 Comportamiento de Índices de Referencia")
        st.dataframe(pd.DataFrame(st.session_state.indices_radar), use_container_width=True)

    if st.session_state.resultados_radar:
        st.markdown(f"📊 **Análisis completo:** Se evaluaron `{st.session_state.total_analizadas}` acciones. `{st.session_state.descartadas}` no cumplieron tu margen de seguridad.")
        df_final = pd.DataFrame(st.session_state.resultados_radar)
        st.dataframe(df_final, use_container_width=True)
        
        # Panel de guardado persistente
        st.markdown("### 📥 Guardar en la Memoria del Agente")
        col_sel, col_btn = st.columns([3, 1])
        with col_sel:
            ticker_guardar = st.selectbox("Selecciona la acción ganadora para archivar:", df_final["Ticker"].tolist(), key="sb_guardar_ticker")
        with col_btn:
            st.write("") 
            if st.button("💾 Guardar Selección", key="btn_guardar_db"):
                fila = df_final[df_final["Ticker"] == ticker_guardar].iloc[0]
                guardar_accion_en_memoria(
                    fila["Ticker"], fila["Empresa"], float(fila["Precio Actual"]), 
                    float(fila["Valor Intrínseco"]), fila["Plazo Sugerido"], float(fila["Margen de Seguridad"])
                )
    elif st.session_state.resultados_radar is not None and len(st.session_state.resultados_radar) == 0:
        st.info(f"🔍 El escaneo procesó las {st.session_state.total_analizadas} acciones, pero NINGUNA cumple con el Margen de Seguridad del {margen_exigido}% en este momento.")

# =====================================================================
# PESTAÑA 3: ROTACIÓN DE SECTORES & BITÁCORA DE APRENDIZAJE
# =====================================================================
with tab3:
    st.subheader("🧱 Análisis de Fuerza Sectorial y Rastreador de Flujos")
    
    if st.button("Análisis de Sectores"):
        st.info("Barrido sectorial ejecutándose...")

    st.markdown("---")
    st.subheader("🧠 Bitácora de Aciertos y Rendimiento de la IA")
    st.write("A continuación se despliegan las acciones que guardaste en el pasado. El agente calcula su rendimiento real de forma automática.")
    
    # Cargar datos de la base de datos local
    conn = sqlite3.connect('agente_memoria.db')
    df_memoria = pd.read_sql_query("SELECT * FROM portafolio_radar", conn)
    conn.close()
    
    if df_memoria.empty:
        st.info("La memoria local está vacía. Ejecuta un escaneo en la Pestaña 2 y guarda un activo para entrenar al agente.")
    else:
        bitacora_actualizada = []
        with st.spinner("Actualizando cotizaciones en tiempo real para verificar aciertos..."):
            for _, fila in df_memoria.iterrows():
                try:
                    t = fila["ticker"]
                    tick = yf.Ticker(t)
                    precio_hoy = tick.info.get('currentPrice', fila["precio_entrada"])
                    
                    rendimiento_real = ((precio_hoy - fila["precio_entrada"]) / fila["precio_entrada"]) * 100
                    status_acierto = "✅ ACERTÓ (Ganancia)" if rendimiento_real >= 0 else "❌ REVISAR (Pérdida)"
                    
                    bitacora_actualizada.append({
                        "Ticker": t, "Empresa": fila["empresa"], "Fecha Registro": fila["fecha_registro"],
                        "Precio Entrada": f"${fila['precio_entrada']:.2f}", "Precio Actual": f"${precio_hoy:.2f}",
                        "Rendimiento Real": f"{rendimiento_real:+.2f}%", "Estatus del Radar": status_acierto,
                        "Plazo": fila["plazo_sugerido"]
                    })
                except: pass
                
        if bitacora_actualizada:
            df_bitacora = pd.DataFrame(bitacora_actualizada)
            st.dataframe(df_bitacora, use_container_width=True)
            
            # Estadísticas globales de acierto
            total_alertas = len(df_bitacora)
            aciertos = len(df_bitacora[df_bitacora["Estatus del Radar"].str.contains("✅")])
            tasa_efectividad = (aciertos / total_alertas) * 100
            
            st.markdown(f"### 🎯 Tasa de Asertividad Actual del Agente: `{tasa_efectividad:.1f}%`")
            st.write(f"El sistema ha procesado un total de {total_alertas} elecciones guardadas en tu máquina.")
