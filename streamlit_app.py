import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ==========================================
# 1. BLOQUEO DE ACCESO (ACCESO PRIVADO)
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
            background: rgba(13, 17, 23, 0.9);
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
        if st.button("Desbloquear App 🚀"):
            if pwd == CLAVE_ACCESO:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Revisa la guía.")
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

    /* Fuente Global Orbitron (excepto Sidebar) */
    html, body, [class*="st-"] {
        font-family: 'Orbitron', sans-serif;
    }

    /* Resetear Sidebar a Sans-Serif para legibilidad */
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

    /* Enlace Clicable con efecto Neón */
    .neon-link {
        color: #00ccff;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .neon-link:hover {
        color: #00ffcc;
        text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #00ffcc;
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
</style>
""", unsafe_allow_html=True)

# Cabecera
ARCHIVO_LOGO = "logo.png" 
if os.path.exists(ARCHIVO_LOGO):
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{st.image(ARCHIVO_LOGO)}" class="centered-logo"></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" class="centered-logo"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; letter-spacing: 2px;'>
    OPERATIVA OFICIAL 
    <a href="https://beacons.ai/inversorenpracticas" target="_blank" class="neon-link">@INVERSORENPRACTICAS</a>
</p>
""", unsafe_allow_html=True)

# ==========================================
# 3. PANEL DE CONTROL (SIDEBAR)
# ==========================================
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rendimiento Esperado (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, 25)

# Lógica de Rentabilidad Ponderada (ORIGINAL)
r_ponderada = (r_bunker * 0.52 + r_cohete * 0.48) / 100
r_mensual = (1 + r_ponderada)**(1/12) - 1
total_meses = anios * 12

# ==========================================
# 4. SIMULACIÓN (CÁLCULOS ORIGINALES)
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

# ==========================================
# 5. RESULTADOS Y BARRA DE PROGRESO
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">PATRIMONIO FINAL</p><p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p><p style="color:#00ccff;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p></div>', unsafe_allow_html=True)
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(f'<div class="metric-card"><p style="color:#8b949e; letter-spacing:2px;">DINERO "GRATIS"</p><p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p><p style="color:#00ccff;">Interés Compuesto</p></div>', unsafe_allow_html=True)

# BARRA DE PROGRESO HACIA 50.000€
st.write("### 📈 Progreso hacia la Meta")
meta_50k = 50000
capital_final = df["Total"].iloc[-1]
porcentaje = min(capital_final / meta_50k, 1.0)
st.progress(porcentaje)
st.markdown(f"<p style='text-align:right; color:#00ffcc;'>Progreso hacia 50.000€ → {porcentaje*100:.1f}%</p>", unsafe_allow_html=True)

# ==========================================
# 6. RADIOGRAFÍA DE ACTIVOS (NUEVA FUNCIÓN)
# ==========================================
st.write("---")
st.header("🧬 Desglose de Activos (Estrategia @InversorEnPracticas)")
col_pie_dist, col_txt_dist = st.columns([1, 1])

# Cálculo de pesos basados en tu estrategia (130 bunker / 120 cohete de cada 250)
# Bunker: Nasdaq (100/250=40%), Bunker/Efectivo (30/250=12%)
# Cohete: MSTR (60/250=24%), ASTS (30/250=12%), PLTR (30/250=12%)
dist_activos = {
    "Activo": ["Nasdaq 100", "Búnker/Efectivo", "Microstrategy (MSTR)", "AST SpaceMobile (ASTS)", "Palantir (PLTR)"],
    "Mensual (€)": [
        aporte_mensual * 0.40,
        aporte_mensual * 0.12,
        aporte_mensual * 0.24,
        aporte_mensual * 0.12,
        aporte_mensual * 0.12
    ],
    "Categoría": ["Búnker", "Búnker", "Explosiva", "Explosiva", "Explosiva"],
    "Color": ["#0044ff", "#0088ff", "#00ffcc", "#00ccaa", "#009988"]
}

with col_pie_dist:
    fig_dist = go.Figure(data=[go.Pie(
        labels=dist_activos["Activo"], 
        values=dist_activos["Mensual (€)"],
        marker=dict(colors=dist_activos["Color"]),
        hole=0.5,
        textinfo='label+percent'
    )])
    fig_dist.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig_dist, use_container_width=True)

