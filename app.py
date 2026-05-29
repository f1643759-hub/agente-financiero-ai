import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Agente Quant Profesional", layout="wide", page_icon="📈")

# =====================================================================
# 🧠 BASE DE DATOS LOCAL Y AUTO-APRENDIZAJE DEL ALGORITMO
# =====================================================================
def inicializar_bd():
    conn = sqlite3.connect('agente_quant.db')
    cursor = conn.cursor()
    # Tabla para registrar operaciones sugeridas por las pestañas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            ticker TEXT,
            precio_entrada REAL,
            stop_loss REAL,
            take_profit REAL,
            estado TEXT DEFAULT 'PENDIENTE'
        )
    ''''')
    # Tabla para almacenar los parámetros de calibración del sistema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calibracion_sistema (
            parametro TEXT PRIMARY KEY,
            valor REAL
        )
    ''''')
    # Insertar margen de seguridad por defecto si no existe (0.15 = 15%)
    cursor.execute("INSERT OR IGNORE INTO calibracion_sistema (parametro, valor) VALUES ('margen_seguridad', 0.15)")
    conn.commit()
    conn.close()

def recalibrar_algoritmo():
    """Revisa operaciones pasadas para medir el Win Rate y ajustar exigencias"""
    conn = sqlite3.connect('agente_quant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, ticker, precio_entrada, stop_loss, take_profit, estado FROM registro_operaciones WHERE estado = 'PENDIENTE'")
    operaciones = cursor.fetchall()
    
    for op in operaciones:
        id_op, ticker, entrada, sl, tp = op[0], op[1], op[2], op[3], op[4]
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="5d")
            if not hist.empty:
                precio_actual = hist['Close'].iloc[-1]
                # Verificación técnica de salida
                if precio_actual <= sl:
                    cursor.execute("UPDATE registro_operaciones SET estado = 'FALLIDA' WHERE id = ?", (id_op,))
                elif precio_actual >= tp:
                    cursor.execute("UPDATE registro_operaciones SET estado = 'EXITOSA' WHERE id = ?", (id_op,))
        except:
            pass
            
    # Calcular Tasa de Acierto histórica para calibración autónoma
    cursor.execute("SELECT estado FROM registro_operaciones WHERE estado IN ('EXITOSA', 'FALLIDA')")
    historico = cursor.fetchall()
    
    if historico:
        exitosas = sum(1 for x in historico if x[0] == 'EXITOSA')
        win_rate = exitosas / len(historico)
        
        # Ajustar dinámicamente el Margen de Seguridad según efectividad
        if win_rate < 0.60:
            # El mercado está difícil: Volverse más exigente aumentando el margen de descuento requerido
            cursor.execute("UPDATE calibracion_sistema SET valor = 0.20 WHERE parametro = 'margen_seguridad'")
        elif win_rate > 0.80:
            # El algoritmo es altamente efectivo: Permitir operaciones con menor descuento
            cursor.execute("UPDATE calibracion_sistema SET valor = 0.12 WHERE parametro = 'margen_seguridad'")
            
    conn.commit()
    
    # Recuperar el valor actual calibrado
    cursor.execute("SELECT valor FROM calibracion_sistema WHERE parametro = 'margen_seguridad'")
    margen_actual = cursor.fetchone()[0]
    conn.close()
    return margen_actual

# Inicialización y ejecución del Cerebro Quant
inicializar_bd()
MARGEN_SEGURIDAD_DINAMICO = recalibrar_algoritmo()

# =====================================================================
# 📋 DEFINICIÓN DE POOLS DE ACTIVOS Y MACROSECTORES (ETFs)
# =====================================================================
# Lista global fija utilizada por la Pestaña 3 e inspeccionada en Pestaña 4
POOL_ACCIONES = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "AVGO", "AMD", "TSLA", # Tech & IA
    "BRK-B", "COST", "WMT", "PG", "JPM", "LLY",                            # Valor / Consumo
    "CCJ", "OKLO", "SMR",                                                   # Energía & Uranio
    "HBAR-USD", "NU", "SQ"                                                  # Disruptivas / Fintech
]

