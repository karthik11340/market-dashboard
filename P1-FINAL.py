"""
================================================================================
CSP MARKET INTELLIGENCE DASHBOARD - ENTERPRISE EDITION [ENHANCED v5]
================================================================================
Premium, modular, production-ready dashboard with executive-grade UX/UI,
advanced filtering, comprehensive insights, and professional PDF/HTML export.

ENHANCEMENTS v5:
  - Fixed-Rate Scoring: SPV = 0.46 pts, Foundation = 0.54 pts (market‑independent)
  - Removed market‑capacity proportional logic
  - Embedded interactive Chart.js charts in company report
  - Updated methodology text and strategic recommendations
  - License status displayed for information only (not scored)

Author: Market Intelligence Team
Version: 5.0 - Fixed-Rate Scoring & Chart Integration
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta, datetime
import base64
from io import BytesIO

# ================================================================================
# PAGE CONFIG & THEME
# ================================================================================

st.set_page_config(
    page_title="CSP Market Intelligence | Enterprise Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "CSP Market Intelligence Platform - v5.0 Fixed-Rate Scoring"}
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
        "accent_yellow": "#fbbf24",
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
        "body_size": "0.94rem",
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
    font-size: 0.94rem;
    color: {DESIGN_SYSTEM['colors']['text_secondary']};
    line-height: 1.5;
}}

/* License Status Styling */
.license-badge {{
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.license-licensed {{
    background-color: rgba(34, 197, 94, 0.2);
    color: {DESIGN_SYSTEM['colors']['accent_green']};
    border: 1px solid {DESIGN_SYSTEM['colors']['accent_green']};
}}

.license-cancelled {{
    background-color: rgba(239, 68, 68, 0.2);
    color: {DESIGN_SYSTEM['colors']['accent_red']};
    border: 1px solid {DESIGN_SYSTEM['colors']['accent_red']};
}}

/* Enhanced Chart Styling */
.chart-container {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}}

/* Company Benchmarking Specific Styles */
.company-highlight {{
    background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
    border: 2px solid {DESIGN_SYSTEM['colors']['accent_blue']};
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}}

.company-metric {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border-left: 4px solid {DESIGN_SYSTEM['colors']['accent_purple']};
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 8px;
}}

.competitor-row {{
    background-color: rgba(96, 165, 250, 0.05);
    border-radius: 8px;
    padding: 0.5rem;
    margin: 0.25rem 0;
}}

/* Benchmark Table Styling */
.benchmark-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    table-layout: fixed;
}}

.benchmark-table th {{
    background-color: {DESIGN_SYSTEM['colors']['bg_tertiary']};
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    padding: 12px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid {DESIGN_SYSTEM['colors']['border']};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.benchmark-table td {{
    padding: 10px 12px;
    border-bottom: 1px solid {DESIGN_SYSTEM['colors']['border']};
    vertical-align: middle;
    word-wrap: break-word;
}}

.benchmark-table tr:hover {{
    background-color: rgba(96, 165, 250, 0.05);
}}

.benchmark-table tr.company-row {{
    background-color: rgba(168, 85, 247, 0.1);
    font-weight: 600;
}}

/* Table Alignment Fixes */
.table-container {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    overflow-x: auto;
}}

.table-container table {{
    width: 100%;
    border-collapse: collapse;
}}

.table-container th {{
    text-align: left;
    padding: 12px 16px;
    font-weight: 600;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    border-bottom: 2px solid {DESIGN_SYSTEM['colors']['border']};
    background-color: {DESIGN_SYSTEM['colors']['bg_tertiary']};
}}

.table-container td {{
    padding: 10px 16px;
    border-bottom: 1px solid {DESIGN_SYSTEM['colors']['border']};
    vertical-align: middle;
}}

/* Company Section Specific */
.company-section-title {{
    font-size: 2rem;
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    margin-top: 1rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid {DESIGN_SYSTEM['colors']['accent_purple']};
    letter-spacing: -0.01em;
}}

.company-section-subtitle {{
    font-size: 1.1rem;
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    margin-bottom: 1.5rem;
    font-weight: 400;
}}

/* Status Indicators */
.status-indicator {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}}

.status-active {{
    background-color: rgba(34, 197, 94, 0.1);
    color: {DESIGN_SYSTEM['colors']['accent_green']};
    border: 1px solid {DESIGN_SYSTEM['colors']['accent_green']};
}}

.status-inactive {{
    background-color: rgba(239, 68, 68, 0.1);
    color: {DESIGN_SYSTEM['colors']['accent_red']};
    border: 1px solid {DESIGN_SYSTEM['colors']['accent_red']};
}}

/* Metric Card Styling */
.metric-card {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    border-color: {DESIGN_SYSTEM['colors']['accent_purple']};
    background-color: rgba(168, 85, 247, 0.05);
}}

.metric-card-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.metric-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['text_primary']};
    margin: 0.5rem 0;
}}

.metric-label {{
    font-size: 0.875rem;
    color: {DESIGN_SYSTEM['colors']['text_muted']};
    margin-bottom: 0.25rem;
}}

.metric-delta {{
    font-size: 0.875rem;
    font-weight: 500;
    margin-top: 0.5rem;
}}

.metric-delta.positive {{
    color: {DESIGN_SYSTEM['colors']['accent_green']};
}}

.metric-delta.negative {{
    color: {DESIGN_SYSTEM['colors']['accent_red']};
}}

/* Benchmark Widget */
.benchmark-widget {{
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}}

.benchmark-widget-title {{
    font-weight: 700;
    color: {DESIGN_SYSTEM['colors']['accent_purple']};
    margin-bottom: 1rem;
    font-size: 1.1rem;
}}

/* Heatmap/Matrix Grid */
.comparison-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}}

.comparison-cell {{
    background-color: {DESIGN_SYSTEM['colors']['bg_secondary']};
    border: 1px solid {DESIGN_SYSTEM['colors']['border']};
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}}

.comparison-cell.high {{
    border-color: {DESIGN_SYSTEM['colors']['accent_green']};
    background-color: rgba(34, 197, 94, 0.1);
}}

.comparison-cell.medium {{
    border-color: {DESIGN_SYSTEM['colors']['accent_orange']};
    background-color: rgba(249, 115, 22, 0.1);
}}

.comparison-cell.low {{
    border-color: {DESIGN_SYSTEM['colors']['accent_red']};
    background-color: rgba(239, 68, 68, 0.1);
}}

</style>
""", unsafe_allow_html=True)

# ================================================================================
# HELPER FUNCTIONS - FIXED-RATE SCORING (0.46 SPV, 0.54 FOUNDATION)
# ================================================================================

def calculate_cagr(start_value, end_value, periods):
    """Calculate Compound Annual Growth Rate (CAGR)"""
    if start_value <= 0 or periods <= 0:
        return 0
    
    try:
        cagr = ((end_value / start_value) ** (1 / periods)) - 1
        return cagr * 100
    except:
        return 0

def calculate_cagr_from_dates(start_value, end_value, start_date, end_date):
    """Calculate CAGR based on dates (handles partial years)"""
    if start_value <= 0:
        return 0
    
    days_difference = (end_date - start_date).days
    if days_difference <= 0:
        return 0
    
    years = days_difference / 365.25
    return calculate_cagr(start_value, end_value, years)

def format_cagr(cagr_value):
    """Format CAGR value for display"""
    if pd.isna(cagr_value) or cagr_value == 0:
        return "0.0%"
    return f"{cagr_value:+.1f}%"

def calculate_market_based_score(company_data, total_market_spv=None, total_market_foundation=None):
    """
    Calculate fixed-rate performance score:
    - Each SPV  = 0.46 points (fixed)
    - Each Foundation = 0.54 points (fixed)
    - Total Score = (SPV Count × 0.46) + (Foundation Count × 0.54)
    """
    POINT_PER_SPV = 0.46
    POINT_PER_FOUNDATION = 0.54

    # Count company SPVs and Foundations
    company_spv_count = len(company_data[company_data["Entity_Subtype"].str.contains(
        "Special Purpose Vehicle|Special purpose vehicle", case=False, na=False)])
    company_foundation_count = len(company_data[company_data["Entity_Subtype"].str.contains(
        "Foundation", case=False, na=False)])

    spv_score = company_spv_count * POINT_PER_SPV
    foundation_score = company_foundation_count * POINT_PER_FOUNDATION
    total_score = spv_score + foundation_score

    return {
        "spv_count": company_spv_count,
        "foundation_count": company_foundation_count,
        "point_per_spv": POINT_PER_SPV,
        "point_per_foundation": POINT_PER_FOUNDATION,
        "spv_score": spv_score,
        "foundation_score": foundation_score,
        "total_score": total_score
    }

def calculate_performance_score(market_share, spv_share, foundation_share, license_rate):
    """
    DEPRECATED: Old scoring system - kept for backward compatibility
    Use calculate_market_based_score instead
    """
    score = 0
    
    # Market Share Component (100 points total)
    if market_share > 0:
        spv_points = min((spv_share / 100) * 46, 46) if spv_share > 0 else 0
        foundation_points = min((foundation_share / 100) * 54, 54) if foundation_share > 0 else 0
        market_component = spv_points + foundation_points
    else:
        market_component = 0
    
    score += market_component
    
    return min(score, 100)

# ================================================================================
# DATA LOADING
# ================================================================================

