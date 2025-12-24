"""
================================================================================
CSP MARKET INTELLIGENCE DASHBOARD - ENTERPRISE EDITION
================================================================================
Premium, modular, production-ready dashboard with executive-grade UX/UI,
advanced filtering, comprehensive insights, and professional PDF/HTML export.

Architecture:
  - Modular functions for reusability
  - Cached data & computations for performance
  - Professional design system with typography hierarchy
  - Advanced filters with real-time aggregation
  - Strategic market insights (growth, dominance, fragmentation)
  - Client-ready export with consulting-style layout

Author: Market Intelligence Team
Version: 2.0
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta, datetime
from collections import defaultdict
import base64
from io import BytesIO

# ================================================================================
# PAGE CONFIG & THEME
# ================================================================================

st.set_page_config(
    page_title="CSP Market Intelligence | Enterprise Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "CSP Market Intelligence Platform v2.0"}
)

# ================================================================================
# PROFESSIONAL DESIGN SYSTEM
# ================================================================================

DESIGN_SYSTEM = {
    "colors": {
        "bg_primary": "#0b0f14",
        "bg_secondary": "#111827",
        "bg_tertiary": "#0f172a",
        "border": "#1f2933",
        "text_primary": "#f9fafb",
        "text_secondary": "#e5e7eb",
        "text_muted": "#9ca3af",
        "accent_blue": "#60a5fa",
        "accent_green": "#22c55e",
        "accent_orange": "#f97316",
        "accent_red": "#ef4444",
        "accent_purple": "#a855f7",
    },
    "spacing": {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
        "2xl": "3rem",
    },
    "typography": {
        "font_family": "'Inter', 'Segoe UI', sans-serif",
        "h1_size": "2.25rem",
        "h2_size": "1.875rem",
        "h3_size": "1.5rem",
        "body_size": "0.9375rem",
        "caption_size": "0.75rem",
    }
}

# Apply professional theme CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html, body, [data-testid="stAppViewContainer"] {{
    font-family: {DESIGN_SYSTEM['typography']['font_family']};
    background-color: {DESIGN_SYSTEM['colors']['bg_primary']};
    color: {DESIGN_SYSTEM['colors']['text_secondary']};
}}

.stApp {{
    background-color: {DESIGN_SYSTEM['colors']['bg_primary']};
}}

#MainMenu, footer {{
    visibility: hidden;
}}

/* Sidebar Professional Styling */
[data-testid="stSidebar"] {{
    background-color: {DESIGN_SYSTEM['colors']['bg_tertiary']};
    border-right: 1px solid {DESIGN_SYSTEM['colors']['border']};
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
    padding-left: 1.5rem;
}}

/* Hero Section */
.hero-container {{
    padding: 2.5rem 2rem;
    border-bottom: 1px solid {DESIGN_SYSTEM['colors']['border']};
    margin-bottom: 2rem;
    background: linear-gradient(135deg, rgba(96, 165, 250, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);
}}

.hero-title {{
    font-size: {DESIGN_SYSTEM['typography']['h1_size']};
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.hero-subtitle {{
    font-size: 1.0625rem;
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    font-weight: 400;
}}

.hero-metadata {{
    font-size: 0.875rem;
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    margin-top: 1.25rem;
    display: flex;
    gap: 2rem;
}}

/* Section Titles & Headers */
.section-title {{
    font-size: {DESIGN_SYSTEM['typography']['h2_size']};
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    margin-top: 2.5rem;
    margin-bottom: 0.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid {DESIGN_SYSTEM['colors']['border']};
    letter-spacing: -0.01em;
}}

.section-subtitle {{
    font-size: {DESIGN_SYSTEM['typography']['body_size']};
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    margin-bottom: 1.5rem;
    font-weight: 400;
}}

/* KPI Cards */
.kpi-container {{
    display: grid;
    gap: 1rem;
}}

.kpi-card {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    padding: 1.25rem;
    transition: all 0.3s ease;
}}

.kpi-card:hover {{
    border-color: {DESIGN_SYSTEM['colors']['accent_blue']};
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.1);
}}

.kpi-label {{
    font-size: {DESIGN_SYSTEM['typography']['caption_size']};
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

.kpi-value {{
    font-size: 1.875rem;
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    letter-spacing: -0.02em;
}}

.kpi-change {{
    font-size: 0.875rem;
    margin-top: 0.5rem;
    font-weight: 500;
}}

.kpi-change.positive {{
    color: {DESIGN_SYSTEM['colors']['accent_green']};
}}

.kpi-change.negative {{
    color: {DESIGN_SYSTEM['colors']['accent_red']};
}}

/* Data Divider */
.divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {DESIGN_SYSTEM['colors']['border']}, transparent);
    margin: 2rem 0;
}}

/* Tables */
.stDataFrame {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    overflow: hidden;
}}

/* Expanders */
[data-testid="stExpander"] {{
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 8px;
    margin-bottom: 1rem;
}}

/* Filter Labels */
.filter-section-label {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Download Button */
.download-button {{
    background: linear-gradient(135deg, {DESIGN_SYSTEM['colors']['accent_blue']} 0%, {DESIGN_SYSTEM['colors']['accent_purple']} 100%);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
}}

/* Insight Box */
.insight-box {{
    background-color: rgba(96, 165, 250, 0.1);
    border-left: 4px solid {DESIGN_SYSTEM['colors']['accent_blue']};
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}}

.insight-title {{
    font-weight: 600;
    color: {DESIGN_SYSTEM['colors']['accent_blue']};
    margin-bottom: 0.5rem;
}}

.insight-text {{
    font-size: 0.9375rem;
    color: {DESIGN_SYSTEM['colors']['text_secondary']};
    line-height: 1.5;
}}
</style>
""", unsafe_allow_html=True)

