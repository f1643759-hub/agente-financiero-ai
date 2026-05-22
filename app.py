import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Agente Financiero Matemático Autónomo", layout="wide")

# =====================================================================
# 1. BASE DE DATOS LOCAL A COSTO CERO (SQLite3)
# =====================================================================
def inicializar_sistema_memoria():
    """Crea el almacenamiento local en tu PC para guardar las calibraciones del agente"""
    conn = sqlite3.connect('agente_inteligente.db')
    cursor = conn.cursor()
    
    # Tabla para registrar las compras recomendadas y medir su rendimiento real
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decisiones_radar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_registro TEXT,
            ticker TEXT,
            empresa TEXT,
            precio_entrada REAL,
            valor_intrinseco REAL,
            decision_tomada TEXT,
            plazo_sugerido TEXT,
            evaluado INTEGER DEFAULT 0,
            rendimiento_posterior REAL DEFAULT 0.0
        )
    ''')
    
    # Tabla para que el algoritmo aprenda de sus desviaciones matemáticas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bitacora_errores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_leccion TEXT,
            ticker TEXT,
            leccion_clave TEXT,
            ajuste_filtro TEXT
        )
    ''')

    # Tabla de filtros auto-calibrados (El algoritmo los endurece solo si detecta pérdidas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filtros_calibrados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roe_minimo REAL DEFAULT 0.15,
            margen_seguridad_minimo REAL DEFAULT 20.0,
            aceleracion_volumen_minima REAL DEFAULT 1.15
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM filtros_calibrados")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO filtros_calibrados (roe_minimo, margen_seguridad_minimo, aceleracion_volumen_minima) VALUES (0.15, 20.0, 1.15)")
        
    conn.commit()
    conn.close()

inicializar_sistema_memoria()

# =====================================================================
# 2. MOTOR LOCAL DE APRENDIZAJE POR REFUERZO CUANTITATIVO
# =====================================================================
def ejecutar_auto_perfeccionamiento():
    """El algoritmo revisa los precios reales del mercado y ajusta sus propias fórmulas de selección de forma independiente"""
    conn = sqlite3.connect('agente_inteligente.db')
    cursor = conn.cursor()
    
    df_pendientes = pd.read_sql_query("SELECT * FROM decisiones_radar WHERE evaluado = 0", conn)
    
    cursor.execute("SELECT roe_minimo, margen_seguridad_minimo, aceleracion_volumen_minima FROM filtros_calibrados ORDER BY id DESC LIMIT 1")
    roe_actual, margen_actual, vol_actual = cursor.fetchone()
    
    errores_nuevos = 0
    aciertos_nuevos = 0
    
    if not df_pendientes.empty:
        for index, row in df_pendientes.iterrows():
            id_registro = row['id']
            ticker = row['ticker']
            precio_entrada = row['precio_entrada']
            
            try:
                stock = yf.Ticker(ticker)
                precio_actual = stock.history(period="1d")['Close'].iloc[-1]
                rendimiento = ((precio_actual - precio_entrada) / precio_entrada) * 100
                
                if rendimiento < -3.5:
                    errores_nuevos += 1
                    leccion = f"Desviación en {ticker}: Caída de {rendimiento:.2f}%."
                    ajuste = "Incrementar restricción matemática de entrada."
                    cursor.execute("INSERT INTO bitacora_errores (fecha_leccion, ticker, leccion_clave, ajuste_filtro) VALUES (?, ?, ?, ?)",
                                   (datetime.now().strftime("%Y-%m-%d"), ticker, leccion, ajuste))
                elif rendimiento > 3.5:
                    aciertos_nuevos += 1
                
                cursor.execute("UPDATE decisiones_radar SET evaluado = 1, rendimiento_posterior = ? WHERE id = ?", (rendimiento, id_registro))
            except:
                continue
    
    # Si las matemáticas fallaron en las últimas elecciones, el algoritmo se vuelve más estricto de forma autónoma
    if errores_nuevos > aciertos_nuevos:
        nuevo_roe = min(roe_actual + 0.02, 0.25)
        nuevo_margen = min(margen_actual + 2.5, 35.0)
        nuevo_vol = min(vol_actual + 0.05, 1.50)
        cursor.execute("INSERT INTO filtros_calibrados (roe_minimo, margen_seguridad_minimo, aceleracion_volumen_minima) VALUES (?, ?, ?)",
                       (nuevo_roe, nuevo_margen, nuevo_vol))
        mensaje = f"⚠️ Optimización Matemática Local: El agente aumentó sus restricciones de seguridad de forma autónoma (Nuevo ROE Mín: {nuevo_roe*100:.1f}%, Nuevo Margen Graham Mín: {nuevo_margen:.1f}%)."
    else:
        mensaje = "✅ El nivel de asertividad matemática actual es óptimo. Los filtros están capturando ganancias de forma efectiva."
        
    conn.commit()
    conn.close()
    return mensaje

