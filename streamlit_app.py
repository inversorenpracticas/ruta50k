import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Ruta 50k - VIP", layout="wide")

# URL de tu logo (ya funcionando)
LOGO_URL = "https://drive.google.com/uc?export=view&id=1l6Iw1f7-sDlMcEAkocHznItSbDIGIoWt"

# CSS AVANZADO: Relieve, Bisel y Sombras Neón
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main {{ 
        background-color: #0d1117; 
        color: #e6edf3; 
    }}
    
    /* Tarjetas con efecto relieve y bisel (Neomorfismo Dark) */
    .metric-card {{ 
        background: #161b22;
        border-radius: 20px; 
        padding: 30px;
        text-align: center;
        box-shadow: 8px 8px 16px #06080a, -4px -4px 12px #1c222d;
        border: 1px solid rgba(0, 255, 204, 0.1);
        margin-bottom: 25px;
    }}
    
    .logo-container {{
        text-align: center;
        padding-bottom: 20px;
    }}
    
    .logo-img {{
        filter: drop-shadow(0 0 10px rgba(0, 255, 204, 0.5));
        border-radius: 50%;
        width: 120px;
    }}

    h1 {{ 
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc; 
        text-shadow: 0 0 15px rgba(0,255,204,0.4); 
        font-weight: 700;
        text-align: center;
    }}
    
    .highlight-val {{ 
        font-size: 38px; 
        font-weight: bold; 
        color: #00ffcc; 
        text-shadow: 2px 2px 0px #000;
        margin: 10px 0;
    }}
    
    /* Estilo para los botones y sliders */
    [data-testid="stSidebar"] {{
        background-color: #0d1117;
        border-right: 2px solid #00ffcc;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA PERSONALIZADA ---
st.markdown(f"""
    <div class="logo-container">
        <img src="{LOGO_URL}" class="logo-img">
    </div>
    """, unsafe_allow_html=True)
st.title("ESTRATEGIA RUTA 50K")
st.markdown("<p style='text-align: center; color: #8b949e;'>Herramienta Exclusiva de @InversorEnPrácticas</p>", unsafe_allow_html=True)

st.write("---")

# --- PANEL LATERAL ---
st.sidebar.header("🕹️ AJUSTES DE TU RUTA")
st.sidebar.markdown("*(Si estás en móvil, usa la flecha arriba a la izquierda)*")

cap_inicial = st.sidebar.number_input("Tu Capital Inicial (€)", value=0, step=100)
aporte_mensual = st.sidebar.slider("Aporte Mensual Total (€)", 50, 1500, 250)
anios = st.sidebar.slider("Años de Constancia", 1, 30, 10)

st.sidebar.subheader("Rentabilidad Anual (%)")
ret_bunker = st.sidebar.slider("Zona Búnker (Segura)", 5, 15, 12)
ret_cohete = st.sidebar.slider("Zona Cohete (Explosiva)", 10, 80, 25)

# Lógica basada en tu guía: 130€ Búnker (52%) y 120€ Cohete (48%)
r_ponderado = (ret_bunker * 0.52 + ret_cohete * 0.48) / 100
r_mensual = (1 + r_ponderado)**(1/12) - 1
meses = anios * 12

# Simulación
data = []
saldo = cap_inicial
invertido = cap_inicial
for m in range(1, meses + 1):
    saldo = (saldo + aporte_mensual) * (1 + r_mensual)
    invertido += aporte_mensual
    if m % 12 == 0:
        data.append({"Año": m//12, "Total": saldo, "Invertido": invertido, "Interés": saldo - invertido})

df = pd.DataFrame(data)

# --- RESULTADOS CON RELIEVE ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="letter-spacing: 1px; color: #8b949e;">PATRIMONIO ESTIMADO</p>
        <p class="highlight-val">{df['Total'].iloc[-1]:,.2f}€</p>
        <p style="color: #00ccff; font-weight: bold;">Tu ahorro: {df['Invertido'].iloc[-1]:,.0f}€</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    interes_ganado = df['Total'].iloc[-1] - df['Invertido'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <p style="letter-spacing: 1px; color: #8b949e;">DINERO "GRATIS"</p>
        <p class="highlight-val" style="color: #00ffcc;">+{interes_ganado:,.2f}€</p>
        <p style="color: #00ffcc; font-weight:
