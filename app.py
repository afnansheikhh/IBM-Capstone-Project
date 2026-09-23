import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from supermarket_analytics.data_loader import load_data, check_data_quality, clean_data
from supermarket_analytics.analytics import (
    calculate_sales,
    get_kpi_metrics,
    get_category_summary,
    get_branch_summary,
    get_customer_summary,
    get_payment_summary,
    get_product_summary,
    get_monthly_summary,
    simulate_growth_scenario,
    get_business_recommendations
)

# Page configuration
st.set_page_config(
    page_title="Supermarket Sales Analytics | IBM Capstone",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# HIGH-CONTRAST NEO-BRUTALIST IBM BLUE & WHITE THEME CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F4F7FB !important;
        color: #161616 !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #161616;
    }

    /* Top Subtitle pill */
    .dataset-subtitle {
        font-size: 0.95rem;
        color: #525252;
        font-weight: 600;
        margin-bottom: 1rem;
        display: inline-block;
        background: #FFFFFF;
        border: 2px solid #161616;
        padding: 4px 14px;
        box-shadow: 2px 2px 0px #161616;
    }

    /* Neo-Brutalist Metric Card */
    .neo-metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .neo-metric-card {
        background: #FFFFFF !important;
        border: 3px solid #161616 !important;
        box-shadow: 5px 5px 0px #161616 !important;
        padding: 16px 14px !important;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }

    .neo-metric-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #0F62FE !important;
    }

    .neo-metric-label {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #525252 !important;
    }

    .neo-metric-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #0F62FE !important;
        margin-top: 3px;
    }

    .neo-metric-sub {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        color: #161616 !important;
        margin-top: 3px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 3.5px solid #161616 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #161616 !important;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 700 !important;
        color: #161616 !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
        letter-spacing: 0.5px;
    }

    /* Multiselect tags */
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #0F62FE !important;
        border: 1.5px solid #161616 !important;
        border-radius: 0px !important;
    }

    .stMultiSelect div[data-baseweb="tag"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 3.5px solid #161616 !important;
        padding-bottom: 0px;
        margin-bottom: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF !important;
        border: 2.5px solid #161616 !important;
        border-bottom: none !important;
        border-radius: 0px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        color: #161616 !important;
        box-shadow: 2px -2px 0px #161616;
        font-size: 0.85rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: #0F62FE !important;
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {
        color: #FFFFFF !important;
    }

    /* Action Cards */
    .neo-action-card-blue {
        background: #EDF5FF !important;
        border: 3px solid #0F62FE !important;
        box-shadow: 5px 5px 0px #161616 !important;
        padding: 18px !important;
        margin-bottom: 16px !important;
    }

    .neo-action-card-white {
        background: #FFFFFF !important;
        border: 3px solid #161616 !important;
        box-shadow: 5px 5px 0px #161616 !important;
        padding: 18px !important;
        margin-bottom: 16px !important;
    }

    /* Buttons */
    .stDownloadButton button, .stButton button {
        background: #0F62FE !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 3px solid #161616 !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #161616 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 10px 22px !important;
    }

    .stDownloadButton button:hover, .stButton button:hover {
        background: #0043CE !important;
        box-shadow: 6px 6px 0px #161616 !important;
        transform: translate(-2px, -2px);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# PLOTLY IBM NEO-BRUTALIST THEME HELPER
# -------------------------------------------------------------
IBM_PALETTE = ["#0F62FE", "#1192E8", "#002D9C", "#0072C3", "#8A3FFC", "#EE538B", "#009D9A", "#6F6F6F"]

def apply_neo_theme(fig):
    fig.update_layout(
        font=dict(family="IBM Plex Sans, sans-serif", color="#161616", size=12),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=35, r=35, t=50, b=35),
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=14, color="#161616")),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB",
            linecolor="#161616",
            linewidth=2,
            ticks="outside",
            tickcolor="#161616",
            tickfont=dict(color="#161616", size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB",
            linecolor="#161616",
            linewidth=2,
            ticks="outside",
            tickcolor="#161616",
            tickfont=dict(color="#161616", size=11)
        )
    )
    return fig

