import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ============================================================
# 1. CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

ARCHIVO_LOGO = "logo.png"
CLAVE_ACCESO = "RUTA50K2026"

# ============================================================
# 2. BLOQUEO DE ACCESO
# ============================================================
if "acceso_ok" not in st.session_state:
    st.session_state.acceso_ok = False

if not st.session_state.acceso_ok:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        .main { background: #0d1117; }
        .lock-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            color: #00ffcc;
            text-align: center;
            text-shadow: 0 0 15px rgba(0,255,204,0.7);
            margin-bottom: 10px;
        }
        .lock-sub {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.85rem;
            color: #8b949e;
            text-align: center;
            letter-spacing: 2px;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    col_c, col_lock, col_d = st.columns([1, 2, 1])
    with col_lock:
        st.markdown('<div class="lock-title">🔐 Acceso Privado</div>', unsafe_allow_html=True)
        st.markdown('<div class="lock-sub">SIMULADOR RUTA 50K — ZONA EXCLUSIVA</div>', unsafe_allow_html=True)

        clave_input = st.text_input("Introduce la clave incluida en la guía", type="password", key="clave_input")
        if st.button("🚀 ENTRAR", use_container_width=True):
            if clave_input == CLAVE_ACCESO:
                st.session_state.acceso_ok = True
                st.rerun()
            else:
                st.error("❌ Clave incorrecta. Revisa tu guía.")
    st.stop()

# ============================================================
# 3. ESTILO CSS AVANZADO
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    /* Fondo animado */
    .main {
        background: linear-gradient(-45deg, #0d1117, #161b22, #0d1117, #1a1f26);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #e6edf3;
        font-family: 'Orbitron', sans-serif;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Aplicar Orbitron a todos los textos del contenido principal */
    .main p, .main div, .main span, .main label,
    .main h1, .main h2, .main h3, .main h4,
    .stMarkdown, .stText, .element-container {
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Título principal */
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

    /* Logo */
    .centered-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px;
        border-radius: 50%;
        filter: drop-shadow(0 0 25px rgba(0, 255, 204, 0.7));
        margin-bottom: 20px;
    }

    /* Tarjetas Glassmorphism */
    .metric-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 35px;
        text-align: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.8), inset 2px 2px 5px rgba(255,255,255,0.05);
        margin-bottom: 30px;
        font-family: 'Orbitron', sans-serif;
    }

    .value-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Enlace neón con hover */
    .neon-link {
        color: #00ccff;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        text-decoration: none;
        letter-spacing: 2px;
        transition: text-shadow 0.3s ease;
    }
    .neon-link:hover {
        color: #00ffcc;
        text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #00ffcc;
    }

    /* Secciones separadoras */
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ffcc;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 10px;
        text-shadow: 0 0 8px rgba(0,255,204,0.4);
    }

    /* Disclaimer */
    .disclaimer {
        background: rgba(255, 0, 85, 0.1);
        border-left: 5px solid #ff0055;
        padding: 20px;
        border-radius: 10px;
        font-size: 13px;
        color: #ffb3c1;
        margin-top: 40px;
        font-family: 'Orbitron', sans-serif;
    }

    /* Sidebar: fuente normal para legibilidad */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 3px solid #00ffcc;
        font-family: sans-serif !important;
    }
    [data-testid="stSidebar"] * {
        font-family: sans-serif !important;
    }

    /* Barra de progreso personalizada */
    .progress-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        color: #00ccff;
        letter-spacing: 1px;
        text-align: center;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 4. CABECERA: LOGO + TÍTULO + ENLACE NEÓN
# ============================================================
if os.path.exists(ARCHIVO_LOGO):
    st.markdown(
        f'<img src="data:image/png;base64,{st.image(ARCHIVO_LOGO)}" class="centered-logo">',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt" class="centered-logo"></div>',
        unsafe_allow_html=True
    )