with col_txt_dist:
    st.write(f"**Distribución de tus {aporte_mensual}€ mensuales:**")
    for i in range(len(dist_activos["Activo"])):
        st.write(f"• **{dist_activos['Activo'][i]}** ({dist_activos['Categoría'][i]}): **{dist_activos['Mensual (€)'][i]:,.2f}€**")
    st.info("💡 Este desglose respeta el equilibrio 52% Búnker / 48% Explosiva como explicamos en la guía.")

# ==========================================
# 7. GRÁFICAS ORIGINALES
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
    fig_bar.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Años de Evolución", yaxis_title="Capital Total (€)")
    st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k (Texto original)
s_meta, m_meta = cap_inicial, 0
while s_meta < meta_50k and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás el hito de los 50.000€ en **{m_meta//12} años y {m_meta%12} meses** aportando {aporte_mensual}€/mes.")

st.write("---")

# ==========================================
# 8. CALCULADORA INVERSA
# ==========================================
st.header("🧮 Calculadora para alcanzar una meta")
col_inv1, col_inv2 = st.columns(2)
with col_inv1:
    obj_meta = st.number_input("Objetivo Final (€)", value=100000, step=5000)
with col_inv2:
    obj_anios = st.number_input("Años disponibles", value=15, step=1)

n_meses = obj_anios * 12
if r_mensual > 0:
    cuota_necesaria = (obj_meta * r_mensual) / ((1 + r_mensual)**n_meses - 1)
    st.success(f"Para alcanzar **{obj_meta:,.2f}€** en {obj_anios} años, necesitas invertir **{cuota_necesaria:,.2f}€ al mes** (con la rentabilidad actual).")
else:
    st.warning("La rentabilidad debe ser superior al 0% para calcular la cuota.")

st.write("---")

# ==========================================
# 9. COMPARADOR DE ESTRATEGIAS
# ==========================================
st.header("⚔️ Comparador de Estrategias")
aporte_est2 = st.number_input("Aporte Mensual Estrategia 2 (€)", value=aporte_mensual + 100, step=50)

# Simulación Estrategia 2
saldo2 = cap_inicial
data2 = []
for m in range(1, total_meses + 1):
    saldo2 = (saldo2 + aporte_est2) * (1 + r_mensual)
    if m % 12 == 0:
        data2.append(saldo2)

fig_comp = go.Figure()
fig_comp.add_trace(go.Scatter(x=df["Año"], y=df["Total"], name=f"Estrat. 1 ({aporte_mensual}€)", line=dict(color='#00ccff', width=3)))
fig_comp.add_trace(go.Scatter(x=df["Año"], y=data2, name=f"Estrat. 2 ({aporte_est2}€)", line=dict(color='#ff0055', width=3, dash='dot')))
fig_comp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title="Estrat. 1 vs Estrat. 2")
st.plotly_chart(fig_comp, use_container_width=True)

st.write("---")

# ==========================================
# 10. GUARDAR SIMULACIONES
# ==========================================
st.header("💾 Guardar simulaciones")
if 'planes' not in st.session_state:
    st.session_state.planes = []

col_save1, col_save2 = st.columns([3, 1])
with col_save1:
    nombre_plan = st.text_input("Nombre de tu plan (ej: Plan Jubilación)", placeholder="Mi plan Pro...")
with col_save2:
    if st.button("Guardar simulación"):
        nuevo_plan = {
            "Nombre": nombre_plan if nombre_plan else "Sin nombre",
            "Cap. Inicial": cap_inicial,
            "Aporte": aporte_mensual,
            "Años": anios,
            "Total": f"{df['Total'].iloc[-1]:,.2f}€"
        }
        st.session_state.planes.append(nuevo_plan)
        st.toast("Simulación guardada con éxito!")

if st.session_state.planes:
    st.table(pd.DataFrame(st.session_state.planes))
    if st.button("Limpiar historial"):
        st.session_state.planes = []
        st.rerun()

# ==========================================
# 11. ADVERTENCIA LEGAL (ORIGINAL)
# ==========================================
st.markdown(f"""
<div class="disclaimer">
    <strong>⚠️ CLÁUSULA DE RESPONSABILIDAD:</strong><br><br>
    Esta herramienta es un simulador matemático basado en proyecciones y rentabilidades históricas. No garantiza resultados futuros. 
    El mercado es volátil y los precios pueden bajar drásticamente. La <strong>"Zona Cohete"</strong> es de alto riesgo.<br><br>
    Esto <strong>NO ES CONSEJO FINANCIERO</strong>. El usuario es el único responsable de sus decisiones y debe investigar por su cuenta antes de invertir dinero real.
</div>
""", unsafe_allow_html=True)
