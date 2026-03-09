import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

# Datos de marca
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt"
BEACONS_URL = "https://beacons.ai/inversorenpracticas?utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAQbflFleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA81NjcwNjczNDMzNTI0MjcAAaeZ6qvarSAZN6VM_yEjdjCY_erebS7SWi2aLC8zY-bHvgQkB0WQzNz0Ze2PFw_aem_432qykbykJ3WIHU2HaOHWQ"

# 2. CSS AVANZADO: FONDO ANIMADO, FUENTES TECH Y TARJETAS
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
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: #00ffcc !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6), 2px 2px 4px #000 !important;
        margin: 10px 0 !important;
        letter-spacing: 2px !important;
        text-align: center;
        text-transform: uppercase;
    }

    .sub-title {
        font-family: 'Orbitron', sans-serif;
        color: #8b949e;
        font-size: 14px;
        letter-spacing: 2px;
        text-align: center;
    }

    .beacons-link {
        color: #00ccff !important;
        text-decoration: none;
        font-weight: bold;
    }

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

    .disclaimer-box {
        background: rgba(255, 0, 85, 0.05);
        border: 1px solid #ff0055;
        padding: 25px;
        border-radius: 15px;
        font-size: 14px;
        color: #ffb3c1;
        margin-top: 40px;
        line-height: 1.6;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 3px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA CENTRADA (Arreglo del Logo sin el "0")
col_1, col_2, col_3 = st.columns([1, 1, 1])
with col_2:
    st.image(LOGO_URL, use_container_width=True)

st.markdown(f"""
    <h1 class="main-title">SIMULADOR RUTA 50K</h1>
    <p class="sub-title">
        OPERATIVA OFICIAL <a href="{BEACONS_URL}" class="beacons-link" target="_blank">@INVERSORENPRÁCTICAS</a>
    </p>
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

meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + total_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás los 50.000€ en **{m_meta//12} años y {m_meta%12} meses**.")

# 7. ADVERTENCIA LEGAL EXTENDIDA (Restaurada)
st.markdown(f"""
<div class="disclaimer-box">
    <strong>⚠️ AVISO IMPORTANTE Y DESCARGO DE RESPONSABILIDAD:</strong><br><br>
    Los cálculos mostrados en este simulador son <strong>estimaciones matemáticas basadas en rendimientos históricos</strong> y no garantizan resultados futuros . La rentabilidad real está sujeta a la volatilidad del mercado, la cual es intrínsecamente impredecible.<br><br>
    La <strong>"Zona Cohete"</strong> (Explosive Zone) descrita en la guía representa activos de alto riesgo y debe considerarse como una apuesta especulativa donde es posible la pérdida total o parcial del capital invertido [cite: 48-49]. Nada de lo aquí expuesto constituye una recomendación personalizada de inversión o consejo financiero [cite: 1-2].<br><br>
    Es responsabilidad exclusiva del lector investigar por su cuenta, formarse adecuadamente y actuar bajo su propia responsabilidad. <strong>@InversorEnPrácticas</strong> no se hace responsable de las decisiones financieras tomadas ni de las posibles pérdidas derivadas del uso de esta herramienta o de la guía adjunta.
</div>
""", unsafe_allow_html=True)
