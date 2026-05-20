import streamlit as st
import yfinance as yf
import pandas as pd
import io

# Configuración de interfaz profesional
st.set_page_config(page_title="Agente IA: Terminal Macro & Horizontes de Inversión", layout="wide")

st.title("🤖 Agente IA: Terminal Macro Global & Horizontes de Inversión")
st.markdown("### Inteligencia de Capitales: Escaneo de Índices, Rotación Sectorial y Clasificación de Oportunidades a Corto y Largo Plazo con Confluencia Fundamental.")
st.markdown("---")

# Sección de Monetización en la barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

# Manteniendo las 3 pestañas intactas y ordenadas
tab1, tab2, tab3 = st.tabs([
    "🔍 Auditoría Manual", 
    "🛰️ Radar Macroeconómico e Índices del Mundo",
    "🧱 Rotación de Sectores y Flujo de Capital"
])

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
# PESTAÑA 2: RADAR MACRO + ESCANEO SEGMENTADO POR ÍNDICE (Con Horizontes)
# =====================================================================
with tab2:
    st.subheader("🛰️ Sistema de Rastreo Global y Filtro Fundamental en Tiempo Real")
    st.write("Selecciona qué índice oficial deseas que el agente barra por completo para extraer las acciones individuales que cumplen tus condiciones.")
    
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
        
        st.subheader("📊 Diagnóstico Técnico de Índices Globales")
        indices_dict = {
            "S&P 500 (EE.UU.) 🏢": "^GSPC", "Dow Jones (EE.UU.) 🏗️": "^DJI", "NASDAQ Composite (EE.UU.) 💻": "^IXIC",
            "NASDAQ 100 (EE.UU.) 🚀": "^NDX", "Russell 2000 (Small Caps) 🌱": "^RUT", "Euro Stoxx 50 (Europa) 🇪🇺": "^STOXX50E",
            "DAX (Alemania) 🇩🇪": "^GDAXI", "FTSE 100 (Reino Unido) 🇬🇧": "^FTSE", "Nikkei 225 (Japón) 🇯🇵": "^N225",
            "Hang Seng (Hong Kong) 🇭🇰": "^HSI", "Bovespa (Brasil) 🇧🇷": "^BVSP", "S&P/BMV IPC (México) 🇲🇽": "^MXX"
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
                            "Región / Índice": nombre_ind, "Nivel de Cierre": round(precio_actual, 2),
                            "Cambio Diario": f"{cambio_diario:+.2f}%", "Tendencia Semanal": tendencia_5d
                        })
                except:
                    pass
        
        df_indices = pd.DataFrame(analisis_indices)
        if not df_indices.empty:
            st.dataframe(df_indices, use_container_width=True)

        dict_sp500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "MA", "JPM", "BAC", "XOM", "CVX", "PG", "KO", "NKE", "TGT", "COST", "WMT", "HD", "JNJ", "PFE", "UNH", "MRK"]
        dict_nasdaq = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "AMD", "QCOM", "INTC", "TSM", "ASML", "ISRG", "NFLX", "ADBE", "PANW", "CEG", "OKLO"]
        dict_dowjones = ["AAPL", "MSFT", "AMZN", "V", "JPM", "AXP", "PG", "KO", "WMT", "HD", "JNJ", "UNH", "MRK", "CAT", "DE", "HON", "BA", "MMM", "DIS", "CVX"]
        dict_russell2000 = ["CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM", "PDFS", "CEVA", "AEIS", "COHR", "UFPI", "AIT", "FIX", "AMWD", "PLUS", "SKX", "MED", "CALM", "SFBS", "CCRN", "NEOG", "LNTH"]

        pool_dinamico = []
        mapeo_origen = {}

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
            for tk in dict_sp500: mapeo_origen[tk] = "S&P 500 🏢"
            for tk in dict_nasdaq: mapeo_origen[tk] = "NASDAQ 100 🚀"
            for tk in dict_dowjones: mapeo_origen[tk] = "Dow Jones 🏗️"
            for tk in dict_russell2000: mapeo_origen[tk] = "Russell 2000 (Small Cap) 🌱"
            pool_dinamico = list(set(dict_sp500 + dict_nasdaq + dict_dowjones + dict_russell2000))

        oportunidades = []
        progress = st.progress(0)
        status = st.empty()
        
        for idx, t in enumerate(pool_dinamico):
            indice_procedencia = mapeo_origen.get(t, "Mercado General")
            status.text(f"Auditando de [{indice_procedencia}] ({idx+1}/{len(pool_dinamico)}): {t}...")
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
                vol_actual = info.get('volume', 1)
                vol_prom = info.get('averageVolume', 1)
                ratio_vol = vol_actual / vol_prom
                
                crecimiento_calculo = crecimiento_ganancias or 0.05
                if crecimiento_calculo <= 0: crecimiento_calculo = 0.05
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento_calculo * 100)))
                    descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                    
                    if valor_intrinseco > precio and descuento >= margen_exigido:
                        is_small_cap = cap_mercado < 6000000000
                        tipo_empresa = "Small Cap de Crecimiento 🚀" if is_small_cap else "Large/Mega Cap 🏢"
                        if is_small_cap and (crecimiento_ganancias is None or crecimiento_ganancias <= 0.02):
                            continue 
                        
                        # ---- ASIGNACIÓN INTELIGENTE DE HORIZONTE TEMPORAL ----
                        # Corto Plazo: Anomalías de inyección institucional (volumen) que impulsarán el precio pronto.
                        # Largo Plazo: Empresas consolidadas con crecimiento constante ideales para compounding.
                        if ratio_vol >= 1.20 or is_small_cap:
                            horizonte_sugerido = "⏳ Corto/Medio Plazo (Momento de Volumen/Catalizador)"
                        else:
                            horizonte_sugerido = "📈 Largo Plazo (Moat Seguro / Compounding)"
                        
                        cumple_graham = "✅ CUMPLE" if (deuda_capital and deuda_capital < 100) else "❌ RIESGO"
                        cumple_buffett = "✅ CUMPLE" if (roe and roe >= 0.15) else "❌ SIN MOAT"
                        cumple_lynch = "✅ CUMPLE" if (peg and peg <= 1.5) else "❌ AJUSTADO"
                        tasa_str = f"{crecimiento_ganancias*100:.1f}%" if crecimiento_ganancias else "N/D"
                        
                        informe_ejecutivo = (f"Índice: {indice_procedencia} | Horizonte: {horizonte_sugerido}\n"
                                             f"Graham: {cumple_graham} | Buffett: {cumple_buffett} | Lynch: {cumple_lynch}")
                        
                        oportunidades.append({
                            "Ticker": t, "Empresa": nombre, "Índice de Origen": indice_procedencia, "Sector": sector,
                            "Plazo Sugerido": horizonte_sugerido, "Precio Actual": precio, "Crecimiento": tasa_str,
                            "Valor Real Estimado": round(valor_intrinseco, 2), "Margen de Seguridad": f"{descuento:.1f}%", "Dictamen del Agente": informe_ejecutivo
                        })
            except:
                pass
                
        status.text("¡Auditoría por índices finalizada!")
        if oportunidades:
            df_final = pd.DataFrame(oportunidades)
            
            # Reorganizar columnas para dar visibilidad al Plazo Sugerido
            cols = ["Ticker", "Empresa", "Índice de Origen", "Plazo Sugerido", "Precio Actual", "Valor Real Estimado", "Margen de Seguridad", "Sector", "Dictamen del Agente"]
            df_final = df_final[cols]
            
            st.dataframe(df_final, use_container_width=True)