st.markdown('<h1 class="main-title">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#00ccff; font-weight:bold; letter-spacing:2px; font-family:\'Orbitron\',sans-serif;">'
    'OPERATIVA OFICIAL '
    '<a href="https://beacons.ai/inversorenpracticas" target="_blank" class="neon-link">@inversorenpracticas</a>'
    '</p>',
    unsafe_allow_html=True
)

# ============================================================
# 5. PANEL DE CONTROL (SIDEBAR)
# ============================================================
st.sidebar.header("🕹️ CONTROL DE MISIÓN")
cap_inicial = st.sidebar.number_input("Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Inversión Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Tiempo (Años)", 1, 35, 10)

st.sidebar.subheader("Rendimiento Esperado (%)")
r_bunker = st.sidebar.slider("Zona Búnker", 5, 20, 12)
r_cohete = st.sidebar.slider("Zona Cohete", 10, 100, 25)

# ============================================================
# 6. SIMULACIÓN (lógica original intacta)
# ============================================================
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
        data.append({"Año": m//12, "Total": saldo, "Tu Dinero": invertido, "Gratis": saldo - invertido})

df = pd.DataFrame(data)

# ============================================================
# 7. RESULTADOS: TARJETAS CRISTALINAS (originales)
# ============================================================
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f'<div class="metric-card">'
        f'<p style="color:#8b949e; letter-spacing:2px;">PATRIMONIO FINAL</p>'
        f'<p class="value-text">{df["Total"].iloc[-1]:,.2f}€</p>'
        f'<p style="color:#00ccff;">Aporte Real: {df["Tu Dinero"].iloc[-1]:,.0f}€</p>'
        f'</div>',
        unsafe_allow_html=True
    )
with col2:
    regalo = df['Total'].iloc[-1] - df['Tu Dinero'].iloc[-1]
    st.markdown(
        f'<div class="metric-card">'
        f'<p style="color:#8b949e; letter-spacing:2px;">DINERO "GRATIS"</p>'
        f'<p class="value-text" style="color:#00ffcc;">+{regalo:,.2f}€</p>'
        f'<p style="color:#00ccff;">Interés Compuesto</p>'
        f'</div>',
        unsafe_allow_html=True
    )

# ============================================================
# 8. BARRA DE PROGRESO HACIA 50.000€
# ============================================================
st.write("---")
st.markdown('<div class="section-title">📊 Progreso hacia los 50.000€</div>', unsafe_allow_html=True)

meta_prog = 50000
capital_actual = df["Total"].iloc[-1]
progreso = min(capital_actual / meta_prog, 1.0)
st.progress(progreso)
st.markdown(
    f'<div class="progress-label">Progreso hacia 50.000€ → {progreso*100:.1f}% '
    f'({capital_actual:,.0f}€ de {meta_prog:,}€)</div>',
    unsafe_allow_html=True
)

# ============================================================
# 9. GRÁFICAS DUALES (originales)
# ============================================================
st.write("---")
col_pie, col_bar = st.columns([1, 2])

with col_pie:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Tu Ahorro', 'Interés'],
        values=[df['Tu Dinero'].iloc[-1], df['Gratis'].iloc[-1]],
        hole=.75,
        marker=dict(colors=['#00ccff', '#00ffcc'], line=dict(color='#0d1117', width=5))
    )])
    fig_pie.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=0, b=0, l=0, r=0)
    )
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
        xaxis_title="Años de Evolución",
        yaxis_title="Capital Total (€)",
        font=dict(family="Orbitron", size=12)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Meta 50k (lógica original intacta)
meta = 50000
s_meta, m_meta = cap_inicial, 0
while s_meta < meta and m_meta < 600:
    s_meta = (s_meta + aporte_mensual) * (1 + r_mensual)
    m_meta += 1
st.success(f"🎯 **PROYECCIÓN RUTA 50K:** Alcanzarás el hito de los 50.000€ en **{m_meta//12} años y {m_meta%12} meses** aportando {aporte_mensual}€/mes.")

