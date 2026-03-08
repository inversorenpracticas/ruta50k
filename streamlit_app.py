import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURACIÓN Y ESTILO (Cero fallos de comillas)
st.set_page_config(page_title="Ruta 50k VIP", layout="wide")

# URL de tu logo
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt"

# CSS para el efecto Bisel, Relieve y Neón
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .main { background-color: #0d1117; color: #e6edf3; }
    
    /* Tarjetas con Relieve y Bisel (Neomorfismo Pro) */
    .metric-card {
        background: #161b22;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 10px 10px 20px #06080a, -5px -5px 15px #1c222d;
        border: 1px solid rgba(0, 255, 204, 0.2);
        margin-bottom: 25px;
    }
    
    .logo-img {
        width: 120px;
        border-radius: 50%;
        filter: drop-shadow(0 0 15px rgba(0, 255, 204, 0.6));
        margin-bottom: 10px;
    }
    
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-shadow: 2px 2px 5px #000, 0 0 20px rgba(0, 255, 204, 0.4);
        text-align: center;
    }

    .highlight-text {
        font-size: 35px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 1px 1px 2px #000;
    }

    /* Sidebar con borde neón */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 2px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f'<div style="text-align: center;"><img src="{LOGO_URL}" class="logo-img"></div>', unsafe_allow_html=True)
st.title("ESTRATEGIA RUTA 50K")
st.markdown("<p style='text-align: center; color: #8b949e; margin-bottom: 30px;'>Herramienta oficial de @InversorEnPrácticas</p>", unsafe_allow_html=True)

# --- PANEL DE CONTROL (SIDEBAR) ---
st.sidebar.header("🕹️ AJUSTA TU RUTA")
st.sidebar.info("Si estás en móvil, pulsa la flecha (>>) arriba a la izquierda.")

cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Tu inversión mensual (€)", 50, 2000, 250)
anios = st.sidebar.slider("Años en el mercado", 1, 30, 10)

# [span_0](start_span)[span_1](start_span)Rentabilidades según tu guía (Búnker 12%, Cohete 25%+) [cite: 19, 31-33]
st.sidebar.subheader("Rentabilidad Anual (%)")
r_bunker = st.sidebar.slider("Zona Segura (Búnker)", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Explosiva (Cohete)", 10, 100, 25)

# Lógica de la Guía: 130€ Búnker (52%) | [cite_start]120€ Cohete (48%)[span_0](end_span)[span_1](end_span)
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

# Simulación
saldo = cap_inicial
invertido = cap_inicial
data = []
for m in range(1, total_meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": invertido, "Gratis": saldo - invertido})

df = pd.DataFrame(data)

# --- RESULTADOS VISUALES ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #8b949e; letter-spacing: 1px;">PATRIMONIO FINAL</p>
        <p class="highlight-text">{df['Total'].iloc[-1]:,.2f}€</p>
        <p style="color: #00ccff;">Invertido: {df['Tu Dinero'].iloc[-1]:,.0f}€</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #8b949e; letter-spacing: 1px;">DINERO "GRATIS"</p>
        <p class="highlight-text">+{regalo:,.2f}€</p>
        <p style="color: #00ccff;">Interés Compuesto</p>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de Quesito
fig_pie = go.Figure(data=[go.Pie(
    labels=['Inversión Real', 'Interés'],
    values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
    hole=.7,
    marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=4))
)])
fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico de Progreso
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Inversión", marker_color='#00ccff'))
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Gratis"], name="Intereses", marker_color='#00ffcc'))
fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.info(f"🎯 **Meta 50k:** Con estos ajustes, alcanzarás tu objetivo en **{m_meta//12} años y {m_meta%12} meses**.")
