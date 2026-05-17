import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de la Página
st.set_page_config(page_title="Agente IA Financiero Pro", layout="wide")

st.title("🤖 Agente Financiero Pro: Multi-Sectores y Valor Intrínseco")
st.markdown("Analizador avanzado y cazador automático de oportunidades con margen de seguridad.")
st.markdown("---")

# Barra lateral para monetización
st.sidebar.header("👑 Membresía VIP")
st.sidebar.write("Accede a las alertas en tiempo real vía Telegram y reportes institucionales detallados.")
st.sidebar.markdown("[👉 Unirse al Club de Inversores](https://substack.com)") 

# Creamos pestañas para organizar las dos funciones sin que choquen
tab1, tab2 = st.tabs(["🔍 Analizar Mis Acciones", "🎯 Cazador Automático Multisectorial"])

# =====================================================================
# PESTAÑA 1: ANALIZAR ACCIONES MANUALES (Tu función anterior intacta)
# =====================================================================
with tab1:
    st.subheader("Analiza tu propia lista de vigilancia")
    tickers_input = st.text_input(
        "Escribe los tickers separados por comas:", 
        "V, NKE, GOOGL, TGT",
        key="manual_tickers"
    )

    lista_tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if st.button("🚀 Iniciar Investigación de Valor", key="btn_manual"):
        if not lista_tickers:
            st.warning("Por favor, introduce al menos un ticker válido.")
        else:
            resultados = []
            with st.spinner("El agente está extrayendo estados financieros..."):
                for t in lista_tickers:
                    try:
                        ticker = yf.Ticker(t)
                        info = ticker.info
                        precio_actual = info.get('currentPrice', 0)
                        eps = info.get('trailingEps', 0)
                        nombre = info.get('longName', t)
                        sector = info.get('sector', 'Desconocido')
                        crecimiento = info.get('earningsGrowth', 0.05) or 0.05
                        if crecimiento <= 0: crecimiento = 0.05
                        
                        if eps and eps > 0:
                            valor_intrinseco = eps * (8.5 + (2 * (crecimiento * 100)))
                            if valor_intrinseco > precio_actual:
                                descuento = ((valor_intrinseco - precio_actual) / valor_intrinseco) * 100
                                oportunidad = f"SÍ ({descuento:.1f}% Desc.) 🔥"
                                veredicto = f"Empresa infravalorada. Cotiza por debajo de su valor real. Sector: {sector}."
                            else:
                                oportunidad = "NO ❌"
                                veredicto = "Sobrevalorada o a precio justo de mercado actualmente."
                        else:
                            valor_intrinseco = 0
                            oportunidad = "N/D"
                            veredicto = "Ganancias negativas o EPS no disponible."

                        resultados.append({
                            "Ticker": t, "Empresa": nombre, "Precio Actual": f"${precio_actual:.2f}",
                            "Valor Estimado (IA)": f"${valor_intrinseco:.2f}" if valor_intrinseco > 0 else "N/D",
                            "¿Oportunidad?": oportunidad, "Informe del Agente": veredicto
                        })
                    except:
                        pass
            if resultados:
                st.dataframe(pd.DataFrame(resultados), use_container_width=True)


# =====================================================================
# PESTAÑA 2: CAZADOR AUTOMÁTICO (Nueva función solicitada)
# =====================================================================
with tab2:
    st.subheader("Cazador de Oportunidades en Todos los Sectores")
    st.write("El agente escaneará una lista predefinida de empresas líderes de múltiples sectores (Tecnología, Consumo, Salud, Financiero, Industrial) para extraer las mejores oportunidades con descuento actual.")
    
    # Lista predefinida multisectorial de alta liquidez para el rastreo automático
    pool_mercado = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", # Tecnología / Digital
        "JPM", "BAC", "V", "MA",                 # Financiero
        "NKE", "TGT", "HD", "WMT", "KO",         # Consumo Cíclico y Básico
        "JNJ", "PFE", "UNH", "MRK",              # Salud / Farmacéutico
        "CAT", "GE", "MMM",                      # Industrial
        "XOM", "CVX"                             # Energía
    ]
    
    # Filtro opcional por si el usuario quiere buscar un margen mínimo de descuento
    margen_minimo = st.slider("Margen de descuento mínimo requerido (%)", 10, 50, 20)

    if st.button("🛰️ Escanear Todo el Mercado", key="btn_auto"):
        oportunidades_encontradas = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for index, t in enumerate(pool_mercado):
            status_text.text(f"Agente investigando sector de: {t}...")
            # Actualizar barra de progreso visual
            progress_bar.progress((index + 1) / len(pool_mercado))
            
            try:
                ticker = yf.Ticker(t)
                info = ticker.info
                
                precio_actual = info.get('currentPrice', 0)
                eps = info.get('trailingEps', 0)
                sector = info.get('sector', 'Otros')
                nombre = info.get('longName', t)
                crecimiento = info.get('earningsGrowth', 0.05) or 0.05
                if crecimiento <= 0: crecimiento = 0.05
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento * 100)))
                    
                    if valor_intrinseco > precio_actual:
                        descuento = ((valor_intrinseco - precio_actual) / valor_intrinseco) * 100
                        
                        # Guardar solo las que superan el margen elegido por el usuario
                        if descuento >= margen_minimo:
                            # El agente redacta el PORQUÉ detallado de la oportunidad
                            porque_informe = (
                                f"Oportunidad detectada en el sector **{sector}**. "
                                f"La empresa muestra una sólida base de ganancias con un EPS de ${eps:.2f}. "
                                f"El mercado la cotiza actualmente a ${precio_actual:.2f}, pero basándose en su ritmo de crecimiento, "
                                f"su valor intrínseco estimado es de **${valor_intrinseco:.2f}**, ofreciéndote un "
                                f"atractivo **{descuento:.1f}% de descuento (Margen de Seguridad)** ante fluctuaciones del mercado."
                            )
                            
                            oportunidades_encontradas.append({
                                "Ticker": t,
                                "Empresa": nombre,
                                "Sector": sector,
                                "Precio": f"${precio_actual:.2f}",
                                "Valor Real": f"${valor_intrinseco:.2f}",
                                "Descuento": f"{descuento:.1f}%",
                                "Tesis / ¿Por qué?": porque_informe
                            })
            except:
                pass
                
        status_text.text("¡Escaneo multisectorial completado!")
        
        # Mostrar resultados del radar masivo
        if oportunidades_encontradas:
            st.success(f"🎯 El Agente detectó {len(oportunidades_encontradas)} acciones con un descuento mayor al {margen_minimo}%.")
            df_oportunidades = pd.DataFrame(oportunidades_encontradas)
            
            # Mostrar como tabla interactiva
            st.dataframe(df_oportunidades, use_container_width=True)
            
            # Opción premium para descargar las alertas del radar
            csv_auto = df_oportunidades.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Tesis de Inversión (CSV)",
                data=csv_auto,
                file_name='radar_oportunidades_ia.csv',
                mime='text/csv',
            )
        else:
            st.info(f"El mercado está ajustado. Ninguna acción de la lista superó el {margen_minimo}% de descuento en este momento.")
