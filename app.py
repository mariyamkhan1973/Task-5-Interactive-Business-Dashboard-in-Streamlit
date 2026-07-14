"""
Task 5: Interactive Business Dashboard in Streamlit
Global Superstore Dataset — Sales, Profit & Segment-wise Performance

Run with:  streamlit run app.py
"""
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore.csv", parse_dates=["Order Date"])
    return df


df = load_data()

st.title("📊 Global Superstore — Business Performance Dashboard")
st.caption("Interactive dashboard for analyzing sales, profit, and segment-wise performance.")

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

regions = sorted(df["Region"].unique())
categories = sorted(df["Category"].unique())

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

subcats_available = sorted(df[df["Category"].isin(selected_categories)]["Sub-Category"].unique())
selected_subcats = st.sidebar.multiselect("Sub-Category", subcats_available, default=subcats_available)

date_min, date_max = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input("Order Date Range", value=(date_min, date_max),
                                    min_value=date_min, max_value=date_max)

# ---------------- Apply filters ----------------
mask = (
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Sub-Category"].isin(selected_subcats)
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask &= (df["Order Date"] >= start) & (df["Order Date"] <= end)

filtered = df[mask]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ---------------- KPIs ----------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = len(filtered)
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()

# ---------------- Charts ----------------
left, right = st.columns(2)

with left:
    st.subheader("Sales & Profit by Category")
    cat_perf = filtered.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig1 = px.bar(cat_perf, x="Category", y=["Sales", "Profit"], barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("Sales by Region")
    region_perf = filtered.groupby("Region")["Sales"].sum().reset_index()
    fig2 = px.pie(region_perf, names="Region", values="Sales", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Monthly Sales & Profit Trend")
trend = filtered.copy()
trend["Month"] = trend["Order Date"].dt.to_period("M").dt.to_timestamp()
trend = trend.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
fig3 = px.line(trend, x="Month", y=["Sales", "Profit"], markers=True)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Sub-Category Performance")
subcat_perf = filtered.groupby("Sub-Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=True).reset_index()
fig4 = px.bar(subcat_perf, x="Sales", y="Sub-Category", orientation="h", color="Profit",
              color_continuous_scale="RdYlGn")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🏆 Top 5 Customers by Sales")
top_customers = (
    filtered.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
fig5 = px.bar(top_customers, x="Sales", y="Customer Name", orientation="h", color="Sales",
              color_continuous_scale="Blues")
fig5.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig5, use_container_width=True)

with st.expander("View Raw Filtered Data"):
    st.dataframe(filtered)
