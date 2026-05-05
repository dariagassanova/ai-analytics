import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

    monthly_closed = (
        closed.groupby(['close_month', 'close_type'])
        .size().unstack(fill_value=0).reset_index()
    )
    monthly_closed['month_str'] = monthly_closed['close_month'].dt.strftime('%b')
    for col in ['Merged', 'NoDuplicates']:
        if col not in monthly_closed.columns:
            monthly_closed[col] = 0

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
        monthly_created=monthly_created,
        monthly_closed=monthly_closed,
        closure_by_value=closure_by_value,
        band_counts=band_counts,
    )


def section_label(text):
    st.markdown(
        f'<div class="section-label"><span>{text}</span></div>',
        unsafe_allow_html=True,
    )


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

    # ── Monthly creation ──────────────────────────────────────────────────────
    section_label("Monthly cluster creation")
    mc = d['monthly_created']
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=mc['month_str'],
        y=mc['created'],
        marker=dict(color=BLUE, line_width=0, cornerradius=4),
        hovertemplate='<b>%{x}</b>  %{y:,}<extra></extra>',
    ))
    fig1.update_layout(
        **base_layout(),
        height=200,
        bargap=0.45,
        xaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRAY, zeroline=False),
        yaxis=dict(gridcolor=GRID, tickfont=dict(size=11), tickformat=',', zeroline=False),
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # ── Two-column charts ─────────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        section_label("Monthly closure rate")
        mclose = d['monthly_closed']
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=mclose['month_str'], y=mclose['Merged'],
            name='Merged',
            marker=dict(color=BLUE, line_width=0, cornerradius=4),
            hovertemplate='<b>%{x}</b> Merged  %{y:,}<extra></extra>',
        ))
        fig2.add_trace(go.Bar(
            x=mclose['month_str'], y=mclose['NoDuplicates'],
            name='No duplicates',
            marker=dict(color="#d4d4d8", line_width=0, cornerradius=4),
            hovertemplate='<b>%{x}</b> No dup  %{y:,}<extra></extra>',
        ))
        fig2.update_layout(
            **base_layout(legend=True),
            height=210, barmode='stack', bargap=0.45,
            xaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRAY, zeroline=False),
            yaxis=dict(gridcolor=GRID, tickfont=dict(size=11), zeroline=False),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        section_label("Closures by score band")
        cv = d['closure_by_value']
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['Merged'],
            name='Merged', orientation='h',
            marker=dict(color=BLUE, line_width=0, cornerradius=4),
            hovertemplate='<b>%{y}</b> Merged  %{x:,}<extra></extra>',
        ))
        fig3.add_trace(go.Bar(
            y=cv.index.astype(str), x=cv['NoDuplicates'],
            name='No duplicates', orientation='h',
            marker=dict(color="#d4d4d8", line_width=0, cornerradius=4),
            hovertemplate='<b>%{y}</b> No dup  %{x:,}<extra></extra>',
        ))
        fig3.update_layout(
            **base_layout(legend=True),
            height=210, barmode='stack', bargap=0.45,
            xaxis=dict(gridcolor=GRID, tickfont=dict(size=11), zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=11), linecolor=GRAY, zeroline=False),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Backlog table ─────────────────────────────────────────────────────────
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
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

if 'uploaded' not in st.session_state or st.session_state.uploaded is None:
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
    if uploaded:
        st.session_state.uploaded = uploaded
        st.rerun()
else:
    uploaded = st.session_state.uploaded
    try:
        df = pd.read_csv(uploaded)
        df = normalise_columns(df)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            st.error(f"Missing columns: {', '.join(sorted(missing))}")
        else:
            render_dashboard(df)
            if st.button("↑ Upload a different file", type="tertiary"):
                st.session_state.uploaded = None
                st.rerun()
    except Exception as e:
        st.error(f"Could not process file: {e}")
        if st.button("↑ Try a different file", type="tertiary"):
            st.session_state.uploaded = None
            st.rerun()