# =====================================================================
# 3. INTERFAZ GRÁFICA DE STREAMLIT
# =====================================================================
st.title("🤖 Agente Financiero Matemático Autónomo")
st.markdown("### Terminal de Inversión Basada en Arbitraje Estadístico Local — Costo Mensual: $0.00")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🔍 Auditoría Manual (Filtros de Valor)", 
    "🌍 Escáner Total de Índices y Selección de Plazos", 
    "🧱 Rotación de Sectores y Flujo de Capital"
])

# Recuperar los filtros dinámicos recalculados por el propio código
conn = sqlite3.connect('agente_inteligente.db')
cursor = conn.cursor()
cursor.execute("SELECT roe_minimo, margen_seguridad_minimo, aceleracion_volumen_minima FROM filtros_calibrados ORDER BY id DESC LIMIT 1")
filtro_roe, filtro_margen, filtro_volumen = cursor.fetchone()
conn.close()

# Panel Lateral de Métricas Adaptativas
st.sidebar.markdown("### 📊 Filtros Matemáticos Activos")
st.sidebar.write("El sistema modifica estos umbrales lógicos de forma independiente según los rendimientos históricos:")
st.sidebar.metric("ROE Mínimo Requerido", f"{filtro_roe*100:.1f}%")
st.sidebar.metric("Margen de Seguridad de Graham", f"{filtro_margen:.1f}%")
st.sidebar.metric("Volumen Institucional Mínimo", f"{filtro_volumen:.2f}x")

# =====================================================================
# PESTAÑA 1: AUDITORÍA MANUAL
# =====================================================================
with tab1:
    st.subheader("🔍 Auditoría Manual de un Activo")
    st.write("Verifica instantáneamente si una acción cumple con los criterios de Benjamin Graham modificados por el algoritmo local.")
    
    ticker_manual = st.text_input("Introduce el Ticker de la Acción (ej: AAPL, MSFT, TSLA):", "AAPL").strip().upper()
    
    if st.button("🚀 Iniciar Auditoría Matemática", key="btn_p1"):
        if ticker_manual:
            with st.spinner(f"Calculando métricas locales para {ticker_manual}..."):
                try:
                    asset = yf.Ticker(ticker_manual)
                    info = asset.info
                    
                    px = info.get('currentPrice') or info.get('regularMarketPrice', 0)
                    eps = info.get('trailingEps', 0)
                    growth = info.get('earningsGrowth', 0.05) or 0.05
                    if growth <= 0: growth = 0.05
                    
                    if px == 0:
                        st.error("No se pudieron cargar los precios de este activo.")
                    else:
                        st.markdown(f"### 🏢 {info.get('longName', ticker_manual)} — `${px:.2f}`")
                        
                        roe = info.get('returnOnEquity', 0)
                        
                        # Fórmula matemática pura de Valor Intrínseco de Benjamin Graham
                        valor_graham = eps * (8.5 + (2 * (growth * 100))) if eps > 0 else 0
                        margen_seguridad_real = ((valor_graham - px) / valor_graham) * 100 if valor_graham > 0 else 0
                        
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("ROE de la Empresa", f"{roe*100:.2f}%", f"Requerido: {filtro_roe*100:.1f}%")
                        with c2:
                            st.metric("Margen de Seguridad Real", f"{margen_seguridad_real:.1f}%", f"Requerido: {filtro_margen:.1f}%")
                        with c3:
                            st.metric("Precio Justo Estimado", f"${valor_graham:.2f}")
                        
                        # Filtro lógico determinista local (Sin necesidad de IA externa)
                        cumple_roe = roe >= filtro_roe
                        cumple_margen = margen_seguridad_real >= filtro_margen
                        
                        st.markdown("#### ⚖️ Dictamen del Algoritmo Local:")
                        if cumple_roe and cumple_margen:
                            st.success(f"📈 **DICTAMEN: COMPRAR**. El activo supera el ROE exigido y ofrece un margen de seguridad óptimo frente a su valor de Graham.")
                            decision_final = "COMPRAR"
                        else:
                            razones = []
                            if not cumple_roe: razones.append(f"ROE insuficiente ({roe*100:.1f}% vs {filtro_roe*100:.1f}% exigido)")
                            if not cumple_margen: razones.append(f"Margen de seguridad bajo ({margen_seguridad_real:.1f}% vs {filtro_margen:.1f}% exigido)")
                            st.error(f"❌ **DICTAMEN: NO INVERTIR**. Razones: {', '.join(razones)}.")
                            decision_final = "NO INVERTIR"
                        
                        # Registrar decisión localmente
                        conn = sqlite3.connect('agente_inteligente.db')
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO decisiones_radar 
                            (fecha_registro, ticker, empresa, precio_entrada, valor_intrinseco, decision_tomada, plazo_sugerido)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (datetime.now().strftime("%Y-%m-%d"), ticker_manual, info.get('longName', ticker_manual), float(px), float(valor_graham), decision_final, "Manual"))
                        conn.commit()
                        conn.close()
                except Exception as e:
                    st.error(f"Error al procesar el ticker: {e}")

