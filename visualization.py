import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


class DataVisualizer:

    def __init__(self, df):
        self.df = df
        self.chart_path = "outputs/charts"

        os.makedirs(self.chart_path, exist_ok=True)

    def category_sales(self):

        plt.figure(figsize=(8,5))

        self.df.groupby("Category")["Sales"].sum().sort_values().plot(
            kind="bar",
            color="steelblue"
        )

        plt.title("Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Sales")
        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/sales_by_category.png")
        plt.close()

    def region_profit(self):

        plt.figure(figsize=(8,5))

        self.df.groupby("Region")["Profit"].sum().plot(
            kind="bar",
            color="green"
        )

        plt.title("Profit by Region")
        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/profit_by_region.png")
        plt.close()

    def monthly_sales(self):

        monthly = self.df.groupby(
            self.df["Order Date"].dt.to_period("M")
        )["Sales"].sum()

        plt.figure(figsize=(12,5))

        monthly.plot(marker="o")

        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.grid(True)

        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/monthly_sales.png")
        plt.close()

    def top_products(self):

        plt.figure(figsize=(12,6))

        self.df.groupby("Product Name")["Sales"]\
            .sum()\
            .sort_values(ascending=False)\
            .head(10)\
            .plot(kind="bar")

        plt.title("Top 10 Products")

        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/top_products.png")
        plt.close()

    def sales_distribution(self):

        plt.figure(figsize=(8,5))

        sns.histplot(
            self.df["Sales"],
            bins=30,
            kde=True
        )

        plt.title("Sales Distribution")

        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/sales_distribution.png")
        plt.close()

    def correlation_heatmap(self):

        plt.figure(figsize=(8,6))

        sns.heatmap(
            self.df[["Sales","Profit","Discount","Quantity"]].corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/correlation_heatmap.png")
        plt.close()

    def customer_segment(self):

        plt.figure(figsize=(7,7))

        self.df["Segment"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%"
        )

        plt.ylabel("")
        plt.title("Customer Segment Distribution")

        plt.tight_layout()

        plt.savefig(f"{self.chart_path}/customer_segment.png")
        plt.close()

    def create_all(self):

        print("\nGenerating Charts...")

        self.category_sales()
        self.region_profit()
        self.monthly_sales()
        self.top_products()
        self.sales_distribution()
        self.correlation_heatmap()
        self.customer_segment()

        print("All charts saved successfully.")