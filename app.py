import streamlit as st
import yfinance as yf
import pandas as pd
import io
import sqlite3
from datetime import datetime

# =====================================================================
# MOTOR DE MEMORIA E INTELIGENCIA (100% GRATUITO)
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
    """Guarda una oportunidad seleccionada por el usuario"""
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
        st.success(f"💾 {ticker} guardada en la memoria del agente con éxito.")
    except Exception as e:
        st.error(f"Error al guardar: {e}")
    finally:
        conn.close()

# Inicializar la base de datos al arrancar la app
inicializar_base_datos()

# =====================================================================
# CONFIGURACIÓN DE INTERFAZ PROFESIONAL
# =====================================================================
st.set_page_config(page_title="Agente IA: Terminal Macro & Memoria", layout="wide")

st.title("🤖 Agente IA: Terminal Macro Global & Sistema de Aprendizaje")
st.markdown("### Inteligencia de Capitales: Radar de Flujos, Horizontes Temporales y Bitácora de Auto-Corrección Asertiva.")
st.markdown("---")

# Barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

# Pestañas del agente
tab1, tab2, tab3 = st.tabs([
    "🔍 Auditoría Manual", 
    "🛰️ Radar Macroeconómico e Índices del Mundo",
    "🧱 Rotación de Sectores y Flujo de Capital"
])

# =====================================================================
# PESTAÑA 1: ANÁLISIS MANUAL (Intacta)
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
# PESTAÑA 2: RADAR MACRO + ESCANEO SEGMENTADO POR ÍNDICE (Con Guardado)
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
    
    margen_exigido = st.slider("Margen de Seguridad Mínimo Exigido (%)", 15, 40, 20, key="slider_macro_p2")

    if st.button("🛰️ Lanzar Algoritmo de Búsqueda Global", key="btn_auto"):
        # Análisis rápido de índices de referencia para contextualizar la salud del mercado
        indices_dict = {"S&P 500": "^GSPC", "NASDAQ 100": "^NDX", "Russell 2000": "^RUT"}
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
        if analisis_indices:
            st.dataframe(pd.DataFrame(analisis_indices), use_container_width=True)

        # Listas de tickers predefinidas
        dict_sp500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "MA", "JPM", "BAC", "PG", "KO", "NKE", "TGT", "WMT", "JNJ", "PFE", "UNH"]
        dict_nasdaq = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "AMD", "QCOM", "INTC", "TSM", "ASML", "NFLX", "ADBE"]
        dict_dowjones = ["AAPL", "MSFT", "AMZN", "V", "JPM", "AXP", "PG", "KO", "WMT", "HD", "CAT", "DIS", "CVX"]
        dict_russell2000 = ["CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "PDFS", "CEVA", "AEIS", "COHR", "UFPI", "AIT", "FIX"]

        pool_dinamico = list(set(dict_sp500 + dict_nasdaq + dict_dowjones + dict_russell2000)) if "Espectro Completo" in enfoque_mercado else (dict_sp500 if "S&P 500" in enfoque_mercado else (dict_nasdaq if "NASDAQ" in enfoque_mercado else (dict_dowjones if "Dow Jones" in enfoque_mercado else dict_russell2000)))

        oportunidades = []
        progress = st.progress(0)
        
        for idx, t in enumerate(pool_dinamico):
            progress.progress((idx + 1) / len(pool_dinamico))
            try:
                ticker = yf.Ticker(t)
                info = ticker.info
                precio = info.get('currentPrice', 0)
                eps = info.get('trailingEps', 0)
                sector = info.get('sector', 'Otros')
                nombre = info.get('longName', t)
                deuda_capital = info.get('debtToEquity', None)
                roe = info.get('returnOnEquity', None)
                peg = info.get('pegRatio', None)
                cap_mercado = info.get('marketCap', 0)
                crecimiento_ganancias = info.get('earningsGrowth', 0.05) or 0.05
                vol_actual = info.get('volume', 1)
                vol_prom = info.get('averageVolume', 1)
                ratio_vol = vol_actual / vol_prom
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento_ganancias * 100)))
                    descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                    
                    if valor_intrinseco > precio and descuento >= margen_exigido:
                        if cap_mercado < 6000000000 and crecimiento_ganancias <= 0.02: continue
                        
                        horizonte_sugerido = "⏳ Corto Plazo" if ratio_vol >= 1.20 or cap_mercado < 6000000000 else "📈 Largo Plazo"
                        
                        oportunidades.append({
                            "Ticker": t, "Empresa": nombre, "Plazo Sugerido": horizonte_sugerido, 
                            "Precio Actual": precio, "Valor Intrínseco": round(valor_intrinseco, 2), 
                            "Margen de Seguridad": round(descuento, 1)
                        })
            except: pass
                
        if oportunidades:
            df_final = pd.DataFrame(oportunidades)
            st.dataframe(df_final, use_container_width=True)
            
            # --- FUNCIÓN DE ACCIÓN RÁPIDA DE GUARDADO ---
            st.markdown("### 📥 Guardar en la Memoria del Agente")
            col_sel, col_btn = st.columns([3, 1])
            with col_sel:
                ticker_guardar = st.selectbox("Selecciona la acción ganadora para archivar:", df_final["Ticker"].tolist())
            with col_btn:
                st.write("") # Espacio estético
                if st.button("💾 Guardar Selección"):
                    fila = df_final[df_final["Ticker"] == ticker_guardar].iloc[0]
                    guardar_accion_en_memoria(
                        fila["Ticker"], fila["Empresa"], fila["Precio Actual"], 
                        fila["Valor Intrínseco"], fila["Plazo Sugerido"], fila["Margen de Seguridad"]
                    )

