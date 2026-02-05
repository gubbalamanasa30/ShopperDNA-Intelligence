import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="ShopperDNA Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" Look
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 14px;
        color: #AAAAAA;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('rfm_results.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure 'rfm_results.csv' exists.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Title and Header
st.title("🧬 ShopperDNA: Behavioral Customer Intelligence")
st.markdown("Dive deep into customer segments to uncover hidden revenue opportunities.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter DNA")

# Segment Filter
all_segments = df['customer_segment'].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Select Segments",
    options=all_segments,
    default=all_segments
)

# Recency Slider
min_recency = int(df['recency_days'].min())
max_recency = int(df['recency_days'].max())
recency_range = st.sidebar.slider(
    "Recency (Days Ago)",
    min_value=min_recency,
    max_value=max_recency,
    value=(min_recency, max_recency)
)

# Apply Filters
filtered_df = df[
    (df['customer_segment'].isin(selected_segments)) &
    (df['recency_days'] >= recency_range[0]) &
    (df['recency_days'] <= recency_range[1])
]

# --- KEY METRICS ---
col1, col2, col3, col4 = st.columns(4)

total_customers = len(filtered_df)
total_revenue = filtered_df['monetary_value'].sum()
avg_recency = filtered_df['recency_days'].mean()
champion_count = len(filtered_df[filtered_df['customer_segment'] == 'Champions'])

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Customers</div>
        <div class="metric-value">{total_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #2196F3;">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FFC107;">
        <div class="metric-label">Avg Recency</div>
        <div class="metric-value">{avg_recency:.0f} days</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #9C27B0;">
        <div class="metric-label">Champions Count</div>
        <div class="metric-value">{champion_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- VISUALIZATIONS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Interactive Intelligence Map")
    # Plotly Scatter
    fig = px.scatter(
        filtered_df,
        x="recency_days",
        y="frequency",
        size="monetary_value",
        color="customer_segment",
        hover_name="customer_name",
        hover_data=["monetary_value", "customer_segment"],
        color_discrete_map={
            "Champions": "#4CAF50",
            "Loyal Customers": "#2196F3",
            "Potential Loyalists": "#03A9F4",
            "Recent Customers": "#00BCD4",
            "At Risk": "#FFC107",
            "Needs Attention": "#FF9800",
            "Lost Customers": "#F44336"
        },
        title="Recency vs Frequency (Size = Revenue)",
        height=500
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Segment Distribution")
    # Plotly Pie/Donut
    seg_counts = filtered_df['customer_segment'].value_counts().reset_index()
    seg_counts.columns = ['segment', 'count']
    
    fig_pie = px.pie(
        seg_counts,
        values='count',
        names='segment',
        hole=0.4,
        color='segment',
        color_discrete_map={
            "Champions": "#4CAF50",
            "Loyal Customers": "#2196F3",
            "Potential Loyalists": "#03A9F4",
            "Recent Customers": "#00BCD4",
            "At Risk": "#FFC107",
            "Needs Attention": "#FF9800",
            "Lost Customers": "#F44336"
        }
    )
    fig_pie.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- DATA EXPLORER ---
st.subheader("📂 Customer Data Explorer")
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.sort_values(by="monetary_value", ascending=False), use_container_width=True)
