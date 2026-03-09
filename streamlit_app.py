import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

# Nombre de tu archivo de logo en GitHub
ARCHIVO_LOGO = "logo.png" 

# Datos de marca
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt"
BEACONS_URL = "https://beacons.ai/inversorenpracticas?utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAQbflFleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA81NjcwNjczNDMzNTI0MjcAAaeZ6qvarSAZN6VM_yEjdjCY_erebS7SWi2aLC8zY-bHvgQkB0WQzNz0Ze2PFw_aem_432qykbykJ3WIHU2HaOHWQ"

# 2. CSS AVANZADO: FONDO ANIMADO, FUENTES TECH Y RELIEVES
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* Fondo animado con movimiento sutil */
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

    /* Título Ultra Grande y Tech */
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

    /* Logo Centrado y Grande con Brillo */
    .centered-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px;
        border-radius: 50%;
        filter: drop-shadow(0 0 25px rgba(0, 255, 204, 0.7));
        margin-bottom: 20px;
    }

    /* Tarjetas estilo Cristal (Glassmorphism) */
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

    /* Disclaimer estilizado */
    .disclaimer {
        background: rgba(255, 0, 85, 0.1);
        border-left: 5px solid #ff0055;
        padding: 20px;
        border-radius: 10px;
        font-size: 13px;
        color: #ffb3c1;
        margin-top: 40px;
    }

    /* Sidebar Neón */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 3px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA: LOGO CENTRADO Y TÍTULO GIGANTE
if os.path.exists(ARCHIVO_LOGO):
    st.markdown(f'<img src="data:image/png;base64,{st.image(ARCHIVO_LOGO)}" class="centered-logo">', unsafe_allow_html=True)
else:
    # Si GitHub no lo carga directo, usamos el link de Drive como respaldo centrado
    st.markdown(f'<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" class="centered-logo"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ccff; font-weight: bold; letter-spacing: 2px;'>OPERATIVA OFICIAL @INVERSORENPRÁCTICAS</p>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (SIDEBAR)
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rendimiento Esperado (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, 25)

# Lógica de la Guía: 130€ (52%) Búnker | 120€ (48%) Cohete [cite: 4, 26, 48]
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

# 5. RESULTADOS EN TARJETAS CRISTALINAS
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">PATRIMONIO FINAL</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p><p style="color:#00ccff;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p><p style="color:#00ccff;">Interés Compuesto</p></div>', unsafe_allow_html=True)

# 6. GRÁFICAS DUALES
st.write("---")
col_pie, col_bar = st.columns([1, 2])

with col_pie:
    # Gráfico Donut
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Tu Ahorro', 'Interés'],
        values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
        hole=.75,
        marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=5))
    )])
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    # Gráfico de Barras Apiladas (Crecimiento Bola de Nieve) [cite: 94-95]
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Inversión Real", marker_color='#00ccff'))
    fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Gratis"], name="Interés Acumulado", marker_color='#00ffcc'))
    fig_bar.update_layout(
        barmode='stack', 
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Años de Evolución",
        yaxis_title="Capital Total (€)",
        font=dict(family="Orbitron", size=12)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás el hito de los 50.000€ en **{m_meta//12} años y {m_meta%12} meses** aportando {aporte_mensual}€/mes[cite: 3].")

# 7. ADVERTENCIA LEGAL PERSONALIZADA
st.markdown(f"""
<div class="disclaimer">
    <strong>⚡ CLÁUSULA DE RESPONSABILIDAD:</strong><br><br>
    Esta herramienta es un simulador matemático basado en proyecciones y rentabilidades históricas [cite: 34, 55-58]. No garantiza resultados futuros. 
    El mercado es volátil y los precios pueden bajar drásticamente. La <strong>"Zona Cohete"</strong> es de alto riesgo [cite: 48-49].<br><br>
    Esto <strong>NO ES CONSEJO FINANCIERO</strong> [cite: 1-2]. El usuario es el único responsable de sus decisiones y debe investigar por su cuenta antes de invertir dinero real[cite: 2].
</div>
""", unsafe_allow_html=True)