# ============================================================
# 10. CALCULADORA INVERSA
# ============================================================
st.write("---")
st.markdown('<div class="section-title">🧮 Calculadora Inversa — Alcanza tu Meta</div>', unsafe_allow_html=True)

col_inv1, col_inv2 = st.columns(2)
with col_inv1:
    objetivo_inv = st.number_input("Objetivo (€)", value=50000, step=1000, key="obj_inv")
with col_inv2:
    anios_inv = st.slider("Años disponibles", 1, 35, 10, key="anios_inv")

meses_inv = anios_inv * 12
# Fórmula inversa: VF = PMT * [((1+r)^n - 1) / r]  +  PV*(1+r)^n
# Despejando PMT: PMT = (VF - PV*(1+r)^n) * r / ((1+r)^n - 1)
factor = (1 + r_mensual)**meses_inv
if factor - 1 > 0:
    pv_futuro = cap_inicial * factor
    pmt_necesario = (objetivo_inv - pv_futuro) * r_mensual / (factor - 1)
    pmt_necesario = max(pmt_necesario, 0)
    st.success(
        f"💡 Para alcanzar **{objetivo_inv:,.0f}€** en {anios_inv} años "
        f"(con la rentabilidad ponderada actual de {r_ponderada*100:.1f}%), "
        f"necesitas invertir **{pmt_necesario:,.2f}€/mes**."
    )
else:
    st.warning("Ajusta los parámetros para obtener un resultado válido.")

