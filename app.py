import streamlit as st
import yfinance as yf
import pandas as pd
import io

# Configuración de interfaz profesional
st.set_page_config(page_title="Agente IA: Macro & Confluencia Global", layout="wide")

st.title("🤖 Agente IA: Análisis de Índices Globales & Confluencia de Valor")
st.markdown("### Auditoría institucionalizada: Diagnóstico macro de los 5 grandes índices combinada con selección estricta de acciones.")
st.markdown("---")

# Sección de Monetización en la barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

tab1, tab2 = st.tabs(["🔍 Auditoría Manual", "🛰️ Radar Macroeconómico e Índices de Mercado"])

# =====================================================================
# PESTAÑA 1: ANÁLISIS MANUAL (Función original intacta)
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
# PESTAÑA 2: RADAR MACROECONÓMICO DE ÍNDICES + ACCIONES & SMALL CAPS
# =====================================================================
with tab2:
    st.subheader("🛰️ Sistema de Rastreo de Índices y Filtro Fundamental en Tiempo Real")
    st.write("El agente ejecutará primero un diagnóstico de salud técnica de los 5 índices principales de EE.UU. y luego buscará oportunidades individuales bajo las reglas de Graham, Buffett y Lynch.")
    
    enfoque_mercado = st.selectbox(
        "Selecciona el universo de mercado a auditar hoy:",
        ["Grandes Líderes del Mercado (S&P 500 + Infraestructura)", "Joyas de Crecimiento (Small Caps / Russell 2000)", "Escanear Todo el Mercado Integrado"]
    )
    
    margen_exigido = st.slider("Margen de Seguridad Mínimo Exigido (%)", 15, 40, 20, key="slider_macro")

    if st.button("🛰️ Lanzar Algoritmo de Búsqueda Global", key="btn_auto"):
        
        # 1. ANÁLISIS EN VIVO DE LOS 5 GRANDES ÍNDICES
        st.subheader("📊 Diagnóstico Técnico de los Índices del Mercado")
        indices_dict = {
            "S&P 500 🏢": "^GSPC",
            "Dow Jones 🏗️": "^DJI",
            "NASDAQ Composite 💻": "^IXIC",
            "NASDAQ 100 🚀": "^NDX",
            "Russell 2000 (Small Caps) 🌱": "^RUT"
        }
        
        analisis_indices = []
        with st.spinner("Agente auditando la tendencia macroeconómica de los índices..."):
            for nombre_ind, ticker_ind in indices_dict.items():
                try:
                    ind = yf.Ticker(ticker_ind)
                    hist = ind.history(period="5d")
                    if len(hist) >= 2:
                        precio_actual = hist['Close'].iloc[-1]
                        precio_previo = hist['Close'].iloc[-2]
                        cambio_diario = ((precio_actual - precio_previo) / precio_previo) * 100
                        
                        # Tendencia básica semanal
                        precio_inicial = hist['Close'].iloc[0]
                        tendencia_5d = "📈 Alcista" if precio_actual > precio_inicial else "📉 Bajista"
                        
                        analisis_indices.append({
                            "Índice": nombre_ind,
                            "Nivel de Cierre": round(precio_actual, 2),
                            "Cambio Diario": f"{cambio_diario:+.2f}%",
                            "Tendencia Corto Plazo": tendencia_5d
                        })
                except:
                    pass
        
        df_indices = pd.DataFrame(analisis_indices)
        if not df_indices.empty:
            st.dataframe(df_indices, use_container_width=True)
        else:
            st.warning("No se pudo extraer la información en tiempo real de los índices.")

        # 2. DEFINICIÓN DEL POOL DE ACCIONES INDIVIDUALEZ SEGÚN TU SELECCIÓN
        with st.spinner("Mapeando el mapa de activos seleccionados..."):
            if enfoque_mercado == "Grandes Líderes del Mercado (S&P 500 + Infraestructura)":
                pool_dinamico = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "V", "MA", "PG", "KO", "NKE", "TGT", "CEG", "OKLO"]
            elif enfoque_mercado == "Joyas de Crecimiento (Small Caps / Russell 2000)":
                pool_dinamico = ["CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "UFPI", "SKX", "CALM"]
            else:
                pool_dinamico = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "V", "MA", "PG", "KO", "NKE", "TGT", "CEG", "OKLO", "CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "UFPI", "SKX", "CALM"]

        oportunidades = []
        progress = st.progress(0)
        status = st.empty()
        
        # 3. FILTRO INDIVIDUAL DE ACCIONES Y SMALL CAPS DE CRECIMIENTO
        for idx, t in enumerate(pool_dinamico):
            status.text(f"Auditoría fundamental en vivo (Graham/Buffett/Lynch): {t}...")
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
                crecimiento_ganancias = info.get('earningsGrowth', None)
                
                crecimiento_calculo = crecimiento_ganancias or 0.05
                if crecimiento_calculo <= 0: crecimiento_calculo = 0.05
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento_calculo * 100)))
                    descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                    
                    if valor_intrinseco > precio and descuento >= margen_exigido:
                        
                        is_small_cap = cap_mercado < 6000000000
                        tipo_empresa = "Small Cap de Crecimiento 🚀" if is_small_cap else "Large/Mega Cap 🏢"
                        
                        # Cortafuegos crítico: Descartar de forma autónoma Small Caps sin crecimiento verificado
                        if is_small_cap and (crecimiento_ganancias is None or crecimiento_ganancias <= 0.02):
                            continue 
                        
                        # Evaluación combinada institucional
                        cumple_graham = "✅ CUMPLE (Baja Deuda)" if (deuda_capital and deuda_capital < 100) else "❌ RIESGO (Apalancada)"
                        cumple_buffett = "✅ CUMPLE (Moat Sólido)" if (roe and roe >= 0.15) else "❌ SIN MOAT (Bajo ROE)"
                        cumple_lynch = "✅ CUMPLE (Buen Precio)" if (peg and peg <= 1.5) else "❌ AJUSTADO (Múltiplo Alto)"
                        
                        tasa_str = f"{crecimiento_ganancias*100:.1f}%" if crecimiento_ganancias else "N/D (Est. 5%)"
                        
                        informe_ejecutivo = (
                            f"Sector: {sector} ({tipo_empresa}). Expansión Trimestral: {tasa_str}.\n"
                            f"Fórmula Graham-Lynch: Valor Intrínseco de ${valor_intrinseco:.2f} vs Cotización de ${precio:.2f} "
                            f"({descuento:.1f}% Margen de Seguridad).\n"
                            f"• Filtro Graham: {cumple_graham} (Relación: {deuda_capital if deuda_capital else 'N/D'}%)\n"
                            f"• Filtro Buffett: {cumple_buffett} (ROE: {f'{roe*100:.1f}%' if roe else 'N/D'})\n"
                            f"• Filtro Peter Lynch: {cumple_lynch} (PEG: {peg if peg else 'N/D'})"
                        )
                        
                        oportunidades.append({
                            "Ticker": t,
                            "Empresa": nombre,
                            "Sector": sector,
                            "Categoría": tipo_empresa,
                            "Precio Actual": precio,
                            "Crecimiento Beneficios": tasa_str,
                            "Valor Real Estimado": round(valor_intrinseco, 2),
                            "Margen de Seguridad": f"{descuento:.1f}%",
                            "Dictamen del Agente": informe_ejecutivo
                        })
            except:
                pass
                
        status.text("¡Auditoría de espectro completo e índices finalizada!")
        
        # 4. ENTREGA DE RESULTADOS MULTI-FORMATO (EXCEL CON PESTAÑAS Y BOLETÍN)
        if oportunidades:
            st.success(f"🎯 El Agente detectó {len(oportunidades)} acciones individuales que superan los filtros.")
            df_final = pd.DataFrame(oportunidades)
            
            # --- CREACIÓN EXCEL NATIVO AVANZADO CON MÚLTIPLES HOJAS ---
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                # Hoja 1: Diagnóstico de Índices del mercado
                df_indices.to_excel(writer, index=False, sheet_name='Estado de Índices Macro')
                # Hoja 2: Acciones individuales baratas y Small Caps filtradas
                df_final.to_excel(writer, index=False, sheet_name='Acciones Filtradas IA')
            buffer.seek(0)
            
            st.subheader("📥 Descarga de Herramientas Profesionales")
            st.download_button(
                label="🟢 Descargar Reporte Completo (Índices + Acciones) en Excel (.xlsx)",
                data=buffer,
                file_name='reporte_macro_y_confluencia_ia.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
            st.subheader("📊 Vista Previa de Acciones Filtradas")
            st.dataframe(df_final, use_container_width=True)
            
            # --- CONSTRUCCIÓN DEL BOLETÍN INTEGRAL PARA SEGUIDORES ---
            boletin = (
                f"📢 **INFORME ESTRATÉGICO GLOBAL: ÍNDICES MACRO & CONFLUENCIA FINANCIERA** 🚀\n\n"
                f"Estimada comunidad: Compartimos el reporte consolidado de nuestro Agente de IA.\n\n"
                f"⚖️ **1. SALUD MACROECONÓMICA DEL MERCADO (ÍNDICES)**\n"
            )
            for idx_row in analisis_indices:
                boletin += f"• {idx_row['Índice']}: Cierre en {idx_row['Nivel de Cierre']} | Variación Diaria: {idx_row['Cambio Diario']} | Tendencia: {idx_row['Tendencia Corto Plazo']}\n"
                
            boletin += (
                f"\n🎯 **2. JOYAS INDIVIDUALES DETECTADAS (FILTRO DE LOS MAESTROS)**\n"
                f"Sometimos el mercado al criterio de Graham, Buffett y Peter Lynch buscando valor e inversión estricta en Small Caps de crecimiento.\n"
                f"======================================================\n"
            )
            for op in oportunidades:
                boletin += (
                    f"\n💎 **{op['Empresa']} ({op['Ticker']})**\n"
                    f"• Sector y Categoría: {op['Sector']} | {op['Categoría']}\n"
                    f"• Expansión Real de Beneficios: {op['Crecimiento Beneficios']}\n"
                    f"• Precio de Cotización: ${op['Precio Actual']:.2f} | Valor Real Estimado: ${op['Valor Real Estimado']:.2f}\n"
                    f"• Margen de Seguridad Presentado: {op['Margen de Seguridad']}\n"
                    f"• Dictamen de Auditoría:\n{op['Dictamen del Agente']}\n"
                    f"------------------------------------------------------\n"
                )
            boletin += "\n*Este informe técnico automatizado evalúa variables financieras macro e institucionales, no constituye asesoría financiera directa.*"
            
            st.subheader("📋 Boletín Integral para Seguidores (Listo para copiar/pegar)")
            st.text_area("Texto Completo (Índices + Acciones):", boletin, height=400)
            
        else:
            st.info("El escáner de acciones no arrojó resultados con el margen exigido, pero puedes ver arriba el estado técnico de los índices.")
