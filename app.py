import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Retail Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/Sample_Superstore.xlsx")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# -----------------------------
# Title
# -----------------------------
st.title("📊 Retail Business Intelligence Dashboard")
st.markdown("---")

# -----------------------------
# KPI Cards
# -----------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = filtered_df["Order ID"].nunique()
customers = filtered_df["Customer ID"].nunique()

avg_discount = filtered_df["Discount"].mean()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0 else 0
)

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

kpi2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

kpi3.metric(
    "💹 Profit Margin",
    f"{profit_margin:.2f}%"
)

kpi4, kpi5, kpi6 = st.columns(3)

kpi4.metric(
    "📦 Orders",
    orders
)

kpi5.metric(
    "👥 Customers",
    customers
)

kpi6.metric(
    "🎯 Avg Discount",
    f"{avg_discount:.2%}"
)

st.divider()
# -----------------------------
# Business Insights
# -----------------------------

st.subheader("📌 Business Insights")

left, right = st.columns([2, 1])

with left:

    best_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    best_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .idxmax()
    )

    best_customer = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .idxmax()
    )

    best_product = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    worst_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .idxmin()
    )

    st.success(f"🏆 Best Category : {best_category}")
    st.success(f"🌍 Best Region : {best_region}")
    st.success(f"👤 Top Customer : {best_customer}")
    st.success(f"📦 Best Product : {best_product}")
    st.error(f"⚠ Lowest Profit Category : {worst_category}")

with right:

    st.info("""
### 💡 Recommendations

✅ Increase inventory for the best-selling category.

✅ Focus marketing in the most profitable region.

✅ Reward high-value customers.

✅ Review pricing and discounts for low-profit categories.

✅ Keep sufficient stock of top-selling products.
""")

st.divider()
# -----------------------------
# Product Performance Analysis
# -----------------------------

st.subheader("📦 Product Performance Analysis")

col1, col2 = st.columns(2)

with col1:

    top_products = (
        filtered_df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="🏆 Top 10 Most Profitable Products",
        color="Profit",
        color_continuous_scale="Greens"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    bottom_products = (
        filtered_df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values()
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        bottom_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="📉 Top 10 Loss-Making Products",
        color="Profit",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()
# -----------------------------
# Discount vs Profit Analysis
# -----------------------------

st.subheader("💹 Discount vs Profit Analysis")

fig = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=["Product Name", "Customer Name"],
    title="Relationship Between Discount and Profit"
)

fig.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("👥 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    color="Sales",
    color_continuous_scale="Blues",
    title="Top 10 Customers by Sales"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🌍 Top 10 States by Sales")

top_states = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_states,
    x="Sales",
    y="State",
    orientation="h",
    color="Sales",
    color_continuous_scale="Viridis",
    title="Top 10 States"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
# -----------------------------
# Row 2
# -----------------------------

col3, col4 = st.columns(2)

with col3:

    monthly_sales = (
        filtered_df.groupby(
            filtered_df["Order Date"].dt.to_period("M").astype(str)
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Product Name",
        y="Sales",
        color="Sales",
        title="Top 10 Products"
    )

    fig.update_layout(xaxis_tickangle=-35)

    st.plotly_chart(fig, use_container_width=True)