def load_data():
    """Load and preprocess CSP market data"""
    try:
        df = pd.read_csv("market_share.csv")
    except FileNotFoundError:
        st.error("⚠️ File 'market_share.csv' not found. Please upload it.")
        st.stop()
    
    df["Incorporation_Date"] = pd.to_datetime(df["Incorporation_Date"], errors="coerce")
    df = df.dropna(subset=["Corporate_Service_Provider", "Incorporation_Date"])
    
    if "Entity_Subtype" not in df.columns:
        df["Entity_Subtype"] = "Special Purpose Vehicle"
    
    if "License_Status" not in df.columns:
        df["License_Status"] = "Licensed"
    
    df["Year"] = df["Incorporation_Date"].dt.year
    df["Quarter"] = df["Incorporation_Date"].dt.quarter
    df["Month"] = df["Incorporation_Date"].dt.month
    df["Month_Name"] = df["Incorporation_Date"].dt.strftime("%B")
    df["Year_Month"] = df["Incorporation_Date"].dt.to_period("M").astype(str)
    df["Year_Quarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    
    return df

df = load_data()

# ================================================================================
# SIDEBAR FILTERS
# ================================================================================

st.sidebar.markdown("### 🎯 INTELLIGENCE FILTERS")

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

st.sidebar.markdown('<div class="filter-section-label">License Status</div>', unsafe_allow_html=True)
license_statuses = sorted(df["License_Status"].unique())
selected_license_statuses = st.sidebar.multiselect(
    "Select License Statuses",
    license_statuses,
    default=license_statuses,
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="filter-section-label">Market Share Filter</div>', unsafe_allow_html=True)
min_share_pct = st.sidebar.slider(
    "Minimum Market Share (%)",
    min_value=0.0,
    max_value=50.0,
    value=0.0,
    step=0.5,
    label_visibility="collapsed"
)

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
    (df["Entity_Subtype"].isin(selected_entity_types)) &
    (df["License_Status"].isin(selected_license_statuses))
]

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
    <div class="hero-title">ADGM Market Intelligence Dashboard</div>
    <div class="hero-subtitle">Executive-grade analytics on market dominance, structural preferences & growth momentum</div>
    <div class="hero-metadata">
        <span><b>Generated:</b> {now}</span>
        <span><b>Period:</b> {filter_summary}</span>
        <span><b>Records Analyzed:</b> {len(filtered_df):,}</span>
        <span><b>License Status:</b> {', '.join(selected_license_statuses)}</span>
        <span><b>Data Status:</b> 🟢 Live Updates</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================================
# SECTION 1: COMPANY BENCHMARKING - ENHANCED WITH FIXED-RATE SCORING & CHARTS
# ================================================================================

# Core metrics
total_incorporations = len(filtered_df)
active_csps = filtered_df["Corporate_Service_Provider"].nunique()
days_analyzed = (end_date - start_date).days + 1
months_count = max(filtered_df["Year_Month"].nunique(), 1)
avg_monthly = round(total_incorporations / months_count)

license_breakdown = filtered_df["License_Status"].value_counts()
licensed_count = license_breakdown.get("Licensed", 0)
cancelled_count = license_breakdown.get("License cancelled", 0)
licensed_pct = round(licensed_count / total_incorporations * 100, 1) if total_incorporations > 0 else 0

entity_breakdown = filtered_df["Entity_Subtype"].value_counts()
dominant_entity = entity_breakdown.index[0] if len(entity_breakdown) > 0 else "N/A"
dominant_entity_share = round((entity_breakdown.iloc[0] / total_incorporations * 100), 1) if len(entity_breakdown) > 0 else 0

csp_counts = filtered_df["Corporate_Service_Provider"].value_counts()
top_csp = csp_counts.index[0] if len(csp_counts) > 0 else "N/A"
top_csp_share = round((csp_counts.iloc[0] / total_incorporations * 100), 1) if len(csp_counts) > 0 else 0
top3_share = round(csp_counts.head(3).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 3 else 0
top10_share = round(csp_counts.head(10).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 10 else 0
hhi_index = sum((csp_counts / total_incorporations) ** 2) * 10000

st.markdown('<div class="section-title">MS - MARKET POSITION</div>', unsafe_allow_html=True)

company_name = "M S CHARTERED ACCOUNTANTS LTD"
company_data = filtered_df[filtered_df["Corporate_Service_Provider"] == company_name]

if len(company_data) == 0:
    st.warning(f"⚠️ No data found for {company_name}. Please check the company name in your dataset.")
    st.info("💡 **Tip**: Check if your company name is spelled exactly as in the CSV file, including spaces and special characters.")
else:
    # Calculate market totals for SPV and Foundation (for display only, not used in scoring)
    total_market_spv = len(filtered_df[filtered_df["Entity_Subtype"].str.contains("Special Purpose Vehicle|Special purpose vehicle", case=False, na=False)])
    total_market_foundation = len(filtered_df[filtered_df["Entity_Subtype"].str.contains("Foundation", case=False, na=False)])
    
    # Company metrics
    company_total = len(company_data)
    company_market_share = (company_total / total_incorporations * 100) if total_incorporations > 0 else 0
    company_rank = (csp_counts.index.get_loc(company_name) + 1) if company_name in csp_counts.index else "Not Ranked"
    
    # Calculate market-based score for company (fixed-rate)
    company_score = calculate_market_based_score(company_data, total_market_spv, total_market_foundation)
    
    company_licenses = company_data["License_Status"].value_counts()
    company_licensed = company_licenses.get("Licensed", 0)
    company_cancelled = company_licenses.get("License cancelled", 0)
    company_license_rate = (company_licensed / company_total * 100) if company_total > 0 else 0
    
    company_entities = company_data["Entity_Subtype"].value_counts()
    company_primary_entity = company_entities.index[0] if len(company_entities) > 0 else "N/A"
    company_primary_share = (company_entities.iloc[0] / company_total * 100) if len(company_entities) > 0 else 0
    
    # Entity type breakdown - FIXED: Use actual counts
    company_spv_count = company_score["spv_count"]
    company_foundation_count = company_score["foundation_count"]
    company_spv_pct = (company_spv_count / company_total * 100) if company_total > 0 else 0
    company_foundation_pct = (company_foundation_count / company_total * 100) if company_total > 0 else 0
    
    company_monthly = company_data.groupby("Year_Month").size()
    company_monthly_df = company_monthly.reset_index(name="Count")
    
    if len(company_monthly_df) >= 2:
        first_month = company_monthly_df.iloc[0]["Count"]
        last_month = company_monthly_df.iloc[-1]["Count"]
        company_growth_rate = ((last_month - first_month) / first_month * 100) if first_month > 0 else 0
        company_avg_monthly = company_monthly.mean()
        company_trend = "📈" if company_growth_rate > 10 else "📊" if company_growth_rate > 0 else "📉"
    else:
        company_growth_rate = 0
        company_avg_monthly = company_monthly.mean() if len(company_monthly) > 0 else 0
        company_trend = "📊"
    
    # Top 5 competitors benchmark
    top_5_csps = csp_counts.head(5)
    competitor_data = []
    
    for csp in top_5_csps.index:
        csp_data = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]
        csp_licenses = csp_data["License_Status"].value_counts()
        csp_licensed = csp_licenses.get("Licensed", 0)
        csp_total = len(csp_data)
        csp_license_rate = (csp_licensed / csp_total * 100) if csp_total > 0 else 0
        
        # Entity type breakdown for competitor
        csp_spv = len(csp_data[csp_data["Entity_Subtype"].str.contains("Special Purpose Vehicle|Special purpose vehicle", case=False, na=False)])
        csp_foundation = len(csp_data[csp_data["Entity_Subtype"].str.contains("Foundation", case=False, na=False)])
        csp_spv_pct = (csp_spv / csp_total * 100) if csp_total > 0 else 0
        csp_foundation_pct = (csp_foundation / csp_total * 100) if csp_total > 0 else 0
        
        csp_monthly = csp_data.groupby("Year_Month").size()
        if len(csp_monthly) >= 2:
            csp_growth = ((csp_monthly.iloc[-1] - csp_monthly.iloc[0]) / csp_monthly.iloc[0] * 100) if csp_monthly.iloc[0] > 0 else 0
        else:
            csp_growth = 0
        
        # Calculate performance score with new system
        market_score = calculate_performance_score(
            (csp_total / total_incorporations * 100),
            csp_spv_pct,
            csp_foundation_pct,
            csp_license_rate
        )
        
        competitor_data.append({
            "CSP": csp,
            "Volume": csp_total,
            "Market Share (%)": round(csp_total / total_incorporations * 100, 2),
            "SPV (%)": round(csp_spv_pct, 1),
            "Foundation (%)": round(csp_foundation_pct, 1),
            "License Rate (%)": round(csp_license_rate, 1),
            "Growth Rate (%)": round(csp_growth, 1),
            "Avg Monthly": round(csp_monthly.mean(), 1) if len(csp_monthly) > 0 else 0,
            "Performance Score": round(market_score, 1)
        })
    
    competitor_df = pd.DataFrame(competitor_data)
    
    # Company KPI Dashboard
    st.markdown('<div class="company-highlight">', unsafe_allow_html=True)
    col_company1, col_company2, col_company3, col_company4 = st.columns(4)
    
    with col_company1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Your Total Volume</div>
            <div class="kpi-value">{company_total:,}</div>
            <div class="kpi-change">Rank #{company_rank}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_company2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Market Share</div>
            <div class="kpi-value">{company_market_share:.2f}%</div>
            <div class="kpi-change">vs Market Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_company3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">License Rate</div>
            <div class="kpi-value">{company_license_rate:.1f}%</div>
            <div class="kpi-change {'positive' if company_license_rate > licensed_pct else 'negative'}">
                vs Market Avg: {licensed_pct:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_company4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Growth Rate</div>
            <div class="kpi-value">{company_growth_rate:.1f}%</div>
            <div class="kpi-change">{company_trend} Period-over-Period</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Competitive Benchmarking Tables
    st.markdown('<div class="section-subtitle">📊 Competitive Benchmarking Tables</div>', unsafe_allow_html=True)
    
    col_table1, col_table2 = st.columns(2)
    
    with col_table1:
        st.markdown("**📈 Volume & Market Share Comparison**")
        
        display_volume = pd.DataFrame({
            "CSP": [company_name] + competitor_df["CSP"].tolist(),
            "Volume": [company_total] + competitor_df["Volume"].tolist(),
            "Market Share": [f"{company_market_share:.2f}%"] + [f"{x:.2f}%" for x in competitor_df["Market Share (%)"]],
            "Rank": [f"#{company_rank}"] + [f"#{i+1}" for i in range(len(competitor_df))]
        })
        
        display_volume["VolumeNum"] = display_volume["Volume"]
        display_volume = display_volume.sort_values("VolumeNum", ascending=False).drop(columns=["VolumeNum"])
        
        def highlight_company(row):
            if row["CSP"] == company_name:
                return ['background-color: rgba(168, 85, 247, 0.1); font-weight: 600'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            display_volume.style.apply(highlight_company, axis=1),
            use_container_width=True,
            hide_index=True
        )
    
    with col_table2:
        st.markdown("**🚀 Entity Type & Performance Comparison**")
        
        display_growth = pd.DataFrame({
            "CSP": [company_name] + competitor_df["CSP"].tolist(),
            "SPV (%)": [f"{company_spv_pct:.1f}%"] + [f"{x:.1f}%" for x in competitor_df["SPV (%)"]],
            "Foundation (%)": [f"{company_foundation_pct:.1f}%"] + [f"{x:.1f}%" for x in competitor_df["Foundation (%)"]],
            "License Rate": [f"{company_license_rate:.1f}%"] + [f"{x:.1f}%" for x in competitor_df["License Rate (%)"]],
            "Performance": [f"{calculate_performance_score(company_market_share, company_spv_pct, company_foundation_pct, company_license_rate):.1f}"] + [f"{x:.1f}" for x in competitor_df["Performance Score"]]
        })
        
        st.dataframe(
            display_growth.style.apply(highlight_company, axis=1),
            use_container_width=True,
            hide_index=True
        )
    
    # Monthly Trend Chart
    st.markdown('<div class="section-subtitle">📈 Monthly Performance Trend</div>', unsafe_allow_html=True)
    
    fig_company_trend = go.Figure()
    
    fig_company_trend.add_trace(go.Scatter(
        x=company_monthly.index,
        y=company_monthly.values,
        mode="lines+markers",
        name=f"{company_name}",
        line=dict(width=3, color=DESIGN_SYSTEM["colors"]["accent_purple"]),
        marker=dict(size=8)
    ))
    
    market_monthly = filtered_df.groupby("Year_Month").size()
    market_avg = market_monthly / active_csps
    
    fig_company_trend.add_trace(go.Scatter(
        x=market_avg.index,
        y=market_avg.values,
        mode="lines",
        name="Market Average per CSP",
        line=dict(width=2, dash="dash", color=DESIGN_SYSTEM["colors"]["text_muted"]),
        opacity=0.7
    ))
    
    fig_company_trend.update_layout(
        title=f"Monthly Performance: {company_name} vs Market Average",
        height=400,
        plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
        paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
        font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
        xaxis=dict(title="Month", gridcolor=DESIGN_SYSTEM["colors"]["border"]),
        yaxis=dict(title="Monthly Incorporations", gridcolor=DESIGN_SYSTEM["colors"]["border"]),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_company_trend, use_container_width=True)
    
    # Metric Cards with Market Benchmarking
    st.markdown('<div class="section-subtitle">🎯 Key Performance Metrics</div>', unsafe_allow_html=True)
    
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    
    with col_metric1:
        market_position = "Leader" if company_rank == 1 else "Top Tier" if company_rank <= 3 else "Middle Tier" if company_rank <= 10 else "Growth Stage"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-title">🏆 Market Position</div>
            <div class="metric-value">{market_position}</div>
            <div class="metric-label">Rank #{company_rank} of {active_csps}</div>
            <div class="metric-delta {'positive' if company_rank <= 10 else 'negative'}">
                {"Industry Leader" if company_rank == 1 else "Top 10" if company_rank <= 10 else "Outside Top 10"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metric2:
        growth_performance = "High Growth" if company_growth_rate > 20 else "Moderate Growth" if company_growth_rate > 0 else "Declining"
        growth_color = "positive" if company_growth_rate > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-title">🚀 Growth Performance</div>
            <div class="metric-value">{company_growth_rate:+.1f}%</div>
            <div class="metric-label">Period-over-Period</div>
            <div class="metric-delta {growth_color}">
                {growth_performance}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metric3:
        compliance_status = "Excellent" if company_license_rate > 95 else "Good" if company_license_rate > 85 else "Needs Attention"
        compliance_color = "positive" if company_license_rate > 90 else "negative" if company_license_rate < 80 else ""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-title">✅ License Compliance</div>
            <div class="metric-value">{company_license_rate:.1f}%</div>
            <div class="metric-label">Active License Rate</div>
            <div class="metric-delta {'positive' if company_license_rate > licensed_pct else 'negative'}">
                {"Above" if company_license_rate > licensed_pct else "Below"} Market Avg ({licensed_pct:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Strategic Recommendations
    st.markdown('<div class="section-subtitle">💡 Strategic Recommendations</div>', unsafe_allow_html=True)
    
    recommendations = []
    
    if company_rank > 10:
        recommendations.append("🔴 **Volume Growth**: Significant opportunity to increase incorporation volume. Consider marketing expansion, service diversification, or competitive pricing strategies.")
    elif company_rank > 5:
        recommendations.append("🟡 **Market Expansion**: Moderate growth potential. Focus on specific entity types or market segments where you can gain share.")
    else:
        recommendations.append("🟢 **Market Leadership**: Maintain current market position through continued excellence and service innovation.")
    
    if company_growth_rate < 0:
        recommendations.append("🔴 **Negative Growth**: Immediate attention required. Analyze market trends, competitor strategies, and operational efficiency.")
    elif company_growth_rate < market_avg.mean():
        recommendations.append("🟡 **Growth Opportunity**: Below-market growth rate. Investigate barriers to growth and competitive positioning.")
    else:
        recommendations.append("🟢 **Strong Growth**: Above-market growth momentum. Continue current strategies and consider scaling operations.")
    
    if company_license_rate < licensed_pct:
        recommendations.append("🔴 **License Compliance**: Below-market license retention rate. Implement enhanced compliance protocols and client screening processes.")
    elif company_license_rate < 95:
        recommendations.append("🟡 **Compliance Monitoring**: Monitor license status trends and implement proactive compliance measures.")
    else:
        recommendations.append("🟢 **Excellent Compliance**: Strong license retention. Maintain current compliance standards.")
    
    if company_market_share < 1:
        recommendations.append("🔴 **Market Share**: Very low market penetration. Consider aggressive growth strategies or niche specialization.")
    elif company_market_share < 5:
        recommendations.append("🟡 **Share Building**: Focus on targeted growth to reach top-tier market position.")
    else:
        recommendations.append("🟢 **Strong Position**: Solid market share. Focus on maintaining and selectively expanding share.")
    
    for rec in recommendations:
        st.markdown(f"- {rec}")
    
    # Enhanced HTML Report with Fixed-Rate Scoring and Charts
    st.markdown('<div class="section-subtitle">📥 Export Company Report</div>', unsafe_allow_html=True)
    
    def generate_market_based_company_report():
        """Generate company benchmarking report with fixed-rate scoring (0.46/SPV, 0.54/Foundation) and charts"""

        # Fixed point values
        SPV_POINTS = 0.46
        FOUNDATION_POINTS = 0.54

        # Calculate competitor scores using fixed rates
        competitor_scores_report = []
        for csp in top_5_csps.index:
            csp_data = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]
            spv_cnt = csp_data[csp_data["Entity_Subtype"].str.contains("Special Purpose Vehicle|Special purpose vehicle", case=False, na=False)].shape[0]
            fnd_cnt = csp_data[csp_data["Entity_Subtype"].str.contains("Foundation", case=False, na=False)].shape[0]
            spv_score = spv_cnt * SPV_POINTS
            fnd_score = fnd_cnt * FOUNDATION_POINTS
            total_score = spv_score + fnd_score
            competitor_scores_report.append({
                "CSP": csp,
                "SPV Count": spv_cnt,
                "Foundation Count": fnd_cnt,
                "SPV Score": spv_score,
                "Foundation Score": fnd_score,
                "Total Score": total_score
            })

        # Company scores (fixed)
        company_spv_score = company_spv_count * SPV_POINTS
        company_fnd_score = company_foundation_count * FOUNDATION_POINTS
        company_total_score = company_spv_score + company_fnd_score
        company_score = {
            "spv_score": company_spv_score,
            "foundation_score": company_fnd_score,
            "total_score": company_total_score,
            "point_per_spv": SPV_POINTS,
            "point_per_foundation": FOUNDATION_POINTS
        }

        # Prepare data for charts (company + top competitors)
        all_competitors = competitor_scores_report[:9]  # show top 9 + company = 10 bars
        chart_csps = [company_name] + [comp["CSP"] for comp in all_competitors]
        chart_spv_scores = [company_spv_score] + [comp["SPV Score"] for comp in all_competitors]
        chart_fnd_scores = [company_fnd_score] + [comp["Foundation Score"] for comp in all_competitors]
        chart_total_scores = [company_total_score] + [comp["Total Score"] for comp in all_competitors]
        chart_spv_counts = [company_spv_count] + [comp["SPV Count"] for comp in all_competitors]
        chart_fnd_counts = [company_foundation_count] + [comp["Foundation Count"] for comp in all_competitors]

        import json
        labels_json = json.dumps(chart_csps)
        spv_scores_json = json.dumps(chart_spv_scores)
        fnd_scores_json = json.dumps(chart_fnd_scores)
        total_scores_json = json.dumps(chart_total_scores)
        spv_counts_json = json.dumps(chart_spv_counts)
        fnd_counts_json = json.dumps(chart_fnd_counts)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{company_name} – Fixed‑Rate Benchmarking Report</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background: #f9f9f9;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: #fff;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #0b0f14 0%, #1f2933 100%);
                    color: #fff;
                    padding: 30px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
                .header p {{ font-size: 0.95em; opacity: 0.9; }}
                h2 {{
                    color: #0b0f14;
                    border-bottom: 3px solid #60a5fa;
                    padding-bottom: 10px;
                    margin-top: 30px;
                    margin-bottom: 20px;
                }}
                h3 {{ color: #1f2933; margin-top: 20px; margin-bottom: 15px; }}
                .kpi-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin: 20px 0;
                }}
                .kpi-item {{
                    background: linear-gradient(135deg, #f5f5f5 0%, #f9f9f9 100%);
                    padding: 20px;
                    border-left: 4px solid #60a5fa;
                    border-radius: 8px;
                    text-align: center;
                }}
                .kpi-label {{ font-size: 0.85em; color: #666; text-transform: uppercase; font-weight: 600; margin-bottom: 10px; }}
                .kpi-value {{ font-size: 2em; font-weight: 700; color: #0b0f14; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                th {{
                    background: linear-gradient(135deg, #0b0f14 0%, #1f2933 100%);
                    color: #fff;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
                tr:nth-child(even) {{ background: #f9f9f9; }}
                tr:hover {{ background: #f0f7ff; }}
                .company-row {{ background: #e3f2fd !important; font-weight: 600; }}
                .insight-section {{
                    background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
                    border-left: 4px solid #60a5fa;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                }}
                .insight-title {{ color: #0b0f14; font-weight: 700; margin-bottom: 10px; font-size: 1.1em; }}
                .benchmark-tool {{
                    background: linear-gradient(135deg, #f3f0ff 0%, #f0f7ff 100%);
                    border: 2px solid #a855f7;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .benchmark-tool-title {{ color: #a855f7; font-weight: 700; margin-bottom: 15px; font-size: 1.1em; }}
                .score-badge {{
                    display: inline-block;
                    background: #a855f7;
                    color: #fff;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: 600;
                    margin: 2px;
                    font-size: 0.9em;
                }}
                .score-badge.high {{ background: #22c55e; }}
                .score-badge.medium {{ background: #f97316; }}
                .score-badge.low {{ background: #ef4444; }}
                .comparison-bar {{
                    background: #eee;
                    border-radius: 4px;
                    overflow: hidden;
                    height: 24px;
                    margin: 10px 0;
                }}
                .comparison-bar-fill {{
                    background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #fff;
                    font-weight: 600;
                    font-size: 0.85em;
                }}
                .footer {{ text-align: center; color: #999; font-size: 0.85em; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }}
                .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
                .chart-wrap {{
                    background: #f8faff;
                    border: 1px solid #dde6f0;
                    border-radius: 10px;
                    padding: 20px 24px;
                    margin: 20px 0;
                }}
                .score-breakdown {{ background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%); padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .score-component {{ display: flex; justify-content: space-between; margin: 8px 0; padding: 8px; background: white; border-radius: 4px; }}
                ul {{ margin-left: 20px; line-height: 1.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header -->
                <div class="header">
                    <h1>{company_name}</h1>
                    <p>Fixed‑Rate Benchmarking & Competitive Intelligence Report</p>
                    <p style="font-size: 0.9em; margin-top: 15px;">
                        Report Generated: {datetime.now().strftime("%d %b %Y, %H:%M")} | 
                        Analysis Period: {start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}
                    </p>
                </div>

                <!-- Executive Summary -->
                <h2>Executive Summary</h2>
                <p>This report evaluates {company_name}'s performance using a <strong>fixed‑rate scoring model</strong>: every Special Purpose Vehicle (SPV) contributes exactly <strong>0.46 points</strong> and every Foundation contributes exactly <strong>0.54 points</strong>. This transparent, market‑independent scoring allows direct comparison of entity portfolios and predictable growth planning.</p>

                <div class="insight-section">
                    <div class="insight-title">Key Performance Metrics</div>
                    <div class="two-column">
                        <div>
                            <p><strong>Market Position:</strong> Rank #{company_rank} of {active_csps}</p>
                            <p><strong>Total Volume:</strong> {company_total:,} entities</p>
                            <p><strong>Market Share:</strong> {company_market_share:.2f}%</p>
                        </div>
                        <div>
                            <p><strong>SPV Count:</strong> {company_spv_count:,}</p>
                            <p><strong>Foundation Count:</strong> {company_foundation_count:,}</p>
                            <p><strong>License Rate (info only):</strong> {company_license_rate:.1f}%</p>
                        </div>
                    </div>
                </div>

                <!-- Scoring Methodology -->
                <h2>Scoring Methodology (Fixed Rate)</h2>
                <div class="scoring-explanation" style="background:#f8f9fa; border-left:4px solid #60a5fa; padding:15px; margin:20px 0; border-radius:6px;">
                    <h3>Fixed‑Rate Scoring System</h3>
                    <p><strong>Total Score = SPV Count × 0.46 + Foundation Count × 0.54</strong><br>
                    There is no maximum score – every entity adds a predictable number of points.</p>
                    <p><strong>Point Values:</strong></p>
                    <ul>
                        <li>Special Purpose Vehicle (SPV) → <strong>0.46 points</strong> each</li>
                        <li>Foundation → <strong>0.54 points</strong> each</li>
                    </ul>
                    <p><strong>Note:</strong> License status is reported for information only and does not affect the performance score.</p>
                </div>

                <!-- Your Score Breakdown -->
                <h2>Your Performance Score Breakdown</h2>
                <div class="score-breakdown">
                    <div class="score-component">
                        <span><strong>SPV Points:</strong> {company_spv_count:,} SPVs × 0.46</span>
                        <span><strong>{company_spv_score:.2f} points</strong></span>
                    </div>
                    <div class="score-component">
                        <span><strong>Foundation Points:</strong> {company_foundation_count:,} Foundations × 0.54</span>
                        <span><strong>{company_fnd_score:.2f} points</strong></span>
                    </div>
                    <div class="score-component" style="background:#e3f2fd; font-weight:bold; font-size:1.1em;">
                        <span><strong>TOTAL PERFORMANCE SCORE:</strong></span>
                        <span><strong>{company_total_score:.2f} points</strong></span>
                    </div>
                </div>

                <!-- Visual Charts -->
                <h2>Visual Benchmarking</h2>

                <!-- Chart 1: Stacked SPV vs Foundation Scores -->
                <div class="chart-wrap">
                    <h3>Score Composition – SPV (0.46) vs Foundation (0.54)</h3>
                    <canvas id="stackedScoreChart" height="100"></canvas>
                </div>

                <!-- Chart 2: Total Score Horizontal Bar -->
                <div class="chart-wrap">
                    <h3>Total Performance Score Comparison</h3>
                    <canvas id="totalScoreChart" height="120"></canvas>
                </div>

                <!-- Chart 3: Entity Counts (Grouped Bar) -->
                <div class="chart-wrap">
                    <h3>Entity Volume – SPV vs Foundation</h3>
                    <canvas id="entityCountChart" height="100"></canvas>
                </div>

                <script>
                    const labels = {labels_json};
                    const spvScores = {spv_scores_json};
                    const fndScores = {fnd_scores_json};
                    const totalScores = {total_scores_json};
                    const spvCounts = {spv_counts_json};
                    const fndCounts = {fnd_counts_json};

                    // Stacked bar chart (SPV + Foundation)
                    new Chart(document.getElementById('stackedScoreChart'), {{
                        type: 'bar',
                        data: {{
                            labels: labels,
                            datasets: [
                                {{ label: 'SPV Score (0.46/ea)', data: spvScores, backgroundColor: 'rgba(96,165,250,0.85)', stack: 'stack' }},
                                {{ label: 'Foundation Score (0.54/ea)', data: fndScores, backgroundColor: 'rgba(168,85,247,0.85)', stack: 'stack' }}
                            ]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{ legend: {{ position: 'top' }}, tooltip: {{ mode: 'index' }} }},
                            scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, title: {{ display: true, text: 'Score' }} }} }}
                        }}
                    }});

                    // Horizontal bar for Total Score
                    new Chart(document.getElementById('totalScoreChart'), {{
                        type: 'bar',
                        data: {{
                            labels: labels,
                            datasets: [{{
                                label: 'Total Score',
                                data: totalScores,
                                backgroundColor: totalScores.map(s => s > 70 ? '#22c55e' : (s > 40 ? '#f97316' : '#ef4444'))
                            }}]
                        }},
                        options: {{
                            indexAxis: 'y',
                            responsive: true,
                            plugins: {{ legend: {{ display: false }}, tooltip: {{ callbacks: {{ label: ctx => ` Score: ${{ctx.raw.toFixed(2)}}` }} }} }},
                            scales: {{ x: {{ title: {{ display: true, text: 'Total Score' }} }} }}
                        }}
                    }});

                    // Grouped bar for SPV and Foundation counts
                    new Chart(document.getElementById('entityCountChart'), {{
                        type: 'bar',
                        data: {{
                            labels: labels,
                            datasets: [
                                {{ label: 'SPV Count', data: spvCounts, backgroundColor: 'rgba(96,165,250,0.85)' }},
                                {{ label: 'Foundation Count', data: fndCounts, backgroundColor: 'rgba(168,85,247,0.85)' }}
                            ]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{ legend: {{ position: 'top' }} }},
                            scales: {{ y: {{ title: {{ display: true, text: 'Entity Count' }} }} }}
                        }}
                    }});
                </script>

                <!-- Competitive Benchmarking Table -->
                <h2>Competitive Benchmarking Analysis</h2>
                <div class="benchmark-tool">
                    <div class="benchmark-tool-title">📊 Top Competitors – Performance Scores</div>
                    <table>
                        <thead>
                            <tr><th>Company</th><th>SPV Count</th><th>Foundation Count</th><th>SPV Score</th><th>Foundation Score</th><th>Total Score</th></tr>
                        </thead>
                        <tbody>
                            <tr class="company-row">
                                <td><strong>{company_name}</strong></td>
                                <td>{company_spv_count:,}</td>
                                <td>{company_foundation_count:,}</td>
                                <td>{company_spv_score:.1f}</td>
                                <td>{company_fnd_score:.1f}</td>
                                <td><strong>{company_total_score:.1f}</strong></td>
                            </tr>
        """
        # Add competitor rows
        for comp in competitor_scores_report:
            score = comp['Total Score']
            score_class = 'high' if score > 70 else 'medium' if score > 40 else 'low'
            html_content += f"""
                            <tr>
                                <td>{comp['CSP']}</td>
                                <td>{comp['SPV Count']:,}</td>
                                <td>{comp['Foundation Count']:,}</td>
                                <td>{comp['SPV Score']:.1f}</td>
                                <td>{comp['Foundation Score']:.1f}</td>
                                <td><span class="score-badge {score_class}">{comp['Total Score']:.1f}</span></td>
                            </tr>
            """
        html_content += f"""
                        </tbody>
                    </table>
                </div>

                <!-- Strategic Analysis -->
                <h2>Strategic Analysis & Recommendations</h2>
                <div class="insight-section">
                    <div class="insight-title">Market Position & Growth Impact</div>
                    <p>Your company holds <strong>{company_spv_count:,} SPVs</strong> and <strong>{company_foundation_count:,} Foundations</strong>, representing <strong>{company_market_share:.2f}%</strong> of the total market volume. Your fixed‑rate performance score is <strong>{company_total_score:.2f}</strong>.</p>
                    <ul>
                        <li><strong>SPV growth:</strong> Each additional SPV adds exactly <strong>0.46 points</strong>.</li>
                        <li><strong>Foundation growth:</strong> Each additional Foundation adds exactly <strong>0.54 points</strong>.</li>
                        <li><strong>Foundation advantage:</strong> Foundations are worth ~17% more per entity than SPVs.</li>
                    </ul>
                    <p><strong>To improve your ranking:</strong> Focus on acquiring Foundations (higher point yield) or increase SPV volume if Foundations are less available in your target market.</p>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p><strong>CSP Market Intelligence Platform </strong></p>
                    <p>Performance Score = SPV×0.46 + Foundation×0.54 &nbsp;|&nbsp; License status not scored</p>
                    <p>Report for {company_name} | {datetime.now().strftime("%d %b %Y")}</p>
                    <p>This report is confidential and prepared for authorized recipients only.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    company_report_html = generate_market_based_company_report()
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        st.download_button(
            label="📊 Download Fixed‑Rate Benchmarking Report",
            data=company_report_html,
            file_name=f"{company_name.replace(' ', '_')}_Fixed_Rate_Benchmark_{start_date.strftime('%Y%m%d')}.html",
            mime="text/html",
            help="HTML report with fixed 0.46/0.54 scoring and interactive charts"
        )
    
    with col_export2:
        company_data_export = company_data.to_csv(index=False)
        st.download_button(
            label="📈 Download Company Raw Data",
            data=company_data_export,
            file_name=f"{company_name.replace(' ', '_')}_Raw_Data_{start_date.strftime('%Y%m%d')}.csv",
            mime="text/csv",
            help="Raw data for your company's incorporations"
        )

st.markdown("---")

# ================================================================================
# SECTION 2: MARKET OVERVIEW - ENHANCED WITH BENCHMARKING TOOLS
# ================================================================================

st.markdown('<div class="section-title">📈 Market Overview & Benchmarking</div>', unsafe_allow_html=True)

# Core metrics (recomputed after filters)
total_incorporations = len(filtered_df)
active_csps = filtered_df["Corporate_Service_Provider"].nunique()
days_analyzed = (end_date - start_date).days + 1
months_count = max(filtered_df["Year_Month"].nunique(), 1)
avg_monthly = round(total_incorporations / months_count)

license_breakdown = filtered_df["License_Status"].value_counts()
licensed_count = license_breakdown.get("Licensed", 0)
cancelled_count = license_breakdown.get("License cancelled", 0)
licensed_pct = round(licensed_count / total_incorporations * 100, 1) if total_incorporations > 0 else 0

entity_breakdown = filtered_df["Entity_Subtype"].value_counts()
dominant_entity = entity_breakdown.index[0] if len(entity_breakdown) > 0 else "N/A"
dominant_entity_share = round((entity_breakdown.iloc[0] / total_incorporations * 100), 1) if len(entity_breakdown) > 0 else 0

csp_counts = filtered_df["Corporate_Service_Provider"].value_counts()
top_csp = csp_counts.index[0] if len(csp_counts) > 0 else "N/A"
top_csp_share = round((csp_counts.iloc[0] / total_incorporations * 100), 1) if len(csp_counts) > 0 else 0
top3_share = round(csp_counts.head(3).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 3 else 0
top10_share = round(csp_counts.head(10).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 10 else 0
hhi_index = sum((csp_counts / total_incorporations) ** 2) * 10000

# Market KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Incorporations</div>
        <div class="kpi-value">{total_incorporations:,}</div>
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
        <div class="kpi-label">Licensed Entities</div>
        <div class="kpi-value">{licensed_count:,}</div>
        <div class="kpi-change positive">{licensed_pct}% Active</div>
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
        <div class="insight-title">📊 Market Concentration</div>
        <div class="insight-text">
        <b>HHI Index:</b> {hhi_index:.0f} | <b>Top-3 Share:</b> {top3_share}% | <b>Top-10 Share:</b> {top10_share}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🏢 License Status Distribution</div>
        <div class="insight-text">
        <b>Licensed:</b> {licensed_count:,} ({licensed_pct}%) | <b>Cancelled:</b> {cancelled_count:,} ({100-licensed_pct}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# SECTION 3: LICENSE STATUS ANALYTICS
# ================================================================================

st.markdown('<div class="section-title">🔐 License Status Analytics</div>', unsafe_allow_html=True)

license_monthly = filtered_df.groupby(["Year_Month", "License_Status"]).size().unstack(fill_value=0)

license_colors = {
    "Licensed": "#22c55e",
    "Cancelled": "#ef4444"
}

license_summary_data = []
for status, count in license_breakdown.items():
    pct = (count / total_incorporations * 100) if total_incorporations > 0 else 0
    color = license_colors.get(status, "#ef4444")
    
    license_summary_data.append({
        "Status": status,
        "Count": count,
        "Share": pct,
        "Color": color
    })

df_license = pd.DataFrame(license_summary_data)

st.markdown('<div class="section-subtitle">📋 License Status Summary</div>', unsafe_allow_html=True)

fig = px.bar(
    df_license,
    x="Count",
    y="Status",
    orientation="h",
    text=df_license["Count"].map("{:,}".format),
    color="Status",
    color_discrete_map=license_colors
)

fig.update_traces(
    textposition='inside',
    insidetextanchor='middle',
    cliponaxis=False
)

max_count = df_license['Count'].max()
for i, row in df_license.iterrows():
    fig.add_annotation(
        x=row['Count'] + max_count * 0.03,
        y=row['Status'],
        text=f"{row['Share']:.1f}%",
        showarrow=False,
        font=dict(color='white', size=12),
        xanchor='left',
        yanchor='middle'
    )

fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=100, r=60, t=40, b=40),
    height=250,
    showlegend=False,
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='white', size=14)
)

st.plotly_chart(fig, use_container_width=True)

# License status by CSP table
st.markdown('<div class="section-subtitle">🏢 License Status by Top CSPs</div>', unsafe_allow_html=True)

license_by_csp = filtered_df.groupby(["Corporate_Service_Provider", "License_Status"]).size().unstack(fill_value=0)
license_by_csp["Total"] = license_by_csp.sum(axis=1)
license_by_csp = license_by_csp.sort_values("Total", ascending=False).head(10)

csp_license_data = []
for csp in license_by_csp.index:
    total = int(license_by_csp.loc[csp, "Total"])
    licensed = int(license_by_csp.loc[csp, "Licensed"]) if "Licensed" in license_by_csp.columns else 0
    cancelled = int(license_by_csp.loc[csp, "License cancelled"]) if "License cancelled" in license_by_csp.columns else 0
    
    licensed_pct_csp = (licensed / total * 100) if total > 0 else 0
    cancelled_pct_csp = (cancelled / total * 100) if total > 0 else 0
    
    csp_license_data.append({
        "CSP": csp,
        "Total": total,
        "Licensed": licensed,
        "Licensed %": licensed_pct_csp,
        "Cancelled": cancelled,
        "Cancelled %": cancelled_pct_csp
    })

csp_license_df = pd.DataFrame(csp_license_data)

st.dataframe(
    csp_license_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "CSP": st.column_config.TextColumn("Corporate Service Provider", width="large"),
        "Total": st.column_config.NumberColumn("Total", format="%d"),
        "Licensed": st.column_config.NumberColumn("✅ Licensed", format="%d"),
        "Licensed %": st.column_config.ProgressColumn(
            "Licensed %",
            help="Percentage of entities with active licenses",
            format="%.1f%%",
            min_value=0,
            max_value=100
        ),
        "Cancelled": st.column_config.NumberColumn("❌ Cancelled", format="%d"),
        "Cancelled %": st.column_config.ProgressColumn(
            "Cancelled %",
            help="Percentage of entities with cancelled licenses",
            format="%.1f%%",
            min_value=0,
            max_value=100
        )
    }
)

# License status trends
if len(license_monthly) > 0:
    fig_license_trends = go.Figure()
    
    for status in license_monthly.columns:
        fig_license_trends.add_trace(go.Scatter(
            x=license_monthly.index,
            y=license_monthly[status],
            mode="lines+markers",
            name=status,
            line=dict(width=2.5),
            marker=dict(size=6)
        ))
    
    fig_license_trends.update_layout(
        title="License Status Trends Over Time",
        height=400,
        plot_bgcolor=DESIGN_SYSTEM["colors"]["bg_secondary"],
        paper_bgcolor=DESIGN_SYSTEM["colors"]["bg_primary"],
        font=dict(color=DESIGN_SYSTEM["colors"]["text_secondary"], family=DESIGN_SYSTEM['typography']['font_family']),
        xaxis=dict(
            title="Month",
            gridcolor=DESIGN_SYSTEM["colors"]["border"],
            showgrid=True
        ),
        yaxis=dict(
            title="Count",
            gridcolor=DESIGN_SYSTEM["colors"]["border"],
            showgrid=True
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_license_trends, use_container_width=True)

# ================================================================================
# SECTION 4: GROWTH TRENDS & CAGR ANALYSIS
# ================================================================================

st.markdown('<div class="section-title">📊 Growth Trends & CAGR Analysis</div>', unsafe_allow_html=True)

monthly_summary = filtered_df.groupby("Year_Month").size().reset_index(name="Count")
monthly_csp = filtered_df.groupby(["Year_Month", "Corporate_Service_Provider"]).size().reset_index(name="Count")

cagr_analysis = []
for csp in csp_counts.head(10).index:
    csp_data = monthly_csp[monthly_csp["Corporate_Service_Provider"] == csp].sort_values("Year_Month")
    
    if len(csp_data) >= 2:
        csp_dates = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]["Incorporation_Date"]
        
        if len(csp_dates) > 0:
            earliest_date = csp_dates.min()
            latest_date = csp_dates.max()
            
            first_month = csp_data.iloc[0]["Count"]
            last_month = csp_data.iloc[-1]["Count"]
            
            cagr = calculate_cagr_from_dates(
                start_value=first_month,
                end_value=last_month,
                start_date=earliest_date,
                end_date=latest_date
            )
            
            total_csp = csp_data["Count"].sum()
            avg_monthly_csp = csp_data["Count"].mean()
            
            cagr_analysis.append({
                "CSP": csp,
                "Recent Month": last_month,
                "Total (Period)": total_csp,
                "CAGR": cagr,
                "Avg Monthly": round(avg_monthly_csp, 1)
            })

if cagr_analysis:
    cagr_df = pd.DataFrame(cagr_analysis).sort_values("CAGR", ascending=False)
else:
    cagr_df = pd.DataFrame(columns=["CSP", "Recent Month", "Total (Period)", "CAGR", "Avg Monthly"])

# Growth trends chart
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

# CAGR Analysis table
st.markdown('<div class="section-subtitle">🚀 High-Growth CSPs (Top 10 by CAGR)</div>', unsafe_allow_html=True)

if not cagr_df.empty:
    display_df = cagr_df.copy()
    display_df['CAGR'] = display_df['CAGR'].apply(lambda x: f"{x:+.1f}%")
    display_df['Recent Month'] = display_df['Recent Month'].apply(lambda x: f"{x:,}")
    display_df['Total (Period)'] = display_df['Total (Period)'].apply(lambda x: f"{x:,}")
    
    trends = []
    for cagr in cagr_df['CAGR']:
        if cagr > 20:
            trends.append("🚀")
        elif cagr > 10:
            trends.append("📈")
        elif cagr > 0:
            trends.append("↗️")
        elif cagr < 0:
            trends.append("📉")
        else:
            trends.append("➡️")
    
    display_df['Trend'] = trends
    display_df = display_df[['CSP', 'Recent Month', 'Total (Period)', 'Avg Monthly', 'CAGR', 'Trend']]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "CSP": st.column_config.TextColumn("Corporate Service Provider", width="large"),
            "Recent Month": st.column_config.TextColumn("Last Month", width="small"),
            "Total (Period)": st.column_config.TextColumn("Total (Period)", width="medium"),
            "Avg Monthly": st.column_config.NumberColumn("Avg Monthly", format="%.1f", width="small"),
            "CAGR": st.column_config.TextColumn("CAGR", help="Compound Annual Growth Rate", width="medium"),
            "Trend": st.column_config.TextColumn("", width="small")
        }
    )
    
    with st.expander("ℹ️ About CAGR (Compound Annual Growth Rate)"):
        st.markdown("""
        **CAGR (Compound Annual Growth Rate)** is the mean annual growth rate of an investment over a specified period.
        
        **Key Points:**
        - More accurate than simple growth rate as it considers compounding
        - Smoothes growth rate over multiple periods
        - Better for comparing growth across different time periods
        - **Formula:** CAGR = (Ending Value / Beginning Value)^(1/Number of Years) - 1
        """)
else:
    st.info("Insufficient data for CAGR analysis. Need at least 2 months of data per CSP.")

# ================================================================================
# SECTION 5: MARKET SHARE & DOMINANCE
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
# SECTION 6: ENTITY TYPE DISTRIBUTION
# ================================================================================

st.markdown('<div class="section-title">🗃️ Entity Type Distribution</div>', unsafe_allow_html=True)

entity_totals = filtered_df["Entity_Subtype"].value_counts()

entity_colors = [
    DESIGN_SYSTEM["colors"]["accent_blue"],
    DESIGN_SYSTEM["colors"]["accent_green"],
    DESIGN_SYSTEM["colors"]["accent_orange"],
    DESIGN_SYSTEM["colors"]["accent_purple"],
    DESIGN_SYSTEM["colors"]["accent_yellow"],
    DESIGN_SYSTEM["colors"]["accent_red"]
]

data_for_plot = []
for idx, (entity_type, count) in enumerate(entity_totals.items()):
    pct = round(count / total_incorporations * 100, 1)
    color = entity_colors[idx % len(entity_colors)]
    data_for_plot.append({
        "Entity Type": entity_type,
        "Count": count,
        "Market Share": pct,
        "Color": color,
        "Count_text": f"{count:,}",
        "Pct_text": f"{pct:.1f}%"
    })

df_plot = pd.DataFrame(data_for_plot)

st.markdown('<div class="section-subtitle">📋 Entity Type Summary</div>', unsafe_allow_html=True)

fig = px.bar(
    df_plot,
    x="Count",
    y="Entity Type",
    orientation="h",
    text="Count_text",
    color="Entity Type",
    color_discrete_sequence=df_plot["Color"].tolist()
)

fig.update_traces(
    texttemplate='%{text}',
    textposition='inside',
    insidetextanchor='start',
    cliponaxis=False
)

max_count = df_plot['Count'].max()
for i, row in df_plot.iterrows():
    fig.add_annotation(
        x=row['Count'] + max_count * 0.02,
        y=row['Entity Type'],
        text=row['Pct_text'],
        showarrow=False,
        font=dict(color='white', size=12),
        xanchor='left',
        yanchor='middle'
    )

fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=100, r=60, t=40, b=40),
    height=400,
    showlegend=False,
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='white', size=14)
)

st.plotly_chart(fig, use_container_width=True)

# Entity type distribution by top CSPs
st.markdown('<div class="section-subtitle">🏢 Entity Type Distribution by Top CSPs</div>', unsafe_allow_html=True)

top_10_csps = csp_counts.head(10).index.tolist()
top_10_df = filtered_df[filtered_df["Corporate_Service_Provider"].isin(top_10_csps)]

entity_by_csp = top_10_df.groupby(["Corporate_Service_Provider", "Entity_Subtype"]).size().unstack(fill_value=0)

csp_entity_data = []
for csp in top_10_csps:
    if csp in entity_by_csp.index:
        csp_entities = entity_by_csp.loc[csp]
        total_csp = csp_entities.sum()
        
        top_entities = csp_entities.sort_values(ascending=False).head(1)
        
        primary_entity = top_entities.index[0] if len(top_entities) > 0 else "N/A"
        primary_pct = (top_entities.iloc[0] / total_csp * 100) if total_csp > 0 else 0
        
        distinct_entities = len(csp_entities[csp_entities > 0])
        
        csp_entity_data.append({
            "CSP": csp,
            "Total": int(total_csp),
            "Primary Type": primary_entity,
            "Primary %": primary_pct,
            "Distinct Types": distinct_entities
        })

csp_entity_df = pd.DataFrame(csp_entity_data)

st.dataframe(
    csp_entity_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "CSP": st.column_config.TextColumn("Corporate Service Provider", width="large"),
        "Total": st.column_config.NumberColumn("Total Entities", format="%d"),
        "Primary Type": st.column_config.TextColumn("Primary Entity Type", width="medium"),
        "Primary %": st.column_config.ProgressColumn(
            "Primary %",
            help="Percentage of this entity type",
            format="%.1f%%",
            min_value=0,
            max_value=100
        ),
        "Distinct Types": st.column_config.NumberColumn("Entity Types Used", format="%d")
    }
)

# ================================================================================
# SECTION 7: CSP RANKINGS WITH BENCHMARK SCORES (FIXED-RATE)
# ================================================================================

st.markdown('<div class="section-title">🏆 CSP Rankings & Benchmark Analysis</div>', unsafe_allow_html=True)

ranking_data = []
for rank, (csp, count) in enumerate(csp_counts.items(), 1):
    share_pct = round(count / total_incorporations * 100, 2)
    
    csp_entities = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]["Entity_Subtype"].value_counts()
    primary_entity = csp_entities.index[0] if len(csp_entities) > 0 else "N/A"
    
    # Entity type breakdown using fixed-rate scoring
    csp_data_ranked = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]
    csp_rank_score = calculate_market_based_score(csp_data_ranked)
    csp_spv = csp_rank_score["spv_count"]
    csp_foundation = csp_rank_score["foundation_count"]
    csp_spv_pct = (csp_spv / count * 100) if count > 0 else 0
    csp_foundation_pct = (csp_foundation / count * 100) if count > 0 else 0
    
    csp_licenses = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]["License_Status"].value_counts()
    license_status_display = []
    if "Licensed" in csp_licenses.index:
        license_status_display.append(f"✅ {csp_licenses['Licensed']}")
    if "License cancelled" in csp_licenses.index:
        license_status_display.append(f"❌ {csp_licenses['License cancelled']}")
    
    csp_monthly = monthly_csp[monthly_csp["Corporate_Service_Provider"] == csp].sort_values("Year_Month")
    csp_dates = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]["Incorporation_Date"]
    
    if len(csp_monthly) >= 2 and len(csp_dates) > 0:
        earliest_date = csp_dates.min()
        latest_date = csp_dates.max()
        
        if len(csp_monthly) >= 2:
            first_month_count = csp_monthly.iloc[0]["Count"]
            last_month_count = csp_monthly.iloc[-1]["Count"]
            
            cagr = calculate_cagr_from_dates(
                start_value=first_month_count,
                end_value=last_month_count,
                start_date=earliest_date,
                end_date=latest_date
            )
        else:
            cagr = 0
    else:
        cagr = 0
    
    ranking_data.append({
        "Rank": rank,
        "CSP": csp,
        "Volume": count,
        "Share (%)": share_pct,
        "SPV Count": csp_spv,
        "Foundation Count": csp_foundation,
        "SPV Score": round(csp_rank_score["spv_score"], 2),
        "Foundation Score": round(csp_rank_score["foundation_score"], 2),
        "Total Score": round(csp_rank_score["total_score"], 2),
        "Primary Type": primary_entity,
        "License Mix": " | ".join(license_status_display),
        "CAGR (%)": round(cagr, 1),
        "Trend": "🚀" if cagr > 20 else "📈" if cagr > 10 else "↗️" if cagr > 0 else "📉"
    })

ranking_df = pd.DataFrame(ranking_data)

st.dataframe(ranking_df, use_container_width=True, hide_index=True)

# ================================================================================
# SECTION 8: ADVANCED ANALYTICS & INSIGHTS
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
        <div class="insight-title">🚀 Growth & CAGR Insights</div>
        <div class="insight-text">
    """, unsafe_allow_html=True)
    
    if not cagr_df.empty:
        avg_cagr = cagr_df["CAGR"].mean()
        max_cagr = cagr_df["CAGR"].max()
        min_cagr = cagr_df["CAGR"].min()
        
        if avg_cagr > 20:
            st.write("🚀 **High Growth Market**: Strong average CAGR indicates expanding market.")
        elif avg_cagr > 10:
            st.write("📈 **Growing Market**: Positive momentum with healthy growth rates.")
        elif avg_cagr > 0:
            st.write("↗️ **Stable Growth**: Moderate but consistent growth across top players.")
        else:
            st.write("📉 **Declining Market**: Negative growth rates require attention.")
        
        st.write(f"**Avg Top 10 CAGR: {avg_cagr:.1f}%** | **Range: {min_cagr:.1f}% to {max_cagr:.1f}%**")
    else:
        st.write("📊 **Growth Analysis**: Insufficient data for CAGR calculation.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================================================================================
# SECTION 9: EXPORT FUNCTIONALITY - ENHANCED MARKET REPORT (FIXED-RATE CHARTS)
# ================================================================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Export & Reporting</div>', unsafe_allow_html=True)

def generate_enhanced_market_report():
    """Generate enhanced market analysis report with fixed-rate scoring and charts"""
    
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    
    # Recalculate totals for report (use current filtered_df)
    total_incorporations = len(filtered_df)
    active_csps = filtered_df["Corporate_Service_Provider"].nunique()
    days_analyzed = (end_date - start_date).days + 1
    months_count = max(filtered_df["Year_Month"].nunique(), 1)
    avg_monthly = round(total_incorporations / months_count)
    
    license_breakdown = filtered_df["License_Status"].value_counts()
    licensed_count = license_breakdown.get("Licensed", 0)
    cancelled_count = license_breakdown.get("License cancelled", 0)
    licensed_pct = round(licensed_count / total_incorporations * 100, 1) if total_incorporations > 0 else 0
    
    entity_breakdown = filtered_df["Entity_Subtype"].value_counts()
    dominant_entity = entity_breakdown.index[0] if len(entity_breakdown) > 0 else "N/A"
    dominant_entity_share = round((entity_breakdown.iloc[0] / total_incorporations * 100), 1) if len(entity_breakdown) > 0 else 0
    
    csp_counts = filtered_df["Corporate_Service_Provider"].value_counts()
    top_csp = csp_counts.index[0] if len(csp_counts) > 0 else "N/A"
    top_csp_share = round((csp_counts.iloc[0] / total_incorporations * 100), 1) if len(csp_counts) > 0 else 0
    top3_share = round(csp_counts.head(3).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 3 else 0
    top10_share = round(csp_counts.head(10).sum() / total_incorporations * 100, 1) if len(csp_counts) >= 10 else 0
    hhi_index = sum((csp_counts / total_incorporations) ** 2) * 10000

    # Build ranking_df with fixed-rate scores for top CSPs
    ranking_data = []
    for rank, (csp, count) in enumerate(csp_counts.head(15).items(), 1):
        csp_data = filtered_df[filtered_df["Corporate_Service_Provider"] == csp]
        score = calculate_market_based_score(csp_data)
        ranking_data.append({
            "Rank": rank,
            "CSP": csp,
            "Volume": count,
            "Share (%)": round(count / total_incorporations * 100, 2),
            "SPV Count": score["spv_count"],
            "Foundation Count": score["foundation_count"],
            "SPV Score": round(score["spv_score"], 2),
            "Foundation Score": round(score["foundation_score"], 2),
            "Total Score": round(score["total_score"], 2)
        })
    ranking_df_report = pd.DataFrame(ranking_data)

    # Prepare chart data for top 15
    top15 = ranking_df_report.head(15)
    chart_labels = [r['CSP'][:22] + '…' if len(r['CSP']) > 22 else r['CSP'] for _, r in top15.iterrows()]
    chart_spv = [r['SPV Score'] for _, r in top15.iterrows()]
    chart_fnd = [r['Foundation Score'] for _, r in top15.iterrows()]
    chart_total = [r['Total Score'] for _, r in top15.iterrows()]
    chart_vol = [r['Volume'] for _, r in top15.iterrows()]
    chart_share = [r['Share (%)'] for _, r in top15.iterrows()]
    chart_spv_cnt = [r['SPV Count'] for _, r in top15.iterrows()]
    chart_fnd_cnt = [r['Foundation Count'] for _, r in top15.iterrows()]

    import json
    j_labels = json.dumps(chart_labels)
    j_spv = json.dumps(chart_spv)
    j_fnd = json.dumps(chart_fnd)
    j_total = json.dumps(chart_total)
    j_vol = json.dumps(chart_vol)
    j_share = json.dumps(chart_share)
    j_spv_cnt = json.dumps(chart_spv_cnt)
    j_fnd_cnt = json.dumps(chart_fnd_cnt)

    ent_labels = json.dumps(list(entity_breakdown.index))
    ent_vals = json.dumps([int(v) for v in entity_breakdown.values])

    lic_labels = json.dumps(list(license_breakdown.index))
    lic_vals = json.dumps([int(v) for v in license_breakdown.values])

    total_market_spv = len(filtered_df[filtered_df["Entity_Subtype"].str.contains("Special Purpose Vehicle|Special purpose vehicle", case=False, na=False)])
    total_market_foundation = len(filtered_df[filtered_df["Entity_Subtype"].str.contains("Foundation", case=False, na=False)])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSP Market Intelligence Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f9f9f9;
                padding: 20px;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: #fff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .cover {{
                background: linear-gradient(135deg, #0b0f14 0%, #1f2933 100%);
                color: #fff;
                padding: 80px 40px;
                text-align: center;
                border-radius: 8px;
                margin-bottom: 40px;
            }}
            .cover h1 {{ font-size: 2.5em; margin-bottom: 20px; font-weight: 700; }}
            .cover p {{ font-size: 1em; opacity: 0.9; margin: 10px 0; }}
            h2 {{
                color: #0b0f14;
                border-bottom: 3px solid #60a5fa;
                padding-bottom: 10px;
                margin-top: 40px;
                margin-bottom: 20px;
            }}
            h3 {{ color: #1f2933; margin-top: 20px; margin-bottom: 15px; }}
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin: 20px 0;
            }}
            .kpi-item {{
                background: linear-gradient(135deg, #f5f5f5 0%, #f9f9f9 100%);
                padding: 20px;
                border-left: 4px solid #60a5fa;
                border-radius: 8px;
                text-align: center;
            }}
            .kpi-label {{ font-size: 0.85em; color: #666; text-transform: uppercase; font-weight: 600; margin-bottom: 10px; }}
            .kpi-value {{ font-size: 2em; font-weight: 700; color: #0b0f14; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            th {{
                background: linear-gradient(135deg, #0b0f14 0%, #1f2933 100%);
                color: #fff;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }}
            td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
            tr:nth-child(even) {{ background: #f9f9f9; }}
            tr:hover {{ background: #f0f7ff; }}
            .insight-section {{
                background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
                border-left: 4px solid #60a5fa;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .insight-title {{ color: #0b0f14; font-weight: 700; margin-bottom: 10px; font-size: 1.1em; }}
            .benchmark-widget {{
                background: linear-gradient(135deg, #f3f0ff 0%, #f0f7ff 100%);
                border: 2px solid #a855f7;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }}
            .benchmark-widget-title {{ color: #a855f7; font-weight: 700; margin-bottom: 15px; font-size: 1.1em; }}
            .score-badge {{
                display: inline-block;
                background: #a855f7;
                color: #fff;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                margin: 2px;
                font-size: 0.9em;
            }}
            .score-badge.high {{ background: #22c55e; }}
            .score-badge.medium {{ background: #f97316; }}
            .score-badge.low {{ background: #ef4444; }}
            .comparison-bar {{
                background: #eee;
                border-radius: 4px;
                overflow: hidden;
                height: 24px;
                margin: 10px 0;
                display: flex;
                align-items: center;
            }}
            .comparison-bar-fill {{
                background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-weight: 600;
                font-size: 0.85em;
                transition: width 0.3s ease;
            }}
            .footer {{ text-align: center; color: #999; font-size: 0.85em; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }}
            .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
            ul {{ margin-left: 20px; line-height: 1.8; }}
            @media print {{
                body {{ padding: 0; }}
                .container {{ box-shadow: none; padding: 20px; }}
                .cover {{ page-break-after: always; }}
            }}
            .chart-wrap {{
                background: #f8faff;
                border: 1px solid #dde6f0;
                border-radius: 10px;
                padding: 20px 24px;
                margin: 20px 0;
            }}
            .chart-wrap h3 {{
                margin-top: 0;
                margin-bottom: 12px;
                color: #1a1a2e;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="cover">
                <h1>CSP Market Intelligence</h1>
                <p>Comprehensive Market Analysis & Benchmarking Report (v5.0 – Fixed-Rate Scoring)</p>
                <p style="font-size: 0.95em; margin-top: 30px;">
                    Generated: {now}<br>
                    Analysis Period: {start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}
                </p>
            </div>
            
            <h2>Executive Summary</h2>
            <p>This comprehensive market analysis covers {total_incorporations:,} incorporations across {active_csps} active Corporate Service Providers (CSPs) during the analysis period. The report uses a <strong>fixed-rate scoring system</strong>: each SPV = 0.46 points, each Foundation = 0.54 points. License status is reported for information only and is not scored.</p>
            
            <div class="insight-section">
                <div class="insight-title">Market Highlights & Strategic Overview</div>
                <ul>
                    <li><strong>Market Leader:</strong> {top_csp} with {top_csp_share}% market share</li>
                    <li><strong>Top-3 Concentration:</strong> {top3_share}% of total market</li>
                    <li><strong>Top-10 Concentration:</strong> {top10_share}% of total market</li>
                    <li><strong>License Compliance:</strong> {licensed_pct}% of entities maintain active licenses (informational)</li>
                    <li><strong>Entity Type Distribution:</strong> Primary focus on {dominant_entity} ({dominant_entity_share}%)</li>
                    <li><strong>Market Structure:</strong> {'Highly concentrated (HHI: ' + str(int(hhi_index)) + ')' if hhi_index > 2500 else 'Moderately concentrated (HHI: ' + str(int(hhi_index)) + ')' if hhi_index > 1500 else 'Competitive (HHI: ' + str(int(hhi_index)) + ')'}</li>
                    <li><strong>Average Monthly Volume:</strong> {avg_monthly:,} incorporations</li>
                    <li><strong>Analysis Timeframe:</strong> {days_analyzed} days across {months_count} months</li>
                </ul>
            </div>
            
            <div class="kpi-grid">
                <div class="kpi-item"><div class="kpi-label">Total Incorporations</div><div class="kpi-value">{total_incorporations:,}</div></div>
                <div class="kpi-item"><div class="kpi-label">Active CSPs</div><div class="kpi-value">{active_csps}</div></div>
                <div class="kpi-item"><div class="kpi-label">Licensed Entities</div><div class="kpi-value">{licensed_count:,}</div></div>
                <div class="kpi-item"><div class="kpi-label">Avg Monthly</div><div class="kpi-value">{avg_monthly:,}</div></div>
            </div>
            
            <h2>Scoring Methodology (Fixed Rate)</h2>
            <div class="benchmark-widget">
                <div class="benchmark-widget-title">📊 Fixed-Rate Scoring System</div>
                <p><strong>Total Score = SPV Count × 0.46 + Foundation Count × 0.54</strong><br>
                There is no maximum score – every entity adds a predictable number of points.</p>
                <ul>
                    <li>SPV → 0.46 points each</li>
                    <li>Foundation → 0.54 points each</li>
                    <li>License status is not scored (display only)</li>
                </ul>
                <p><strong>Foundation Advantage:</strong> Foundations are worth ~17% more per entity than SPVs.</p>
            </div>
            
            <h2>📊 Visual Analytics & Charts</h2>
            <div class="chart-wrap"><h3>Score Breakdown — SPV vs Foundation (Top 15 CSPs)</h3><canvas id="chartStackedScore" height="110"></canvas></div>
            <div class="chart-wrap"><h3>Total Performance Score — Top 15 CSPs</h3><canvas id="chartTotalScore" height="140"></canvas></div>
            <div class="chart-wrap"><h3>Incorporation Volume — Top 15 CSPs</h3><canvas id="chartVolume" height="110"></canvas></div>
            <div class="chart-wrap"><h3>Market Share (%) — Top 15 CSPs</h3><canvas id="chartShare" height="110"></canvas></div>
            <div class="chart-wrap"><h3>Entity Count Comparison — SPV vs Foundation (Top 15 CSPs)</h3><canvas id="chartEntityCount" height="110"></canvas></div>
            <div class="chart-wrap" style="display:inline-block;width:48%;vertical-align:top;"><h3>Entity Type Distribution</h3><canvas id="chartEntityDist" height="200"></canvas></div>
            <div class="chart-wrap" style="display:inline-block;width:48%;vertical-align:top;"><h3>License Status Distribution</h3><canvas id="chartLicense" height="200"></canvas></div>
            <div class="chart-wrap"><h3>Volume vs Performance Score — Competitive Positioning Matrix</h3><canvas id="chartScatter" height="180"></canvas></div>
            
            <script>
                const BLUE = 'rgba(96,165,250,0.85)', PURPLE = 'rgba(168,85,247,0.85)', GREEN = 'rgba(34,197,94,0.85)', ORANGE = 'rgba(249,115,22,0.85)', RED = 'rgba(239,68,68,0.85)', TEAL = 'rgba(20,184,166,0.85)';
                const PIE_COLORS = [BLUE,PURPLE,GREEN,ORANGE,RED,TEAL,'rgba(251,191,36,0.85)','rgba(236,72,153,0.85)'];
                const labels = {j_labels};
                const spvScr = {j_spv}, fndScr = {j_fnd}, totScr = {j_total}, vols = {j_vol}, shares = {j_share}, spvCnt = {j_spv_cnt}, fndCnt = {j_fnd_cnt};
                new Chart(document.getElementById('chartStackedScore'), {{ type:'bar', data:{{ labels, datasets:[{{ label:'SPV Score (0.46/ea)', data:spvScr, backgroundColor:BLUE, stack:'s' }},{{ label:'Foundation Score (0.54/ea)', data:fndScr, backgroundColor:PURPLE, stack:'s' }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ position:'top' }}, tooltip:{{ mode:'index' }} }}, scales:{{ x:{{ stacked:true }}, y:{{ stacked:true, title:{{ display:true, text:'Score' }} }} }} }} }});
                new Chart(document.getElementById('chartTotalScore'), {{ type:'bar', data:{{ labels, datasets:[{{ label:'Total Score', data:totScr, backgroundColor:totScr.map(v=> v>10?GREEN:v>5?ORANGE:RED) }}] }}, options:{{ indexAxis:'y', responsive:true, plugins:{{ legend:{{ display:false }}, tooltip:{{ callbacks:{{ label: ctx=>` Score: ${{ctx.raw.toFixed(2)}}` }} }} }}, scales:{{ x:{{ title:{{ display:true, text:'Total Score' }} }} }} }} }});
                new Chart(document.getElementById('chartVolume'), {{ type:'bar', data:{{ labels, datasets:[{{ label:'Total Incorporations', data:vols, backgroundColor:TEAL }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ title:{{ display:true, text:'Count' }} }} }} }} }});
                new Chart(document.getElementById('chartShare'), {{ type:'line', data:{{ labels, datasets:[{{ label:'Market Share (%)', data:shares, borderColor:ORANGE, backgroundColor:'rgba(249,115,22,0.15)', tension:0.3, fill:true, pointRadius:5 }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ display:false }} }}, scales:{{ y:{{ title:{{ display:true, text:'Share (%)' }} }} }} }} }});
                new Chart(document.getElementById('chartEntityCount'), {{ type:'bar', data:{{ labels, datasets:[{{ label:'SPV Count', data:spvCnt, backgroundColor:BLUE }},{{ label:'Foundation Count', data:fndCnt, backgroundColor:PURPLE }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ position:'top' }} }}, scales:{{ y:{{ title:{{ display:true, text:'Entity Count' }} }} }} }} }});
                new Chart(document.getElementById('chartEntityDist'), {{ type:'doughnut', data:{{ labels:{ent_labels}, datasets:[{{ data:{ent_vals}, backgroundColor:PIE_COLORS, borderWidth:2 }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ position:'bottom' }} }} }} }});
                new Chart(document.getElementById('chartLicense'), {{ type:'pie', data:{{ labels:{lic_labels}, datasets:[{{ data:{lic_vals}, backgroundColor:[GREEN,RED,ORANGE,BLUE], borderWidth:2 }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ position:'bottom' }} }} }} }});
                const scatterData = labels.map((l,i)=>({{ x:vols[i], y:totScr[i], label:l }}));
                new Chart(document.getElementById('chartScatter'), {{ type:'scatter', data:{{ datasets:[{{ label:'CSPs', data:scatterData, backgroundColor:PURPLE, pointRadius:7, pointHoverRadius:10 }}] }}, options:{{ responsive:true, plugins:{{ legend:{{ display:false }}, tooltip:{{ callbacks:{{ label: ctx=>` ${{ctx.raw.label}}: Vol=${{ctx.raw.x}}, Score=${{ctx.raw.y.toFixed(2)}}` }} }} }}, scales:{{ x:{{ title:{{ display:true, text:'Incorporation Volume' }} }}, y:{{ title:{{ display:true, text:'Total Score' }} }} }} }} }});
            </script>
            
            <h2>Top CSP Rankings (Fixed-Rate Scores)</h2>
            <table>
                <thead><tr><th>Rank</th><th>CSP</th><th>Volume</th><th>SPV Count</th><th>Foundation Count</th><th>SPV Score</th><th>Foundation Score</th><th>Total Score</th></tr></thead>
                <tbody>
    """
    for _, row in ranking_df_report.iterrows():
        score_class = 'high' if row['Total Score'] > 70 else 'medium' if row['Total Score'] > 50 else 'low'
        html_content += f"""
                    <tr>
                        <td>{row['Rank']}</td>
                        <td><strong>{row['CSP']}</strong></td>
                        <td>{row['Volume']:,}</td>
                        <td>{row['SPV Count']:,}</td>
                        <td>{row['Foundation Count']:,}</td>
                        <td>{row['SPV Score']:.1f}</td>
                        <td>{row['Foundation Score']:.1f}</td>
                        <td><span class="score-badge {score_class}">{row['Total Score']:.1f}</span></td>
                    </tr>
        """
    html_content += f"""
                </tbody>
            </table>
            
            <h2>Strategic Insights</h2>
            <div class="insight-section">
                <div class="insight-title">Fixed-Rate Scoring Implications</div>
                <ul>
                    <li>Each SPV adds exactly <strong>0.46 points</strong>; each Foundation adds exactly <strong>0.54 points</strong>.</li>
                    <li>Foundations are ~17% more valuable per entity than SPVs.</li>
                    <li>Scoring is market‑independent and predictable – ideal for performance tracking.</li>
                    <li>Total market SPV pool: {total_market_spv:,} SPVs → {total_market_spv*0.46:,.2f} points available.</li>
                    <li>Total market Foundation pool: {total_market_foundation:,} Foundations → {total_market_foundation*0.54:,.2f} points available.</li>
                </ul>
            </div>
            
            <div class="footer">
                <p><strong>CSP Market Intelligence Platform </strong></p>
                <p>Performance Score = SPV×0.46 + Foundation×0.54 | License status not scored</p>
                <p>Report Details: {total_incorporations:,} incorporations | {active_csps} CSPs | {months_count} months analyzed</p>
                <p>This report is confidential and prepared for authorized recipients only.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

market_report_html = generate_enhanced_market_report()

col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    st.download_button(
        label="📊 Download Market Report",
        data=market_report_html,
        file_name=f"CSP_Market_Report_{start_date.strftime('%Y%m%d')}.html",
        mime="text/html",
        help="Comprehensive market analysis and benchmark report (fixed-rate scoring)"
    )

with col_export2:
    csv_export = ranking_df.to_csv(index=False)
    st.download_button(
        label="📈 Download Rankings (CSV)",
        data=csv_export,
        file_name=f"CSP_Rankings_{start_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="CSP rankings with performance scores"
    )

with col_export3:
    license_export = csp_license_df.to_csv(index=False)
    st.download_button(
        label="🔐 Download Compliance Data",
        data=license_export,
        file_name=f"License_Analysis_{start_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="License status analysis by CSP"
    )

# ================================================================================
# FOOTER
# ================================================================================

st.markdown(
    "<div style='text-align: center; color: #9ca3af; font-size: 0.85rem; margin-top: 40px;'>"
    "<p><strong>CSP Market Intelligence Platform </strong></p>"
    "<p><i>Executive-Grade Analytics with Transparent Fixed-Rate Performance Scoring</i></p>"
    f"<p>Report generated: {now} | Data records: {len(df):,} | Active CSPs: {active_csps}</p>"
    "<p><strong>Performance Score v5.0:</strong> SPV × 0.46 + Foundation × 0.54 = Total Score</p>"
    "</div>",
    unsafe_allow_html=True)

# ================================================================================
# END OF ENHANCED APPLICATION - v5.0
# ================================================================================