# ================================================================================
# DATA LOADING & CACHING
# ================================================================================

@st.cache_data
def load_data():
    """Load and preprocess CSP market data."""
    try:
        df = pd.read_excel("market_share.xlsx")
    except FileNotFoundError:
        st.error("⚠️ File 'market_share.xlsx' not found. Please upload it.")
        st.stop()
    
    # Date conversion
    df["Incorporation_Date"] = pd.to_datetime(df["Incorporation_Date"], errors="coerce")
    df = df.dropna(subset=["Corporate_Service_Provider", "Incorporation_Date"])
    
    # Entity Subtype default
    if "Entity_Subtype" not in df.columns:
        df["Entity_Subtype"] = "Special Purpose Vehicle"
    
    # Create temporal features
    df["Year"] = df["Incorporation_Date"].dt.year
    df["Quarter"] = df["Incorporation_Date"].dt.quarter
    df["Month"] = df["Incorporation_Date"].dt.month
    df["Month_Name"] = df["Incorporation_Date"].dt.strftime("%B")
    df["Year_Month"] = df["Incorporation_Date"].dt.to_period("M").astype(str)
    df["Year_Quarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    
    return df

df = load_data()

# ================================================================================
# SIDEBAR FILTERS (ENHANCED)
# ================================================================================

st.sidebar.markdown("### 🎯 INTELLIGENCE FILTERS")

# Date Range Filter
st.sidebar.markdown('<div class="filter-section-label">Date Range</div>', unsafe_allow_html=True)

min_date = df["Incorporation_Date"].min().date()
max_date = df["Incorporation_Date"].max().date()

preset = st.sidebar.selectbox(
    "Quick Select",
    ["Custom", "Last 1 Month", "Last 3 Months", "Last 6 Months", "Last 12 Months", "All Data"],
    label_visibility="collapsed"
)

if preset == "Last 1 Month":
    start_date, end_date = max_date - timedelta(days=30), max_date
elif preset == "Last 3 Months":
    start_date, end_date = max_date - timedelta(days=90), max_date
elif preset == "Last 6 Months":
    start_date, end_date = max_date - timedelta(days=180), max_date
elif preset == "Last 12 Months":
    start_date, end_date = max_date - timedelta(days=365), max_date
elif preset == "All Data":
    start_date, end_date = min_date, max_date
else:
    start_date, end_date = st.sidebar.date_input(
        "Select Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

# Time-based comparison toggle
st.sidebar.markdown('<div class="filter-section-label">Comparison</div>', unsafe_allow_html=True)
enable_comparison = st.sidebar.checkbox("Compare with Previous Period", value=False, help="Show MoM/QoQ/YoY metrics")

# CSP Filters
st.sidebar.markdown('<div class="filter-section-label">Corporate Service Providers</div>', unsafe_allow_html=True)

csps = sorted(df["Corporate_Service_Provider"].unique())
csp_filter_type = st.sidebar.radio("Selection", ["All", "Top-N", "Custom"], horizontal=True, label_visibility="collapsed")

if csp_filter_type == "Top-N":
    top_n = st.sidebar.slider("Show Top N CSPs", min_value=5, max_value=len(csps), value=10, label_visibility="collapsed")
    csp_counts = df[
        (df["Incorporation_Date"].dt.date >= start_date) &
        (df["Incorporation_Date"].dt.date <= end_date)
    ]["Corporate_Service_Provider"].value_counts()
    selected_csps = csp_counts.head(top_n).index.tolist()
elif csp_filter_type == "Custom":
    selected_csps = st.sidebar.multiselect("Select CSPs", csps, default=csps[:5], label_visibility="collapsed")
else:
    selected_csps = csps

# Market Share Threshold Filter
st.sidebar.markdown('<div class="filter-section-label">Market Share Filter</div>', unsafe_allow_html=True)
min_share_pct = st.sidebar.slider(
    "Minimum Market Share (%)",
    min_value=0.0,
    max_value=50.0,
    value=0.0,
    step=0.5,
    label_visibility="collapsed"
)

# Entity Type Filter
st.sidebar.markdown('<div class="filter-section-label">Entity Types</div>', unsafe_allow_html=True)
entity_types = sorted(df["Entity_Subtype"].unique())
selected_entity_types = st.sidebar.multiselect(
    "Select Entity Types",
    entity_types,
    default=entity_types,
    label_visibility="collapsed"
)

# Apply all filters
filtered_df = df[
    (df["Incorporation_Date"].dt.date >= start_date) &
    (df["Incorporation_Date"].dt.date <= end_date) &
    (df["Corporate_Service_Provider"].isin(selected_csps)) &
    (df["Entity_Subtype"].isin(selected_entity_types))
]

# Apply market share threshold (calculate within filtered set)
csp_counts_full = filtered_df["Corporate_Service_Provider"].value_counts()
total_full = len(filtered_df)
min_share_threshold = (min_share_pct / 100) * total_full
qualified_csps = csp_counts_full[csp_counts_full >= min_share_threshold].index.tolist()

if min_share_pct > 0:
    filtered_df = filtered_df[filtered_df["Corporate_Service_Provider"].isin(qualified_csps)]

# ================================================================================
# HERO SECTION
# ================================================================================

now = datetime.now().strftime("%d %b %Y, %H:%M")
filter_summary = f"{start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}"

st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">📊 CSP Market Intelligence Dashboard</div>
    <div class="hero-subtitle">Executive-grade analytics on market dominance, structural preferences & growth momentum</div>
    <div class="hero-metadata">
        <span><b>Generated:</b> {now}</span>
        <span><b>Period:</b> {filter_summary}</span>
        <span><b>Records Analyzed:</b> {len(filtered_df):,}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================================
# SECTION 1: MARKET OVERVIEW (EXPANDED WITH INSIGHTS)
# ================================================================================

st.markdown('<div class="section-title">📈 Market Overview</div>', unsafe_allow_html=True)

# Core metrics computation
total_incorporations = len(filtered_df)
active_csps = filtered_df["Corporate_Service_Provider"].nunique()
days_analyzed = (end_date - start_date).days + 1
months_count = max(filtered_df["Year_Month"].nunique(), 1)
avg_monthly = round(total_incorporations / months_count)

# Entity type breakdown
entity_breakdown = filtered_df["Entity_Subtype"].value_counts()
dominant_entity = entity_breakdown.index[0] if len(entity_breakdown) > 0 else "N/A"
dominant_entity_share = round((entity_breakdown.iloc[0] / total_incorporations * 100), 1) if len(entity_breakdown) > 0 else 0

# CSP concentration metrics
csp_counts = filtered_df["Corporate_Service_Provider"].value_counts()
top_csp = csp_counts.index[0] if len(csp_counts) > 0 else "N/A"
top_csp_share = round((csp_counts.iloc[0] / total_incorporations * 100), 1) if len(csp_counts) > 0 else 0
top3_share = round(csp_counts.head(3).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 3 else 0
top10_share = round(csp_counts.head(10).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 10 else 0
hhi_index = sum((csp_counts / total_incorporations) ** 2) * 10000  # Herfindahl Index

# Previous period metrics (if comparison enabled)
if enable_comparison:
    if preset in ["Last 1 Month", "Last 3 Months", "Last 6 Months"]:
        if preset == "Last 1 Month":
            prev_days = 30
        elif preset == "Last 3 Months":
            prev_days = 90
        else:
            prev_days = 180
        
        prev_start = start_date - timedelta(days=prev_days)
        prev_end = start_date - timedelta(days=1)
        
        prev_df = df[
            (df["Incorporation_Date"].dt.date >= prev_start) &
            (df["Incorporation_Date"].dt.date <= prev_end) &
            (df["Corporate_Service_Provider"].isin(selected_csps)) &
            (df["Entity_Subtype"].isin(selected_entity_types))
        ]
        
        prev_total = len(prev_df)
        mom_change = ((total_incorporations - prev_total) / prev_total * 100) if prev_total > 0 else 0
    else:
        mom_change = None
else:
    mom_change = None

# Display KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Incorporations</div>
        <div class="kpi-value">{total_incorporations:,}</div>
        {f'<div class="kpi-change positive">+{mom_change:.1f}% MoM</div>' if mom_change and mom_change > 0 else f'<div class="kpi-change negative">{mom_change:.1f}% MoM</div>' if mom_change else ''}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Active CSPs</div>
        <div class="kpi-value">{active_csps}</div>
        <div class="kpi-change">Market Participants</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Monthly Volume</div>
        <div class="kpi-value">{avg_monthly:,}</div>
        <div class="kpi-change">Per Month</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Market Leader</div>
        <div class="kpi-value" style="font-size: 1.25rem;">{top_csp}</div>
        <div class="kpi-change">{top_csp_share}% Share</div>
    </div>
    """, unsafe_allow_html=True)

# Market Structure Insights
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🎯 Market Concentration</div>
        <div class="insight-text">
        <b>HHI Index:</b> {hhi_index:.0f} | <b>Top-3 Share:</b> {top3_share}% | <b>Top-10 Share:</b> {top10_share}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🏢 Entity Type Dominance</div>
        <div class="insight-text">
        <b>{dominant_entity}:</b> {dominant_entity_share}% of market | <b>Active Types:</b> {len(entity_breakdown)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# SECTION 2: GROWTH TRENDS & HIGH-GROWTH ANALYSIS
# ================================================================================

st.markdown('<div class="section-title">📊 Growth Trends & High-Growth CSPs</div>', unsafe_allow_html=True)

# Monthly growth data
monthly_summary = filtered_df.groupby("Year_Month").size().reset_index(name="Count")

# Identify high-growth CSPs (MoM/QoQ analysis)
monthly_csp = filtered_df.groupby(["Year_Month", "Corporate_Service_Provider"]).size().reset_index(name="Count")

# Calculate growth rates for top CSPs
growth_analysis = []
for csp in csp_counts.head(10).index:
    csp_data = monthly_csp[monthly_csp["Corporate_Service_Provider"] == csp].sort_values("Year_Month")
    if len(csp_data) >= 2:
        first_month = csp_data.iloc[0]["Count"]
        last_month = csp_data.iloc[-1]["Count"]
        total_csp = csp_data["Count"].sum()
        growth_rate = ((last_month - first_month) / first_month * 100) if first_month > 0 else 0
        avg_monthly_csp = csp_data["Count"].mean()
        
        growth_analysis.append({
            "CSP": csp,
            "Recent Month": last_month,
            "Total (Period)": total_csp,
            "Growth Rate (%)": growth_rate,
            "Avg Monthly": round(avg_monthly_csp, 1)
        })

growth_df = pd.DataFrame(growth_analysis).sort_values("Growth Rate (%)", ascending=False)

# Display growth trends chart
fig_trends = go.Figure()

for csp in csp_counts.head(5).index:
    csp_monthly = monthly_csp[monthly_csp["Corporate_Service_Provider"] == csp].sort_values("Year_Month")
    fig_trends.add_trace(go.Scatter(
        x=csp_monthly["Year_Month"],
        y=csp_monthly["Count"],
        mode="lines+markers",
        name=csp,
        line=dict(width=2.5),
        marker=dict(size=6)
    ))

fig_trends.update_layout(
    title="Top 5 CSPs - Monthly Incorporation Trend",
    height=450,
    plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
    paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
    font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
    xaxis=dict(
        title="Month",
        gridcolor=DESIGN_SYSTEM["colors"]["border"],
        showgrid=True
    ),
    yaxis=dict(
        title="Incorporations",
        gridcolor=DESIGN_SYSTEM["colors"]["border"],
        showgrid=True
    ),
    hovermode="x unified"
)

st.plotly_chart(fig_trends, use_container_width=True)

# High-growth CSPs table
st.markdown('<div class="section-subtitle">🚀 High-Growth CSPs (Top 10 by Growth Rate)</div>', unsafe_allow_html=True)
st.dataframe(growth_df, use_container_width=True, hide_index=True)

# ================================================================================
# SECTION 3: MARKET SHARE & DOMINANCE
# ================================================================================

st.markdown('<div class="section-title">💼 Market Share by CSP</div>', unsafe_allow_html=True)

top20 = csp_counts.head(20)

fig_share = go.Figure(go.Bar(
    x=top20.values,
    y=top20.index,
    orientation="h",
    marker=dict(
        color=top20.values,
        colorscale="Blues",
        showscale=True,
        colorbar=dict(title="Volume")
    ),
    text=top20.values,
    textposition="outside"
))

fig_share.update_layout(
    title="Top 20 CSPs by Incorporation Volume",
    height=600,
    plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
    paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
    font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
    xaxis=dict(title="Incorporations", gridcolor=DESIGN_SYSTEM["colors"]["border"]),
    yaxis=dict(autorange="reversed"),
    hovermode="y"
)

st.plotly_chart(fig_share, use_container_width=True)

# Market fragmentation metric
st.markdown(f"""
<div class="insight-box">
    <div class="insight-title">📊 Market Fragmentation Index</div>
    <div class="insight-text">
    <b>Long-Tail Share (Bottom 50%):</b> {round(100 - top10_share, 1)}% | 
    <b>Total CSPs:</b> {active_csps} | 
    <b>Market Concentration:</b> {'Highly Concentrated (HHI > 2500)' if hhi_index > 2500 else 'Moderate (HHI 1500-2500)' if hhi_index > 1500 else 'Competitive (HHI < 1500)'}
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================================
# SECTION 4: ENTITY TYPE DISTRIBUTION
# ================================================================================

st.markdown('<div class="section-title">🏗️ Entity Type Distribution</div>', unsafe_allow_html=True)

entity_totals = filtered_df["Entity_Subtype"].value_counts()

# Pie chart for entity type overall
fig_entity_pie = go.Figure(data=[go.Pie(
    labels=entity_totals.index,
    values=entity_totals.values,
    marker=dict(colors=[DESIGN_SYSTEM["colors"]["accent_blue"], DESIGN_SYSTEM["colors"]["accent_green"], DESIGN_SYSTEM["colors"]["accent_orange"]]),
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
)])

fig_entity_pie.update_layout(
    height=400,
    plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
    paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
    font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
)

col_pie, col_breakdown = st.columns([1, 1])

with col_pie:
    st.plotly_chart(fig_entity_pie, use_container_width=True)

with col_breakdown:
    st.markdown("**Entity Type Breakdown**")
    for entity_type, count in entity_totals.items():
        pct = round(count / total_incorporations * 100, 1)
        st.metric(entity_type, f"{count:,}", f"{pct}% of market")

# Entity type preferences by CSP
st.markdown('<div class="section-subtitle">Structural Preferences by Top CSPs</div>', unsafe_allow_html=True)

entity_by_csp = filtered_df.groupby(["Corporate_Service_Provider", "Entity_Subtype"]).size().unstack(fill_value=0)
entity_by_csp = entity_by_csp.loc[csp_counts.head(10).index]

fig_entity_csp = go.Figure()

for entity_type in entity_by_csp.columns:
    fig_entity_csp.add_trace(go.Bar(
        x=entity_by_csp.index,
        y=entity_by_csp[entity_type],
        name=entity_type
    ))

fig_entity_csp.update_layout(
    title="Entity Type Distribution by Top 10 CSPs",
    barmode="stack",
    height=800,
    plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
    paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
    font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
    xaxis=dict(title="CSP"),
    yaxis=dict(title="Count", gridcolor=DESIGN_SYSTEM["colors"]["border"]),
)

st.plotly_chart(fig_entity_csp, use_container_width=True)

# ================================================================================
# SECTION 5: DETAILED CSP RANKINGS
# ================================================================================

st.markdown('<div class="section-title">🏆 CSP Rankings & Details</div>', unsafe_allow_html=True)

# Create comprehensive ranking table
ranking_data = []
for rank, (csp, count) in enumerate(csp_counts.items(), 1):
    share_pct = round(count / total_incorporations * 100, 2)
    
    # Entity type mix
    csp_entities = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]["Entity_Subtype"].value_counts()
    primary_entity = csp_entities.index[0] if len(csp_entities) > 0 else "N/A"
    
    # Growth rate
    csp_monthly = monthly_csp[monthly_csp["Corporate_Service_Provider"] == csp].sort_values("Year_Month")
    if len(csp_monthly) >= 2:
        growth = ((csp_monthly.iloc[-1]["Count"] - csp_monthly.iloc[0]["Count"]) / csp_monthly.iloc[0]["Count"] * 100)
    else:
        growth = 0
    
    ranking_data.append({
        "Rank": rank,
        "CSP": csp,
        "Volume": count,
        "Share (%)": share_pct,
        "Primary Type": primary_entity,
        "Growth (%)": round(growth, 1),
        "Trend": "📈" if growth > 10 else "📊" if growth > 0 else "📉"
    })

ranking_df = pd.DataFrame(ranking_data)

st.dataframe(ranking_df, use_container_width=True, hide_index=True)

# ================================================================================
# SECTION 6: MONTHLY DATA TABLE
# ================================================================================

st.markdown('<div class="section-title">📋 Monthly Incorporation Summary</div>', unsafe_allow_html=True)

pivot_monthly = filtered_df.pivot_table(
    index="Corporate_Service_Provider",
    columns="Year_Month",
    values="Incorporation_Date",
    aggfunc="count",
    fill_value=0
)

pivot_monthly["Total"] = pivot_monthly.sum(axis=1)
pivot_monthly = pivot_monthly.sort_values("Total", ascending=False)

st.dataframe(pivot_monthly, use_container_width=True)

# ================================================================================
# SECTION 7: ADVANCED ANALYTICS & INSIGHTS
# ================================================================================

st.markdown('<div class="section-title">🔍 Advanced Market Insights</div>', unsafe_allow_html=True)

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">📊 Market Structure</div>
        <div class="insight-text">
    """, unsafe_allow_html=True)
    
    if hhi_index > 2500:
        st.write("🔴 **Highly Concentrated**: Market dominated by few players. Barriers to entry likely high.")
    elif hhi_index > 1500:
        st.write("🟡 **Moderately Concentrated**: Mixed competitive dynamics with notable market leaders.")
    else:
        st.write("🟢 **Competitive**: Fragmented market with distributed share among many players.")
    
    st.write(f"**HHI Index: {hhi_index:.0f}** (Theoretical max: 10,000)")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

with col_insight2:
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🚀 Growth Momentum</div>
        <div class="insight-text">
    """, unsafe_allow_html=True)
    
    if mom_change and mom_change > 20:
        st.write("📈 **Strong Growth**: Market expanding rapidly. High demand for CSP services.")
    elif mom_change and mom_change > 0:
        st.write("📊 **Steady Growth**: Consistent market expansion with positive momentum.")
    elif mom_change and mom_change < -20:
        st.write("📉 **Sharp Decline**: Market contraction. Monitor macro conditions and CSP activity.")
    else:
        st.write("⏸️ **Flat/Declining**: Market consolidating or facing headwinds.")
    
    if mom_change:
        st.write(f"**MoM Change: {mom_change:+.1f}%**")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================================================================================
# SECTION 8: EXPORT FUNCTIONALITY
# ================================================================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📥 Export & Reporting</div>', unsafe_allow_html=True)

# Professional PDF/HTML Report Generation
def generate_professional_html_report():
    """Generate consulting-style HTML report."""
    
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSP Market Intelligence Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #fff;
            }}
            
            .page-break {{
                page-break-after: always;
            }}
            
            /* Cover Page */
            .cover {{
                background: linear-gradient(135deg, #0b0f14 0%, #1f2933 100%);
                color: #fff;
                padding: 80px 40px;
                text-align: center;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            
            .cover h1 {{
                font-size: 3em;
                margin-bottom: 20px;
                font-weight: 700;
            }}
            
            .cover .subtitle {{
                font-size: 1.5em;
                color: #ccc;
                margin-bottom: 80px;
            }}
            
            .cover .report-meta {{
                margin-top: auto;
                font-size: 0.95em;
                border-top: 1px solid rgba(255,255,255,0.2);
                padding-top: 40px;
            }}
            
            /* Content Pages */
            .content {{
                padding: 60px 40px;
                max-width: 900px;
                margin: 0 auto;
            }}
            
            h2 {{
                color: #0b0f14;
                font-size: 1.8em;
                margin-top: 40px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #60a5fa;
            }}
            
            h3 {{
                color: #1f2933;
                font-size: 1.3em;
                margin-top: 25px;
                margin-bottom: 15px;
            }}
            
            p {{
                margin-bottom: 15px;
                text-align: justify;
            }}
            
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin: 30px 0;
            }}
            
            .kpi-item {{
                background: #f5f5f5;
                padding: 20px;
                border-left: 4px solid #60a5fa;
                border-radius: 4px;
            }}
            
            .kpi-label {{
                font-size: 0.85em;
                color: #666;
                text-transform: uppercase;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .kpi-value {{
                font-size: 1.8em;
                font-weight: 700;
                color: #0b0f14;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: #fff;
            }}
            
            th {{
                background: #0b0f14;
                color: #fff;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #ddd;
            }}
            
            tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            
            .insight-section {{
                background: #f0f7ff;
                border-left: 4px solid #60a5fa;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            
            .insight-title {{
                color: #0b0f14;
                font-weight: 700;
                margin-bottom: 10px;
            }}
            
            .footer {{
                text-align: center;
                color: #999;
                font-size: 0.85em;
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
            
            .filter-info {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 4px;
                font-size: 0.9em;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <!-- COVER PAGE -->
        <div class="cover page-break">
            <h1>CSP Market Intelligence</h1>
            <div class="subtitle">Executive Report & Market Analysis</div>
            <div class="report-meta">
                <p><strong>Report Generated:</strong> {now}</p>
                <p><strong>Analysis Period:</strong> {start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}</p>
                <p style="margin-top: 20px; color: #999;">Market Intelligence Platform v2.0</p>
            </div>
        </div>
        
        <!-- EXECUTIVE SUMMARY PAGE -->
        <div class="content page-break">
            <h2>Executive Summary</h2>
            
            <p>This report presents comprehensive market intelligence on the Corporate Service Provider (CSP) sector for the period {start_date.strftime('%d %b %Y')} through {end_date.strftime('%d %b %Y')}. The analysis encompasses {total_incorporations:,} incorporations across {active_csps} active CSPs, providing decision-grade insights on market dominance, structural preferences, and growth trajectories.</p>
            
            <h3>Key Findings</h3>
            <ul style="margin: 15px 40px; color: #333;">
                <li><strong>Market Leadership:</strong> {top_csp} leads the market with {top_csp_share}% share ({csp_counts.iloc[0]:,} incorporations)</li>
                <li><strong>Market Concentration:</strong> Top-3 CSPs control {top3_share}% of the market (HHI: {hhi_index:.0f})</li>
                <li><strong>Dominant Entity Type:</strong> {dominant_entity} accounts for {dominant_entity_share}% of incorporations</li>
                <li><strong>Average Monthly Volume:</strong> {avg_monthly:,} incorporations per month</li>
                <li><strong>Market Structure:</strong> {'Highly concentrated market with significant barriers to entry' if hhi_index > 2500 else 'Moderately concentrated market with competitive dynamics' if hhi_index > 1500 else 'Competitive, fragmented market with distributed share'}</li>
            </ul>
            
            <div class="kpi-grid">
                <div class="kpi-item">
                    <div class="kpi-label">Total Incorporations</div>
                    <div class="kpi-value">{total_incorporations:,}</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Active CSPs</div>
                    <div class="kpi-value">{active_csps}</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Market Leader</div>
                    <div class="kpi-value" style="font-size: 1.1em;">{top_csp}</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Avg Monthly</div>
                    <div class="kpi-value">{avg_monthly:,}</div>
                </div>
            </div>
            
            <div class="filter-info">
                <strong>Report Parameters:</strong><br>
                Date Range: {start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')} | 
                CSPs Analyzed: {', '.join(selected_csps[:5])}{'...' if len(selected_csps) > 5 else ''} | 
                Entity Types: {', '.join(selected_entity_types)}
            </div>
        </div>
        
        <!-- MARKET OVERVIEW PAGE -->
        <div class="content page-break">
            <h2>Market Overview & Structure</h2>
            
            <h3>Market Concentration Analysis</h3>
            <p>The CSP market exhibits a {'highly concentrated' if hhi_index > 2500 else 'moderately concentrated' if hhi_index > 1500 else 'competitive'} structure with significant implications for market dynamics:</p>
            
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Interpretation</th>
                </tr>
                <tr>
                    <td>HHI Index</td>
                    <td>{hhi_index:.0f}</td>
                    <td>{'Market highly concentrated (potential monopoly concerns)' if hhi_index > 2500 else 'Moderate concentration (competitive but with leaders)' if hhi_index > 1500 else 'Competitive market structure'}</td>
                </tr>
                <tr>
                    <td>Top-3 Concentration</td>
                    <td>{top3_share}%</td>
                    <td>{'Oligopolistic structure' if top3_share > 50 else 'Balanced leadership' if top3_share > 30 else 'Highly fragmented'}</td>
                </tr>
                <tr>
                    <td>Top-10 Share</td>
                    <td>{top10_share}%</td>
                    <td>Long-tail: {100-top10_share}%</td>
                </tr>
                <tr>
                    <td>Active Participants</td>
                    <td>{active_csps}</td>
                    <td>Market breadth and competitive depth</td>
                </tr>
            </table>
            
            <h3>Entity Type Distribution</h3>
            <p>Structural preferences reveal market demand patterns and regulatory/commercial dynamics:</p>
            
            <table>
                <tr>
                    <th>Entity Type</th>
                    <th>Count</th>
                    <th>Share (%)</th>
                </tr>
    """
    
    # Add entity breakdown rows
    for entity_type, count in entity_breakdown.items():
        pct = round(count / total_incorporations * 100, 1)
        html_content += f"""
                <tr>
                    <td>{entity_type}</td>
                    <td>{count:,}</td>
                    <td>{pct}%</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <!-- CSP RANKINGS PAGE -->
        <div class="content page-break">
            <h2>CSP Rankings & Market Position</h2>
            
            <p>Detailed rankings of market participants based on incorporation volume, market share, and growth metrics:</p>
            
            <table>
                <tr>
                    <th>Rank</th>
                    <th>CSP</th>
                    <th>Volume</th>
                    <th>Market Share</th>
                    <th>Primary Entity Type</th>
                </tr>
    """
    
    # Add top 20 CSPs to table
    for idx, row in ranking_df.head(20).iterrows():
        html_content += f"""
                <tr>
                    <td>{row['Rank']}</td>
                    <td><strong>{row['CSP']}</strong></td>
                    <td>{row['Volume']:,}</td>
                    <td>{row['Share (%)']:.2f}%</td>
                    <td>{row['Primary Type']}</td>
                </tr>
        """
    
    html_content += f"""
            </table>
        </div>
        
        <!-- INSIGHTS PAGE -->
        <div class="content page-break">
            <h2>Strategic Insights & Recommendations</h2>
            
            <h3>Growth Momentum</h3>
            <div class="insight-section">
                <div class="insight-title">Market Growth Analysis</div>
                {'<p>The market is experiencing strong growth momentum with average monthly incorporations of ' + str(avg_monthly) + '. Expansion is driven by demand across multiple entity types and distributed among market participants.</p>' if total_incorporations > 100 else '<p>The market shows consolidation patterns with focused activity among key players.</p>'}
            </div>
            
            <h3>Competitive Dynamics</h3>
            <div class="insight-section">
                <div class="insight-title">Market Structure Observations</div>
                {'<p>The market is dominated by a small number of players, suggesting high barriers to entry and strong competitive advantages for market leaders. New entrants should focus on niche specialization or service differentiation.</p>' if top3_share > 50 else '<p>The market remains competitive with opportunities for both established players and emerging entrants. Growth is possible through service innovation and targeted market positioning.</p>'}
            </div>
            
            <h3>Entity Type Trends</h3>
            <div class="insight-section">
                <div class="insight-title">Structural Preferences</div>
                <p>{dominant_entity} entities dominate the market at {dominant_entity_share}% share. This reflects regulatory preferences, tax efficiency, or specific commercial requirements in the jurisdictions analyzed.</p>
            </div>
            
            <h3>Recommendations</h3>
            <ul style="margin: 15px 40px; color: #333;">
                <li><strong>Market Entry:</strong> Focus on underserved entity types or geographic niches where concentration is lower</li>
                <li><strong>Service Strategy:</strong> Differentiate through specialized services, technology integration, or vertical market focus</li>
                <li><strong>Growth Opportunities:</strong> Monitor {', '.join(growth_df.head(3)['CSP'].tolist())} for partnership or acquisition opportunities</li>
                <li><strong>Risk Mitigation:</strong> {'Monitor concentration trends and regulatory responses to market consolidation' if top3_share > 50 else 'Maintain service quality and innovation to compete in fragmented market'}</li>
            </ul>
        </div>
        
        <!-- FOOTER PAGE -->
        <div class="content">
            <h2>Methodology & Definitions</h2>
            
            <h3>Data Sources & Quality</h3>
            <p>This report analyzes {total_incorporations:,} incorporation records across {active_csps} CSPs for the period {start_date.strftime('%d %b %Y')} through {end_date.strftime('%d %b %Y')}. Data is sourced from incorporation registries and CSP service records.</p>
            
            <h3>Key Metrics</h3>
            <ul style="margin: 15px 40px; color: #333;">
                <li><strong>HHI Index:</strong> Herfindahl-Hirschman Index measuring market concentration (0-10,000 scale)</li>
                <li><strong>Market Share:</strong> Percentage of total incorporations handled by each CSP</li>
                <li><strong>Growth Rate:</strong> Period-over-period change in incorporation volumes</li>
                <li><strong>Entity Type:</strong> Classification of incorporated entities (SPV, Foundation, etc.)</li>
            </ul>
            
            <div class="footer">
                <p><strong>CSP Market Intelligence Platform v2.0</strong></p>
                <p>Report generated: {now}</p>
                <p>This report is confidential and intended for authorized recipients only.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

# Export buttons
col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    html_report = generate_professional_html_report()
    st.download_button(
        label="📄 Download HTML Report",
        data=html_report,
        file_name=f"CSP_Intelligence_Report_{start_date.strftime('%Y%m%d')}.html",
        mime="text/html",
        help="Professional HTML report (printable to PDF)"
    )

with col_export2:
    csv_export = pivot_monthly.to_csv()
    st.download_button(
        label="📊 Download CSP Data (CSV)",
        data=csv_export,
        file_name=f"CSP_Monthly_Data_{start_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Detailed monthly breakdown by CSP"
    )

with col_export3:
    ranking_export = ranking_df.to_csv(index=False)
    st.download_button(
        label="🏆 Download Rankings (CSV)",
        data=ranking_export,
        file_name=f"CSP_Rankings_{start_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Ranked CSPs with metrics"
    )

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9ca3af; font-size: 0.85rem; margin-top: 40px;'>"
    "<p><strong>CSP Market Intelligence Platform v2.0</strong></p>"
    "<p>Enterprise-grade analytics | Production-ready | Client-presentable</p>"
    f"<p>Report generated: {now} | Data records: {len(df):,}</p>"
    "</div>",
    unsafe_allow_html=True
)

# ================================================================================
# END OF APPLICATION
# ================================================================================