import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración Visual de la App
st.set_page_config(page_title="Agente IA Inversión", layout="wide", initial_sidebar_state="expanded")

st.title("🤖 Agente Financiero IA: Filtro de Valor")
st.markdown("---")

# Barra lateral para el modelo de monetización (puedes cambiar este texto por tu link de pago)
st.sidebar.header("👑 Versión Premium")
st.sidebar.write("Obtén acceso al cálculo automático del **Margen de Seguridad** y alertas por correo.")
st.sidebar.markdown("[👉 Suscribirse a la Newsletter Premium](https://substack.com)") 

# 2. Entrada de Datos
st.subheader("🔍 Analizar Lista de Vigilancia")
tickers_input = st.text_input(
    "Introduce los tickers de las acciones separados por comas (ejemplo: V, NKE, GOOGL, TGT, MSFT):", 
    "V, NKE, GOOGL, TGT"
)

# Procesar los tickers que el usuario escribe
lista_tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

if st.button("🚀 Ejecutar Investigación del Agente"):
    if not lista_tickers:
        st.warning("Por favor, introduce al menos un ticker válido.")
    else:
        resultados = []
        
        # Barra de carga animada
        with st.spinner("El agente está escaneando los sectores, estados financieros y ganancias..."):
            for t in lista_tickers:
                try:
                    ticker = yf.Ticker(t)
                    info = ticker.info
                    
                    # Extracción de métricas clave (Value Investing)
                    pe = info.get('trailingPE', float('inf'))
                    roe = info.get('returnOnEquity', 0)
                    deuda = info.get('debtToEquity', float('inf'))
                    precio = info.get('currentPrice', 0)
                    nombre = info.get('longName', t)
                    sector = info.get('sector', 'Desconocido')
                    
                    # Lógica y criterios de filtrado del agente
                    razones = []
                    if pe != float('inf') and pe < 22: 
                        razones.append(f"PER atractivo ({pe:.1f})")
                    if roe > 0.15: 
                        razones.append(f"Alta eficiencia (ROE: {roe*100:.1f}%)")
                    if deuda != float('inf') and deuda < 120: 
                        razones.append("Deuda bajo control")
                    
                    # Clasificación
                    es_oportunidad = "SÍ 🔥" if len(razones) >= 2 else "NO ❌"
                    
                    resultados.append({
                        "Ticker": t,
                        "Empresa": nombre,
                        "Sector": sector,
                        "Precio Actual": f"${precio:.2f}" if precio else "N/D",
                        "PER": f"{pe:.1f}" if pe != float('inf') else "N/D",
                        "¿Oportunidad?": es_oportunidad,
                        "Análisis Técnico del Agente": ", ".join(razones) if razones else "No cumple los filtros de calidad mínimos."
                    })
                except Exception as e:
                    # En caso de que falle un ticker, el agente continúa con los demás
                    pass
        
        # 3. Mostrar Resultados en pantalla
        if resultados:
            df = pd.DataFrame(resultados)
            
            # Resaltar las oportunidades detectadas
            st.success("¡Análisis completado con éxito!")
            st.dataframe(df, use_container_width=True)
            
            # Opción para descargar el reporte generado por la IA en Excel/CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Reporte de Oportunidades (CSV)",
                data=csv,
                file_name='reporte_agente_ia.csv',
                mime='text/csv',
            )
        else:
            st.error("No se pudieron obtener datos. Verifica que los tickers sean correctos.")