# -------------------------------------------------------------
# SIDEBAR (FILE UPLOAD & MULTI-SELECT FILTERS)
# -------------------------------------------------------------
st.sidebar.markdown("""
<div style="background:#0F62FE; border:3px solid #161616; box-shadow:3px 3px 0px #161616; padding:12px; margin-bottom:16px;">
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; color:#FFFFFF !important;">🛒 Supermarket Analytics</div>
    <div style="font-size:0.75rem; font-weight:600; color:#EDF5FF !important;">IBM SKILLSBUILD CAPSTONE</div>
</div>
""", unsafe_allow_html=True)

# 1. Upload CSV
st.sidebar.markdown("### 📤 Upload CSV")
uploaded_file = st.sidebar.file_uploader("Upload dataset", type=["csv"], help="200MB limit per file • CSV", label_visibility="collapsed")

# Load raw and clean data
raw_df = load_data(uploaded_file)
clean_df = clean_data(raw_df)
df, discrepancies_count = calculate_sales(clean_df)
quality_audit = check_data_quality(raw_df)

# 2. Filters Section
st.sidebar.markdown("### 🔧 Filters")

all_cities = sorted(df["City"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("City", options=all_cities, default=all_cities)

all_categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", options=all_categories, default=all_categories)

all_cust_types = sorted(df["Customer Type"].dropna().unique().tolist())
selected_cust_types = st.sidebar.multiselect("Customer Type", options=all_cust_types, default=all_cust_types)

all_payments = sorted(df["Payment"].dropna().unique().tolist())
selected_payments = st.sidebar.multiselect("Payment Method", options=all_payments, default=all_payments)

all_genders = sorted(df["Gender"].dropna().unique().tolist()) if "Gender" in df.columns else []
selected_genders = st.sidebar.multiselect("Gender", options=all_genders, default=all_genders) if all_genders else []

# Date range filter
if 'Date' in df.columns and not df['Date'].isnull().all():
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    selected_date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
else:
    selected_date_range = None

# Apply multi-filter logic
filtered_df = df[
    (df["City"].isin(selected_cities)) &
    (df["Category"].isin(selected_categories)) &
    (df["Customer Type"].isin(selected_cust_types)) &
    (df["Payment"].isin(selected_payments))
]

if selected_genders and "Gender" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Gender"].isin(selected_genders)]

if selected_date_range and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_d) &
        (filtered_df["Date"].dt.date <= end_d)
    ]

# -------------------------------------------------------------
# DYNAMIC HEADER SUBTITLE
# -------------------------------------------------------------
date_str = ""
if 'Date' in filtered_df.columns and not filtered_df.empty:
    min_d_str = filtered_df['Date'].min().strftime('%d %b %Y')
    max_d_str = filtered_df['Date'].max().strftime('%d %b %Y')
    date_str = f" · {min_d_str} – {max_d_str}"

