import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(
    page_title="Cluster Analytics",
    page_icon="🔗",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Page chrome ── */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section[data-testid="stSidebar"] { background: #ffffff !important; }
    .main { background: #ffffff; }
    .block-container {
        padding: 2.5rem 3.5rem;
        max-width: 1320px;
    }

    /* ── Header ── */
    .page-header {
        display: flex;
        align-items: baseline;
        gap: 1.25rem;
        margin-bottom: 3rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e4e4e7;
    }
    .page-header h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #09090b;
        margin: 0;
        letter-spacing: -0.025em;
    }
    .page-header .subtitle {
        font-size: 0.8rem;
        color: #a1a1aa;
        letter-spacing: 0.01em;
    }
    .page-header .dot { color: #d4d4d8; margin: 0 0.25rem; }

    /* ── Metric cards ── */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: #e4e4e7;
        border: 1px solid #e4e4e7;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 3rem;
    }
    .metric-card {
        background: #ffffff;
        padding: 1.5rem 1.75rem;
        position: relative;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: 20%;
        right: 0;
        height: 60%;
        width: 1px;
        background: #e4e4e7;
    }
    .metric-card:last-child::after { display: none; }
    .metric-card .label {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a1a1aa;
        margin-bottom: 0.75rem;
    }
    .metric-card .value {
        font-size: 2.25rem;
        font-weight: 600;
        color: #09090b;
        letter-spacing: -0.04em;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-card .sub {
        font-size: 0.72rem;
        color: #a1a1aa;
        margin-top: 0.5rem;
        letter-spacing: 0.01em;
    }
    .metric-card.highlight .value { color: #16a34a; }
    .metric-card.highlight .label { color: #86efac; }
    .metric-card.highlight { background: #f0fdf4; }

    /* ── Section labels ── */
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.875rem;
    }
    .section-label span {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a1a1aa;
    }
    .section-label::before {
        content: '';
        display: block;
        width: 3px;
        height: 3px;
        border-radius: 50%;
        background: #d4d4d8;
        flex-shrink: 0;
    }

    /* ── Chart cards ── */
    .chart-card {
        background: #fafafa;
        border: 1px solid #e4e4e7;
        border-radius: 12px;
        padding: 1.5rem 1.5rem 0.75rem;
        overflow: hidden;
    }

    /* ── Table ── */
    .tbl-card {
        background: #fafafa;
        border: 1px solid #e4e4e7;
        border-radius: 12px;
        overflow: hidden;
    }
    .backlog-table {
        width: 100%;
        border-collapse: collapse;
    }
    .backlog-table th {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a1a1aa;
        text-align: left;
        padding: 0.875rem 1.5rem;
        border-bottom: 1px solid #e4e4e7;
    }
    .backlog-table th:not(:first-child) { text-align: right; }
    .backlog-table td {
        padding: 0.75rem 1.5rem;
        color: #52525b;
        border-bottom: 1px solid #f4f4f5;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }
    .backlog-table td:first-child {
        font-family: 'Inter', sans-serif;
        color: #3f3f46;
        font-size: 0.85rem;
    }
    .backlog-table td:not(:first-child) { text-align: right; }
    .backlog-table tbody tr:last-child td {
        border-bottom: none;
        color: #09090b;
        font-weight: 500;
        border-top: 1px solid #e4e4e7;
        background: #f4f4f5;
    }
    .backlog-table tbody tr:last-child td:first-child {
        font-family: 'Inter', sans-serif;
    }
    .backlog-table tbody tr:hover td { background: #f4f4f5; }
    .backlog-table tbody tr:last-child:hover td { background: #f4f4f5; }

    /* ── Progress bar inside table ── */
    .pct-bar-wrap {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 0.6rem;
    }
    .pct-bar {
        height: 3px;
        border-radius: 2px;
        background: #93c5fd;
        min-width: 2px;
    }
    .pct-bar.green { background: #86efac; }

    /* ── Valuable tag ── */
    .val-tag {
        display: inline-block;
        background: #dcfce7;
        color: #16a34a;
        font-size: 0.6rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 8px;
        font-family: 'Inter', sans-serif;
        vertical-align: middle;
    }

    /* ── Upload screen ── */
    .upload-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
    }
    .upload-icon {
        width: 48px;
        height: 48px;
        background: #f4f4f5;
        border: 1px solid #e4e4e7;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        margin-bottom: 1.25rem;
    }
    .upload-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #09090b;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
    }
    .upload-hint {
        font-size: 0.8rem;
        color: #a1a1aa;
        margin-bottom: 2rem;
        text-align: center;
        line-height: 1.6;
    }
    .upload-hint code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        background: #f4f4f5;
        border: 1px solid #e4e4e7;
        padding: 1px 5px;
        border-radius: 4px;
        color: #52525b;
    }

    /* ── Streamlit file uploader overrides ── */
    .stFileUploader > div { background: transparent !important; }
    .stFileUploader label { display: none !important; }
    [data-testid="stFileUploaderDropzone"] {
        background: #fafafa !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 12px !important;
        transition: border-color 0.15s;
        padding: 1.5rem !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover { border-color: #a1a1aa !important; }
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span { color: #a1a1aa !important; font-size: 0.8rem !important; }
    [data-testid="stFileUploaderDropzone"] small { color: #d4d4d8 !important; }

    /* ── Threshold slider ── */
    .threshold-label {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a1a1aa;
        margin-bottom: 0.25rem;
    }
    div[data-testid="stSlider"] { padding-top: 0.25rem; }
    div[data-testid="stSlider"] label { display: none; }

    /* ── Divider spacer ── */
    .spacer { height: 2rem; }
    .spacer-sm { height: 1.25rem; }

    .stPlotlyChart { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

BG_CARD  = "#fafafa"
GRID     = "#e4e4e7"
TEXT_DIM = "#a1a1aa"
BLUE     = "#3b82f6"
GRAY     = "#d4d4d8"
GREEN    = "#4ade80"


def base_layout(legend=False):
    layout = dict(
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family="Inter, sans-serif", color="#71717a", size=11),
        margin=dict(l=4, r=4, t=4, b=4),
        showlegend=legend,
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#e4e4e7",
            font=dict(family="Inter, sans-serif", size=12, color="#09090b"),
        ),
    )
    if legend:
        layout['legend'] = dict(
            orientation='h', x=0, y=1.18,
            font=dict(size=11, color="#71717a"),
            bgcolor='rgba(0,0,0,0)',
        )
    return layout


BAND_LOWER = {'< 0.7': 0.0, '0.7–0.8': 0.7, '0.8–0.9': 0.8, '0.9–1.0': 0.9}

ATHENA_QUERY = """\
SELECT
    cc.cluster_id,
    'https://cluster-tracker-ui.prod.kobaltmusic.com/work_mapping?id=' || cc.cluster_id AS cluster_link,
    MAX(cs.cluster_state) AS current_cluster_status,
    MAX(cc.createcluster) AS created_date,
    MAX(cc.terminatingevent) AS terminated_date,
    -- Takes the highest score found in the cluster and rounds it
    ROUND(MAX(ws.work_score_percentile), 2) AS cluster_max_work_score
FROM cmdq_kobalt_prod.wk_cluster_conversion cc
JOIN cmdq_kobalt_prod.cluster_summary cs ON cc.cluster_id = cs.cluster_id
LEFT JOIN repertoire_kobalt_prod.work_score_current ws ON cs.cluster_item = ws.work_id
GROUP BY
    cc.cluster_id,
    cc.createcluster,
    cc.terminatingevent
ORDER BY cluster_max_work_score DESC;\
"""

COLUMN_ALIASES = {
    'created_date':            'createcluster',
    'terminated_date':         'terminatingevent',
    'cluster_max_work_score':  'wk_score_2dp',
}

REQUIRED_COLUMNS = {'cluster_id', 'current_cluster_status', 'createcluster',
                    'terminatingevent', 'wk_score_2dp'}


def normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={k: v for k, v in COLUMN_ALIASES.items() if k in df.columns})


def analyse(df, threshold=0.90):
    df = normalise_columns(df)
    clusters = df.drop_duplicates('cluster_id').copy()
    clusters['createcluster']    = pd.to_datetime(clusters['createcluster'])
    clusters['terminatingevent'] = pd.to_datetime(clusters['terminatingevent'])
    clusters = clusters[clusters['createcluster'] >= '2026-01-01'].copy()
    clusters['create_month'] = clusters['createcluster'].dt.to_period('M')
    clusters['close_month']  = clusters['terminatingevent'].dt.to_period('M')

    monthly_created = clusters.groupby('create_month').size().reset_index(name='created')

    closed_statuses = ['NoDuplicates', 'Merged', 'MergeBlocked']
    closed = clusters[
        clusters['current_cluster_status'].isin(closed_statuses) &
        clusters['terminatingevent'].notna() &
        (clusters['terminatingevent'] >= '2026-01-01')
    ].copy()
    closed['close_type'] = closed['current_cluster_status'].apply(
        lambda x: 'Merged' if x == 'Merged' else 'NoDuplicates'
    )

    # Monthly totals for dual-line chart
    monthly_closed_agg = closed.groupby('close_month').size().reset_index(name='closed')
    monthly_totals = (
        monthly_created.rename(columns={'create_month': 'month'})
        .merge(
            monthly_closed_agg.rename(columns={'close_month': 'month'}),
            on='month', how='outer',
        )
        .fillna(0)
        .sort_values('month')
    )
    monthly_totals['month_str'] = monthly_totals['month'].dt.strftime('%b')
    monthly_totals['created']   = monthly_totals['created'].astype(int)
    monthly_totals['closed']    = monthly_totals['closed'].astype(int)

    closed['value_band'] = pd.cut(
        closed['wk_score_2dp'],
        bins=[0, 0.7, 0.8, 0.9, 1.001],
        labels=['< 0.7', '0.7–0.8', '0.8–0.9', '0.9–1.0'],
        right=False,
    )
    closure_by_value = (
        closed.groupby(['value_band', 'close_type'])
        .size().unstack(fill_value=0)
    )
    for col in ['Merged', 'NoDuplicates']:
        if col not in closure_by_value.columns:
            closure_by_value[col] = 0
    closure_by_value['total'] = closure_by_value['Merged'] + closure_by_value['NoDuplicates']

    backlog = clusters[clusters['current_cluster_status'] == 'SuspectedDuplicates'].copy()
    total_backlog = len(backlog)
    backlog['band'] = pd.cut(
        backlog['wk_score_2dp'],
        bins=[0, 0.7, 0.8, 0.9, 1.001],
        labels=['< 0.7', '0.7–0.8', '0.8–0.9', '0.9–1.0'],
        right=False,
    )
    band_counts = backlog['band'].value_counts().sort_index()

    return dict(
        total_created=len(clusters),
        total_closed=len(closed),
        total_backlog=total_backlog,
        valuable_backlog=int((backlog['wk_score_2dp'] >= threshold).sum()),
        monthly_totals=monthly_totals,
        closure_by_value=closure_by_value,
        band_counts=band_counts,
    )


def section_label(text):
    st.markdown(
        f'<div class="section-label"><span>{text}</span></div>',
        unsafe_allow_html=True,
    )


def build_insights_csv(d, threshold):
    lines = [
        "# Cluster Analytics — Insights snapshot",
        f"# Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        f"# Value threshold: {threshold:.2f}",
        "",
        "## Summary",
        "Metric,Value",
        f"Clusters created (Jan 2026+),{d['total_created']}",
        f"Closed clusters,{d['total_closed']}",
        f"Open backlog (SuspectedDuplicates),{d['total_backlog']}",
        f"Valuable backlog (score >= {threshold:.2f}),{d['valuable_backlog']}",
        "",
        "## Monthly totals",
        "Month,Created,Closed",
    ]
    for _, row in d['monthly_totals'].iterrows():
        lines.append(f"{row['month_str']},{row['created']},{row['closed']}")
    lines += [
        "",
        "## Backlog score distribution (SuspectedDuplicates)",
        "Score band,Clusters,% of backlog",
    ]
    total = d['total_backlog']
    for band, count in d['band_counts'].items():
        pct = f"{count / total * 100:.1f}%" if total else "—"
        lines.append(f"{band},{count},{pct}")
    return "\n".join(lines)


def render_dashboard(df):
    # ── Header + threshold control ────────────────────────────────────────────
    hcol, scol = st.columns([3, 1])
    with hcol:
        st.markdown("""
        <div class="page-header">
            <h1>Cluster Analytics</h1>
            <span class="subtitle">Jan 2026 onwards</span>
        </div>
        """, unsafe_allow_html=True)
    with scol:
        st.markdown('<div class="threshold-label">Value threshold</div>', unsafe_allow_html=True)
        threshold = st.slider(
            "Value threshold", min_value=0.70, max_value=0.99,
            value=0.90, step=0.01, format="%.2f",
            label_visibility="collapsed",
        )

    d = analyse(df, threshold)
    st.session_state.last_insights = build_insights_csv(d, threshold)
    st.session_state.last_insights_ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    # ── Metrics ───────────────────────────────────────────────────────────────
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
            <div class="sub">SuspectedDuplicates only</div>
        </div>
        <div class="metric-card highlight">
            <div class="label">Valuable backlog</div>
            <div class="value">{d['valuable_backlog']:,}</div>
            <div class="sub">Score ≥ {threshold:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Created vs Closed dual-line chart ────────────────────────────────────
    section_label("Monthly created vs closed")
    mt = d['monthly_totals']
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=mt['month_str'], y=mt['created'],
        name='Created',
        mode='lines+markers',
        line=dict(color='#3266ad', width=2, shape='spline', smoothing=0.3),
        marker=dict(color='#3266ad', size=5, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(50, 102, 173, 0.08)',
        hovertemplate='Created: <b>%{y:,}</b><extra></extra>',
    ))
    fig1.add_trace(go.Scatter(
        x=mt['month_str'], y=mt['closed'],
        name='Closed',
        mode='lines+markers',
        line=dict(color='#1D9E75', width=2, shape='spline', smoothing=0.3),
        marker=dict(color='#1D9E75', size=5, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(29, 158, 117, 0.08)',
        hovertemplate='Closed: <b>%{y:,}</b><extra></extra>',
    ))
    fig1.update_layout(
        **base_layout(legend=True),
        height=280,
        hovermode='x unified',
        xaxis=dict(
            showgrid=False, tickfont=dict(size=11), linecolor=GRAY,
            zeroline=False, tickmode='array',
            tickvals=mt['month_str'].tolist(), ticktext=mt['month_str'].tolist(),
        ),
        yaxis=dict(gridcolor=GRID, tickfont=dict(size=11), zeroline=False, tickformat='.2~s'),
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # ── Closures by score band + backlog table (side by side) ─────────────────
    col_chart, col_table = st.columns(2, gap="large")

    with col_chart:
        section_label("Closures by score band")
        cv = d['closure_by_value']
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['Merged'],
            name='Merged', orientation='h',
            marker=dict(color='#3266ad', line_width=0, cornerradius=4),
            hovertemplate='<b>%{y}</b> Merged  %{x:,}<extra></extra>',
        ))
        fig2.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['NoDuplicates'],
            name='No duplicates', orientation='h',
            marker=dict(color="#d4d4d8", line_width=0, cornerradius=4),
            hovertemplate='<b>%{y}</b> No dup  %{x:,}<extra></extra>',
        ))
        fig2.update_layout(
            **base_layout(legend=True),
            height=240, barmode='stack', bargap=0.45,
            xaxis=dict(gridcolor=GRID, tickfont=dict(size=11), zeroline=False, tickformat='.2~s'),
            yaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRAY, zeroline=False),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_table:
        section_label("Unresolved backlog — score distribution")
        bc    = d['band_counts']
        total = d['total_backlog']
        rows  = ""
        for band, count in bc.items():
            pct      = count / total * 100
            pct_str  = f"{pct:.1f}%"
            bar_w    = max(2, int(pct * 0.8))
            is_val   = BAND_LOWER.get(str(band), 0.0) >= threshold
            tag      = '<span class="val-tag">valuable</span>' if is_val else ''
            bar_cls  = 'green' if is_val else ''
            bar_cell = (
                f'<div class="pct-bar-wrap">'
                f'<div class="pct-bar {bar_cls}" style="width:{bar_w}px"></div>'
                f'{pct_str}</div>'
            )
            rows += f"<tr><td>{band}{tag}</td><td>{count:,}</td><td>{bar_cell}</td></tr>"
        rows += f"<tr><td>Total</td><td>{total:,}</td><td>100%</td></tr>"

        st.markdown(f"""
        <div class="tbl-card">
            <table class="backlog-table">
                <thead><tr>
                    <th>Score band</th>
                    <th>Clusters</th>
                    <th style="text-align:right">% of backlog</th>
                </tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────

if 'df' not in st.session_state:
    st.markdown("""
    <div class="upload-wrap">
        <div class="upload-icon">📊</div>
        <div class="upload-title">Cluster Analytics</div>
        <div class="upload-hint">
            Drop a CSV file with the required columns:<br>
            <code>cluster_id</code> &nbsp;
            <code>current_cluster_status</code> &nbsp;
            <code>createcluster</code> &nbsp;
            <code>terminatingevent</code> &nbsp;
            <code>wk_score_2dp</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        with st.expander("Get data from Athena"):
            st.code(ATHENA_QUERY, language="sql")
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            df = normalise_columns(df)
            missing = REQUIRED_COLUMNS - set(df.columns)
            if missing:
                st.error(f"Missing columns: {', '.join(sorted(missing))}")
            else:
                st.session_state.df = df
                st.rerun()
        except Exception as e:
            st.error(f"Could not process file: {e}")
else:
    render_dashboard(st.session_state.df)
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    dl_col, _, switch_col = st.columns([2, 6, 2])
    with dl_col:
        if 'last_insights' in st.session_state:
            st.download_button(
                label="Download insights",
                data=st.session_state.last_insights,
                file_name=f"cluster_insights_{datetime.utcnow().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
    with switch_col:
        if st.button("↑ Upload a different file", type="tertiary"):
            del st.session_state.df
            st.rerun()
