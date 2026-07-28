import os
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Dashboard:

    def __init__(self, df):
        self.df = df
        os.makedirs("outputs", exist_ok=True)

    def create_dashboard(self):

        # ==========================
        # KPI VALUES
        # ==========================

        total_sales = self.df["Sales"].sum()
        total_profit = self.df["Profit"].sum()
        total_orders = self.df["Order ID"].nunique()
        total_customers = self.df["Customer ID"].nunique()

        # ==========================
        # DATA
        # ==========================

        category_sales = (
            self.df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        region_profit = (
            self.df.groupby("Region")["Profit"]
            .sum()
            .reset_index()
        )

        monthly_sales = (
            self.df.groupby(
                self.df["Order Date"].dt.to_period("M").astype(str)
            )["Sales"]
            .sum()
            .reset_index()
        )

        top_products = (
            self.df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        # ==========================
        # CHARTS
        # ==========================

        fig1 = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            title="Sales by Category"
        )

        fig2 = px.bar(
            region_profit,
            x="Region",
            y="Profit",
            title="Profit by Region",
            color="Profit"
        )

        fig3 = px.line(
            monthly_sales,
            x="Order Date",
            y="Sales",
            title="Monthly Sales Trend",
            markers=True
        )

        fig4 = px.bar(
            top_products,
            x="Product Name",
            y="Sales",
            title="Top 10 Products"
        )

        # ==========================
        # DASHBOARD LAYOUT
        # ==========================

        dashboard = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Sales by Category",
                "Profit by Region",
                "Monthly Sales Trend",
                "Top 10 Products"
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )

        # Chart 1
        for trace in fig1.data:
            dashboard.add_trace(trace, row=1, col=1)

        # Chart 2
        for trace in fig2.data:
            dashboard.add_trace(trace, row=1, col=2)

        # Chart 3
        for trace in fig3.data:
            dashboard.add_trace(trace, row=2, col=1)

        # Chart 4
        for trace in fig4.data:
            dashboard.add_trace(trace, row=2, col=2)

        dashboard.update_layout(

            title={
                "text": "Retail Business Intelligence Dashboard",
                "x": 0.5,
                "font": {"size": 24}
            },

            height=900,
            width=1400,

            showlegend=False,

            template="plotly_white",

            annotations=list(dashboard.layout.annotations)+[
                dict(
                    text=f"<b>Total Sales</b><br>${total_sales:,.0f}",
                    x=0.13,
                    y=1.18,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18)
                ),

                dict(
                    text=f"<b>Total Profit</b><br>${total_profit:,.0f}",
                    x=0.37,
                    y=1.18,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18)
                ),

                dict(
                    text=f"<b>Total Orders</b><br>{total_orders}",
                    x=0.63,
                    y=1.18,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18)
                ),

                dict(
                    text=f"<b>Customers</b><br>{total_customers}",
                    x=0.87,
                    y=1.18,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=18)
                )
            ]
        )

        dashboard.write_html("outputs/dashboard.html")

        print("\nInteractive Dashboard Created Successfully!")
        print("Saved as outputs/dashboard.html")