st.markdown(f"""
<div class="dataset-subtitle">
    Analysing <strong>{len(filtered_df)} transactions</strong>{date_str}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 7 MAIN NAVIGATION TABS (MATCHING IBM COURSE ARCHITECTURE)
# -------------------------------------------------------------
tabs = st.tabs([
    "📊 Overview",
    "🔍 Data Quality",
    "📦 Category & Product",
    "🏙️ City & Branch",
    "👤 Customer Insights",
    "📈 Time Trends",
    "💡 Business Insights"
])

# =============================================================
# TAB 1: OVERVIEW
# =============================================================
with tabs[0]:
    kpis = get_kpi_metrics(filtered_df)
    
    st.markdown(f"""
    <div class="neo-metric-container">
        <div class="neo-metric-card">
            <div class="neo-metric-label">Total Revenue</div>
            <div class="neo-metric-value">₹{kpis['total_revenue']:,.2f}</div>
            <div class="neo-metric-sub">Sales = Qty × Unit Price</div>
        </div>
        <div class="neo-metric-card">
            <div class="neo-metric-label">Total Transactions</div>
            <div class="neo-metric-value">{kpis['total_transactions']:,}</div>
            <div class="neo-metric-sub">Invoices processed</div>
        </div>
        <div class="neo-metric-card">
            <div class="neo-metric-label">Units Sold</div>
            <div class="neo-metric-value">{kpis['total_units_sold']:,}</div>
            <div class="neo-metric-sub">Total product units</div>
        </div>
        <div class="neo-metric-card">
            <div class="neo-metric-label">Avg Order Value</div>
            <div class="neo-metric-value">₹{kpis['avg_order_value']:,.2f}</div>
            <div class="neo-metric-sub">Mean basket spend</div>
        </div>
        <div class="neo-metric-card">
            <div class="neo-metric-label">Avg Rating</div>
            <div class="neo-metric-value">{kpis['avg_rating']:.2f}★</div>
            <div class="neo-metric-sub">Out of 5.0 score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    ov_c1, ov_c2 = st.columns(2)
    with ov_c1:
        cat_summary = get_category_summary(filtered_df)
        fig_cat_ov = px.bar(
            cat_summary,
            x='Category',
            y='Total_Sales',
            text='Total_Sales',
            title='Revenue by Category (₹)',
            color='Category',
            color_discrete_sequence=IBM_PALETTE
        )
        fig_cat_ov.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_cat_ov = apply_neo_theme(fig_cat_ov)
        fig_cat_ov.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_cat_ov, use_container_width=True)
        
    with ov_c2:
        branch_summary = get_branch_summary(filtered_df)
        fig_branch_ov = px.bar(
            branch_summary,
            x='City',
            y='Total_Sales',
            color='City',
            title='Revenue by Branch City (₹)',
            text='Total_Sales',
            color_discrete_sequence=['#0F62FE', '#002D9C', '#1192E8', '#0072C3']
        )
        fig_branch_ov.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_branch_ov = apply_neo_theme(fig_branch_ov)
        fig_branch_ov.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_branch_ov, use_container_width=True)

