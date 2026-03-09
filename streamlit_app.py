import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Ruta 50k - Inversor PRO", layout="wide")

CLAVE_ACCESO = "RUTA50K2026"

# ---------- BLOQUEO DE ACCESO ----------
if "acceso" not in st.session_state:
    st.session_state.acceso = False

if not st.session_state.acceso:

    st.title("🔐 Acceso privado")

    clave = st.text_input("Introduce la clave incluida en la guía", type="password")

    if clave == CLAVE_ACCESO:
        st.session_state.acceso = True
        st.rerun()

    st.stop()

# ---------- ESTILO ----------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body, [class*="css"] {
font-family:'Orbitron', sans-serif;
}

[data-testid="stSidebar"] * {
font-family:sans-serif !important;
}

.neon-link{
color:#00ffcc;
text-decoration:none;
}

.neon-link:hover{
text-shadow:0 0 5px #00ffcc,0 0 20px #00ffcc;
}

.metric-card{
background:rgba(22,27,34,0.6);
border-radius:20px;
padding:30px;
text-align:center;
}

.value-text{
font-size:40px;
color:#00ffcc;
}

</style>
""", unsafe_allow_html=True)

# ---------- CABECERA ----------
st.markdown('<h1 style="text-align:center;">SIMULADOR RUTA 50K</h1>', unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center'>
OPERATIVA OFICIAL 
<a class="neon-link" target="_blank"
href="https://beacons.ai/inversorenpracticas?utm_source=ig&utm_medium=social&utm_content=link_in_bio">
@inversorenpracticas
</a>
</p>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("Control")

capital = st.sidebar.number_input("Capital inicial",0,100000,0)

aporte = st.sidebar.slider("Aporte mensual",50,2000,250)

anios = st.sidebar.slider("Años",1,40,10)

bunker = st.sidebar.slider("Rentabilidad Bunker %",5,20,12)

cohete = st.sidebar.slider("Rentabilidad Cohete %",10,100,25)

rent = (bunker*0.52 + cohete*0.48)/100

r_mensual = (1+rent)**(1/12)-1

meses = anios*12

# ---------- SIMULACION ----------
saldo = capital
invertido = capital

data=[]

for m in range(1,meses+1):

    saldo = (saldo+aporte)*(1+r_mensual)

    invertido+=aporte

    if m%12==0:

        data.append({

        "Año":m//12,

        "Total":saldo,

        "Invertido":invertido,

        "Interes":saldo-invertido

        })

df=pd.DataFrame(data)

# ---------- RESULTADOS ----------
col1,col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="metric-card">
    <p>Patrimonio final</p>
    <p class="value-text">{df["Total"].iloc[-1]:,.0f} €</p>
    </div>
    """,unsafe_allow_html=True)

with col2:

    interes = df["Interes"].iloc[-1]

    st.markdown(f"""
    <div class="metric-card">
    <p>Interés generado</p>
    <p class="value-text">{interes:,.0f} €</p>
    </div>
    """,unsafe_allow_html=True)

# ---------- BARRA META ----------
meta = 50000

progreso = min(df["Total"].iloc[-1]/meta,1)

st.progress(progreso)

st.write(f"Progreso hacia 50.000€ → {progreso*100:.1f}%")

# ---------- GRAFICA ----------
fig = go.Figure()

fig.add_trace(go.Bar(

x=df["Año"],

y=df["Invertido"],

name="Tu dinero"

))

fig.add_trace(go.Bar(

x=df["Año"],

y=df["Interes"],

name="Interés"

))

fig.update_layout(barmode="stack")

st.plotly_chart(fig,use_container_width=True)

# ---------- CALCULADORA INVERSA ----------
st.write("---")
st.subheader("Calculadora para alcanzar una meta")

objetivo = st.number_input("Objetivo (€)",1000,1000000,50000)

anios_obj = st.slider("Años disponibles",1,40,10)

meses_obj = anios_obj*12

r = r_mensual

aporte_necesario = (objetivo * r) / ((1+r)**meses_obj - 1)

st.success(f"Necesitas invertir aproximadamente {aporte_necesario:.0f} € al mes")

# ---------- COMPARADOR ----------
st.write("---")

st.subheader("Comparar estrategias")

aporte2 = st.slider("Aporte estrategia 2",50,2000,400)

saldo2=capital

for m in range(1,meses+1):

    saldo2=(saldo2+aporte2)*(1+r_mensual)

st.write(f"Estrategia 1 → {df['Total'].iloc[-1]:,.0f} €")

st.write(f"Estrategia 2 → {saldo2:,.0f} €")

# ---------- GUARDAR SIMULACION ----------
st.write("---")

if "planes" not in st.session_state:

    st.session_state.planes=[]

nombre = st.text_input("Nombre del plan")

if st.button("Guardar simulación"):

    st.session_state.planes.append({

    "nombre":nombre,

    "capital":capital,

    "aporte":aporte,

    "años":anios

    })

st.write("Planes guardados")

st.write(st.session_state.planes)
