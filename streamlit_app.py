import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

ARCHIVO_LOGO = "logo.png" 

# 2. CSS AVANZADO (Mantenido y Optimizado)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
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
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 900;
        color: #00ffcc;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.8), 2px 2px 5px #000;
        margin-top: -10px;
        letter-spacing: 3px;
    }
    .centered-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px;
        border-radius: 50%;
        filter: drop-shadow(0 0 25px rgba(0, 255, 204, 0.7));
        margin-bottom: 20px;
    }
    .metric-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 35px;
        text-align: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), inset 2px 2px 5px rgba(255,255,255,0.05);
        margin-bottom: 30px;
    }
    .value-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }
    .disclaimer {
        background: rgba(255, 0, 85, 0.1);
        border-left: 5px solid #ff0055;
        padding: 20px;
        border-radius: 10px;
        font-size: 13px;
        color: #ffb3c1;
        margin-top: 40px;
    }
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 3px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA
if os.path.exists(ARCHIVO_LOGO):
    st.image(ARCHIVO_LOGO, width=180)
else:
    st.markdown(f'<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" class="centered-logo"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ccff; font-weight: bold; letter-spacing: 2px;'>OPERATIVA OFICIAL @INVERSORENPRÁCTICAS</p>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (SIDEBAR)
st.sidebar.header("🕹️ CONTROL DE MISIÓN")

# Nuevo: Presets de riesgo
escenario = st.sidebar.selectbox("Escenario de Mercado", ["Moderado (Personal)", "Optimista", "Conservador"])
if escenario == "Optimista":
    def_bunker, def_cohete = 15, 40
elif escenario == "Conservador":
    def_bunker, def_cohete = 8, 15
else:
    def_bunker, def_cohete = 12, 25

cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rentabilidad Anual (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, def_bunker)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, def_cohete)

# LÓGICA DE CÁLCULO (Intacta)
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

data = []
saldo = cap_inicial
invertido = cap_inicial
for m in range(1, total_meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": round(saldo, 2), "Tu Dinero": invertido, "Gratis": round(saldo - invertido, 2)})

df = pd.DataFrame(data)

# 5. RESULTADOS
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">PATRIMONIO FINAL</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p><p style="color:#00ccff;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p><p style="color:#00ccff;">Interés Compuesto</p></div>', unsafe_allow_html=True)

# 6. DISTRIBUCIÓN DE CARTERA (Nueva Función Visual)
st.subheader("📊 Estrategia de Asignación")
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.info(f"🛡️ **Búnker (52%):** {(aporte_mensual * 0.52):,.1f}€/mes")
with c2:
    st.warning(f"🚀 **Cohete (48%):** {(aporte_mensual * 0.48):,.1f}€/mes")
with c3:
    # Botón de descarga
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Proyección", csv, "ruta_50k.csv", "text/csv")

# 7. GRÁFICAS
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
    fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          xaxis_title="Años", yaxis_title="Euros (€)", font=dict(family="Orbitron"))
    st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás los 50.000€ en **{m_meta//12} años y {m_meta%12} meses**.")

# 8. ADVERTENCIA LEGAL
st.markdown("""<div class="disclaimer"><strong>⚡ CLÁUSULA DE RESPONSABILIDAD:</strong><br>Simulador matemático. No garantiza resultados futuros. La Zona Cohete implica riesgo de pérdida total. NO ES CONSEJO FINANCIERO.</div>""", unsafe_allow_html=True)
