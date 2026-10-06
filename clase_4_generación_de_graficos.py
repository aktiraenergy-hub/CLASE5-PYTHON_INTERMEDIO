# ==============================================================================
# DASHBOARD EJECUTIVO COMERCIAL 2024 - STREAMLIT & PLOTLY
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL DE STREAMLIT
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Comercial 2024",
    page_icon="📊",
    layout="wide"
)

COLOR_NAVY = '#1E1B4B'
COLOR_BLUE = '#2563EB'
COLOR_RED = '#DC2626'
COLOR_GREEN = '#10B981'
COLOR_CANAL = ['#1E1B4B', '#3B82F6', '#10B981', '#F59E0B']

# ------------------------------------------------------------------------------
# 2. CARGA DE DATOS
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
# 3. FILTROS EN BARRA LATERAL (SIDEBAR)
# ------------------------------------------------------------------------------
st.sidebar.header("🔍 Filtros de Negocio")

# Filtro por Región
regiones_disponibles = sorted(df_raw['Region'].dropna().unique())
filtro_region = st.sidebar.multiselect(
    "Región Geográfica:",
    options=regiones_disponibles,
    default=regiones_disponibles
)

# Filtro por Canal de Venta
canales_disponibles = sorted(df_raw['Canal_Venta'].dropna().unique())
filtro_canal = st.sidebar.multiselect(
    "Canal Comercial:",
    options=canales_disponibles,
    default=canales_disponibles
)

# Filtro por Categoría
categorias_disponibles = sorted(df_raw['Categoria'].dropna().unique())
filtro_categoria = st.sidebar.multiselect(
    "Categoría:",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# Aplicar filtros sobre el DataFrame
df_filtrado = df_raw[
    (df_raw['Region'].isin(filtro_region)) &
    (df_raw['Canal_Venta'].isin(filtro_canal)) &
    (df_raw['Categoria'].isin(filtro_categoria))
]

if df_filtrado.empty:
    st.warning("⚠️️ No hay datos disponibles para la combinación de filtros seleccionada.")
    st.stop()

# ------------------------------------------------------------------------------
# 4. ENCABEZADO Y TARJETAS DE MÉTRICAS (KPIs)
# ------------------------------------------------------------------------------
st.title("📊 Cuadro de Mando Ejecutivo de Rendimiento Comercial 2024")

total_venta = df_filtrado['Venta_Real_USD'].sum()
total_meta = df_filtrado['Meta_Ventas_USD'].sum()
total_ganancia = df_filtrado['Ganancia_USD'].sum()
cumplimiento = (total_venta / total_meta * 100) if total_meta > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Venta Real Total", f"${total_venta:,.0f}")
col2.metric("Meta Comercial Total", f"${total_meta:,.0f}")
col3.metric("Cumplimiento", f"{cumplimiento:.1f}%")
col4.metric("Ganancia Neta", f"${total_ganancia:,.0f}")

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. GENERACIÓN DEL DASHBOARD 2x2
# ------------------------------------------------------------------------------
df_mes = df_filtrado.groupby('Mes_Nombre', sort=False)[['Venta_Real_USD', 'Meta_Ventas_USD']].sum()
df_cat = df_filtrado.groupby('Categoria')['Venta_Real_USD'].sum().sort_values()
df_canal = df_filtrado.groupby('Canal_Venta')['Venta_Real_USD'].sum()
df_reg = df_filtrado.groupby('Region')['Ganancia_USD'].sum().sort_values(ascending=False)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "<b>A. Evolución Mensual vs Meta Comercial</b>",
        "<b>B. Ranking de Ventas por Categoría</b>",
        "<b>C. Mix de Ingresos por Canal</b>",
        "<b>D. Ganancia Neta por Región</b>"
    ),
    specs=[
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "domain"}, {"type": "xy"}]
    ],
    vertical_spacing=0.15,
    horizontal_spacing=0.10
)

# Cuadrante 1: Línea Temporal
fig.add_trace(
    go.Scatter(
        x=df_mes.index,
        y=df_mes['Venta_Real_USD'],
        name='Venta Real',
        mode='lines+markers',
        line=dict(color=COLOR_BLUE, width=3),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.12)',
        hovertemplate='<b>Mes:</b> %{x}<br><b>Venta Real:</b> $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=df_mes.index,
        y=df_mes['Meta_Ventas_USD'],
        name='Meta Comercial',
        mode='lines',
        line=dict(color=COLOR_RED, width=3, dash='dash'),
        hovertemplate='<b>Mes:</b> %{x}<br><b>Meta:</b> $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# Cuadrante 2: Barras por Categoría
fig.add_trace(
    go.Bar(
        y=df_cat.index,
        x=df_cat.values,
        orientation='h',
        name='Venta Categoría',
        marker=dict(color=COLOR_NAVY),
        text=[f"${v:,.0f}" for v in df_cat.values],
        textposition='outside',
        hovertemplate='<b>Categoría:</b> %{y}<br><b>Venta:</b> $%{x:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=1, col=2
)

# Cuadrante 3: Donut por Canal
fig.add_trace(
    go.Pie(
        labels=df_canal.index,
        values=df_canal.values,
        hole=0.5,
        name='Canal',
        marker=dict(colors=COLOR_CANAL, line=dict(color='#FFFFFF', width=2)),
        textinfo='label+percent',
        hovertemplate='<b>Canal:</b> %{label}<br><b>Venta:</b> $%{value:,.0f}<br><b>Share:</b> %{percent}<extra></extra>',
        showlegend=False
    ),
    row=2, col=1
)

# Cuadrante 4: Ganancia por Región
fig.add_trace(
    go.Bar(
        x=df_reg.index,
        y=df_reg.values,
        name='Ganancia Región',
        marker=dict(color=COLOR_GREEN),
        text=[f"${v:,.0f}" for v in df_reg.values],
        textposition='outside',
        hovertemplate='<b>Región:</b> %{x}<br><b>Ganancia:</b> $%{y:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=2, col=2
)

# Ajustes de diseño
fig.update_layout(
    template='plotly_white',
    height=800,
    hoverlabel=dict(bgcolor="white", font_size=12),
    legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0.0),
    margin=dict(t=80, b=40, l=40, r=40)
)

fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=1, col=1)
fig.update_xaxes(tickprefix="$", tickformat=",.0f", row=1, col=2)
fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=2, col=2)

# Despliegue en Streamlit
st.plotly_chart(fig, use_container_width=True)
