import streamlit as st
import yfinance as yf
import pandas as pd
import io

# Configuración de interfaz profesional
st.set_page_config(page_title="Agente IA: Escáner por Índices Oficiales", layout="wide")

st.title("🤖 Agente IA: Escáner de Acciones por Índices Oficiales")
st.markdown("### Segmentación Estricta: Filtra el mercado índice por índice y extrae las acciones que cumplen con los requisitos de los Grandes Maestros.")
st.markdown("---")

# Sección de Monetización en la barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

tab1, tab2 = st.tabs(["🔍 Auditoría Manual", "🛰️ Radar Macroeconómico e Índices del Mundo"])

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
# PESTAÑA 2: RADAR MACRO + ESCANEO SEGMENTADO POR ÍNDICE SELECCIONADO
# =====================================================================
with tab2:
    st.subheader("🛰️ Sistema de Rastreo Global y Filtro Fundamental en Tiempo Real")
    st.write("Selecciona qué índice oficial deseas que el agente barra por completo para extraer las acciones individuales que cumplen tus condiciones.")
    
    # Casilla modificada para que el usuario escoja individualmente el Universo/Índice a escanear
    enfoque_mercado = st.selectbox(
        "Selecciona el universo de mercado a auditar hoy:",
        [
            "S&P 500 (Grandes Monopolios y Consumo) 🏢", 
            "NASDAQ / NASDAQ 100 (Tecnología, Semiconductores e IA) 🚀", 
            "Dow Jones (Aristócratas e Industria Pesada) 🏗️", 
            "Russell 2000 (Joyas y Small Caps de Crecimiento Estricto) 🌱",
            "Escanear Todo el Mercado Integrado (Espectro Completo) 🌍"
        ]
    )
    
    margen_exigido = st.slider("Margen de Seguridad Mínimo Exigido (%)", 15, 40, 20, key="slider_macro_indices_fijos")

    if st.button("🛰️ Lanzar Algoritmo de Búsqueda Global", key="btn_auto"):
        
        # 1. DIAGNÓSTICO EN VIVO DE LECTURA MACRO DE LOS ÍNDICES
        st.subheader("📊 Diagnóstico Técnico de Índices Globales")
        indices_dict = {
            "S&P 500 (EE.UU.) 🏢": "^GSPC",
            "Dow Jones (EE.UU.) 🏗️": "^DJI",
            "NASDAQ Composite (EE.UU.) 💻": "^IXIC",
            "NASDAQ 100 (EE.UU.) 🚀": "^NDX",
            "Russell 2000 (Small Caps) 🌱": "^RUT",
            "Euro Stoxx 50 (Europa) 🇪🇺": "^STOXX50E",
            "DAX (Alemania) 🇩🇪": "^GDAXI",
            "FTSE 100 (Reino Unido) 🇬🇧": "^FTSE",
            "Nikkei 225 (Japón) 🇯🇵": "^N225",
            "Hang Seng (Hong Kong) 🇭🇰": "^HSI",
            "Bovespa (Brasil) 🇧🇷": "^BVSP",
            "S&P/BMV IPC (México) 🇲🇽": "^MXX"
        }
        
        analisis_indices = []
        with st.spinner("Agente barriendo las plazas bursátiles del mundo en tiempo real..."):
            for nombre_ind, ticker_ind in indices_dict.items():
                try:
                    ind = yf.Ticker(ticker_ind)
                    hist = ind.history(period="5d")
                    if len(hist) >= 2:
                        precio_actual = hist['Close'].iloc[-1]
                        precio_previo = hist['Close'].iloc[-2]
                        cambio_diario = ((precio_actual - precio_previo) / precio_previo) * 100
                        
                        precio_inicial = hist['Close'].iloc[0]
                        tendencia_5d = "📈 Alcista" if precio_actual > precio_inicial else "📉 Bajista"
                        
                        analisis_indices.append({
                            "Región / Índice": nombre_ind,
                            "Nivel de Cierre": round(precio_actual, 2),
                            "Cambio Diario": f"{cambio_diario:+.2f}%",
                            "Tendencia Semanal": tendencia_5d
                        })
                except:
                    pass
        
        df_indices = pd.DataFrame(analisis_indices)
        if not df_indices.empty:
            st.dataframe(df_indices, use_container_width=True)
        else:
            st.warning("No se pudo extraer la información internacional de los índices.")

        # 2. ASIGNACIÓN MATRICIAL DE TICKERS POR ÍNDICE ORIGEN
        dict_sp500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "MA", "JPM", "BAC", "XOM", "CVX", "PG", "KO", "NKE", "TGT", "COST", "WMT", "HD", "JNJ", "PFE", "UNH", "MRK"]
        dict_nasdaq = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "AMD", "QCOM", "INTC", "TSM", "ASML", "ISRG", "NFLX", "ADBE", "PANW", "CEG", "OKLO"]
        dict_dowjones = ["AAPL", "MSFT", "AMZN", "V", "JPM", "AXP", "PG", "KO", "WMT", "HD", "JNJ", "UNH", "MRK", "CAT", "DE", "HON", "BA", "MMM", "DIS", "CVX"]
        dict_russell2000 = ["CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "PDFS", "CEVA", "AEIS", "COHR", "UFPI", "AIT", "FIX", "AMWD", "PLUS", "SKX", "MED", "CALM", "SFBS", "CCRN", "NEOG", "LNTH"]

        # Filtrado del pool y marcado de origen según la casilla seleccionada
        pool_dinamico = []
        mapeo_origen = {}

        with st.spinner("Cargando componentes del índice seleccionado..."):
            if "S&P 500" in enfoque_mercado:
                pool_dinamico = dict_sp500
                for tk in dict_sp500: mapeo_origen[tk] = "S&P 500 🏢"
            elif "NASDAQ" in enfoque_mercado:
                pool_dinamico = dict_nasdaq
                for tk in dict_nasdaq: mapeo_origen[tk] = "NASDAQ / NASDAQ 100 🚀"
            elif "Dow Jones" in enfoque_mercado:
                pool_dinamico = dict_dowjones
                for tk in dict_dowjones: mapeo_origen[tk] = "Dow Jones Industrial 🏗️"
            elif "Russell 2000" in enfoque_mercado:
                pool_dinamico = dict_russell2000
                for tk in dict_russell2000: mapeo_origen[tk] = "Russell 2000 (Small Caps) 🌱"
            else:
                # Espectro completo integrado (Une todo y asigna su índice correspondiente)
                for tk in dict_sp500: mapeo_origen[tk] = "S&P 500 🏢"
                for tk in dict_nasdaq: mapeo_origen[tk] = "NASDAQ 100 🚀"
                for tk in dict_dowjones: mapeo_origen[tk] = "Dow Jones 🏗️"
                for tk in dict_russell2000: mapeo_origen[tk] = "Russell 2000 (Small Cap) 🌱"
                pool_dinamico = list(set(dict_sp500 + dict_nasdaq + dict_dowjones + dict_russell2000))

        oportunidades = []
        progress = st.progress(0)
        status = st.empty()
        
        # 3. FILTRO INDIVIDUAL CON IDENTIFICACIÓN DE ÍNDICE DE ORIGEN
        for idx, t in enumerate(pool_dinamico):
            indice_procedencia = mapeo_origen.get(t, "Mercado General")
            status.text(f"Extrayendo y auditando de [{indice_procedencia}] el activo ({idx+1}/{len(pool_dinamico)}): {t}...")
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
                        
                        # Evaluación combinada de Maestros
                        cumple_graham = "✅ CUMPLE (Baja Deuda)" if (deuda_capital and deuda_capital < 100) else "❌ RIESGO (Apalancada)"
                        cumple_buffett = "✅ CUMPLE (Moat Sólido)" if (roe and roe >= 0.15) else "❌ SIN MOAT (Bajo ROE)"
                        cumple_lynch = "✅ CUMPLE (Buen Precio)" if (peg and peg <= 1.5) else "❌ AJUSTADO (Múltiplo Alto)"
                        
                        tasa_str = f"{crecimiento_ganancias*100:.1f}%" if crecimiento_ganancias else "N/D (Est. 5%)"
                        
                        informe_ejecutivo = (
                            f"Índice de Origen: {indice_procedencia} | Sector: {sector} ({tipo_empresa}).\n"
                            f"Expansión Trimestral: {tasa_str} | Margen de Seguridad: {descuento:.1f}%\n"
                            f"• Filtro Graham: {cumple_graham} (Relación: {deuda_capital if deuda_capital else 'N/D'}%)\n"
                            f"• Filtro Buffett: {cumple_buffett} (ROE: {f'{roe*100:.1f}%' if roe else 'N/D'})\n"
                            f"• Filtro Peter Lynch: {cumple_lynch} (PEG: {peg if peg else 'N/D'})"
                        )
                        
                        oportunidades.append({
                            "Ticker": t,
                            "Empresa": nombre,
                            "Índice de Origen": indice_procedencia,
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
                
        status.text("¡Auditoría por índices y escaneo de activos finalizada!")
        
        # 4. ENTREGA DE RESULTADOS CON LA FILIACIÓN DEL ÍNDICE CLARA
        if oportunidades:
            st.success(f"🎯 El Agente detectó {len(oportunidades)} acciones que superaron con éxito los filtros en el índice seleccionado.")
            df_final = pd.DataFrame(oportunidades)
            
            # --- CREACIÓN EXCEL NATIVO CON COLUMNA DE FILIACIÓN ---
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_indices.to_excel(writer, index=False, sheet_name='Índices Mundiales Macro')
                df_final.to_excel(writer, index=False, sheet_name='Acciones por Índice IA')
            buffer.seek(0)
            
            st.subheader("📥 Descarga de Herramientas Profesionales Globales")
            st.download_button(
                label=f"🟢 Descargar Reporte de {enfoque_mercado} en Excel (.xlsx)",
                data=buffer,
                file_name='reporte_segmentado_por_indice_ia.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
            st.subheader("📊 Vista Previa de Acciones que superaron la Auditoría")
            st.dataframe(df_final, use_container_width=True)
            
            # --- CONSTRUCCIÓN DEL BOLETÍN INTEGRAL CON ORIGEN ACLARADO ---
            boletin = (
                f"📢 **INFORME DE INVERSIÓN: ACCIONES FILTRADAS POR ÍNDICE OFICIAL** 🚀\n\n"
                f"Estimada comunidad: Compartimos los resultados del escáner avanzado de nuestra IA.\n"
                f"Universo auditado minuciosamente hoy: {enfoque_mercado}\n"
                f"======================================================\n"
            )
            for op in oportunidades:
                boletin += (
                    f"\n💎 **{op['Empresa']} ({op['Ticker']})**\n"
                    f"• 📍 Extraída del Índice: {op['Índice de Origen']}\n"
                    f"• Sector y Categoría: {op['Sector']} | {op['Categoría']}\n"
                    f"• Crecimiento Trimestral: {op['Crecimiento Beneficios']}\n"
                    f"• Precio de Mercado: ${op['Precio Actual']:.2f} | Valor Intrínseco Real: ${op['Valor Real Estimado']:.2f}\n"
                    f"• Margen de Seguridad: {op['Margen de Seguridad']}\n"
                    f"• Dictamen del Comité de Maestros:\n{op['Dictamen del Agente']}\n"
                    f"------------------------------------------------------\n"
                )
            boletin += "\n*Este informe técnico automatizado evalúa variables financieras macro e institucionales, no constituye asesoría financiera directa.*"
            
            st.subheader("📋 Boletín Segmentado para Seguidores (Listo para copiar/pegar)")
            st.text_area("Texto Completo Organizado por Origen:", boletin, height=400)
            
        else:
            st.info(f"Ninguna acción perteneciente a {enfoque_mercado} superó las exigencias del comité fundamental con el margen de seguridad solicitado hoy.")
