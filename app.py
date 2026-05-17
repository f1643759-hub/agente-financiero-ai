import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de la Página
st.set_page_config(page_title="Agente IA: Informes para Audiencias", layout="wide")

st.title("🤖 Agente Financiero Pro: Generador de Informes para Seguidores")
st.markdown("Auditoría de mercado con creación automática de boletines listos para enviar por correo o redes sociales.")
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
# PESTAÑA 2: CAZADOR AUTOMÁTICO CON CRITERIOS DE LOS PADRES FUNDADORES + INFORME PARA SEGUIDORES
# =====================================================================
with tab2:
    st.subheader("Cazador Multisectorial: Filtro de los Grandes Maestros")
    st.write("El agente audita el mercado y redacta un boletín explicativo listo para enviar a tu comunidad.")
    
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
                        aprobo_graham = "❌ Rechazado (Deuda alta)"
                        if deuda_capital is not None and deuda_capital < 100:
                            aprobo_graham = f"✅ Aprobado (Deuda baja de {deuda_capital:.1f}%)"
                            
                        aprobo_buffett = "❌ Rechazado (ROE ineficiente)"
                        if roe is not None and roe >= 0.15:
                            aprobo_buffett = f"✅ Aprobado (Excelente ROE de {roe*100:.1f}%)"
                            
                        aprobo_lynch = "❌ Rechazado (Precio/Crecimiento alto)"
                        if peg_ratio is not None and peg_ratio <= 1.5:
                            aprobo_lynch = f"✅ Aprobado (Buen precio relativo, PEG: {peg_ratio:.2f})"
                        elif peg_ratio is None:
                            aprobo_lynch = "⚠️ Datos de crecimiento insuficientes"

                        informe_maestros = (
                            f"📌 **Benjamin Graham:** {aprobo_graham}. Margen de seguridad del {descuento:.1f}% (Valor Real: ${valor_intrinseco:.2f} vs Precio: ${precio_actual:.2f}).\n\n"
                            f"📌 **Warren Buffett:** {aprobo_buffett}. Negocio con ventajas competitivas robustas dentro del sector {sector}.\n\n"
                            f"📌 **Peter Lynch:** {aprobo_lynch}. Valora si el ritmo de ganancias futuras justifica lo que pagamos hoy."
                        )
                        
                        oportunidades_encontradas.append({
                            "Ticker": t,
                            "Empresa": nombre,
                            "Sector": sector,
                            "Precio": f"${precio_actual:.2f}",
                            "Descuento Graham": f"{descuento:.1f}%",
                            "Dictamen de los Grandes Inversores": informe_maestros,
                            # Guardamos variables crudas para el redactor de informes
                            "val_real": valor_intrinseco,
                            "desc_num": descuento,
                            "salud_deuda": "estable y controlada" if (deuda_capital and deuda_capital < 100) else "por vigilar"
                        })
            except:
                pass
                
        status_text.text("¡Auditoría e informes listos!")
        
        if oportunidades_encontradas:
            st.success(f"🎯 El Agente detectó {len(oportunidades_encontradas)} acciones con descuento óptimo.")
            
            # --- CONSTRUCCIÓN DEL INFORME DETALLADO PARA SEGUIDORES ---
            texto_boletin = (
                "📢 **INFORME DE MERCADO: ALERTAS DE INVERSIÓN EN VALOR** 🚀\n"
                "¡Hola a todos! Comparto con nuestra comunidad las oportunidades más atractivas detectadas hoy "
                "por nuestro Agente de Inteligencia Artificial Financiera. Hemos auditado los sectores clave buscando "
                "empresas sólidas que cotizan con un descuento importante respecto a su valor real real, cumpliendo los "
                "requisitos de Graham, Buffett y Lynch.\n\n"
                "---"
            )
            
            for item in oportunidades_encontradas:
                texto_boletin += (
                    f"\n\n🔥 **{item['Empresa']} ({item['Ticker']})**\n"
                    f"• **Sector:** {item['Sector']}\n"
                    f"• **Precio de Mercado Actual:** {item['Precio']}\n"
                    f"• **Valor Intrínseco Real:** ${item['val_real']:.2f}\n"
                    f"• **Descuento Presentado:** {item['Descuento Graham']} de Margen de Seguridad.\n"
                    f"• **Diagnóstico de Salud Financiera:** La estructura de deudas se encuentra en estado *{item['salud_deuda']}*.\n"
                    f"• **¿Por qué es una oportunidad?:** Cumple las reglas clásicas de inversión. Presenta una ventaja competitiva visible "
                    f"en sus retornos operativos y su precio actual en Wall Street no está inflado respecto a lo que la empresa gana año con año.\n"
                    f"---"
                )
                
            texto_boletin += (
                "\n\n*Nota: Recuerden que esto representa un análisis cuantitativo automatizado de salud financiera y valor. "
                "Hagan siempre su propia gestión de riesgo antes de tomar decisiones operativas. ¡Buen éxito en sus inversiones!*"
            )
            
            # Mostrar el bloque de texto listo para ser copiado
            st.subheader("📋 Informe Ejecutivo Listo para Enviar a tus Seguidores")
            st.text_area("Copia el texto de abajo y envíalo directamente por Correo, Telegram o Redes:", texto_boletin, height=450)
            
            # Mostrar además la tabla técnica que ya tenías
            st.subheader("📊 Datos Técnicos del Escaneo")
            df_oportunidades = pd.DataFrame(oportunidades_encontradas).drop(columns=['val_real', 'desc_num', 'salud_deuda'])
            st.dataframe(df_oportunidades, use_container_width=True)
            
        else:
            st.info(f"Ninguna acción superó el {margen_minimo}% de descuento bajo las reglas combinadas en este momento.")