# =====================================================================
# PESTAÑA 3: ROTACIÓN DE SECTORES & BITÁCORA DE APRENDIZAJE
# =====================================================================
with tab3:
    st.subheader("🧱 Análisis de Fuerza Sectorial y Rastreador de Flujos")
    
    if st.button("Análisis de Sectores"):
        st.info("Barrido sectorial ejecutándose...")
        # (Aquí corre tu motor sectorial estándar que ya posees en la versión anterior)

    st.markdown("---")
    st.subheader("🧠 Bitácora de Aciertos y Rendimiento de la IA")
    st.write("A continuación se despliegan las acciones que guardaste en el pasado. El agente calcula de forma automática su rendimiento real para comprobar si fue certero.")
    
    # Leer datos guardados en SQLite
    conn = sqlite3.connect('agente_memoria.db')
    df_memoria = pd.read_sql_query("SELECT * FROM portafolio_radar", conn)
    conn.close()
    
    if df_memoria.empty:
        st.info("La memoria está vacía. Guarda tu primera acción en la Pestaña 2 para empezar el entrenamiento del agente.")
    else:
        bitacora_actualizada = []
        with st.spinner("Actualizando cotizaciones en tiempo real para verificar aciertos..."):
            for _, fila in df_memoria.iterrows():
                try:
                    t = fila["ticker"]
                    tick = yf.Ticker(t)
                    precio_hoy = tick.info.get('currentPrice', fila["precio_entrada"])
                    
                    # Calcular ganancia o pérdida matemática
                    rendimiento_real = ((precio_hoy - fila["precio_entrada"]) / fila["precio_entrada"]) * 100
                    status_acierto = "✅ ACERTOU (Ganancia)" if rendimiento_real > 0 else "❌ REVISAR (Pérdida)"
                    
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
            
            # --- ESTADÍSTICAS DE PRECISIÓN ---
            total_alertas = len(df_bitacora)
            aciertos = len(df_bitacora[df_bitacora["Estatus del Radar"].str.contains("✅")])
            tasa_efectividad = (aciertos / total_alertas) * 100
            
            st.markdown(f"### 🎯 Tasa de Asertividad Actual del Agente: `{tasa_efectividad:.1f}%`")
            st.write(f"El sistema ha procesado un total de {total_alertas} elecciones guardadas por ti.")
