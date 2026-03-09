import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ==========================================
# 1. CONFIGURACIÓN Y BLOQUEO DE ACCESO
# ==========================================
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

CLAVE_ACCESO = "RUTA50K2026"

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        .auth-container {
            text-align: center;
            padding: 100px;
            font-family: 'Orbitron', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col_auth, _ = st.columns([1, 1])
    with col_auth:
        st.markdown('<h1 style="font-family:Orbitron; color:#00ffcc;">🔐 ACCESO PRIVADO</h1>', unsafe_allow_html=True)
        password = st.text_input("Introduce la clave incluida en la guía", type="password")
        if st.button("Desbloquear Terminal"):
            if password == CLAVE_ACCESO:
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Revisa la guía.")
    st.stop()

# ==========================================
# 2. ESTILO CSS AVANZADO (ORBITRON & NEON)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* Aplicar Orbitron a todo excepto Sidebar */
    html, body, [data-testid="stVerticalBlock"] {
        font-family: 'Orbitron', sans-serif !important;
    }

    [data-testid="stSidebar"] * {
        font-family: 'sans-serif' !important;
    }

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
        font-size: 3.5rem !important;
        font-weight: 900;
        color: #00ffcc;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 204, 0.8), 2px 2px 5px #000;
        margin-top: -10px;
        letter-spacing: 3px;
    }

    /* Enlace Neón */
    .neon-wrapper {
        text-align: center;
        margin-bottom: 20px;
    }
    .neon-link {
        color: #00ccff;
        text-decoration: none;
        font-weight: bold;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }
    .neon-link:hover {
        color: #00ffcc;
        text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #00ffcc;
    }

    .centered-logo {
        display: block;
        margin: auto;
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
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 30px;
    }

    .value-text {
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

# ==========================================
# 3. CABECERA
# ==========================================
ARCHIVO_LOGO = "logo.png"
if os.path.exists(ARCHIVO_LOGO):
    st.markdown(f'<img src="data:image/png;base64,{st.image(ARCHIVO_LOGO)}" class="centered-logo">', unsafe_allow_html=True)
else:
    st.markdown(f'<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" class="centered-logo"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown("""
    <div class="neon-wrapper">
        <span style="color:white">OPERATIVA OFICIAL </span>
        <a href="https://beacons.ai/inversorenpracticas" target="_blank" class="neon-link">@INVERSORENPRACTICAS</a>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. PANEL DE CONTROL (SIDEBAR)
# ==========================================
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rendimiento Esperado (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, 25)

# Lógica original intacta
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

# ==========================================
# 5. SIMULACIÓN Y CÁLCULOS
# ==========================================
data = []
saldo = cap_inicial
invertido = cap_inicial
for m in range(1, total_meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": invertido, "Gratis": saldo - invertido})

df = pd.DataFrame(data)
cap_final = df["Total"].iloc[-1]

# ==========================================
# 6. RESULTADOS Y BARRA DE PROGRESO
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">PATRIMONIO FINAL</p><p class="value-text">{cap_final:,.2f}€</p><p style="color:#00ccff;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = cap_final - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p><p style="color:#00ccff;">Interés Compuesto</p></div>', unsafe_allow_html=True)

# BARRA DE PROGRESO HACIA 50.000€
st.write("### 📈 PROGRESO HACIA EL OBJETIVO")
meta_50k = 50000
progreso = min(cap_final / meta_50k, 1.0)
st.progress(progreso)
st.markdown(f"<p style='text-align:center;'>Progreso hacia 50.000€ → **{progreso*100:.1f}%**</p>", unsafe_allow_html=True)

# ==========================================
# 7. GRÁFICAS DUALES Y DESGLOSE ACTIVOS
# ==========================================
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
    fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Años de Evolución", yaxis_title="Capital Total (€)", font=dict(family="Orbitron", size=12))
    st.plotly_chart(fig_bar, use_container_width=True)

# NUEVA GRÁFICA: DESGLOSE DE ACTIVOS (Basado en la Guía)
st.write("### 💎 DISTRIBUCIÓN MENSUAL POR ACTIVO")
# Cálculo de distribución basado en tus pesos conocidos
dist_data = {
    "Activo": ["Nasdaq 100", "Búnker/Groupama", "Microstrategy", "AST Spacemobile", "Palantir"],
    "Mensual (€)": [100, 30, 60, 30, 30],
    "Zona": ["Segura", "Segura", "Explosiva", "Explosiva", "Explosiva"]
}
df_dist = pd.DataFrame(dist_data)
fig_dist = go.Figure(data=[go.Bar(
    x=df_dist["Activo"], 
    y=df_dist["Mensual (€)"],
    marker_color=['#00ccff', '#00ccff', '#ff0055', '#ff0055', '#ff0055']
)])
fig_dist.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Orbitron"))
st.plotly_chart(fig_dist, use_container_width=True)

# Meta 50k - Lógica original
s_meta, m_meta = cap_inicial, 0
while s_meta < meta_50k and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás el hito de los 50.000€ en **{m_meta//12} años y {m_meta%12} meses** aportando {aporte_mensual}€/mes.")

# ==========================================
# 8. CALCULADORA INVERSA
# ==========================================
st.write("---")
st.header("🧮 CALCULADORA PARA ALCANZAR UNA META")
col_inv1, col_inv2 = st.columns(2)
with col_inv1:
    obj_final = st.number_input("Objetivo Final (€)", value=50000, step=1000)
with col_inv2:
    anios_obj = st.slider("Años para lograrlo", 1, 35, 10)

meses_obj = anios_obj * 12
# Fórmula del valor futuro de una anualidad: Pago = (FV * r) / ((1 + r)^n - 1)
if r_mensual > 0:
    pago_necesario = (obj_final * r_mensual) / ((1 + r_mensual)**meses_obj - 1)
    st.success(f"Para alcanzar **{obj_final:,.0f}€** en {anios_obj} años, necesitas invertir **{pago_necesario:,.2f}€/mes** (con el {r_ponderada*100:.1f}% anual).")

# ==========================================
# 9. COMPARADOR DE ESTRATEGIAS
# ==========================================
st.write("---")
st.header("⚖️ COMPARADOR DE ESTRATEGIAS")
aporte_est2 = st.number_input("Aporte Mensual Estrategia 2 (€)", value=float(aporte_mensual + 100))

# Simulación Estrategia 2
saldo2 = cap_inicial
for m in range(1, total_meses + 1):
    saldo2 = (saldo2 + aporte_est2) * (1 + r_mensual)

col_c1, col_c2 = st.columns(2)
col_c1.metric("Estrategia 1 (Actual)", f"{cap_final:,.2f}€")
col_c2.metric("Estrategia 2", f"{saldo2:,.2f}€", delta=f"{saldo2-cap_final:,.2f}€")

# ==========================================
# 10. GUARDAR SIMULACIONES
# ==========================================
st.write("---")
st.header("💾 MIS PLANES GUARDADOS")

if 'planes' not in st.session_state:
    st.session_state['planes'] = []

with st.expander("Guardar Plan Actual"):
    nombre_plan = st.text_input("Nombre del plan (ej: Plan Jubilación)")
    if st.button("Guardar Simulación"):
        nuevo_plan = {
            "Nombre": nombre_plan,
            "Cap. Inicial": cap_inicial,
            "Aporte": aporte_mensual,
            "Años": anios,
            "Resultado": f"{cap_final:,.2f}€"
        }
        st.session_state['planes'].append(nuevo_plan)
        st.toast("Simulación guardada con éxito")

if st.session_state['planes']:
    st.table(pd.DataFrame(st.session_state['planes']))

# ==========================================
# 11. ADVERTENCIA LEGAL
# ==========================================
st.markdown(f"""
<div class="disclaimer">
  <strong>⚡ CLÁUSULA DE RESPONSABILIDAD:</strong><br><br>
  Esta herramienta es un simulador matemático basado en proyecciones y rentabilidades históricas. No garantiza resultados futuros.<br>
  El mercado es volátil y los precios pueden bajar drásticamente. La <strong>"Zona Cohete"</strong> es de alto riesgo.<br><br>
  Esto <strong>NO ES CONSEJO FINANCIERO</strong>. El usuario es el único responsable de sus decisiones y debe investigar por su cuenta antes de invertir dinero real.
</div>
""", unsafe_allow_html=True)