# Estructura Macro para Rotación de Capital (Pestaña 1 y Pestaña 5)
ETFS_ROTACION = {
    "Semicondutores (IA)": "SMH",
    "Uranio y Energía Nuclear": "URNM",
    "Ciberseguridad": "HACK",
    "Software & Cloud": "IGV",
    "Consumo Defensivo": "XLP",
    "Banca y Finanzas": "XLF",
    "Oro y Refugio": "GLD"
}

# Componentes de cada ETF para desglose táctico y optimización de riesgo
COMPONENTES_ETFS = {
    "SMH": ["NVDA", "TSMC", "AVGO", "AMD", "INTC", "ASML"],
    "URNM": ["CCJ", "UUUU", "SRUUF", "DNN", "SMR", "OKLO"],
    "HACK": ["PANW", "FTNT", "CRWD", "NET", "OKTA", "ZS"],
    "IGV": ["MSFT", "ORCL", "CRM", "ADBE", "INTU", "NOW"],
    "XLP": ["PG", "WMT", "COST", "KO", "PEP", "PM"],
    "XLF": ["JPM", "BAC", "WFC", "C", "MS", "GS"],
    "GLD": ["NEM", "GOLD", "AEM", "AU", "KGC", "GFI"]
}

# =====================================================================
# 🖥️ INTERFAZ DE USUARIO (TABS DE STREAMLIT)
# =====================================================================
st.title("📊 Terminal Quant con Auto-Aprendizaje y Flujo de Volumen")
st.sidebar.markdown(f"### 🧠 Estado del Motor Quant\n**Margen de Seguridad Calibrado:** `{MARGEN_SEGURIDAD_DINAMICO*100:.1f}%`")
st.sidebar.info("El margen se ajusta automáticamente analizando la tasa de acierto de tus operaciones simuladas.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛰️ Rotación Macro", 
    "🧱 Radar de Descuento", 
    "🎯 Impulso Táctico", 
    "🔍 Consultor Libre",
    "🛡️ Portafolio Mínimo Riesgo (Volumen)"
])

# =====================================================================
# PESTAÑA 1: ROTACIÓN DE CAPITAL MACRO
# =====================================================================
with tab1:
    st.subheader("🛰️ Escáner de Volumen Relativo Sectorial")
    st.write("Identifica hacia dónde se están moviendo las manos fuertes del mercado en tiempo real.")
    
    if st.button("🛰️ Analizar Flujos Macroeconómicos", key="btn_p1"):
        resultados_macro = []
        for nombre, ticker in ETFS_ROTACION.items():
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="20d")
                if not hist.empty:
                    vol_promedio = hist['Volume'].mean()
                    vol_hoy = hist['Volume'].iloc[-1]
                    vol_relativo = vol_hoy / vol_promedio
                    precio_cierre = hist['Close'].iloc[-1]
                    
                    resultados_macro.append({
                        "Sector": nombre, "ETF": ticker, "Precio": precio_cierre, "Volumen Relativo": vol_relativo
                    })
            except:
                pass
                
        if resultados_macro:
            df_macro = pd.DataFrame(resultados_macro).sort_values(by="Volumen Relativo", ascending=False)
            st.dataframe(df_macro.style.format({"Precio": "${:.2f}", "Volumen Relativo": "{:.2f}x"}))
            
            sector_top = df_macro.iloc[0]
            st.success(f"🔥 El sector líder es **{sector_top['Sector']} ({sector_top['ETF']})** con un volumen de **{sector_top['Volumen Relativo']:.2f}x** superior a su promedio.")
            
            # Desglose de componentes del líder
            etf_ganador = sector_top['ETF']
            componentes_ganadores = COMPONENTES_ETFS.get(etf_ganador, [])
            st.write(f"🔍 Analizando los componentes de `{etf_ganador}` para buscar al líder del sector:")
            
            detalles_comp = []
            for comp in componentes_ganadores:
                try:
                    c_tk = yf.Ticker(comp)
                    c_hist = c_tk.history(period="5d")
                    if len(c_hist) >= 2:
                        rendimiento = ((c_hist['Close'].iloc[-1] - c_hist['Close'].iloc[-2]) / c_hist['Close'].iloc[-2]) * 100
                        detalles_comp.append({"Componente": comp, "Rendimiento Diario": rendimiento})
                except:
                    pass
            if detalles_comp:
                st.table(pd.DataFrame(detalles_comp).sort_values(by="Rendimiento Diario", ascending=False))

