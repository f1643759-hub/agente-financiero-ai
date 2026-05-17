import streamlit as st
import yfinance as yf
import pandas as pd
import io

# 1. Configuración de la Página
st.set_page_config(page_title="Agente IA: Informes en Excel", layout="wide")

st.title("🤖 Agente Financiero Pro: Generador de Informes en Excel")
st.markdown("Auditoría de mercado con creación automática de boletines y reportes descargables en formato Excel (.xlsx).")
st.markdown("---")

# Barra lateral para monetización
st.sidebar.header("👑 Membresía VIP")
st.sidebar.write("Accede a las alertas en tiempo real vía Telegram y reportes institucionales detallados.")
st.sidebar.markdown("[👉 Unirse al Club de Inversores](https://substack.com)") 

# Pestañas de navegación
tab1, tab2 = st.tabs(["🔍 Analizar Mis Acciones", "🎯 Cazador Automático Multisectorial"])

# =====================================================================
# PESTAÑA 1: ANALIZAR ACCIONES MANUALES (Función original intacta)
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
# PESTAÑA 2: CAZADOR AUTOMÁTICO CON CRITERIOS DE MAESTROS GENERADOR DE EXCEL
# =====================================================================
with tab2:
    st.subheader("Cazador Multisectorial: Filtro de los Grandes Maestros")
    st.write("El agente audita el mercado y empaqueta un informe descargable directamente en formato nativo de Excel.")
    
    pool_mercado = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
        "JPM", "BAC", "V", "MA",                 
        "NKE", "TGT", "HD", "WMT", "KO",         
        "JNJ", "PFE", "UNH", "MRK",              
        "CAT", "GE", "MMM",                      
        "XOM", "CVX"                             
    ]
    
    margen_minimo = st.slider("Margen de descuento mínimo requerido (%)", 10, 50, 15, key="slider_auto")

    if st.button("🛰️ Escanear Todo el Mercado", key="btn_auto"):
        oportunidades_encontradas = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for index, t in enumerate(pool_mercado):
            status_text.text(f"Evaluando {t} bajo las tesis de Graham, Buffett y Lynch...")
            progress_bar.progress((index + 1) / len(pool_mercado))
            
            try:
                ticker = yf.Ticker(t)
                info = ticker.info
                
                precio_actual = info.get('currentPrice', 0)
                eps = info.get('trailingEps', 0)
                sector = info.get('sector', 'Otros')
                nombre = info.get('longName', t)
                
                deuda_capital = info.get('debtToEquity', None)
                roe = info.get('returnOnEquity', None)        
                peg_ratio = info.get('pegRatio', None)        
                
                crecimiento = info.get('earningsGrowth', 0.05) or 0.05
                if crecimiento <= 0: crecimiento = 0.05
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento * 100)))
                    descuento = ((valor_intrinseco - precio_actual) / valor_intrinseco) * 100
                    
                    if valor_intrinseco > precio_actual and descuento >= margen_minimo:
                        
                        # Auditoría de los maestros
                        aprobo_graham = "Rechazado (Deuda alta)"
                        if deuda_capital is not None and deuda_capital < 100:
                            aprobo_graham = f"Aprobado (Deuda baja de {deuda_capital:.1f}%)"
                            
                        aprobo_buffett = "Rechazado (ROE ineficiente)"
                        if roe is not None and roe >= 0.15:
                            aprobo_buffett = f"Aprobado (Excelente ROE de {roe*100:.1f}%)"
                            
                        aprobo_lynch = "Rechazado (Precio/Crecimiento alto)"
                        if peg_ratio is not None and peg_ratio <= 1.5:
                            aprobo_lynch = f"Aprobado (Buen precio, PEG: {peg_ratio:.2f})"
                        elif peg_ratio is None:
                            aprobo_lynch = "Datos de crecimiento insuficientes"

                        informe_maestros = (
                            f"Graham: {aprobo_graham}. Margen de seguridad del {descuento:.1f}% (Valor Real: ${valor_intrinseco:.2f} vs Precio: ${precio_actual:.2f}). | "
                            f"Buffett: {aprobo_buffett}. Ventajas competitivas en sector {sector}. | "
                            f"Lynch: {aprobo_lynch}."
                        )
                        
                        oportunidades_encontradas.append({
                            "Ticker": t,
                            "Empresa": nombre,
                            "Sector": sector,
                            "Precio Actual": precio_actual,
                            "Valor Real Estimado": round(valor_intrinseco, 2),
                            "Descuento Presentado": f"{descuento:.1f}%",
                            "Estructura Deuda": "Estable" if (deuda_capital and deuda_capital < 100) else "Vigilar",
                            "Dictamen de los Grandes Inversores": informe_maestros
                        })
            except:
                pass
                
        status_text.text("¡Auditoría e informes listos!")
        
        if oportunidades_encontradas:
            st.success(f"🎯 El Agente detectó {len(oportunidades_encontradas)} acciones con descuento óptimo.")
            
            # Formatear el DataFrame para visualización e informe en Excel
            df_oportunidades = pd.DataFrame(oportunidades_encontradas)
            
            # --- CONVERSIÓN EXCLUSIVA A ARCHIVO EXCEL DE MEMORIA INTERNA ---
            buffer_excel = io.BytesIO()
            with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
                # Guardamos los datos limpios en una hoja llamada 'Alertas IA'
                df_oportunidades.to_excel(writer, index=False, sheet_name='Alertas IA')
            
            buffer_excel.seek(0)
            
            # --- BOTÓN DE DESCARGA EN EXCEL DIRECTO ---
            st.subheader("📥 Descarga el reporte para tus Seguidores")
            st.download_button(
                label="🟢 Descargar Informe Oficial en Excel (.xlsx)",
                data=buffer_excel,
                file_name='informe_maestros_inversion_ia.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
            # Mostrar la vista previa en la aplicación web para el administrador
            st.subheader("📊 Vista Previa de los Datos que incluye el Excel")
            st.dataframe(df_oportunidades, use_container_width=True)
            
            # Conservamos también la versión de boletín escrito por si deseas copiar texto rápido
            texto_boletin = "📢 **INFORME DE MERCADO: ALERTAS DE INVERSIÓN EN VALOR**\n\n"
            for item in oportunidades_encontradas:
                texto_boletin += f"🔥 **{item['Empresa']} ({item['Ticker']})**\n• Sector: {item['Sector']}\n• Precio Actual: ${item['Precio Actual']}\n• Valor Real: ${item['Valor Real Estimado']}\n• Descuento: {item['Descuento Presentado']}\n---\n"
            st.subheader("📋 Versión resumida para texto rápido:")
            st.text_area("Copia rápida:", texto_boletin, height=200)
            
        else:
            st.info(f"Ninguna acción superó el {margen_minimo}% de descuento bajo las reglas combinadas en este momento.")