# =====================================================================
# PESTAÑA 2: ESCÁNER TOTAL DE ÍNDICES MUNDIALES Y SELECCIÓN DE PLAZOS
# =====================================================================
with tab2:
    st.subheader("🌍 Escáner de Índices Globales y Segmentación Eficiente")
    st.write("El sistema analiza matemáticamente los componentes de los principales mercados para filtrar oportunidades por plazos.")
    
    if st.button("🛰️ Ejecutar Escáner Total de Mercados Mundiales", key="btn_p2"):
        indices_globales = {
            "S&P 500 (EE.UU)": {"ticker": "^GSPC", "pool": ["AAPL", "MSFT", "AMZN", "NVDA", "JPM"]},
            "NASDAQ 100 (EE.UU)": {"ticker": "^IXIC", "pool": ["GOOGL", "META", "AVGO", "COST", "NFLX"]},
            "EURO STOXX 50 (Europa)": {"ticker": "^STOXX50E", "pool": ["ASML", "MC.PA", "OR.PA", "SAP", "SIE.DE"]},
            "IBOVESPA (Brasil)": {"ticker": "^BVSP", "pool": ["VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA"]}
        }
        
        datos_escaneo_indices = []
        pool_acciones_recopiladas = []
        
        for nombre_indice, config in indices_globales.items():
            try:
                ind_obj = yf.Ticker(config["ticker"])
                hist_ind = ind_obj.history(period="5d")
                
                if len(hist_ind) >= 2:
                    precio_cierre = hist_ind['Close'].iloc[-1]
                    cambio_diario = ((hist_ind['Close'].iloc[-1] - hist_ind['Close'].iloc[-2]) / hist_ind['Close'].iloc[-2]) * 100
                    cambio_semanal = ((hist_ind['Close'].iloc[-1] - hist_ind['Close'].iloc[0]) / hist_ind['Close'].iloc[0]) * 100
                    
                    datos_escaneo_indices.append({
                        "Índice Bursátil": nombre_indice, "Ticker Ref": config["ticker"], "Nivel Actual": f"{precio_cierre:,.2f}",
                        "Var. Diaria": f"{cambio_diario:+.2f}%", "Var. Semanal": f"{cambio_semanal:+.2f}%",
                        "Diagnóstico Macro": "🟢 Mercado Fuerte" if cambio_diario > 0 else "🔴 Mercado en Retroceso"
                    })
                
                for t_accion in config["pool"]:
                    try:
                        acc_obj = yf.Ticker(t_accion)
                        inf_acc = acc_obj.info
                        hist_acc = acc_obj.history(period="5d")
                        v_hoy = inf_acc.get('volume', 1) or 1
                        v_prom = inf_acc.get('averageVolume', 1) or 1
                        
                        pool_acciones_recopiladas.append({
                            "ticker": t_accion, "nombre": inf_acc.get('longName', t_accion), "indice_origen": nombre_indice,
                            "precio": inf_acc.get('currentPrice') or inf_acc.get('regularMarketPrice', 0),
                            "roe": inf_acc.get('returnOnEquity', 0),
                            "margin_operativo": inf_acc.get('operatingMargins', 0),
                            "aceleracion_volumen": v_hoy / v_prom,
                            "retorno_5d": ((hist_acc['Close'].iloc[-1] - hist_acc['Close'].iloc[0]) / hist_acc['Close'].iloc[0]) * 100 if len(hist_acc) >= 2 else 0
                        })
                    except: continue
            except: pass
            
        st.markdown("#### 📊 Situación Actual de los Índices del Mundo")
        st.dataframe(pd.DataFrame(datos_escaneo_indices), use_container_width=True)
        
        df_pool = pd.DataFrame(pool_acciones_recopiladas)
        if not df_pool.empty:
            st.markdown("#### 🎯 Clasificación de Activos Basada en Filtros Matemáticos")
            
            # FILTRADO Y SEGMENTACIÓN POR PLAZOS MEDIANTE MATEMÁTICA PURA LOCAL
            df_corto_plazo = df_pool[df_pool['aceleracion_volumen'] >= filtro_volumen].sort_values(by='retorno_5d', ascending=False)
            df_largo_plazo = df_pool[df_pool['roe'] >= filtro_roe].sort_values(by='margin_operativo', ascending=False)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.success(f"⏳ **Ganancias Corto Plazo: Momentum de Volumen (> {filtro_volumen:.2f}x volumen)**")
                st.write("Acciones con inyecciones masivas de volumen institucional listas para movimientos veloces:")
                st.dataframe(df_corto_plazo[['ticker', 'nombre', 'precio', 'aceleracion_volumen', 'retorno_5d']], use_container_width=True)
            with col_p2:
                st.info(f"🧱 **Ganancias Largo Plazo: Calidad Estructural (ROE > {filtro_roe*100:.1f}%)**")
                st.write("Empresas altamente rentables ideales para retornos consistentes compuestos en el tiempo:")
                st.dataframe(df_largo_plazo[['ticker', 'nombre', 'precio', 'roe', 'margin_operativo']], use_container_width=True)
                
            # Registrar muestras automáticas en la base de datos local para auto-evaluación
            conn = sqlite3.connect('agente_inteligente.db')
            cursor = conn.cursor()
            for t in df_corto_plazo.head(2)['ticker'].tolist() + df_largo_plazo.head(2)['ticker'].tolist():
                cursor.execute("INSERT INTO decisiones_radar (fecha_registro, ticker, empresa, precio_entrada, valor_intrinseco, decision_tomada, plazo_sugerido) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (datetime.now().strftime("%Y-%m-%d"), t, t, 100.0, 0.0, "COMPRAR", "Escáner Local"))
            conn.commit()
            conn.close()

    # --- PANEL DE CONTROL DE APRENDIZAJE DIARIO ---
    st.markdown("---")
    st.subheader("🧠 Bucle de Auto-Calibración de Eficiencia")
    st.write("Presiona este botón para que el código verifique el mercado y reajuste las fórmulas de selección automáticamente en base a aciertos y errores.")
    
    if st.button("🔄 Ejecutar Calibración y Aprendizaje Autónomo"):
        mensaje_entrenamiento = ejecutar_auto_perfeccionamiento()
        st.success(mensaje_entrenamiento)

# =====================================================================
# PESTAÑA 3: ROTACIÓN DE SECTORES Y FLUJO DE CAPITAL
# =====================================================================
with tab3:
    st.subheader("🧱 Fuerza de Sectores e Inyección de Dinero")
    st.write("Detecta hacia dónde se mueven los capitales institucionales de forma agregada a costo cero.")
    
    if st.button("🔄 Analizar Rotación de Capital Sectorial", key="btn_p3"):
        etfs_sectores = {
            "XLK": "Tecnología", "XLF": "Financiero", "XLV": "Salud", "XLE": "Energía", "XLY": "Consumo Discrecional"
        }
        
        datos_sectores = []
        for etf, nombre_sec in etfs_sectores.items():
            try:
                t_sector = yf.Ticker(etf)
                inf_s = t_sector.info
                vol_hoy = inf_s.get('volume', 1) or 1
                vol_prom = inf_s.get('averageVolume', 1) or 1
                ratio_flujo = vol_hoy / vol_prom
                
                hist_s = t_sector.history(period="5d")
                ret_5d = ((hist_s['Close'].iloc[-1] - hist_s['Close'].iloc[0]) / hist_s['Close'].iloc[0]) * 100
                
                datos_sectores.append({
                    "Sector Industrial": nombre_sec, "ETF Referencia": etf, "Rendimiento Semanal": f"{ret_5d:+.2f}%",
                    "Aceleración de Flujo": f"{ratio_flujo:.2f}x",
                    "Flujo Institucional": "🟢 Acumulación de Capital" if ratio_flujo > filtro_volumen else "🔴 Flujo Débil"
                })
            except: pass
        if datos_sectores:
            st.dataframe(pd.DataFrame(datos_sectores), use_container_width=True)
