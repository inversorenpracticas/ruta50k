import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ruta 50k - Inversor VIP", layout="wide")

# 2. ESTILO AVANZADO (Bisel y Relieve)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
    .main { background-color: #0d1117; color: #e6edf3; }
    
    /* Efecto Bisel y Relieve en Tarjetas */
    .metric-card {
        background: #161b22;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        /* Sombra doble para crear relieve 3D */
        box-shadow: 10px 10px 20px #06080a, -5px -5px 15px #1c222d;
        border: 1px solid rgba(0, 255, 204, 0.15);
        margin-bottom: 25px;
    }
    
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
        text-align: center;
        margin-top: -20px;
    }

    .value-text {
        font-size: 36px;
        font-weight: bold;
        color: #00ffcc;
        margin: 10px 0;
    }

    /* Estilo del Panel Lateral */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 2px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# 3. CABECERA CON LOGO (Método estable)
# Intentamos cargar el logo desde GitHub. Si no lo has subido aún, pondrá un cohete.
col_l, col_r = st.columns([1, 1])
with col_l:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        # Si falla el archivo local, usamos tu link de Drive como respaldo (entre comillas)
        st.image("https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt", width=120)

st.title("ESTRATEGIA RUTA 50K")
st.markdown("<p style='text-align: center; color: #8b949e;'>Herramienta de @InversorEnPrácticas</p>", unsafe_allow_html=True)

# 4. PANEL DE CONTROL (AJUSTES)
st.sidebar.header("🕹️ AJUSTES")
st.sidebar.warning("Móvil: Pulsa el símbolo '>>' arriba a la izquierda para ver los ajustes.")

cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Aporte Mensual (€)", 50, 1500, 250)
anios = st.sidebar.slider("Años de Inversión", 1, 30, 10)

# [span_1](start_span)[span_2](start_span)[span_3](start_span)Rentabilidades según tu guía[span_1](end_span)[span_2](end_span)[span_3](end_span)
st.sidebar.subheader("Rentabilidad Anual (%)")
r_bunker = st.sidebar.slider("Búnker (Nasdaq)", 5, 20, 12)
r_cohete = st.sidebar.slider("Cohete (Explosiva)", 10, 80, 25)

# Lógica 50k: 52% Búnker | [span_4](start_span)[span_5](start_span)48% Cohete[span_4](end_span)[span_5](end_span)
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

# 5. VISUALIZACIÓN
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="metric-card"><p style="color: #8b949e;">PATRIMONIO</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p></div>', unsafe_allow_html=True)
with c2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color: #8b949e;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p></div>', unsafe_allow_html=True)

# Gráfico de Quesito
fig_pie = go.Figure(data=[go.Pie(
    labels=['Tu Esfuerzo', 'Interés Compuesto'],
    values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
    hole=.7,
    marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=5))
)])
fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_pie, use_container_width=True)

# Barra de Progreso
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Inversión", marker_color='#00ccff'))
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Gratis"], name="Intereses", marker_color='#00ffcc'))
fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)

# [span_6](start_span)[span_7](start_span)[span_8](start_span)Meta 50k[span_6](end_span)[span_7](end_span)[span_8](end_span)
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.info(f"🎯 **Hito Ruta 50k:** Alcanzarás los 50.000€ en **{m_meta//12} años y {m_meta%12} meses**.")