# =====================================================================
# PESTAÑA 2: RADAR DE DESCUENTO (LARGO PLAZO)
# =====================================================================
with tab2:
    st.subheader("🧱 Escáner Estadístico de Suelo Institucional")
    st.write("Busca activos subvaluados utilizando percentiles históricos de los últimos 60 días de cotización.")
    
    if st.button("🧱 Buscar Oportunidades de Valor", key="btn_p2"):
        gangas = []
        for ticker in POOL_ACCIONES:
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="60d")
                if len(hist) >= 15:
                    precio_actual = hist['Close'].iloc[-1]
                    suelo_institucional = np.percentile(hist['Close'], 15)
                    techo_historico = hist['High'].max()
                    
                    # Calcular margen de descuento real
                    if precio_actual <= suelo_institucional * (1 + MARGEN_SEGURIDAD_DINAMICO):
                        gangas.append({
                            "Ticker": ticker, "Precio Actual": precio_actual, "Suelo (P15)": suelo_institucional, "Máximo 60D": techo_historico
                        })
            except:
                pass
                
        if gangas:
            st.dataframe(pd.DataFrame(gangas).style.format({"Precio Actual": "${:.2f}", "Suelo (P15)": "${:.2f}", "Máximo 60D": "${:.2f}"}))
        else:
            st.info("Ningún activo del pool se encuentra en zona de suelo institucional con el margen de seguridad requerido actualmente.")

