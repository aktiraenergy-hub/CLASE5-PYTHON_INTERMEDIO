# ==============================================================================
# DASHBOARD EJECUTIVO COMERCIAL 2024 - ESTILO INVOME (3x2 + OKRs + GITHUB SYNC)
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
    filtro_region = st.sidebar.multiselect("Región Geográfica:", options=regiones, default=regiones)

    canales = sorted(df_raw['Canal_Venta'].dropna().unique())
    filtro_canal = st.sidebar.multiselect("Canal Comercial:", options=canales, default=canales)

    categorias = sorted(df_raw['Categoria'].dropna().unique())
    filtro_categoria = st.sidebar.multiselect("Categoría:", options=categorias, default=categorias)

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

# Objetivos numéricos OKR
VALOR_OBJETIVO_VENTA = total_meta
prog_barra_venta = min(100.0, (total_venta / VALOR_OBJETIVO_VENTA * 100)) if VALOR_OBJETIVO_VENTA > 0 else 0

VALOR_OBJETIVO_META = total_meta
prog_barra_meta = 100.0

VALOR_OBJETIVO_CUMPLIMIENTO = 100.0
prog_barra_cumplimiento = min(100.0, (cumplimiento / VALOR_OBJETIVO_CUMPLIMIENTO * 100))

VALOR_OBJETIVO_GANANCIA = total_meta * 0.35
prog_barra_ganancia = min(100.0, (total_ganancia / VALOR_OBJETIVO_GANANCIA * 100)) if VALOR_OBJETIVO_GANANCIA > 0 else 0

# ------------------------------------------------------------------------------
# 6. ENCABEZADO Y TARJETAS KPI CON VALORES OBJETIVO EN LOS OKRs
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
                    <span>OKR Meta Anual</span>
                    <span>Obj: ${VALOR_OBJETIVO_VENTA:,.0f}</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {prog_barra_venta}%;"></div>
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
                    <span>OKR Presupuesto</span>
                    <span>Base: ${VALOR_OBJETIVO_META:,.0f}</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {prog_barra_meta}%;"></div>
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
                    <span>OKR Eficiencia</span>
                    <span>Obj: ≥ {VALOR_OBJETIVO_CUMPLIMIENTO:.1f}%</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {prog_barra_cumplimiento}%;"></div>
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
                    <span>OKR Margen (35%)</span>
                    <span>Obj: ${VALOR_OBJETIVO_GANANCIA:,.0f}</span>
                </div>
                <div class="okr-progress-bg">
                    <div class="okr-progress-fill" style="width: {prog_barra_ganancia}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. DASHBOARD 3x2: GENERACIÓN DE LOS 6 GRÁFICOS
# ------------------------------------------------------------------------------
df_cat_grp = df_filtrado.groupby('Categoria', as_index=False)['Venta_Real_USD'].sum()
df_pareto = df_cat_grp.sort_values(by='Venta_Real_USD', ascending=False).reset_index(drop=True)
df_pareto['Acumulado'] = df_pareto['Venta_Real_USD'].cumsum()
df_pareto['Porcentaje_Acumulado'] = (df_pareto['Acumulado'] / df_pareto['Venta_Real_USD'].sum()) * 100

df_mes = df_filtrado.groupby('Mes_Nombre', sort=False)[['Venta_Real_USD', 'Meta_Ventas_USD']].sum()
df_canal = df_filtrado.groupby('Canal_Venta')['Venta_Real_USD'].sum()

fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "<b>1. Evolución Mensual vs Meta Comercial</b>",
        "<b>2. Diagrama de Pareto por Categoría (80/20)</b>",
        "<b>3. Análisis Multidimensional (Venta, Ganancia, Margen, Canal)</b>",
        "<b>4. Dispersión y Outliers por Región (Bigotes / Box Plot)</b>",
        "<b>5. Mix de Ingresos por Canal Comercial</b>",
        "<b>6. Histograma de Distribución de Ganancia</b>"
    ),
    specs=[
        [{"type": "xy"}, {"type": "xy", "secondary_y": True}],
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "domain"}, {"type": "xy"}]
    ],
    vertical_spacing=0.11,
    horizontal_spacing=0.08
)

# [1, 1] Evolución Mensual
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

