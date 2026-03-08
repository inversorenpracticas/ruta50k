import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Ruta 50k - VIP", layout="wide")

# CSS AVANZADO: Efectos de relieve, neón y cristal
st.markdown("""
    <style>
    .main { 
        background-color: #0d1117; 
        background-image: radial-gradient(circle at 50% 50%, #161b22 0%, #0d1117 100%);
        color: #e6edf3; 
    }
    /* Tarjetas con relieve y brillo neón */
    .metric-card { 
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        padding: 25px; 
        border-radius: 20px; 
        text-align: center;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5), -5px -5px 15px rgba(255,255,255,0.02), 0 0 15px rgba(0,255,204,0.1);
        margin-bottom: 20px;
    }
    h1 { 
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc; 
        text-shadow: 2px 2px 4px #000, 0 0 20px rgba(0,255,204,0.6); 
        font-weight: 800;
        letter-spacing: 2px;
    }
    .highlight-val { 
        font-size: 32px; 
        font-weight: bold; 
        color: #00ffcc; 
        text-shadow: 0 0 10px rgba(0,255,204,0.5); 
    }
    /* Estilo para el Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO ---
# Si tienes una URL de tu logo (ej: de tu Instagram o web), ponla aquí:
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" 

col_logo, col_tit = st.columns([1, 4])
with col_logo:
    # Si no tienes URL, esto pondrá un icono temporal
    st.markdown("## 🚀") 
with col_tit:
    st.title("RUTA 50K: CALCULADORA PRO")
    st.markdown("#### Propiedad de @InversorEnPrácticas")

st.write("---")

# --- SIDEBAR (CONTROLADORES) ---
st.sidebar.header("⚙️ PANEL DE CONTROL")
st.sidebar.info("Pulsa la flecha arriba si estás en móvil para ver los ajustes.")

cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0)
aporte_base = st.sidebar.slider("Aporte mensual base (€)", 50, 2000, 250)
aporte_extra = st.sidebar.slider("🔥 Aporte Extra Mensual (€)", 0, 1000, 0)
anios_vista = st.sidebar.slider("Años de inversión", 1, 35, 10)

total_mensual = aporte_base + aporte_extra

# Rentabilidades
st.sidebar.subheader("Rentabilidad Anual")
ret_bunker = st.sidebar.slider("Búnker (%)", 5, 15, 12)
ret_cohete = st.sidebar.slider("Cohete (%)", 10, 80, 25)

# [span_1](start_span)[span_2](start_span)Lógica (52% Búnker, 48% Cohete)[span_1](end_span)[span_2](end_span)
r_ponderado = (ret_bunker * 0.52 + ret_cohete * 0.48) / 100
r_mensual = (1 + r_ponderado)**(1/12) - 1
meses = anios_vista * 12

# Simulación
saldo = cap_inicial
invertido = cap_inicial
data = []
for m in range(1, meses + 1):
    saldo = (saldo + total_mensual) * (1 + r_mensual)
    invertido += total_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Invertido": invertido, "Interés": saldo - invertido})

df = pd.DataFrame(data)

# --- CUERPO PRINCIPAL ---
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="font-size: 18px;">PATRIMONIO FINAL</p>
        <p class="highlight-val">{df['Total'].iloc[-1]:,.2f}€</p>
        <p style="color: #00ccff;">Tu ahorro: {df['Invertido'].iloc[-1]:,.0f}€</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    ganancia = df['Total'].iloc[-1] - df['Invertido'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <p style="font-size: 18px;">DINERO "GRATIS"</p>
        <p class="highlight-val" style="color: #00ffcc;">+{ganancia:,.2f}€</p>
        <p style="color: #00ffcc;">Gracias al Interés Compuesto</p>
    </div>
    """, unsafe_allow_html=True)

# Gráfica de Quesito (Relieve)
fig_pie = go.Figure(data=[go.Pie(
    labels=['Inversión Real', 'Interés Generado'],
    values=[df['Invertido'].iloc[-1], df['Interés'].iloc[-1]],
    hole=.7,
    marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=4))
)])
fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_pie, use_container_width=True)

# Gráfica de Barras Pro
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Invertido"], name="Inversión", marker_color='#00ccff'))
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Interés"], name="Intereses", marker_color='#00ffcc'))
fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + total_mensual) * (1 + r_mensual)
    m_meta += 1
st.info(f"🎯 **Hito Ruta 50k:** Alcanzarás tu objetivo en **{m_meta//12} años y {m_meta%12} meses**.")
