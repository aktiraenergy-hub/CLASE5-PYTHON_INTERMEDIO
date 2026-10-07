# ==============================================================================
# DASHBOARD EJECUTIVO COMERCIAL 2024 - ESTILO INVOME (3x2 + OKRs)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL
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

    /* Header superior */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 1.2rem 0;
    }
    .top-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    .badge-btn {
        background: #10B981;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.5rem 1.1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        cursor: pointer;
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
        background: rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        padding: 0.45rem 0.6rem;
        margin-top: 0.4rem;
    }
    .okr-title {
        font-size: 0.68rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
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

    /* Contenedor del Dashboard */
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
# 4. SIDEBAR
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
        <div style="background: #F8FAFC; border-radius: 12px; padding: 0.6rem 0.8rem; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #CBD5E1; display:flex; align-items:center; justify-content:center; font-size: 0.8rem; font-weight:700;">EY</div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #1E293B;">Eren Yeager</div>
                <div style="font-size: 0.65rem; color: #94A3B8;">Super Admin</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>Filtros de Negocio</p>", unsafe_allow_html=True)

    regiones = sorted(df_raw['Region'].dropna().unique())
    filtro_region = st.multiselect("Región Geográfica:", options=regiones, default=regiones)

    canales = sorted(df_raw['Canal_Venta'].dropna().unique())
    filtro_canal = st.multiselect("Canal Comercial:", options=canales, default=canales)

    categorias = sorted(df_raw['Categoria'].dropna().unique())
    filtro_categoria = st.multiselect("Categoría:", options=categorias, default=categorias)

df_filtrado = df_raw[
    (df_raw['Region'].isin(filtro_region)) &
    (df_raw['Canal_Venta'].isin(filtro_canal)) &
    (df_raw['Categoria'].isin(filtro_categoria))
].copy()

if df_filtrado.empty:
    st.warning("⚠ No hay datos disponibles para la combinación de filtros seleccionada.")
    st.stop()

# ------------------------------------------------------------------------------
# 5. CÁLCULO DE KPIs Y DEFINICIÓN DE OKRs
# ------------------------------------------------------------------------------
total_venta = df_filtrado['Venta_Real_USD'].sum()
total_meta = df_filtrado['Meta_Ventas_USD'].sum()
total_ganancia = df_filtrado['Ganancia_USD'].sum()
cumplimiento = (total_venta / total_meta * 100) if total_meta > 0 else 0
margen_promedio = (total_ganancia / total_venta * 100) if total_venta > 0 else 0

# Objetivos OKR
OKR_META_VENTA = total_meta
okr_prog_venta = min(100.0, (total_venta / OKR_META_VENTA * 100)) if OKR_META_VENTA > 0 else 0

OKR_CUMPLIMIENTO_OBJ = 100.0
okr_prog_cump = min(100.0, (cumplimiento / OKR_CUMPLIMIENTO_OBJ * 100))

OKR_GANANCIA_OBJ = total_meta * 0.35
okr_prog_ganancia = min(100.0, (total_ganancia / OKR_GANANCIA_OBJ * 100)) if OKR_GANANCIA_OBJ > 0 else 0

OKR_MARGEN_OBJ = 35.0
okr_prog_margen = min(100.0, (margen_promedio / OKR_MARGEN_OBJ * 100))

# ------------------------------------------------------------------------------
# 6. ENCABEZADO Y TARJETAS KPI CON OKRs
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="top-header">
        <div class="top-title">Dashboard Comercial 2024</div>
        <div class="badge-btn">+ Generar Reporte</div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card grad-emerald">
            <div class="card-top">
                <span class="card-label">Venta Real Total</span>
                <div class="card-chip"></div>
            </div>
            <div class="card-value">${total_venta:,.0f}</div>
            <div class="okr-box">
                <div class="okr-title">
                    <span>OKR: Superar Meta Anual</span>
                    <span>{okr_prog_venta:.1f}%</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {okr_prog_venta}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card grad-orange">
            <div class="card-top">
                <span class="card-label">Meta Comercial</span>
                <div class="card-chip"></div>
            </div>
            <div class="card-value">${total_meta:,.0f}</div>
            <div class="okr-box">
                <div class="okr-title">
                    <span>OKR: Base Presupuestal</span>
                    <span>100% Fijada</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: 100%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card grad-blue">
            <div class="card-top">
                <span class="card-label">Cumplimiento</span>
                <div class="card-chip"></div>
            </div>
            <div class="card-value">{cumplimiento:.1f}%</div>
            <div class="okr-box">
                <div class="okr-title">
                    <span>OKR: Eficiencia &gt;= 100%</span>
                    <span>{okr_prog_cump:.1f}%</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {okr_prog_cump}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card grad-purple">
            <div class="card-top">
                <span class="card-label">Ganancia Neta</span>
                <div class="card-chip"></div>
            </div>
            <div class="card-value">${total_ganancia:,.0f}</div>
            <div class="okr-box">
                <div class="okr-title">
                    <span>OKR: Margen &gt;= 35% ({margen_promedio:.1f}%)</span>
                    <span>{okr_prog_margen:.1f}%</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {okr_prog_margen}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. DASHBOARD 3x2: GENERACIÓN DE LOS 6 GRÁFICOS
# ------------------------------------------------------------------------------
df_pareto = df_filtrado.groupby('Categoria')['Venta_Real_USD'].sum().sort_values(ascending=False).reset