# ============================================================
# 11. COMPARADOR DE ESTRATEGIAS
# ============================================================
st.write("---")
st.markdown('<div class="section-title">⚔️ Comparador de Estrategias</div>', unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.markdown("**Estrategia 1** — Valores actuales del simulador")
    st.info(f"Aporte: {aporte_mensual}€/mes | {anios} años | Rent. {r_ponderada*100:.1f}%")

with col_e2:
    st.markdown("**Estrategia 2** — Configura tu alternativa")
    aporte_e2 = st.slider("Aporte mensual E2 (€)", 50, 1500, min(aporte_mensual + 100, 1500), key="aporte_e2")
    anios_e2 = st.slider("Años E2", 1, 35, anios, key="anios_e2")
    r_bunker_e2 = st.slider("Zona Búnker E2 (%)", 5, 20, r_bunker, key="rb_e2")
    r_cohete_e2 = st.slider("Zona Cohete E2 (%)", 10, 100, r_cohete, key="rc_e2")

# Cálculo Estrategia 2
r_pond_e2 = (r_bunker_e2 * 0.52 + r_cohete_e2 * 0.48) / 100
r_mens_e2 = (1 + r_pond_e2)**(1/12) - 1
meses_e2 = anios_e2 * 12

data_e2 = []
saldo_e2 = cap_inicial
inv_e2 = cap_inicial
for m in range(1, meses_e2 + 1):
    saldo_e2 = (saldo_e2 + aporte_e2) * (1 + r_mens_e2)
    inv_e2 += aporte_e2
    if m % 12 == 0:
        data_e2.append({"Año": m//12, "Total": saldo_e2, "Tu Dinero": inv_e2})

df_e2 = pd.DataFrame(data_e2)

# Resultados comparativos
final_e1 = df["Total"].iloc[-1]
final_e2 = df_e2["Total"].iloc[-1]
diferencia = final_e2 - final_e1

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown(
        f'<div class="metric-card">'
        f'<p style="color:#8b949e; letter-spacing:1px; font-size:0.75rem;">ESTRATEGIA 1</p>'
        f'<p class="value-text" style="font-size:28px;">{final_e1:,.0f}€</p>'
        f'</div>',
        unsafe_allow_html=True
    )
with col_r2:
    color_dif = "#00ffcc" if diferencia >= 0 else "#ff0055"
    signo = "+" if diferencia >= 0 else ""
    st.markdown(
        f'<div class="metric-card">'
        f'<p style="color:#8b949e; letter-spacing:1px; font-size:0.75rem;">ESTRATEGIA 2</p>'
        f'<p class="value-text" style="font-size:28px; color:{color_dif};">{final_e2:,.0f}€</p>'
        f'<p style="color:{color_dif}; font-size:0.8rem;">{signo}{diferencia:,.0f}€ vs E1</p>'
        f'</div>',
        unsafe_allow_html=True
    )

# Gráfica comparativa
años_comunes = list(range(1, max(anios, anios_e2) + 1))
totales_e1 = []
totales_e2_graf = []

s1, s2 = cap_inicial, cap_inicial
for m in range(1, max(anios, anios_e2) * 12 + 1):
    if m <= total_meses:
        s1 = (s1 + aporte_mensual) * (1 + r_mensual)
    if m <= meses_e2:
        s2 = (s2 + aporte_e2) * (1 + r_mens_e2)
    if m % 12 == 0:
        totales_e1.append(s1)
        totales_e2_graf.append(s2)

fig_comp = go.Figure()
fig_comp.add_trace(go.Scatter(
    x=años_comunes[:len(totales_e1)], y=totales_e1,
    mode='lines+markers', name='Estrategia 1',
    line=dict(color='#00ccff', width=3)
))
fig_comp.add_trace(go.Scatter(
    x=años_comunes[:len(totales_e2_graf)], y=totales_e2_graf,
    mode='lines+markers', name='Estrategia 2',
    line=dict(color='#00ffcc', width=3, dash='dash')
))
fig_comp.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Años",
    yaxis_title="Capital (€)",
    font=dict(family="Orbitron", size=11),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)
st.plotly_chart(fig_comp, use_container_width=True)

# ============================================================
# 12. GUARDAR SIMULACIONES
# ============================================================
st.write("---")
st.markdown('<div class="section-title">💾 Guardar Simulaciones</div>', unsafe_allow_html=True)

if "simulaciones" not in st.session_state:
    st.session_state.simulaciones = []

col_g1, col_g2 = st.columns([3, 1])
with col_g1:
    nombre_plan = st.text_input("Nombre del plan", placeholder="Ej: Plan conservador 2026", key="nombre_plan")
with col_g2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Guardar simulación", use_container_width=True):
        if nombre_plan.strip():
            nueva_sim = {
                "Nombre": nombre_plan.strip(),
                "Capital Inicial": f"{cap_inicial:,.0f}€",
                "Aporte/mes": f"{aporte_mensual}€",
                "Años": anios,
                "Búnker %": r_bunker,
                "Cohete %": r_cohete,
                "Patrimonio Final": f"{df['Total'].iloc[-1]:,.0f}€"
            }
            st.session_state.simulaciones.append(nueva_sim)
            st.success(f"✅ Plan '{nombre_plan}' guardado correctamente.")
        else:
            st.warning("Escribe un nombre para el plan antes de guardar.")

if st.session_state.simulaciones:
    st.markdown('<div class="section-title" style="font-size:0.9rem;">📋 Planes Guardados</div>', unsafe_allow_html=True)
    df_sims = pd.DataFrame(st.session_state.simulaciones)
    st.dataframe(df_sims, use_container_width=True, hide_index=True)

    if st.button("🗑️ Borrar todos los planes"):
        st.session_state.simulaciones = []
        st.rerun()
else:
    st.caption("No hay simulaciones guardadas aún.")

# ============================================================
# 13. ADVERTENCIA LEGAL (original intacta)
# ============================================================
st.markdown(f"""
<div class="disclaimer">
    <strong>⚡ CLÁUSULA DE RESPONSABILIDAD:</strong><br><br>
    Esta herramienta es un simulador matemático basado en proyecciones y rentabilidades históricas. No garantiza resultados futuros. 
    El mercado es volátil y los precios pueden bajar drásticamente. La <strong>"Zona Cohete"</strong> es de alto riesgo.<br><br>
    Esto <strong>NO ES CONSEJO FINANCIERO</strong>. El usuario es el único responsable de sus decisiones y debe investigar por su cuenta antes de invertir dinero real.
</div>
""", unsafe_allow_html=True)
