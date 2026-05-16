import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de la Página
st.set_page_config(page_title="Agente IA: Valor Intrínseco", layout="wide")

st.title("🤖 Agente Financiero Pro: Valor Intrínseco y Descuento")
st.markdown("Analizador avanzado de acciones basado en los principios de Benjamin Graham y Warren Buffett.")
st.markdown("---")

# Barra lateral para conversión de clientes / monetización
st.sidebar.header("👑 Membresía VIP")
st.sidebar.write("Obtén reportes en PDF creados por el agente con proyecciones de crecimiento detalladas.")
st.sidebar.markdown("[👉 Unirse al Club de Inversores](https://substack.com)") 

# 2. Entrada de Datos del Usuario
st.subheader("🔍 Portafolio bajo Análisis")
tickers_input = st.text_input(
    "Escribe los tickers separados por comas:", 
    "V, NKE, GOOGL, TGT"
)

lista_tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

if st.button("🚀 Iniciar Investigación de Valor"):
    if not lista_tickers:
        st.warning("Por favor, introduce al menos un ticker válido.")
    else:
        resultados = []
        
        with st.spinner("El agente está extrayendo estados financieros y calculando valores intrínsecos..."):
            for t in lista_tickers:
                try:
                    ticker = yf.Ticker(t)
                    info = ticker.info
                    
                    # Variables necesarias para el cálculo
                    precio_actual = info.get('currentPrice', 0)
                    eps = info.get('trailingEps', 0)
                    nombre = info.get('longName', t)
                    sector = info.get('sector', 'Desconocido')
                    
                    # Intentar obtener la tasa de crecimiento estimada (o usar un 5% conservador por defecto)
                    crecimiento = info.get('earningsGrowth', 0.05)
                    if crecimiento is None or crecimiento <= 0:
                        crecimiento = 0.05
                    tasa_crecimiento_porcentaje = crecimiento * 100
                    
                    # --- CÁLCULO DE VALOR INTRÍNSECO (Fórmula de Graham simplificada) ---
                    # Valor = EPS * (8.5 + 2 * Tasa de crecimiento)
                    if eps and eps > 0:
                        valor_intrinseco = eps * (8.5 + (2 * tasa_crecimiento_porcentaje))
                        
                        # Calcular el Descuento / Margen de Seguridad
                        if valor_intrinseco > precio_actual:
                            descuento = ((valor_intrinseco - precio_actual) / valor_intrinseco) * 100
                            oportunidad = f"SÍ ({descuento:.1f}% Desc.) 🔥"
                            veredicto = f"Empresa infravalorada. Cotiza por debajo de su valor real. Sector: {sector}."
                        else:
                            descuento = 0
                            oportunidad = "NO ❌"
                            veredicto = "Sobrevalorada o a precio justo de mercado actualmente."
                    else:
                        valor_intrinseco = 0
                        descuento = 0
                        oportunidad = "N/D"
                        veredicto = "No aplica (Ganancias negativas o EPS no disponible)."

                    resultados.append({
                        "Ticker": t,
                        "Empresa": nombre,
                        "Precio Actual": f"${precio_actual:.2f}",
                        "Valor Estimado (IA)": f"${valor_intrinseco:.2f}" if valor_intrinseco > 0 else "N/D",
                        "¿Oportunidad?": oportunidad,
                        "Informe del Agente": veredicto
                    })
                except Exception as e:
                    pass
        
        # 3. Presentación de Resultados en Tabla
        if resultados:
            df = pd.DataFrame(resultados)
            st.success("¡Investigación finalizada!")
            st.dataframe(df, use_container_width=True)
            
            # Botón de Descarga
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Informe Detallado (CSV)",
                data=csv,
                file_name='informe_valor_intrinseco.csv',
                mime='text/csv',
            )
        else:
            st.error("Hubo un problema al procesar las acciones. Revisa los códigos ingresados.")
