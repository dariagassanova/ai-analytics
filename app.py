import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Cluster Analytics",
    page_icon="🔗",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .main { background: #0f0f11; }
    .block-container { padding: 2rem 3rem; max-width: 1400px; }

    .header-block {
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #222;
    }
    .header-block h1 {
        font-size: 1.75rem;
        font-weight: 600;
        color: #f0f0f0;
        margin: 0 0 0.25rem;
        letter-spacing: -0.02em;
    }
    .header-block p {
        color: #666;
        font-size: 0.875rem;
        margin: 0;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2.5rem;
    }
    .metric-card {
        background: #17171a;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
    }
    .metric-card .label {
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 600;
        color: #f0f0f0;
        letter-spacing: -0.03em;
        line-height: 1;
        font-family: 'DM Mono', monospace;
    }
    .metric-card .sub {
        font-size: 0.75rem;
        color: #444;
        margin-top: 0.4rem;
    }
    .metric-card.highlight {
        border-color: #2a3a2a;
        background: #141a14;
    }
    .metric-card.highlight .value { color: #6fcf7a; }

    .section-header {
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #555;
        margin: 0 0 1rem;
    }

    .backlog-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.875rem;
    }
    .backlog-table th {
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #555;
        text-align: left;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #222;
    }
    .backlog-table th:not(:first-child) { text-align: right; }
    .backlog-table td {
        padding: 0.65rem 1rem;
        color: #ccc;
        border-bottom: 1px solid #1a1a1d;
        font-family: 'DM Mono', monospace;
        font-size: 0.825rem;
    }
    .backlog-table td:first-child {
        font-family: 'DM Sans', sans-serif;
        color: #888;
    }
    .backlog-table td:not(:first-child) { text-align: right; }
    .backlog-table tr:last-child td {
        border-bottom: none;
        color: #f0f0f0;
        font-weight: 500;
        border-top: 1px solid #222;
    }
    .backlog-table tr:last-child td:first-child { font-family: 'DM Sans', sans-serif; }
    .val-tag {
        display: inline-block;
        background: #1a2e1a;
        color: #6fcf7a;
        font-size: 0.65rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        padding: 2px 7px;
        border-radius: 20px;
        margin-left: 6px;
        font-family: 'DM Sans', sans-serif;
        vertical-align: middle;
    }

    .upload-area {
        background: #17171a;
        border: 1px dashed #333;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 3rem auto;
        max-width: 500px;
    }
    .upload-area h2 { color: #f0f0f0; font-size: 1.25rem; font-weight: 500; margin-bottom: 0.5rem; }
    .upload-area p { color: #555; font-size: 0.875rem; margin-bottom: 1.5rem; }

    .stFileUploader > div { background: transparent !important; }
    [data-testid="stFileUploaderDropzone"] {
        background: #1e1e22 !important;
        border: 1px solid #2a2a2e !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover { border-color: #444 !important; }

    .chart-section { margin-bottom: 2.5rem; }
    .chart-container {
        background: #17171a;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 1.25rem;
    }
    .table-container {
        background: #17171a;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 0.25rem 0;
        overflow: hidden;
    }
    .stPlotlyChart { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

PLOT_BG = "#17171a"
GRID_COLOR = "#222"
TEXT_COLOR = "#888"
BLUE = "#4a90d9"
GRAY = "#5a5a60"
GREEN = "#6fcf7a"

def make_fig():
    return dict(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color=TEXT_COLOR, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )

def analyse(df):
    clusters = df.drop_duplicates('cluster_id').copy()
    clusters['createcluster'] = pd.to_datetime(clusters['createcluster'])
    clusters['terminatingevent'] = pd.to_datetime(clusters['terminatingevent'])
    clusters = clusters[clusters['createcluster'] >= '2026-01-01'].copy()
    clusters['create_month'] = clusters['createcluster'].dt.to_period('M')
    clusters['close_month'] = clusters['terminatingevent'].dt.to_period('M')

    monthly_created = clusters.groupby('create_month').size().reset_index(name='created')
    monthly_created['month_str'] = monthly_created['create_month'].dt.strftime('%b')

    closed_statuses = ['NoDuplicates', 'Merged', 'MergeBlocked']
    closed = clusters[
        clusters['current_cluster_status'].isin(closed_statuses) &
        clusters['terminatingevent'].notna() &
        (clusters['terminatingevent'] >= '2026-01-01')
    ].copy()
    closed['close_type'] = closed['current_cluster_status'].apply(
        lambda x: 'Merged' if x == 'Merged' else 'NoDuplicates'
    )

    monthly_closed = closed.groupby(['close_month', 'close_type']).size().unstack(fill_value=0).reset_index()
    monthly_closed['month_str'] = monthly_closed['close_month'].dt.strftime('%b')
    for col in ['Merged', 'NoDuplicates']:
        if col not in monthly_closed.columns:
            monthly_closed[col] = 0

    closed['value_band'] = pd.cut(
        closed['wk_score_2dp'],
        bins=[0, 0.7, 0.8, 0.9, 1.001],
        labels=['< 0.7', '0.7–0.8', '0.8–0.9', '0.9–1.0'],
        right=False
    )
    closure_by_value = closed.groupby(['value_band', 'close_type']).size().unstack(fill_value=0)
    for col in ['Merged', 'NoDuplicates']:
        if col not in closure_by_value.columns:
            closure_by_value[col] = 0
    closure_by_value['total'] = closure_by_value['Merged'] + closure_by_value['NoDuplicates']

    open_statuses = ['SuspectedDuplicates', 'SuspectedDuplicatesRevisited', 'MergeReady', 'HasConflicts', 'WritersMapped']
    backlog = clusters[clusters['current_cluster_status'].isin(open_statuses)].copy()
    total_backlog = len(backlog)
    backlog['band'] = pd.cut(
        backlog['wk_score_2dp'],
        bins=[0, 0.7, 0.8, 0.9, 1.001],
        labels=['< 0.7', '0.7–0.8', '0.8–0.9', '0.9–1.0'],
        right=False
    )
    band_counts = backlog['band'].value_counts().sort_index()

    return dict(
        total_created=len(clusters),
        total_closed=len(closed),
        total_backlog=total_backlog,
        valuable_backlog=int((backlog['wk_score_2dp'] >= 0.9).sum()),
        monthly_created=monthly_created,
        monthly_closed=monthly_closed,
        closure_by_value=closure_by_value,
        band_counts=band_counts,
    )

def render_dashboard(data):
    st.markdown("""
    <div class="header-block">
        <h1>Cluster Analytics</h1>
        <p>Jan 2026 onwards &nbsp;·&nbsp; Valuable threshold: score ≥ 0.9</p>
    </div>
    """, unsafe_allow_html=True)

    d = data
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Clusters created</div>
            <div class="value">{d['total_created']:,}</div>
            <div class="sub">Jan 2026 onwards</div>
        </div>
        <div class="metric-card">
            <div class="label">Closed clusters</div>
            <div class="value">{d['total_closed']:,}</div>
            <div class="sub">Merged + NoDuplicates</div>
        </div>
        <div class="metric-card">
            <div class="label">Open backlog</div>
            <div class="value">{d['total_backlog']:,}</div>
            <div class="sub">Suspected duplicates</div>
        </div>
        <div class="metric-card highlight">
            <div class="label">Valuable backlog</div>
            <div class="value">{d['valuable_backlog']:,}</div>
            <div class="sub">Score ≥ 0.9</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Monthly creation chart
    st.markdown('<p class="section-header">Monthly cluster creation</p>', unsafe_allow_html=True)
    mc = d['monthly_created']
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=mc['month_str'], y=mc['created'],
        marker_color=BLUE, marker_line_width=0,
        hovertemplate='%{x}: <b>%{y:,}</b><extra></extra>'
    ))
    fig1.update_layout(
        **make_fig(),
        height=220,
        xaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=11), tickformat=','),
        bargap=0.35,
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="section-header">Monthly closure rate</p>', unsafe_allow_html=True)
        mclose = d['monthly_closed']
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=mclose['month_str'], y=mclose['Merged'],
            name='Merged', marker_color=BLUE, marker_line_width=0,
            hovertemplate='%{x} Merged: <b>%{y:,}</b><extra></extra>'
        ))
        fig2.add_trace(go.Bar(
            x=mclose['month_str'], y=mclose['NoDuplicates'],
            name='No duplicates', marker_color=GRAY, marker_line_width=0,
            hovertemplate='%{x} No duplicates: <b>%{y:,}</b><extra></extra>'
        ))
        fig2.update_layout(
            **make_fig(),
            height=220, barmode='stack', bargap=0.35,
            showlegend=True,
            legend=dict(
                orientation='h', x=0, y=1.15,
                font=dict(size=11, color=TEXT_COLOR),
                bgcolor='rgba(0,0,0,0)'
            ),
            xaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRID_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=11)),
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-header">Closures by score band</p>', unsafe_allow_html=True)
        cv = d['closure_by_value']
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['Merged'],
            name='Merged', orientation='h',
            marker_color=BLUE, marker_line_width=0,
            hovertemplate='%{y} Merged: <b>%{x:,}</b><extra></extra>'
        ))
        fig3.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['NoDuplicates'],
            name='No duplicates', orientation='h',
            marker_color=GRAY, marker_line_width=0,
            hovertemplate='%{y} No duplicates: <b>%{x:,}</b><extra></extra>'
        ))
        fig3.update_layout(
            **make_fig(),
            height=220, barmode='stack', bargap=0.35,
            showlegend=True,
            legend=dict(
                orientation='h', x=0, y=1.15,
                font=dict(size=11, color=TEXT_COLOR),
                bgcolor='rgba(0,0,0,0)'
            ),
            xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=11)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRID_COLOR),
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">Unresolved backlog — score distribution</p>', unsafe_allow_html=True)

    bc = d['band_counts']
    total = d['total_backlog']
    rows = ""
    for band, count in bc.items():
        pct = f"{count/total*100:.1f}%"
        tag = '<span class="val-tag">valuable</span>' if band == '0.9–1.0' else ''
        rows += f"<tr><td>{band}{tag}</td><td>{count:,}</td><td>{pct}</td></tr>"
    rows += f"<tr><td>Total</td><td>{total:,}</td><td>100%</td></tr>"

    st.markdown(f"""
    <div class="table-container">
        <table class="backlog-table">
            <thead><tr><th>Score band</th><th>Clusters</th><th>% of backlog</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────

uploaded = st.file_uploader(
    "Upload cluster CSV",
    type=["csv"],
    label_visibility="collapsed"
)

if uploaded is None:
    st.markdown("""
    <div class="upload-area">
        <h2>Cluster Analytics</h2>
        <p>Upload your cluster CSV file to generate the dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    st.file_uploader("Upload CSV", type=["csv"], key="hidden", label_visibility="collapsed")
else:
    try:
        df = pd.read_csv(uploaded)
        required = {'cluster_id', 'current_cluster_status', 'createcluster', 'terminatingevent', 'wk_score_2dp'}
        missing = required - set(df.columns)
        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
        else:
            data = analyse(df)
            render_dashboard(data)
    except Exception as e:
        st.error(f"Could not process file: {e}")