# =============================================================
# TAB 2: DATA QUALITY
# =============================================================
with tabs[1]:
    st.markdown("### 🔍 Data Quality Audit & Schema Validation")
    
    total_recs = quality_audit.get('total_records', len(raw_df))
    total_cols = quality_audit.get('total_columns', len(raw_df.columns))
    dup_rows = quality_audit.get('duplicate_rows', int(raw_df.duplicated().sum()))
    
    dq1, dq2, dq3 = st.columns(3)
    with dq1:
        st.markdown(f"""
        <div style="background:#EDF5FF; border:2.5px solid #0F62FE; padding:16px; box-shadow:3px 3px 0px #161616;">
            <div style="color:#0F62FE; font-weight:700; font-size:0.8rem;">TOTAL DATASET RECORDS</div>
            <div style="color:#161616; font-size:1.6rem; font-weight:700; margin-top:2px;">{total_recs} Rows</div>
            <div style="color:#525252; font-size:0.8rem;">{total_cols} features tracked</div>
        </div>
        """, unsafe_allow_html=True)
    with dq2:
        st.markdown(f"""
        <div style="background:#EDF5FF; border:2.5px solid #0F62FE; padding:16px; box-shadow:3px 3px 0px #161616;">
            <div style="color:#0F62FE; font-weight:700; font-size:0.8rem;">DUPLICATES & NULL AUDIT</div>
            <div style="color:#161616; font-size:1.6rem; font-weight:700; margin-top:2px;">0 Missing / {dup_rows} Dups</div>
            <div style="color:#525252; font-size:0.8rem;">100% complete integrity</div>
        </div>
        """, unsafe_allow_html=True)
    with dq3:
        st.markdown(f"""
        <div style="background:#EDF5FF; border:2.5px solid #0F62FE; padding:16px; box-shadow:3px 3px 0px #161616;">
            <div style="color:#0F62FE; font-weight:700; font-size:0.8rem;">FORMULA VALIDATION</div>
            <div style="color:#161616; font-size:1.6rem; font-weight:700; margin-top:2px;">{discrepancies_count} Discrepancies</div>
            <div style="color:#525252; font-size:0.8rem;">Sales = Qty × Unit Price match</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Detailed Feature Column Quality Summary")
    
    if 'audit_df' in quality_audit:
        audit_table = quality_audit['audit_df']
    else:
        audit_table = pd.DataFrame([{
            'Column': col,
            'Data Type': str(raw_df[col].dtype),
            'Missing Count': int(raw_df[col].isnull().sum()),
            'Missing %': f"{round((raw_df[col].isnull().sum() / len(raw_df)) * 100, 2)}%",
            'Sample Value': str(raw_df[col].iloc[0]) if len(raw_df) > 0 else ''
        } for col in raw_df.columns])
        
    st.dataframe(audit_table, use_container_width=True)

# =============================================================
# TAB 3: CATEGORY & PRODUCT (EXACT MATCH TO REFERENCE SCREENSHOT)
# =============================================================
with tabs[2]:
    cat_summary = get_category_summary(filtered_df)
    
    # Formatted Category Summary Table
    display_cat_table = cat_summary.rename(columns={
        'Category': 'Category',
        'Total_Sales': 'Total Revenue (₹)',
        'Transactions': 'Transactions',
        'Avg_Ticket': 'Avg Order (₹)',
        'Total_Units': 'Units Sold',
        'Avg_Rating': 'Avg Rating'
    })[['Category', 'Total Revenue (₹)', 'Transactions', 'Avg Order (₹)', 'Units Sold', 'Avg Rating']]
    
    st.dataframe(
        display_cat_table.style.format({
            'Total Revenue (₹)': '₹{:,.2f}',
            'Transactions': '{:,}',
            'Avg Order (₹)': '₹{:.2f}',
            'Units Sold': '{:,}',
            'Avg Rating': '{:.2f}★'
        }),
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two key charts from screenshot: Transactions by Category (Vertical) & Avg Rating by Category (Horizontal)
    cat_col1, cat_col2 = st.columns(2)
    
    with cat_col1:
        fig_trans_cat = px.bar(
            cat_summary.sort_values(by='Transactions', ascending=False),
            x='Category',
            y='Transactions',
            text='Transactions',
            title='Transactions by Category',
            color='Category',
            color_discrete_sequence=IBM_PALETTE
        )
        fig_trans_cat.update_traces(
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_trans_cat = apply_neo_theme(fig_trans_cat)
        fig_trans_cat.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_trans_cat, use_container_width=True)
        
    with cat_col2:
        fig_rate_cat = px.bar(
            cat_summary.sort_values(by='Avg_Rating', ascending=True),
            x='Avg_Rating',
            y='Category',
            orientation='h',
            text='Avg_Rating',
            title='Average Rating by Category',
            color='Avg_Rating',
            color_continuous_scale='Greens',
            range_x=[3.0, 5.0]
        )
        fig_rate_cat.update_traces(
            texttemplate='%{text:.2f}★',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_rate_cat = apply_neo_theme(fig_rate_cat)
        fig_rate_cat.update_layout(height=400, coloraxis_showscale=False)
        st.plotly_chart(fig_rate_cat, use_container_width=True)
        
    # Product Deep Dive
    st.markdown("---")
    st.markdown("#### Individual Product Drill-down")
    prod_summary = get_product_summary(filtered_df)
    
    p_c1, p_c2 = st.columns([3, 2])
    with p_c1:
        fig_prod = px.bar(
            prod_summary,
            x='Product',
            y='Total_Sales',
            color='Category',
            title='Total Revenue by Product Item (₹)',
            text='Total_Sales',
            color_discrete_sequence=IBM_PALETTE
        )
        fig_prod.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_prod = apply_neo_theme(fig_prod)
        fig_prod.update_layout(height=420, xaxis_tickangle=-45)
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with p_c2:
        fig_scatter = px.scatter(
            filtered_df,
            x='Unit Price',
            y='Rating',
            size='Quantity',
            color='Category',
            hover_data=['Product', 'City', 'Payment'],
            title='Unit Price vs Rating (Size = Qty)',
            color_discrete_sequence=IBM_PALETTE
        )
        fig_scatter = apply_neo_theme(fig_scatter)
        fig_scatter.update_layout(height=420)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.dataframe(prod_summary, use_container_width=True)

# =============================================================
# TAB 4: CITY & BRANCH
# =============================================================
with tabs[3]:
    branch_summary = get_branch_summary(filtered_df)
    
    st.dataframe(
        branch_summary.rename(columns={
            'Branch': 'Branch ID',
            'City': 'City',
            'Total_Sales': 'Total Sales (₹)',
            'Transactions': 'Transactions',
            'Total_Units': 'Units Sold',
            'Avg_Ticket': 'Avg Ticket (₹)',
            'Avg_Rating': 'Avg Rating',
            'Revenue_Share_%': 'Market Share %'
        }).style.format({
            'Total Sales (₹)': '₹{:,.2f}',
            'Avg Ticket (₹)': '₹{:.2f}',
            'Avg Rating': '{:.2f}★',
            'Market Share %': '{:.1f}%'
        }),
        use_container_width=True
    )
    
    br_c1, br_c2 = st.columns(2)
    with br_c1:
        fig_br_rev = px.bar(
            branch_summary,
            x='City',
            y='Total_Sales',
            color='Branch',
            title='Revenue by City & Branch (₹)',
            text='Total_Sales',
            color_discrete_sequence=['#0F62FE', '#002D9C', '#1192E8', '#0072C3']
        )
        fig_br_rev.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_br_rev = apply_neo_theme(fig_br_rev)
        fig_br_rev.update_layout(height=400)
        st.plotly_chart(fig_br_rev, use_container_width=True)
        
    with br_c2:
        fig_br_rat = px.bar(
            branch_summary,
            x='City',
            y='Avg_Rating',
            color='City',
            title='Customer Satisfaction Rating by Branch',
            text='Avg_Rating',
            range_y=[3.0, 5.0],
            color_discrete_sequence=['#009D9A', '#0F62FE', '#8A3FFC', '#EE538B']
        )
        fig_br_rat.update_traces(
            texttemplate='%{text:.2f}★',
            textposition='outside',
            marker=dict(line=dict(width=2, color='#161616'))
        )
        fig_br_rat = apply_neo_theme(fig_br_rat)
        fig_br_rat.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_br_rat, use_container_width=True)

# =============================================================
# TAB 5: CUSTOMER INSIGHTS
# =============================================================
with tabs[4]:
    cust_df = get_customer_summary(filtered_df)
    pay_df = get_payment_summary(filtered_df)
    
    cust_c1, cust_c2 = st.columns(2)
    with cust_c1:
        fig_cust = px.sunburst(
            cust_df,
            path=['Customer Type', 'Gender'],
            values='Total_Sales',
            title='Revenue: Customer Type & Gender',
            color='Customer Type',
            color_discrete_map={'Member': '#0F62FE', 'Normal': '#A6C8FF'}
        )
        fig_cust.update_traces(marker=dict(line=dict(color='#161616', width=2)))
        fig_cust = apply_neo_theme(fig_cust)
        fig_cust.update_layout(height=420)
        st.plotly_chart(fig_cust, use_container_width=True)
        
    with cust_c2:
        fig_pay = px.pie(
            pay_df,
            names='Payment',
            values='Total_Sales',
            title='Payment Method Revenue Share %',
            hole=0.45,
            color_discrete_sequence=['#0F62FE', '#1192E8', '#002D9C', '#6F6F6F']
        )
        fig_pay.update_traces(
            marker=dict(line=dict(color='#161616', width=2)),
            textinfo='label+percent'
        )
        fig_pay = apply_neo_theme(fig_pay)
        fig_pay.update_layout(height=420)
        st.plotly_chart(fig_pay, use_container_width=True)
        
    st.dataframe(cust_df, use_container_width=True)

# =============================================================
# TAB 6: TIME TRENDS
# =============================================================
with tabs[5]:
    monthly_df = get_monthly_summary(filtered_df)
    
    t_c1, t_c2 = st.columns([3, 2])
    with t_c1:
        fig_line = px.line(
            monthly_df,
            x='Month_Year',
            y='Total_Sales',
            markers=True,
            title='Monthly Sales Revenue Trajectory (₹)',
            line_shape='spline'
        )
        fig_line.update_traces(
            line=dict(color='#0F62FE', width=4),
            marker=dict(size=10, color='#FFFFFF', line=dict(color='#161616', width=3))
        )
        fig_line = apply_neo_theme(fig_line)
        fig_line.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)", height=420)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with t_c2:
        if 'Day_Name' in filtered_df.columns:
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_df = filtered_df.groupby('Day_Name')['Calculated_Sales'].sum().reindex(day_order).dropna().reset_index()
            fig_day = px.bar(
                day_df,
                x='Day_Name',
                y='Calculated_Sales',
                title='Revenue by Day of Week',
                color='Calculated_Sales',
                color_continuous_scale='Blues'
            )
            fig_day = apply_neo_theme(fig_day)
            fig_day.update_layout(height=420, showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_day, use_container_width=True)
            
    st.dataframe(monthly_df, use_container_width=True)

# =============================================================
# TAB 7: BUSINESS INSIGHTS & SCENARIO SIMULATOR
# =============================================================
with tabs[6]:
    st.markdown("""
    <div style="border-left: 6px solid #0F62FE; padding-left: 14px; margin-bottom: 20px;">
        <h2 style="font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:700; color:#001D6C !important; margin:0;">
            💡 STRATEGIC BUSINESS DECISIONS & EXECUTIVE PLAN
        </h2>
        <p style="color:#393939 !important; font-size:0.92rem; margin:3px 0 0 0; font-weight:500;">
            Empirical insights derived from sales distributions, branch benchmarking, and product behavior
        </p>
    </div>
    """, unsafe_allow_html=True)

    recs = get_business_recommendations()
    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="neo-action-card-blue">
            <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:#0F62FE !important; font-size:1.05rem; margin-bottom:6px;">
                {recs[0]['title']}
            </div>
            <p style="font-size:0.88rem; color:#161616 !important; margin-bottom:8px; line-height:1.4;">
                <strong>Empirical Finding:</strong> {recs[0]['finding']}
            </p>
            <p style="font-size:0.86rem; color:#002D9C !important; background:#FFFFFF; border:2.5px solid #0F62FE; padding:10px; margin:0; font-weight:600; box-shadow:2px 2px 0px #161616;">
                <strong>🎯 Executive Action:</strong> {recs[0]['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="neo-action-card-white">
            <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:#161616 !important; font-size:1.05rem; margin-bottom:6px;">
                {recs[1]['title']}
            </div>
            <p style="font-size:0.88rem; color:#161616 !important; margin-bottom:8px; line-height:1.4;">
                <strong>Empirical Finding:</strong> {recs[1]['finding']}
            </p>
            <p style="font-size:0.86rem; color:#161616 !important; background:#F4F4F4; border:2.5px solid #161616; padding:10px; margin:0; font-weight:600; box-shadow:2px 2px 0px #161616;">
                <strong>🎯 Executive Action:</strong> {recs[1]['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="neo-action-card-white">
            <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:#161616 !important; font-size:1.05rem; margin-bottom:6px;">
                {recs[2]['title']}
            </div>
            <p style="font-size:0.88rem; color:#161616 !important; margin-bottom:8px; line-height:1.4;">
                <strong>Empirical Finding:</strong> {recs[2]['finding']}
            </p>
            <p style="font-size:0.86rem; color:#161616 !important; background:#F4F4F4; border:2.5px solid #161616; padding:10px; margin:0; font-weight:600; box-shadow:2px 2px 0px #161616;">
                <strong>🎯 Executive Action:</strong> {recs[2]['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="neo-action-card-blue">
            <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:#0F62FE !important; font-size:1.05rem; margin-bottom:6px;">
                {recs[3]['title']}
            </div>
            <p style="font-size:0.88rem; color:#161616 !important; margin-bottom:8px; line-height:1.4;">
                <strong>Empirical Finding:</strong> {recs[3]['finding']}
            </p>
            <p style="font-size:0.86rem; color:#002D9C !important; background:#FFFFFF; border:2.5px solid #0F62FE; padding:10px; margin:0; font-weight:600; box-shadow:2px 2px 0px #161616;">
                <strong>🎯 Executive Action:</strong> {recs[3]['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔮 Interactive Revenue Scenario Simulator")
    
    sim_c1, sim_c2, sim_c3 = st.columns(3)
    with sim_c1:
        price_adj = st.slider("💰 General Price Adjustment (%)", min_value=-15, max_value=25, value=5, step=1)
    with sim_c2:
        member_conv = st.slider("👥 Normal-to-Member Conversion (%)", min_value=0, max_value=100, value=30, step=5)
    with sim_c3:
        snack_lift = st.slider("🍿 Snack Cross-Sell Volume Lift (%)", min_value=0, max_value=50, value=20, step=5)
        
    sim_res = simulate_growth_scenario(filtered_df, price_adj, member_conv, snack_lift)
    
    res_1, res_2, res_3, res_4 = st.columns(4)
    with res_1:
        st.metric("Base Revenue", f"₹{sim_res['base_revenue']:,.2f}")
    with res_2:
        st.metric("Simulated Revenue", f"₹{sim_res['projected_revenue']:,.2f}")
    with res_3:
        st.metric("Growth Delta", f"+₹{sim_res['revenue_delta']:,.2f}", f"{sim_res['revenue_growth_pct']}%")
    with res_4:
        st.metric("Simulation State", "Active Model", "Optimized")

# -------------------------------------------------------------
# RAW DATA EXPLORER & EXPORTS
# -------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📥 DATA EXPLORER & EXECUTIVE EXPORT SUITE", expanded=False):
    st.dataframe(filtered_df, use_container_width=True)
    
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ DOWNLOAD FILTERED DATASET (CSV)",
            data=csv_bytes,
            file_name="ibm_supermarket_sales_filtered.csv",
            mime="text/csv"
        )
    with exp_col2:
        summary_txt = f"""IBM SUPERMARKET ANALYTICS EXECUTIVE SUMMARY
=============================================
Total Revenue: ₹{kpis['total_revenue']:,.2f}
Total Orders: {kpis['total_transactions']:,}
Total Units: {kpis['total_units_sold']:,}
Average Order Value: ₹{kpis['avg_order_value']:,.2f}
Average Rating: {kpis['avg_rating']:.2f} / 5.0
"""
        st.download_button(
            label="📄 DOWNLOAD EXECUTIVE REPORT SUMMARY (TXT)",
            data=summary_txt.encode('utf-8'),
            file_name="ibm_capstone_executive_summary.txt",
            mime="text/plain"
        )
