import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Agente Financiero Inteligente", layout="wide")

# =====================================================================
# 1. BASE DE DATOS INTERNA DEL AGENTE
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

# =====================================================================
# 2. INTERFAZ GRÁFICA PRINCIPAL
# =====================================================================
st.title("🤖 Tu Asistente Inteligente de Inversiones")
st.markdown("### Encuentra las mejores opciones para ganar dinero a corto plazo sin complicaciones")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sectores Calientes", 
    "🎓 Filtros de Leyendas",
    "🛰️ Escáner de Índices", 
    "🎯 Buscador de Acciones Seguro (Sin Lenguaje Técnico)"
])

# Mantener pestañas de soporte vacías para no romper la estructura que ya tenías
with tab1: st.subheader("Monitor de Sectores")
with tab2: st.subheader("Filtros Tradicionales")
with tab3: st.subheader("Escáner")

# =====================================================================
# PESTAÑA 4: TOTALMENTE TRADUCIDA A LENGUAJE HUMANO Y SIMPLE
# =====================================================================
with tab4:
    st.subheader("🔎 Analizador de Acciones para Comprar y Vender Rápido")
    st.write("Configura tu cuenta aquí abajo para que el sistema calcule exactamente qué hacer y proteja tu dinero de errores.")
    
    # Configuración inicial en pesos o dólares (muy sencillo)
    col_cap1, col_cap2 = st.columns(2)
    with col_cap1:
        capital_total = st.number_input("¿Cuánto dinero tienes en total para invertir en tu cuenta (USD)?", min_value=10.0, value=2000.0, step=50.0)
    with col_cap2:
        riesgo_maximo = st.slider("Si la inversión sale mal, ¿qué porcentaje máximo de tu dinero permites perder?", 0.5, 5.0, 1.0, 0.5)

    st.markdown("---")
    
    # Selector sencillo de empresas conocidas para evitar que el usuario deba saberse los códigos (tickers)
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
    
    empresa_seleccionada = st.selectbox("Selecciona la empresa que quieres revisar hoy:", list(diccionario_empresas.keys()))
    codigo_accion = diccionario_empresas[empresa_seleccionada]
    
    if st.button("⚡ Analizar Oportunidad de Ganancia", key="btn_auditar_humano"):
        with st.spinner(f"Revisando los movimientos de {empresa_seleccionada} hoy..."):
            try:
                asset = yf.Ticker(codigo_accion)
                hist = asset.history(period="60d")
                inf = asset.info
                precio_actual = inf.get('currentPrice') or inf.get('regularMarketPrice', 0)
                nombre_real = inf.get('longName', empresa_seleccionada)
                
                if len(hist) < 20 or precio_actual == 0:
                    st.error("No pudimos conectar con el mercado. Inténtalo de nuevo en unos segundos.")
                else:
                    # --- Cálculos matemáticos internos (ocultos para el usuario) ---
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
                    
                    # --- Semáforo de Condiciones ---
                    condicion_direccion = precio_actual > ema_actual
                    condicion_fuerza = 45 <= rsi_actual <= 70
                    condicion_grandes_compradores = aceleracion_vol >= 1.2
                    
                    st.markdown(f"## 🏢 {nombre_real}")
                    st.markdown(f"**Precio de cada acción en este momento:** `${precio_actual:.2f} USD`")
                    st.markdown("---")
                    
                    st.markdown("### 🚦 Semáforo de Seguridad (¿Es buen momento?)")
                    c1, c2, c3 = st.columns(3)
                    
                    with c1:
                        if condicion_direccion:
                            st.success("🟢 **Dirección del Precio:**\n\nLa acción está subiendo con constancia en los últimos días. El viento está a favor.")
                        else:
                            st.error("🔴 **Dirección del Precio:**\n\nLa acción viene cayendo. Comprar ahora es peligroso porque puede seguir bajando.")
                            
                    with c2:
                        if condicion_fuerza:
                            st.success("🟢 **Fuerza de Compra:**\n\nHay un interés saludable de la gente. No está ni abandonada ni exageradamente inflada.")
                        elif rsi_actual > 70:
                            st.warning("⚠️ **Fuerza de Compra:**\n\nEstá demasiado inflada por la emoción del momento. Podría caer de golpe si compras hoy.")
                        else:
                            st.error("🔴 **Fuerza de Compra:**\n\nNadie está interesado en esta empresa ahora mismo. El precio está estancado.")
                            
                    with c3:
                        if condicion_grandes_compradores:
                            st.success("🟢 **Dinero de los Profesionales:**\n\nLos grandes bancos y fondos de inversión están inyectando mucho dinero hoy.")
                        else:
                            st.error("🔴 **Dinero de los Profesionales:**\n\nNo hay movimientos grandes hoy. Solo inversores pequeños operando.")

                    st.markdown("---")
                    
                    # --- Plan de acción masticado ---
                    st.markdown("### 📋 Tu Plan de Acción Masticado (Para Evitar Errores)")
                    
                    # Cálculos del plan
                    precio_salida_perdida = precio_actual - (1.5 * atr_actual)
                    perdida_porcentaje = ((precio_actual - precio_salida_perdida) / precio_actual) * 100
                    
                    precio_salida_ganancia = precio_actual + (3.0 * atr_actual)
                    ganancia_porcentaje = ((precio_salida_ganancia - precio_actual) / precio_actual) * 100
                    
                    dinero_maximo_a_perder = capital_total * (riesgo_maximo / 100)
                    riesgo_por_accion = precio_actual - precio_salida_perdida
                    
                    if riesgo_por_accion > 0:
                        cantidad_acciones = int(dinero_maximo_a_perder / riesgo_por_accion)
                        dinero_total_compra = cantidad_acciones * precio_actual
                    else:
                        cantidad_acciones = 0
                        dinero_total_compra = 0
                    
                    col_p1, col_p2, col_p3 = st.columns(3)
                    with col_p1:
                        st.metric(label="🛑 Si baja de este precio, VENDE de inmediato:", value=f"${precio_salida_perdida:.2f} USD", delta=f"-{perdida_porcentaje:.1f}%")
                        st.caption("Esta es tu red de seguridad. Si el precio toca este número, te sales para evitar que un error te cueste caro.")
                    with col_p2:
                        st.metric(label="🎯 Si sube a este precio, COBRA tus ganancias:", value=f"${precio_salida_ganancia:.2f} USD", delta=f"+{ganancia_porcentaje:.1f}%")
                        st.caption("Este es tu objetivo. Al llegar aquí, retiras tu dinero con la ganancia en el bolsillo.")
                    with col_p3:
                        st.metric(label="📦 Cantidad exacta a comprar:", value=f"{cantidad_acciones} acciones", delta=f"Invertirás: ${dinero_total_compra:,.2f} USD")
                        st.caption(f"Comprando esta cantidad, si la inversión sale mal, solo habrás perdido **${dinero_maximo_a_perder:.2f} USD** (el {riesgo_maximo}% que configuraste).")

                    st.markdown("---")
                    
                    # --- Veredicto Final Inteligente ---
                    st.markdown("### 🤖 Conclusión Final del Asistente")
                    puntos = sum([condicion_direccion, condicion_fuerza, condicion_grandes_compradores])
                    
                    if puntos == 3:
                        st.success(f"🚀 **¡TODO SE ALÍNEA! BUENA OPORTUNIDAD:** {empresa_seleccionada} tiene las 3 luces en verde. Está subiendo, hay dinero grande entrando y el riesgo está controlado. Sigue el plan de arriba para comprar de forma segura.")
                    elif puntos == 2:
                        st.warning(f"⚠️ **RIESGO MODERADO / MEJOR ESPERA:** Tiene cosas buenas, pero una de las luces del semáforo está en amarillo o rojo. No es una compra perfecta, es mejor esperar a que se ponga totalmente en verde.")
                    else:
                        st.error(f"❌ **NO COMPRAR POR NINGÚN MOTIVO:** Esta empresa tiene demasiadas alertas rojas hoy. Meter tu dinero aquí ahora mismo es una lotería y tienes las de perder. El sistema te recomienda buscar otra opción.")
                        
            except Exception as e:
                st.error(f"Hubo un problema al leer la información de la empresa. Intenta con otra.")
