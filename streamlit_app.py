import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

# Datos de marca
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt"
BEACONS_URL = "https://beacons.ai/inversorenpracticas?utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAQbflFleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA81NjcwNjczNDMzNTI0MjcAAaeZ6qvarSAZN6VM_yEjdjCY_erebS7SWi2aLC8zY-bHvgQkB0WQzNz0Ze2PFw_aem_432qykbykJ3WIHU2HaOHWQ"

# 2. CSS AVANZADO: FONDO ANIMADO Y TIPOGRAFÍA TECH
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* Fondo animado */
    .main {
        background: linear-gradient(-45deg, #0d1117, #161b22, #0d1117, #1a1f26);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #e6edf3;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Contenedor de Cabecera Centrada */
    .header-container {
        text-align: center;
        padding-bottom: 20px;
    }

    /* Logo con tamaño equilibrado */
    .centered-logo {
        width: 145px;
        border-radius: 50%;
        filter: drop-shadow(0 0 15px rgba(0, 255, 204, 0.6));
        margin-bottom: 10px;
    }

    /* Título con Orbitron */
    .main-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #00ffcc !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6), 2px 2px 4px #000 !important;
        margin: 0 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase;
    }

    /* Subtítulo y Enlace Beacons */
    .sub-title {
        font-family: 'Orbitron', sans-serif;
        color: #8b949e;
        font-size: 14px;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    .beacons-link {
        color: #00ccff !important;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .beacons-link:hover {
        color: #00ffcc !important;
        text-shadow: 0 0 10px #00ffcc;
    }

    /* Tarjetas estilo Cristal */
    .metric-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
    }

    .value-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 38px;
        font-weight: bold;
        color: #00ffcc;
    }

    .disclaimer {
        background: rgba(255, 0, 85, 0.1);
        border-left: 5px solid #ff0055;
        padding: 15px;
        border-radius: 10px;
        font-size: 12px;
        color: #ffb3c1;
        margin-top: 30px;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 3px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA CENTRADA
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_URL}" class="centered-logo">
        <h1 class="main-title">SIMULADOR RUTA 50K</h1>
        <p class="sub-title">
            OPERATIVA OFICIAL <a href="{BEACONS_URL}" class="beacons-link" target="_blank">@INVERSORENPRÁCTICAS</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. PANEL DE CONTROL (SIDEBAR)
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rendimiento Esperado (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, 25)

# Lógica: 130€ (52%) Búnker | 120€ (48%) Cohete
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

saldo = cap_inicial
invertido = cap_inicial
data = []
for m in range(1, total_meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": invertido, "Gratis": saldo - invertido})

df = pd.DataFrame(data)

# 5. RESULTADOS
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:1px; font-size:14px;">PATRIMONIO FINAL</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p><p style="color:#00ccff; font-size:13px;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:1px; font-size:14px;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p><p style="color:#00ccff; font-size:13px;">Interés Compuesto</p></div>', unsafe_allow_html=True)

# 6. GRÁFICAS DUALES
st.write("---")
col_pie, col_bar = st.columns([1, 2])

with col_pie:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Tu Ahorro', 'Interés'],
        values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
        hole=.75,
        marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=5))
    )])
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Inversión Real", marker_color='#00ccff'))
    fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Gratis"], name="Interés Acumulado", marker_color='#00ffcc'))
    fig_bar.update_layout(
        barmode='stack', 
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Años",
        yaxis_title="Capital (€)",
        font=dict(family="Orbitron", size=11)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Hito
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás los 50.000€ en **{m_meta//12} años y {m_meta%12} meses**.")

# 7. DISCLAIMER LEGAL
st.markdown(f"""
<div class="disclaimer">
    <strong>⚡ CLÁUSULA DE RESPONSABILIDAD:</strong><br><br>
    Estimaciones matemáticas basadas en datos históricos [cite: 34, 55-58]. Sin garantías futuras. Mercado volátil. La Zona Cohete es de alto riesgo [cite: 48-49]. Esto NO constituye consejo financiero [cite: 1-2].
</div>
""", unsafe_allow_html=True)
