import streamlit as st
import yfinance as yf
import pandas as pd
import io

# Configuración de interfaz profesional
st.set_page_config(page_title="Agente IA: Confluencia de Valor", layout="wide")

st.title("🤖 Agente IA: Confluencia de Valor & Infraestructura")
st.markdown("### El criterio definitivo de los Grandes Maestros combinado con auditoría de salud financiera.")
st.markdown("---")

# Sección de Monetización en la barra lateral
st.sidebar.header("👑 Acceso Premium Alpha")
st.sidebar.write("Recibe alertas institucionales y análisis de sectores emergentes de alta barrera de entrada.")
st.sidebar.markdown("[👉 Suscribirse al Boletín VIP](https://substack.com)") 

tab1, tab2 = st.tabs(["🔍 Auditoría Manual", "🛰️ Radar de Confluencia Multisectorial"])

# =====================================================================
# PESTAÑA 1: ANÁLISIS MANUAL
# =====================================================================
with tab1:
    st.subheader("Auditoría personalizada de activos")
    tickers_input = st.text_input("Introduce los tickers clave (ej: GOOGL, V, NKE, TGT, CEG):", "GOOGL, V, NKE, TGT")
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
# PESTAÑA 2: RADAR MULTISECTORIAL PROPIO (A mi gusto y manera)
# =====================================================================
with tab2:
    st.subheader("🛰️ Escáner de Activos de Alta Calidad e Infraestructura")
    st.write("Este radar busca en un pool seleccionado que incluye gigantes tecnológicos, consumo defensivo y el sector clave de **Infraestructura Energética e Inteligencia Artificial**.")
    
    # Pool seleccionado a mi gusto: Grandes maestros + Infraestructura Crítica (CEG, OKLO)
    pool_agente = [
        "GOOGL", "MSFT", "AAPL", "META",        # Big Tech e Infraestructura Digital
        "CEG", "OKLO",                           # Energía Nuclear / Infraestructura de Datos
        "V", "MA", "JPM",                        # Monopolios Financieros y de Crédito
        "NKE", "TGT", "PG", "KO",                # Consumo Líder y Cadenas de Reversión (Snowball)
        "JNJ", "UNH"                             # Salud Defensiva
    ]
    
    margen_exigido = st.slider("Margen de Seguridad Mínimo Exigido (%)", 15, 40, 20)

    if st.button("🛰️ Activar Radar de Confluencia", key="btn_auto"):
        oportunidades = []
        progress = st.progress(0)
        status = st.empty()
        
        for idx, t in enumerate(pool_agente):
            status.text(f"Agente evaluando foso competitivo y liquidez de: {t}...")
            progress.progress((idx + 1) / len(pool_agente))
            
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
                
                crecimiento = info.get('earningsGrowth', 0.05) or 0.05
                if crecimiento <= 0: crecimiento = 0.05
                
                if eps and eps > 0:
                    valor_intrinseco = eps * (8.5 + (2 * (crecimiento * 100)))
                    descuento = ((valor_intrinseco - precio) / valor_intrinseco) * 100
                    
                    # FILTRO ESTRICTO DEL AGENTE: Valor con descuento + Salud básica
                    if valor_intrinseco > precio and descuento >= margen_exigido:
                        
                        # Evaluación de Criterios
                        c_graham = "CUMPLE" if (deuda_capital and deuda_capital < 100) else "RIESGO"
                        c_buffett = "CUMPLE" if (roe and roe >= 0.15) else "SIN MOAT"
                        c_lynch = "CUMPLE" if (peg and peg <= 1.5) else "AJUSTADO"
                        
                        informe_ejecutivo = (
                            f"Análisis del Sector: {sector}. "
                            f"La empresa cotiza a ${precio:.2f} con un Valor Intrínseco de ${valor_intrinseco:.2f}, "
                            f"ofreciendo un Margen de Seguridad del {descuento:.1f}%.\n"
                            f"• Filtro Graham (Deuda): {c_graham} (Relación: {deuda_capital if deuda_capital else 'N/D'}%)\n"
                            f"• Filtro Buffett (Eficiencia): {c_buffett} (ROE: {f'{roe*100:.1f}%' if roe else 'N/D'})\n"
                            f"• Filtro Lynch (Crecimiento/Precio): {c_lynch} (PEG: {peg if peg else 'N/D'})"
                        )
                        
                        oportunidades.append({
                            "Ticker": t,
                            "Empresa": nombre,
                            "Sector": sector,
                            "Precio Actual": precio,
                            "Valor Real Estimado": round(valor_intrinseco, 2),
                            "Margen de Seguridad": f"{descuento:.1f}%",
                            "Evaluación del Comité": informe_ejecutivo
                        })
            except:
                pass
                
        status.text("¡Escaneo estratégico finalizado!")
        
        if oportunidades:
            st.success(f"🎯 Se detectaron {len(oportunidades)} activos con confluencia de valor real.")
            df_final = pd.DataFrame(oportunidades)
            
            # --- CREACIÓN EXCEL NATIVO EN MEMORIA ---
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Oportunidades Alfa')
            buffer.seek(0)
            
            # Botón de Descarga Oficial
            st.download_button(
                label="🟢 Descargar Reporte Maestro en Excel (.xlsx)",
                data=buffer,
                file_name='reporte_confluencia_valor.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            
            # Tabla Visual para el administrador de la plataforma
            st.dataframe(df_final, use_container_width=True)
            
            # --- REDACCIÓN DE BOLETÍN DE FÁCIL COMPRENSIÓN ---
            boletin = (
                "📈 **INFORME MAESTRO: RADAR ALFA DE INVERSIÓN** 🚀\n\n"
                "Estimada comunidad: Comparto el análisis sectorial de nuestro Agente de IA. "
                "Buscamos negocios con ventajas competitivas masivas que coticen con un Margen de Seguridad real "
                "frente a la volatilidad del mercado.\n"
                "======================================================\n"
            )
            for op in oportunidades:
                boletin += (
                    f"\n💎 **{op['Empresa']} ({op['Ticker']})**\n"
                    f"• Sector de Operación: {op['Sector']}\n"
                    f"• Precio de Cotización: ${op['Precio Actual']:.2f}\n"
                    f"• Valor Intrínseco Calculado: ${op['Valor Real Estimado']:.2f}\n"
                    f"• Brecha de Descuento: {op['Margen de Seguridad']}\n"
                    f"• Dictamen Interno:\n{op['Evaluación del Comité']}\n"
                    f"------------------------------------------------------\n"
                )
            boletin += "\n*Este informe técnico automatizado evalúa variables financieras e infraestructura, no constituye asesoría financiera directa.*"
            
            st.subheader("📋 Boletín para Seguidores (Listo para copiar/pegar)")
            st.text_area("Texto del Reporte:", boletin, height=350)
            
        else:
            st.info("Ningún activo de la lista cumple con el margen de seguridad exigido en este momento.")