# [1, 2] Pareto por Categoría
fig.add_trace(
    go.Bar(
        x=df_pareto['Categoria'],
        y=df_pareto['Venta_Real_USD'],
        name='Venta ($)',
        marker=dict(color='#1E293B'),
        hovertemplate='<b>%{x}</b><br>Venta: $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=2, secondary_y=False
)
fig.add_trace(
    go.Scatter(
        x=df_pareto['Categoria'],
        y=df_pareto['Porcentaje_Acumulado'],
        name='% Acumulado',
        mode='lines+markers',
        line=dict(color='#F97316', width=3),
        marker=dict(size=7, color='#EA580C'),
        hovertemplate='<b>%{x}</b><br>Acumulado: %{y:.1f}%<extra></extra>'
    ),
    row=1, col=2, secondary_y=True
)
fig.add_hline(y=80, line_dash="dot", line_color="#94A3B8", row=1, col=2, secondary_y=True)

# [2, 1] Multidimensional (4 Variables)
palette_canal = {'E-commerce': '#10B981', 'Tienda Física': '#F97316', 'Ventas B2B': '#2563EB', 'Mayorista': '#8B5CF6'}

for canal in df_filtrado['Canal_Venta'].dropna().unique():
    sub_df = df_filtrado[df_filtrado['Canal_Venta'] == canal]
    margen_calc = np.clip((sub_df['Ganancia_USD'] / sub_df['Venta_Real_USD'].replace(0, 1)) * 100, 5, 80)
    
    fig.add_trace(
        go.Scatter(
            x=sub_df['Venta_Real_USD'],
            y=sub_df['Ganancia_USD'],
            name=f'Canal: {canal}',
            mode='markers',
            marker=dict(
                size=margen_calc,
                sizemode='diameter',
                sizeref=2.5,
                color=palette_canal.get(canal, '#64748B'),
                opacity=0.75,
                line=dict(width=1, color='#FFFFFF')
            ),
            hovertemplate=(
                f'<b>Canal: {canal}</b><br>' +
                'Venta: $%{x:,.0f}<br>' +
                'Ganancia: $%{y:,.0f}<br>' +
                '<extra></extra>'
            )
        ),
        row=2, col=1
    )

# [2, 2] Bigotes / Box Plot por Región (VERIFICADO CON CIERRES EXACTOS)
colores_box = ['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B', '#EC4899']
for i, reg in enumerate(df_filtrado['Region'].dropna().unique()):
    sub_df = df_filtrado[df_filtrado['Region'] == reg]
    fig.add_trace(
        go.Box(
            y=sub_df['Venta_Real_USD'],
            name=reg,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(color=colores_box[i % len(colores_box)]),
            line=dict(width=2),
            showlegend=False
        ),
        row=2, col=2
    )

# [3, 1] Mix por Canal (Donut)
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
        showlegend=False
    ),
    row=3, col=1
)

# [3, 2] Histograma de Ganancia
fig.add_trace(
    go.Histogram(
        x=df_filtrado['Ganancia_USD'],
        nbinsx=25,
        name='Frecuencia',
        marker=dict(
            color='#10B981',
            line=dict(color='#FFFFFF', width=1)
        ),
        hovertemplate='Rango: $%{x}<br>Cantidad de Registros: %{y}<extra></extra>',
        showlegend=False
    ),
    row=3, col=2
)

# Layout General Plotly
fig.update_layout(
    font=dict(family='Plus Jakarta Sans, sans-serif', color='#475569', size=11),
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    height=1100,
    hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_family="Plus Jakarta Sans"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=11)
    ),
    margin=dict(t=80, b=40, l=40, r=40)
)

fig.update_xaxes(showgrid=True, gridcolor='#F1F5F9', zeroline=False)
fig.update_yaxes(showgrid=True, gridcolor='#F1F5F9', zeroline=False)

fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=1, col=1)
fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=1, col=2, secondary_y=False)
fig.update_yaxes(ticksuffix="%", range=[0, 105], row=1, col=2, secondary_y=True)

fig.update_xaxes(tickprefix="$", tickformat=",.0f", row=2, col=1)
fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=2, col=1)
fig.update_yaxes(tickprefix="$", tickformat=",.0f", row=2, col=2)
fig.update_xaxes(tickprefix="$", tickformat=",.0f", row=3, col=2)

# Despliegue de Gráficos
st.markdown('<div class="dashboard-wrapper">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. TABLA DE REGISTROS EDITABLE Y SINCRONIZACIÓN CON GITHUB
# ------------------------------------------------------------------------------
st.markdown('<div class="dashboard-wrapper">', unsafe_allow_html=True)
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
        <div>
            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #0F172A;">📋 Gestión y Edición de Registros</h3>
            <p style="margin: 0; font-size: 0.8rem; color: #64748B;">Edita los datos directamente en las celdas y sincronízalos de forma permanente con el repositorio de GitHub.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Editor interactivo de datos
df_editable = st.data_editor(
    df_raw,
    num_rows="dynamic",
    use_container_width=True,
    height=400,
    key="editor_ventas"
)

# Función para persistir cambios en GitHub
def guardar_en_github(df_actualizado):
    try:
        if "GITHUB_TOKEN" not in st.secrets or "GITHUB_REPO" not in st.secrets:
            return False, "Faltan configurar GITHUB_TOKEN y GITHUB_REPO en los Secrets de Streamlit."

        token = st.secrets["GITHUB_TOKEN"]
        repo_name = st.secrets["GITHUB_REPO"]
        archivo_path = "Dataset_Visualizacion_Reporte_Empresarial_Sesion4.xlsx"
        sheet_name = "Data_Ventas_Historica"

        g = Github(token)
        repo = g.get_repo(repo_name)
        contenido_remoto = repo.get_contents(archivo_path)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_actualizado.to_excel(writer, sheet_name=sheet_name, index=False)
        contenido_binario = buffer.getvalue()

        repo.update_file(
            path=contenido_remoto.path,
            message="Actualización de datos desde Dashboard Streamlit",
            content=contenido_binario,
            sha=contenido_remoto.sha
        )
        return True, "¡Cambios guardados con éxito en GitHub! La aplicación se actualizará automáticamente."
    except Exception as err:
        return False, f"Error al guardar en GitHub: {err}"

# Botón de guardado
col_btn1, col_btn2 = st.columns([1.5, 4])
with col_btn1:
    if st.button("💾 Guardar cambios en GitHub", use_container_width=True):
        with st.spinner("Sincronizando con el repositorio..."):
            exito, mensaje = guardar_en_github(df_editable)
            if exito:
                st.success(mensaje)
                st.cache_data.clear()
            else:
                st.error(mensaje)

st.markdown('</div>', unsafe_allow_html=True)
