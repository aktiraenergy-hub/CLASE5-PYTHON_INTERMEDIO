# ==============================================================================
# DASHBOARD EJECUTIVO COMERCIAL 2024 - ESTILO INVOME (VISTAS ALTERNABLES + GITHUB)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from github import Github

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL DE STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Invome - Executive Sales Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. ESTILOS CSS PERSONALIZADOS (INVOME CARDS & OKRs)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #EEF2F6;
    }

    /* Estilo del selector de vistas superior */
    div[data-testid="stRadio"] > div {
        flex-direction: row;
        background: #EEF2F6;
        padding: 4px;
        border-radius: 12px;
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background: transparent;
        border: none;
        padding: 6px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 700;
        font-size: 0.85rem;
        color: #475569;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #10B981 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.25);
    }

    /* Tarjetas KPI con OKRs integrados */
    .kpi-card {
        border-radius: 18px;
        padding: 1.2rem 1.3rem;
        color: #FFFFFF;
        min-height: 180px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-label {
        font-size: 0.78rem;
        font-weight: 600;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .card-chip {
        width: 32px;
        height: 22px;
        background: rgba(255, 255, 255, 0.25);
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    .card-value {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0.3rem 0;
    }
    
    /* Contenedor OKR */
    .okr-box {
        background: rgba(0, 0, 0, 0.18);
        border-radius: 10px;
        padding: 0.5rem 0.65rem;
        margin-top: 0.4rem;
    }
    .okr-title {
        font-size: 0.70rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        opacity: 0.95;
    }
    .okr-progress-bg {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        overflow: hidden;
    }
    .okr-progress-fill {
        height: 100%;
        background: #FFFFFF;
        border-radius: 4px;
    }

    /* Gradientes */
    .grad-emerald { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
    .grad-orange  { background: linear-gradient(135deg, #F97316 0%, #EA580C 100%); }
    .grad-blue    { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); }
    .grad-purple  { background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%); }

    /* Contenedor del Dashboard y Tablas */
    .dashboard-wrapper {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #EEF2F6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. CARGA DE DATOS
# ------------------------------------------------------------------------------
@st.cache_data
def cargar_datos():
    archivo_excel = 'Dataset_Visualizacion_Reporte_Empresarial_Sesion4.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='Data_Ventas_Historica')
    return df

try:
    df_raw = cargar_datos()
except Exception as e:
    st.error(f"Error al leer el archivo Excel: {e}")
    st.stop()

# ------------------------------------------------------------------------------
# 4. SIDEBAR (PERFIL Y FILTROS)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem;">
            <div style="width: 40px; height: 40px; border-radius: 12px; background: #E6F4EA; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">
                📗
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #0F172A; line-height: 1.2;">invome</div>
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">Invoicing Admin</div>
            </div>
        </div>
        <div style="background: #F8FAFC; border-radius: 12px; padding: 0.
