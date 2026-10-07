# ==============================================================================
# DASHBOARD EJECUTIVO COMERCIAL 2024 - ESTILO INVOME ADMIN
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# 2. INYECCIÓN CSS PERSONALIZADO (LOOK & FEEL INVOME)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Fondo principal gris suave */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Ocultar barra superior por defecto de Streamlit */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar con estilo blanco minimalista */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #EEF2F6;
    }
    
    [data-testid="stSidebar"] hr {
        margin: 1.2rem 0;
        border-color: #F1F5F9;
    }

    /* Header superior tipo Invome */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 1.5rem 0;
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
        display: inline-block;
    }

    /* Tarjetas KPI estilo tarjeta bancaria con gradiente */
    .kpi-card {
        border-radius: 18px;
        padding: 1.3rem 1.3rem 1.1rem 1.3rem;
        color: #FFFFFF;
        position: relative;
        min-height: 145px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    .card-label {
        font-size: 0.78rem;
        font-weight: 500;
        opacity: 0.9;
        text-transform: capitalize;
    }
    .card-chip {
        width: 32px;
        height: 24px;
        background: rgba(255, 255, 255, 0.25);
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }
    .card-value {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0.6rem 0;
    }
    .card-footer-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.68rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Gradientes individuales tipo tarjeta */
    .grad-emerald { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
    .grad-orange  { background: linear-gradient(135deg, #F97316 0%, #EA580C 100%); }
    .grad-blue    { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); }
    .grad-purple  { background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%); }

    /* Contenedor gráfico estilo tarjeta blanca */
    .plot-container {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 1.5rem;
        border: 1px solid #F1F5F9;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
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
# 4. SIDEBAR ESTILIZADO (PERFIL & FILTROS)
# ------------------------------------------------------------------------------
with st.sidebar:
    # Perfil corporativo de la interfaz Invome
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem;">
            <div style="width: 42px; height: 42px; border-radius: 12px; background: #E6F4EA; display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
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

    regiones_disponibles = sorted(df_raw['Region'].dropna().unique())
    filtro_region = st.multiselect("Región Geográfica:", options=regiones_disponibles, default=regiones_disponibles)

    canales_disponibles = sorted(df_raw['Canal_Venta'].dropna().unique())
    filtro_canal = st.multiselect("Canal Comercial:", options=canales_disponibles, default=canales_disponibles)

    categorias_disponibles = sorted(df_raw['Categoria'].dropna().unique())
    filtro_categoria = st.multiselect("Categoría:", options=categorias_disponibles, default=categorias_disponibles)

# Aplicar filtros
df_filtrado = df_raw[
    (df_raw['Region'].isin(filtro_region)) &
    (df_raw['Canal_Venta'].isin(filtro_canal)) &
    (df_raw['Categoria'].isin(filtro_categoria))
]

if df_filtrado.empty:
    st.warning("⚠ No hay datos disponibles para la combinación de filtros seleccionada.")
    st.stop()

# ------------------------------------------------------------------------------
# 5. ENCABEZADO Y TARJETAS EN FORMA DE TARJETA (KPIS)
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="top-header">
        <div class="top-title">Dashboard Comercial</div>
        <div class="badge-btn">+ Generar Reporte</div>
    </div>
""", unsafe_allow_html=True)

total_venta = df_filtrado['Venta_Real_USD'].sum()
total_meta = df_filtrado['Meta_Ventas_USD'].sum()
total_ganancia = df_filtrado['Ganancia_USD'].sum()
cumplimiento = (total_venta / total_meta * 100) if total_meta > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card grad-emerald">
            <div class="card-top">
                <span class="card-label">Venta Real Total</span>
                <div class="card-chip"></div>
            </div>
            <div class="card-value">${total_venta:,.0f}</div>
            <div class="card-footer-info">
                <span>Valid: 12/24</span>
                <span>Active</span>
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
            <div class="card-footer-info">
                <span>Target: 2024</span>
                <span>Budget</span>
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
            <div class="card-footer-info">
                <span>KPI Ratio</span>
                <span>Performance</span>
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
            <div class="card-footer-info">
                <span>Margin USD</span>
                <span>Net Profit</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 6. GRÁFICOS (2x2) CON PALETA Y ESTILOS MODERNOS
# ------------------------------------------------------------------------------
df_mes = df_filtrado.groupby('Mes_Nombre', sort=False)[['Venta_Real_USD', 'Meta_Ventas_USD']].sum()
df_cat = df_filtrado.groupby('Categoria')['Venta_Real_USD'].sum().sort_values()
df_canal = df_filtrado.groupby('Canal_Venta')['Venta_Real_USD'].sum()
df_reg = df_filtrado.groupby('Region')['Ganancia_USD'].sum().sort_values(ascending=False)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "<b>Evolución Mensual vs Meta Comercial</b>",
        "<b>Ranking de Ventas por Categoría</b>",
        "<b>Mix de Ingresos por Canal</b>",
        "<b>Ganancia Neta por Región</b>"
    ),
    specs=[
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "domain"}, {"type": "xy"}]
    ],
    vertical_spacing=0.15,
    horizontal_spacing=0.10
)

# Cuadrante 1: Área y Línea
fig.add_trace(
    go.Scatter(
        x=df_mes.index,
        y=df_mes['Venta_Real_USD'],
        name='Venta Real',
        mode='lines+markers',
        line=dict(color='#2563EB', width=3, shape='spline'),
        marker=dict(size=6, color='#2563EB'),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.08)',
        hovertemplate='<b>%{x}</b><br>Venta: $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=df_mes.index,
        y=df_mes['Meta_Ventas_USD'],
        name='Meta Comercial',
        mode='lines',
        line=dict(color='#EF4444', width=2.5, dash='dash', shape='spline'),
        hovertemplate='<b>%{x}</b><br>Meta: $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# Cuadrante 2: Barras Horizontales con esquinas redondeadas
fig.add_trace(
    go.Bar(
        y=df_cat.index,
        x=df_cat.values,
        orientation='h',
        name='Venta Categoría',
        marker=dict(color='#0F172A', line_width=0),
        text=[f"${v:,.0f}" for v in df_cat.values],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Venta: $%{x:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=1, col=2
)

# Cuadrante 3: Donut Chart con paleta Invome
fig.add_trace(
    go.Pie(
        labels=df_canal.index,
        values=df_canal.values,
        hole=0.68,
        name='Canal',
        marker=dict(
            colors=['#10B981', '#F97316', '#2563EB', '#8B5CF6'],
            line=dict(color='#FFFFFF', width=3)
        ),
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>',
        showlegend=True
    ),
    row=2, col=1
)

# Cuadrante 4: Ganancia por Región
fig.add_trace(
    go.Bar(
        x=df_reg.index,
        y=df_reg.values,
        name='Ganancia Región',
        marker=dict(color='#10B981', line_width=0),
        text=[f"${v:,.0f}" for v in df_reg.values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Ganancia: $%{y:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=2, col=2
)

# Ajuste global del Plotly canvas a blanco y tipografía limpia
fig.update_layout(
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#475569'),
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    height=750,
    hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_family="Plus Jakarta Sans"),
    legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0.0),
    margin=dict(t=70, b=30, l=30, r=30)
)

fig.update_xaxes(showgrid=True, gridcolor='#F1F5F9', zeroline=False)
fig.update_yaxes(showgrid=True, gridcolor='#F1F5F9', zeroline=False)

fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=1, col=1)
fig.update_xaxes(tickprefix="$", tickformat=",.0f", row=1, col=2)
fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=2, col=2)

# Despliegue dentro del contenedor blanco con sombra
st.markdown('<div class="plot-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
