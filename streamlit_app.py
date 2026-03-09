import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ==========================================
# 1. BLOQUEO DE ACCESO
# ==========================================
CLAVE_ACCESO = "RUTA50K2026"

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def check_password():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        .auth-container {
            font-family: 'Orbitron', sans-serif;
            text-align: center;
            padding: 50px;
            background: #0d1117;
            border: 2px solid #00ffcc;
            border-radius: 20px;
            box-shadow: 0 0 20px #00ffcc;
            margin-top: 50px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("🔐 Acceso Privado")
        pwd = st.text_input("Introduce la clave incluida en la guía", type="password")
        if st.button("Desbloquear Ruta 50K"):
            if pwd == CLAVE_ACCESO:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Clave incorrecta.")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.autenticado:
    check_password()
    st.stop()

# ==========================================
# 2. CONFIGURACIÓN Y ESTILO CSS
# ==========================================
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Orbitron', sans-serif;
    }

    [data-testid="stSidebar"] * {
        font-family: 'sans-serif' !important;
    }

    .main {
        background: linear-gradient(-45deg, #0d1117, #161b22, #0d1117, #1a1f26);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main-title {
        font-size: 3.5rem !important;
        font-weight: 900;
        color: #00ffcc;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.8);
        margin-top: -10px;
    }

    .neon-link {
        color: #00ccff;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .neon-link:hover {
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
    }

    .metric-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
    }

    .value-text {
        font-size: 38px;
        font-weight: bold;
        color: #00ffcc;
    }

    .disclaimer {
        background: rgba(255, 0, 85, 0.05);
        border-left: 5px solid #ff0055;
        padding: 15px;
        font-size: 12px;
        color: #ffb3c1;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Logo y Título
st.markdown('<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" style="width:150px; border-radius:50%; filter: drop-shadow(0 0 15px #00ffcc);"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown("""<p style='text-align: center;'>OPERATIVA OFICIAL <a href="https://beacons.ai/inversorenpracticas" target="_blank" class="neon-link">@INVERSORENPRACTICAS</a></p>""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR
# ==========================================
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rentabilidad Esperada")
r_bunker = st.sidebar.slider("Zona Búnker %", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete %", 10, 100, 25)

# Lógica Original
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1

# ==========================================
# 4. CÁLCULOS Y BARRA DE PROGRESO
# ==========================================
data = []
saldo = cap_inicial
for m in range(1, (anios * 12) + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    if m % 12 == 0:
        inv_real = cap_inicial + (aporte_mensual * m)
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": inv_real, "Gratis": saldo - inv_real})

df = pd.DataFrame(data)

# Resultados Top
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e;">PATRIMONIO FINAL</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{df["Gratis"].iloc[-1]:,.2f}€</p></div>', unsafe_allow_html=True)

# Barra Progreso
st.write("### 📈 Progreso hacia la Meta")
prog_val = min(df["Total"].iloc[-1] / 50000, 1.0)
st.progress(prog_val)
st.caption(f"Meta 50.000€: {prog_val*100:.1f}% alcanzado")

# ==========================================
# 5. NUEVO: RADIOGRAFÍA DE LA CARTERA
# ==========================================
st.write("---")
st.header("🧬 Radiografía de tu Inversión Mensual")
col_pie_dist, col_txt_dist = st.columns([1, 1])

# Distribución basada en tu estrategia real
dist_data = {
    "Activo": ["Nasdaq 100 (Búnker)", "Efectivo/Búnker", "MSTR (Cohete)", "ASTS (Cohete)", "PLTR (Cohete)"],
    "Euros": [
        aporte_mensual * 0.40,  # 100€ de 250€ aprox
        aporte_mensual * 0.12,  # 30€ de 250€ aprox
        aporte_mensual * 0.24,  # 60€ de 250€ aprox
        aporte_mensual * 0.12,  # 30€ de 250€ aprox
        aporte_mensual * 0.12   # 30€ de 250€ aprox
    ],
    "Color": ["#0044ff", "#0088ff", "#00ffcc", "#00ccaa", "#009988"]
}

with col_pie_dist:
    fig_dist = go.Figure(data=[go.Pie(labels=dist_data["Activo"], values=dist_data["Euros"], 
                                     marker=dict(colors=dist_data["Color"]), hole=0.5)])
    fig_dist.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig_dist, use_container_width=True)

with col_txt_dist:
    for i in range(len(dist_data["Activo"])):
        st.write(f"**{dist_data['Activo'][i]}:** {dist_data['Euros'][i]:,.2f}€ / mes")

# ==========================================
# 6. GRÁFICAS Y META
# ==========================================
st.write("---")
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Tu Dinero"], name="Tu Inversión", marker_color='#00ccff'))
fig_bar.add_trace(go.Bar(x=df["Año"], y=df["Gratis"], name="Interés Compuesto", marker_color='#00ffcc'))
fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# 7. CALCULADORA INVERSA Y COMPARADOR
# ==========================================
col_inv, col_comp = st.columns(2)

with col_inv:
    st.subheader("🧮 Calculadora Inversa")
    m_obj = st.number_input("Meta Objetivo (€)", value=100000)
    a_obj = st.number_input("Años", value=15)
    n = a_obj * 12
    if r_mensual > 0:
        pmt = (m_obj * r_mensual) / ((1 + r_mensual)**n - 1)
        st.info(f"Necesitas: **{pmt:,.2f}€/mes**")

with col_comp:
    st.subheader("⚔️ Comparador")
    aporte_2 = st.number_input("Aporte Estrategia 2 (€)", value=aporte_mensual+100)
    s2 = cap_inicial
    for _ in range(anios * 12): s2 = (s2 + aporte_2) * (1 + r_mensual)
    st.warning(f"Estrat. 2: **{s2:,.2f}€**")

# ==========================================
# 8. GUARDAR Y LEGAL
# ==========================================
st.write("---")
if 'planes' not in st.session_state: st.session_state.planes = []
nombre_p = st.text_input("Nombre del plan")
if st.button("Guardar Simulación"):
    st.session_state.planes.append({"Nombre": nombre_p, "Total": f"{df['Total'].iloc[-1]:,.0f}€", "Mes": aporte_mensual})
if st.session_state.planes: st.table(st.session_state.planes)

st.markdown('<div class="disclaimer"><strong>⚡ NO ES CONSEJO FINANCIERO.</strong> Simulador basado en proyecciones. El usuario es responsable de sus decisiones.</div>', unsafe_allow_html=True)