# =====================================================================
# PESTAÑA 3: IMPULSO TÁCTICO (CORTO PLAZO + GESTIÓN DE RIESGO)
# =====================================================================
with tab3:
    st.subheader("🎯 Escáner de Momentum con Control de Riesgo Integrado")
    st.write("Detecta aceleración alcista limpia y calcula el tamaño exacto de posición adaptado a tu capital.")
    
    capital_usuario = st.number_input("Tu Capital Total disponible para trading (USD):", min_value=100.0, value=5000.0, step=100.0)
    riesgo_permitido = st.slider("Porcentaje máximo de riesgo por operación (% del capital):", 0.5, 5.0, 1.0, 0.1) / 100.0
    
    if st.button("🎯 Buscar Señales de Impulso", key="btn_p3"):
        senales = []
        for ticker in POOL_ACCIONES:
            try:
                tk = yf.Ticker(ticker)
                hist = tk.history(period="30d")
                if len(hist) >= 10:
                    precio_actual = hist['Close'].iloc[-1]
                    ema_5 = hist['Close'].ewm(span=5, adjust=False).mean().iloc[-1]
                    vol_rel = hist['Volume'].iloc[-1] / hist['Volume'].mean()
                    
                    # Filtro de Aceleración: Precio sobre EMA y volumen comprador acompañando
                    if precio_actual > ema_5 and vol_rel > 1.05:
                        # Cálculo matemático del ATR (Average True Range) para Stop Loss técnico
                        high_low = hist['High'] - hist['Low']
                        high_close = np.abs(hist['High'] - hist['Close'].shift())
                        low_close = np.abs(hist['Low'] - hist['Close'].shift())
                        ranges = pd.concat([high_low, high_close, low_close], axis=1)
                        true_range = ranges.max(axis=1)
                        atr = true_range.rolling(14).mean().iloc[-1]
                        
                        score = (precio_actual / ema_5) * vol_rel
                        senales.append({
                            "Ticker": ticker, "Precio": precio_actual, "ATR": atr, "Score": score
                        })
            except:
                pass
                
        if senales:
            top_5 = pd.DataFrame(senales).sort_values(by="Score", ascending=False).head(5)
            st.write("### 🔥 Top 5 Activos con Mayor Fuerza de Aceleración")
            
            # Conexión para guardar la sugerencia operativa
            conn = sqlite3.connect('agente_quant.db')
            cursor = conn.cursor()
            
            for index, fila in top_5.iterrows():
                tk_name = fila['Ticker']
                p_ent = fila['Precio']
                atr_val = fila['ATR']
                
                # Gestión de Riesgo Estricta: Stop Loss a 1.5x ATR
                stop_loss = p_ent - (1.5 * atr_val)
                take_profit = p_ent + (3.0 * atr_val)
                distancia_sl = p_ent - stop_loss
                
                riesgo_usd = capital_usuario * riesgo_permitido
                acciones_a_comprar = int(riesgo_usd // distancia_sl) if distancia_sl > 0 else 1
                if acciones_a_comprar <= 0: acciones_a_comprar = 1
                
                # Registrar en la base de datos local para auto-aprendizaje posterior
                cursor.execute("INSERT INTO registro_operaciones (fecha, ticker, precio_entrada, stop_loss, take_profit) VALUES (?, ?, ?, ?, ?)",
                               (datetime.now().strftime("%Y-%m-%d"), tk_name, p_ent, stop_loss, take_profit))
                
                st.success(f"🚀 **SEÑAL ACTIVA: {tk_name}** (Score: {fila['Score']:.2f})")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Entrada Sugerida:", f"${p_ent:.2f} USD")
                    st.write(f"📦 **Comprar:** {acciones_a_comprar} acciones")
                with c2:
                    st.metric("Stop Loss Técnico:", f"${stop_loss:.2f} USD")
                    st.caption(f"Arriesgando: ${riesgo_usd:.2f} USD")
                with c3:
                    st.metric("Take Profit Objetivo:", f"${take_profit:.2f} USD")
                    st.caption(f"Ratio Riesgo/Beneficio: 1:2")
                st.markdown("---")
                
            conn.commit()
            conn.close()

# =====================================================================
# PESTAÑA 4: CONSULTOR LIBRE DE ACTIVOS
# =====================================================================
with tab4:
    st.subheader("🔍 Filtro de Diagnóstico Personalizado")
    st.write("Introduce cualquier ticker que no esté en la lista fija para analizar su estado bajo los criterios del agente.")
    
    ticker_usuario = st.text_input("Ingresa el Ticker del activo (Ej: WDC, GOOGL, HBAR-USD):", "WDC").strip().upper()
    
    if st.button("🔍 Auditar Activo", key="btn_p4"):
        try:
            tk = yf.Ticker(ticker_usuario)
            hist = tk.history(period="60d")
            if not hist.empty:
                precio_actual = hist['Close'].iloc[-1]
                suelo_p15 = np.percentile(hist['Close'], 15)
                vol_rel = hist['Volume'].iloc[-1] / hist['Volume'].mean()
                
                st.write(f"### 📊 Diagnóstico Técnico para `{ticker_usuario}`")
                col_u1, col_u2, col_u3 = st.columns(3)
                with col_u1:
                    st.metric("Precio Actual:", f"${precio_actual:.2f} USD")
                with col_u2:
                    st.metric("Suelo de Acumulación (P15):", f"${suelo_p15:.2f} USD")
                with col_u3:
                    st.metric("Volumen Diario Relativo:", f"{vol_rel:.2f}x")
                    
                # Dictamen algorítmico según los parámetros dinámicos
                if precio_actual <= suelo_p15 * (1 + MARGEN_SEGURIDAD_DINAMICO):
                    st.success("🟢 **ESTADO: APROBADO.** El activo se encuentra en zona de descuento seguro con fuerte respaldo institucional en el suelo.")
                elif vol_rel > 1.25:
                    st.warning("🟡 **ESTADO: EN LISTA DE ESPERA (MOMENTUM).** No tiene descuento a largo plazo, pero registra un fuerte ingreso de volumen hoy.")
                else:
                    st.error("🔴 **ESTADO: RECHAZADO.** El precio está extendido fuera de las zonas seguras de compra y carece de anomalías de volumen institucional.")
            else:
                st.error("No se encontraron datos. Verifica si el ticker es correcto en Yahoo Finance.")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")

# =====================================================================
# 🛡️ NUEVA PESTAÑA 5: FILTRO DE PRESIÓN REAL DE VOLUMEN COMPRA/VENTA
# =====================================================================
with tab5:
    st.subheader("🛡️ Optimización Avanzada de Mínima Varianza y Criterio de Riesgo")
    st.write("Esta pestaña localiza el sector líder, desglosa si el volumen es comprador o vendedor, y estructura un portafolio blindado libre de techos.")
    
    presupuesto_total = st.number_input("Capital total para este portafolio blindado (USD):", min_value=100.0, value=3000.0, step=100.0, key="p5_presupuesto")
    
    if st.button("🛡️ Ejecutar Optimización de Mínimo Riesgo", key="btn_p5_ejecutar"):
        st.write("📡 Escaneando mercados globales y analizando presión del volumen...")
        
        sector_lider = None
        max_vol_macro = -1
        presion_sector_lider = "DESCONOCIDO"
        
        # 1. Escaneo dinámico del sector líder midiendo la presión real del dinero
        for nombre, tick in ETFS_ROTACION.items():
            try:
                m_tk = yf.Ticker(tick)
                m_h = m_tk.history(period="5d")
                if len(m_h) >= 2:
                    v_rel = m_h['Volume'].iloc[-1] / m_h['Volume'].mean()
                    
                    # Capturar la vela de hoy para calcular la presión del flujo
                    cierre = m_h['Close'].iloc[-1]
                    maximo = m_h['High'].iloc[-1]
                    minimo = m_h['Low'].iloc[-1]
                    
                    # Fórmula Quant de Presión: Rango de cierre respecto al rango total del día
                    rango_total = maximo - minimo
                    if rango_total > 0:
                        factor_presion = (cierre - minimo) / rango_total
                    else:
                        factor_presion = 0.5
                        
                    # Si da >= 0.5, el precio cerró en la mitad superior de la vela (Presión Compradora)
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
            
            # CONTROL DE SEGURIDAD EXTREMO: Si el volumen del sector es de venta, abortamos la operación
            if "VENTA" in presion_sector_lider:
                st.error(f"⛔ **OPERACIÓN ABORTADA POR EL ALGORITMO:** Aunque el sector `{sector_lider}` mueve mucho capital, las manos fuertes están **VENDIENDO** para tomar ganancias. Comprar aquí sería entrar en el techo. Espera a que el flujo cambie a COMPRA.")
            else:
                componentes = COMPONENTES_ETFS[sector_lider]
                st.info(f"🎯 El flujo es saludable. Estructurando portafolio seguro con los componentes de `{sector_lider}`: {componentes}")
                
                datos_riesgo = []
                barra_p5 = st.progress(0)
                
                for index, ticker in enumerate(componentes):
                    try:
                        tk = yf.Ticker(ticker)
                        hist = tk.history(period="60d")
                        
                        if len(hist) >= 20:
                            # Confirmar que la acción individual también tenga volumen comprador hoy
                            c_cierre = hist['Close'].iloc[-1]
                            c_max = hist['High'].iloc[-1]
                            c_min = hist['Low'].iloc[-1]
                            c_rango = c_max - c_min
                            c_factor = (c_cierre - c_min) / c_rango if c_rango > 0 else 0.5
                            
                            # Solo dejamos pasar acciones donde el flujo de hoy sea neutral o comprador
                            if c_factor >= 0.45:
                                retornos = hist['Close'].pct_change().dropna()
                                volatilidad_real = retornos.std()
                                precio_act = hist['Close'].iloc[-1]
                                
                                # ATR para Stop Loss
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
                    # Seleccionar las 3 acciones con menor volatilidad (las más estables)
                    df_riesgo = pd.DataFrame(datos_riesgo).sort_values(by="Volatilidad", ascending=True).head(3)
                    
                    # Aplicar fórmula de Varianza Inversa para ponderar capital
                    df_riesgo['Inversa_Vol'] = 1.0 / df_riesgo['Volatilidad']
                    suma_inversas = df_riesgo['Inversa_Vol'].sum()
                    df_riesgo['Ponderación'] = df_riesgo['Inversa_Vol'] / suma_inversas
                    
                    st.markdown("## 🛡️ Portafolio Optimizado con Volumen Comprador Confirmado")
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
