import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN Y NOMBRE DEL LOGO
st.set_page_config(page_title="Ruta 50k - Simulador Oficial", layout="wide")

# CAMBIA ESTO por el nombre exacto de tu archivo en GitHub
ARCHIVO_LOGO = "logo.png" 

# 2. ESTILO AVANZADO (Bisel, Neón y Disclaimer)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .main { background-color: #0d1117; color: #e6edf3; }
    
    .metric-card {
        background: #161b22;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 10px 10px 20px #06080a, -5px -5px 15px #1c222d;
        border: 1px solid rgba(0, 255, 204, 0.2);
        margin-bottom: 25px;
    }
    
    .disclaimer-box {
        background: rgba(255, 0, 85, 0.05);
        border: 1px solid #ff0055;
        padding: 15px;
        border-radius: 10px;
        font-size: 13px;
        color: #ffb3c1;
        margin-top: 30px;
    }

    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
        text-align: center;
    }

    .highlight-val {
        font-size: 36px;
        font-weight: bold;
        color: #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA Y LOGO
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    if os.path.exists(ARCHIVO_LOGO):
        st.image(ARCHIVO_LOGO, width=150)
    else:
        st.warning(f"⚠️ Sube tu logo a GitHub con el nombre '{ARCHIVO_LOGO}'")

st.title("SIMULADOR RUTA 50K")
st.markdown("<p style='text-align: center; color: #8b949e;'>Por @InversorEnPrácticas</p>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (SIDEBAR)
st.sidebar.header("🕹️ AJUSTA TU ESTRATEGIA")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Tu inversión mensual (€)", 50, 1500, 250)
anios = st.sidebar.slider("Años proyectados", 1, 30, 10)

st.sidebar.subheader("Rentabilidad Anual Proyectada")
r_bunker = st.sidebar.slider("Zona Búnker (Nasdaq/Segura)", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete (Explosiva/Apuesta)", 10, 100, 25)

# Lógica: 130€ Búnker (52%) | 120€ Cohete (48%)
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

# Simulación
data = []
saldo = cap_inicial
invertido = cap_inicial
for m in range(1, total_meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": invertido, "Gratis": saldo - invertido})

df = pd.DataFrame(data)

# 5. VISUALIZACIÓN DE RESULTADOS
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p>PATRIMONIO FINAL</p><p class="highlight-val">{df["Total"].iloc[-1]:,.2f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p>DINERO "GRATIS" (INTERÉS)</p><p class="highlight-val">+{regalo:,.2f}€</p></div>', unsafe_allow_html=True)

# Gráfica de Quesito
fig_pie = go.Figure(data=[go.Pie(
    labels=['Inversión Real', 'Interés Generado'],
    values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
    hole=.7,
    marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=5))
)])
fig_pie.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#8b949e"), height=300)
st.plotly_chart(fig_pie, use_container_width=True)

# Hito 50k
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.info(f"🎯 **Meta 50k:** Según estos ajustes, tardarías **{m_meta//12} años y {m_meta%12} meses**.")

# 6. ADVERTENCIA LEGAL Y DISCLAIMER
st.markdown(f"""
<div class="disclaimer-box">
    <strong>⚠️ AVISO IMPORTANTE Y DESCARGO DE RESPONSABILIDAD:</strong><br><br>
    Los cálculos mostrados son <strong>estimaciones matemáticas basadas en datos históricos</strong> y no garantizan resultados futuros[cite: 1, 2]. 
    La rentabilidad real dependerá de la volatilidad del mercado, la cual es impredecible.<br><br>
    La <strong>"Zona Explosiva" (Cohete)</strong> mencionada en esta guía implica un alto riesgo y debe considerarse una apuesta especulativa donde es posible perder gran parte del capital[cite: 49, 53]. 
    Nada de lo aquí expuesto constituye una recomendación personalizada de inversión[cite: 1].<br><br>
    Es responsabilidad exclusiva del usuario informarse, formarse y actuar bajo su propio riesgo[cite: 2]. 
    @InversorEnPrácticas no se hace responsable de posibles pérdidas financieras derivados del uso de esta herramienta.
</div>
""", unsafe_allow_html=True)
