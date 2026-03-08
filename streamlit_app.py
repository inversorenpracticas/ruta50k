import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Simulador Ruta 50k", layout="wide")

# Estética Inversor en Prácticas (Dark Tech & Neón)
st.markdown("""
    <style>
    .main { background-color: #0b1016; color: #e0e0e0; }
    .stSlider > div > div > div > div { background: linear-gradient(90deg, #00ffcc, #00ccff); }
    h1 { color: #00ffcc; text-shadow: 0 0 15px #00ffcc; font-family: 'Courier New'; }
    .metric-card { 
        background: #1a1f26; 
        border: 1px solid #00ffcc; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center;
        box-shadow: 0 0 20px rgba(0,255,204,0.1);
    }
    .highlight-green { color: #00ffcc; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ RUTA 50K: TU MÁQUINA DE INTERÉS COMPUESTO")
st.markdown("### Herramienta oficial de @InversorEnPrácticas")
st.write("---")

# --- SIDEBAR: CONFIGURACIÓN ---
st.sidebar.header("🕹️ CONFIGURACIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_base = st.sidebar.slider("Aporte mensual base (€)", 50, 1000, 250)
aporte_extra = st.sidebar.slider("🚀 Aporte extra (Efecto Café) (€)", 0, 500, 0)
anios_vista = st.sidebar.slider("Años de proyección", 1, 30, 10)

total_mensual = aporte_base + aporte_extra

# Rentabilidades según tu guía (Búnker ~12%, Cohete ~25%+)
ret_bunker = st.sidebar.slider("Zona Segura (Búnker)", 5, 15, 12)
ret_cohete = st.sidebar.slider("Zona Explosiva (Cohete)", 10, 60, 25)

# [span_0](start_span)[span_1](start_span)Distribución: 130€ (52%) Búnker, 120€ (48%) Cohete[span_0](end_span)[span_1](end_span)
p_bunker, p_cohete = 0.52, 0.48
ret_ponderado = (ret_bunker * p_bunker + ret_cohete * p_cohete) / 100
r_mensual = (1 + ret_ponderado)**(1/12) - 1
meses = anios_vista * 12

# Simulación mes a mes
datos = []
saldo = cap_inicial
total_invertido_acum = cap_inicial

for m in range(1, meses + 1):
    saldo = (saldo + total_mensual) * (1 + r_mensual)
    total_invertido_acum += total_mensual
    if m % 12 == 0:
        datos.append({
            "Año": m // 12, 
            "Capital Total": round(saldo, 2),
            "Tu Dinero": round(total_invertido_acum, 2),
            "Intereses": round(saldo - total_invertido_acum, 2)
        })

df = pd.DataFrame(datos)
final_total = df["Capital Total"].iloc[-1]
final_invertido = df["Tu Dinero"].iloc[-1]
final_intereses = df["Intereses"].iloc[-1]

# --- VISUALIZACIÓN ---
col_stats, col_pie = st.columns([1, 1])

with col_stats:
    st.markdown(f"""
    <div class="metric-card">
        <h4>RESULTADO A {anios_vista} AÑOS</h4>
        <h2 style="color: #00ffcc;">{final_total:,.2f}€</h2>
        <p>Tu inversión: <span style="color: #00ccff;">{final_invertido:,.0f}€</span></p>
        <p>Dinero "Gratis": <span class="highlight-green">{final_intereses:,.0f}€</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # [span_2](start_span)[span_3](start_span)Meta 50k[span_2](end_span)[span_3](end_span)
    meta = 50000
    s_meta, m_meta = cap_inicial, 0
    while s_meta < meta and m_meta < 600:
        s_meta = (s_meta + total_mensual) * (1 + r_mensual)
        m_meta += 1
    
    st.write("")
    st.success(f"🎯 **Meta 50k:** Llegarás a los 50.000€ en **{m_meta//12} años y {m_meta%12} meses**.")

with col_pie:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Tu Esfuerzo', 'Intereses'],
        values=[final_invertido, final_intereses],
        hole=.6,
        marker=dict(colors=['#00ccff', '#00ffcc']),
        textinfo='percent'
    )])
    fig_pie.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#e0e0e0"), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

# Gráfica Barras
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Inversión", marker_color='#00ccff'))
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Intereses"], name="Interés Compuesto", marker_color='#00ffcc'))
fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)