# =====================================================================
# PESTAÑA 3: ROTACIÓN DE SECTORES Y FLUJO DE CAPITAL (Con Horizontes)
# =====================================================================
with tab3:
    st.subheader("🧱 Análisis de Fuerza Sectorial y Rastreador de Flujos (Smart Money)")
    st.write("El agente audita los 11 ETFs sectoriales del SPDR (GICS) para identificar el sector más castigado y monitorizar anomalías de volumen institucional.")
    
    margen_sectores = st.slider("Margen de Seguridad para Acciones Sectoriales (%)", 15, 40, 20, key="slider_p3")

    if st.button("🛰️ Analizar Rotación de Sectores e Inyección de Capital", key="btn_p3"):
        
        sectores_etf = {
            "Tecnológico de Información 💻": "XLK", "Finanzas 🏦": "XLF", "Salud 🩺": "XLV",
            "Consumo Discrecional 🛍️": "XLY", "Consumo Básico 🛒": "XLP", "Comunicación 📱": "XLC",
            "Industrial 🏗️": "XLI", "Energía ⚡": "XLE", "Materiales 🧱": "XLB",
            "Servicios Públicos (Utilities) 🚰": "XLU", "Inmobiliario (Real Estate) 🏢": "XLRE"
        }
        
        desempeno_sectores = []
        
        with st.spinner("Midiendo fuerza relativa y variaciones de los 11 sectores oficiales..."):
            for nombre_sec, ticker_sec in sectores_etf.items():
                try:
                    etf = yf.Ticker(ticker_sec)
                    hist_sec = etf.history(period="5d")
                    if len(hist_sec) >= 2:
                        cierre_hoy = hist_sec['Close'].iloc[-1]
                        cierre_previo = hist_sec['Close'].iloc[-2]
                        var_diaria = ((cierre_hoy - cierre_previo) / cierre_previo) * 100
                        cierre_inicial = hist_sec['Close'].iloc[0]
                        rendimiento_5d = ((cierre_hoy - cierre_inicial) / cierre_inicial) * 100
                        
                        desempeno_sectores.append({
                            "Sector": nombre_sec, "ETF Referencia": ticker_sec,
                            "Cambio Diario": var_diaria, "Rendimiento Semanal (%)": round(rendimiento_5d, 2)
                        })
                except:
                    pass
                    
        df_sectores = pd.DataFrame(desempeno_sectores)
        
        if not df_sectores.empty:
            df_sectores = df_sectores.sort_values(by="Rendimiento Semanal (%)", ascending=True)
            sector_mas_castigado = df_sectores.iloc[0]['Sector']
            ticker_castigado = df_sectores.iloc[0]['ETF Referencia']
            peor_rendimiento = df_sectores.iloc[0]['Rendimiento Semanal (%)']
            
            st.success(f"🚨 **Sector Más Castigado del Mercado:** {sector_mas_castigado} ({ticker_castigado}) con un rendimiento semanal de {peor_rendimiento:.2f}%")
            
            st.markdown("### 📊 Desempeño de los 11 Sectores GICS")
            df_sec_mostrar = df_sectores.copy()
            df_sec_mostrar["Cambio Diario"] = df_sec_mostrar["Cambio Diario"].map("{:+.2f}%".format)
            st.dataframe(df_sec_mostrar, use_container_width=True)
            
            mapeo_acciones_sector = {
                "Tecnológico de Información 💻": ["AAPL", "MSFT", "NVDA", "AVGO", "AMD", "QCOM", "CRUS", "POWI", "SLAB", "NVMI", "ONTO", "FORM"],
                "Finanzas 🏦": ["V", "MA", "JPM", "BAC", "MS", "GS", "AXP", "SFBS", "CCRN"],
                "Salud 🩺": ["JNJ", "PFE", "UNH", "MRK", "ABV", "LLY", "NEOG", "LNTH"],
                "Consumo Discrecional 🛍️": ["NKE", "TGT", "HD", "AMZN", "SBUX", "SKX", "DECK", "CROX"],
                "Consumo Básico 🛒": ["PG", "KO", "PEP", "COST", "WMT", "CL", "CALM"],
                "Comunicación 📱": ["GOOGL", "META", "NFLX", "DIS"],
                "Industrial 🏗️": ["CAT", "DE", "HON", "UPS", "FDX", "UFPI", "AIT", "FIX", "PLUS"],
                "Energía ⚡": ["XOM", "CVX", "CEG", "OKLO", "VST", "SMR"],
                "Materiales 🧱": ["XLB", "AWI", "MLI"],
                "Servicios Públicos (Utilities) 🚰": ["NEE", "XLU"],
                "Inmobiliario (Real Estate) 🏢": ["XLRE", "PLD"]
            }
            
            st.markdown(f"### 🔍 Buscando Oportunidades en el Sector Castigado: {sector_mas_castigado}")
            acciones_a_evaluar = mapeo_acciones_sector.get(sector_mas_castigado, ["GOOGL", "V", "NKE"])
            
            oportunidades_sectoriales = []
            for t in acciones_a_evaluar:
                try:
                    ticker = yf.Ticker(t)
                    info = ticker.info
                    precio = info.get('currentPrice', 0)
                    eps = info.get('trailingEps', 0)
                    cap_mercado = info.get('marketCap', 0)
                    crecimiento_ganancias = info.get('earningsGrowth', 0.05) or 0.05
                    
                    if eps and eps > 0:
                        valor_intrinseco = eps * (8.5 + (2 * (crecimiento_ganancias * 100)))
                        descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                        
                        if valor_intrinseco > precio and descuento >= margen_sectores:
                            is_small_cap = cap_mercado < 6000000000
                            if is_small_cap and crecimiento_ganancias <= 0.02:
                                continue
                            
                            # En el sector castigado, la capitulación abre oportunidades tácticas de Corto/Medio Plazo por rebote fundamental
                            hz_sectorial = "⏳ Corto/Medio Plazo (Rebote Táctico en Zona de Pánico)" if peor_rendimiento < -2 else "📈 Largo Plazo (Moat Estable)"
                                
                            oportunidades_sectoriales.append({
                                "Ticker": t, "Empresa": info.get('longName', t), "Plazo Asignado": hz_sectorial, "Precio": precio,
                                "Valor Intrínseco": round(valor_intrinseco, 2), "Descuento": f"{descuento:.1f}%"
                            })
                except:
                    pass
                    
            if oportunidades_sectoriales:
                st.dataframe(pd.DataFrame(oportunidades_sectoriales), use_container_width=True)
                
            # 3. MONITOREO DE ACUMULACIÓN Y FLUJO DE CAPITAL (SMART MONEY)
            st.markdown("### 🛰️ Rastreador de Flujo de Capital (Anomalías de Volumen)")
            
            todos_los_activos = []
            for lista in mapeo_acciones_sector.values():
                todos_los_activos.extend(lista)
            todos_los_activos = list(set(todos_los_activos))
            
            flujo_capital = []
            with st.spinner("Analizando volumen de transacciones institucionales..."):
                for t in todos_los_activos:
                    try:
                        ticker = yf.Ticker(t)
                        info = ticker.info
                        volumen_actual = info.get('volume', 0)
                        volumen_promedio = info.get('averageVolume', 1)
                        precio = info.get('currentPrice', 0)
                        sector_pertenece = info.get('sector', 'Otros')
                        ratio_volumen = volumen_actual / volumen_promedio
                        
                        if volumen_actual > 0:
                            flujo_capital.append({
                                "Ticker": t, "Empresa": info.get('longName', t), "Sector": sector_pertenece,
                                "Precio": precio, "Volumen Hoy": volumen_actual, "Anomalía de Inyección (Ratio)": round(ratio_volumen, 2)
                            })
                    except:
                        pass
                        
            df_flujo = pd.DataFrame(flujo_capital)
            if not df_flujo.empty:
                df_acumulacion = df_flujo.sort_values(by="Anomalía de Inyección (Ratio)", ascending=False).head(5)
                
                st.write("🔥 **Top 5 Acciones con Mayor Acumulación de Volumen hoy:**")
                st.dataframe(df_acumulacion, use_container_width=True)
                
                sector_migracion = df_flujo.groupby("Sector")["Anomalía de Inyección (Ratio)"].mean().reset_index()
                sector_migracion = sector_migracion.sort_values(by="Anomalía de Inyección (Ratio)", ascending=False)
                sector_lider_flujo = sector_migracion.iloc[0]['Sector']
                st.info(f"💰 **Destino Institucional:** El capital inteligente está migrando o acumulándose con mayor fuerza en el sector: **{sector_lider_flujo}**")
