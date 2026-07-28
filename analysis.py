import pandas as pd
import numpy as np
import os


class DataAnalyzer:

    def __init__(self):
        self.file_path = "data/Sample_Superstore.xlsx"
        self.output_path = "outputs"
        self.df = None

    # -----------------------------
    # Load Dataset
    # -----------------------------
    def load_data(self):
        print("\nLoading dataset...")

        self.df = pd.read_excel(self.file_path)

        print("Dataset Loaded Successfully")
        print(f"Rows : {self.df.shape[0]}")
        print(f"Columns : {self.df.shape[1]}")

        return self.df

    # -----------------------------
    # Data Cleaning
    # -----------------------------
    def clean_data(self):

        print("\nCleaning Data...")

        self.df.drop_duplicates(inplace=True)

        self.df["Order Date"] = pd.to_datetime(self.df["Order Date"])
        self.df["Ship Date"] = pd.to_datetime(self.df["Ship Date"])

        self.df["Year"] = self.df["Order Date"].dt.year
        self.df["Month"] = self.df["Order Date"].dt.month_name()
        self.df["Quarter"] = self.df["Order Date"].dt.quarter

        print("Data Cleaned Successfully")

        self.df.to_excel(
            os.path.join(self.output_path, "cleaned_data.xlsx"),
            index=False
        )

        return self.df

    # -----------------------------
    # KPI
    # -----------------------------
    def calculate_kpi(self):

        print("\n========== KPI ==========\n")

        total_sales = self.df["Sales"].sum()
        total_profit = self.df["Profit"].sum()
        avg_sales = self.df["Sales"].mean()
        avg_profit = self.df["Profit"].mean()
        avg_discount = self.df["Discount"].mean()

        total_orders = self.df["Order ID"].nunique()
        total_customers = self.df["Customer ID"].nunique()

        print(f"Total Sales      : ${total_sales:,.2f}")
        print(f"Total Profit     : ${total_profit:,.2f}")
        print(f"Average Sales    : ${avg_sales:,.2f}")
        print(f"Average Profit   : ${avg_profit:,.2f}")
        print(f"Average Discount : {avg_discount:.2%}")
        print(f"Total Orders     : {total_orders}")
        print(f"Customers        : {total_customers}")

    # -----------------------------
    # Category Analysis
    # -----------------------------
    def category_analysis(self):

        print("\nSales By Category\n")

        category_sales = (
            self.df
            .groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        print(category_sales)

        return category_sales

    # -----------------------------
    # Region Analysis
    # -----------------------------
    def region_analysis(self):

        print("\nProfit By Region\n")

        region_profit = (
            self.df
            .groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        print(region_profit)

        return region_profit

    # -----------------------------
    # Customer Analysis
    # -----------------------------
    def customer_analysis(self):

        print("\nTop Customers\n")

        customers = (
            self.df
            .groupby("Customer Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        print(customers)

        return customers

    # -----------------------------
    # Product Analysis
    # -----------------------------
    def product_analysis(self):

        print("\nTop Products\n")

        products = (
            self.df
            .groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        print(products)

        return products

    # -----------------------------
    # Monthly Trend
    # -----------------------------
    def monthly_sales(self):

        monthly = (
            self.df
            .groupby(self.df["Order Date"].dt.to_period("M"))["Sales"]
            .sum()
        )

        return monthly

    # -----------------------------
    # Business Insights
    # -----------------------------
    def insights(self):

        print("\n========== BUSINESS INSIGHTS ==========\n")

        print(
            "Highest Revenue Category :",
            self.df.groupby("Category")["Sales"].sum().idxmax()
        )

        print(
            "Highest Profit Region :",
            self.df.groupby("Region")["Profit"].sum().idxmax()
        )

        print(
            "Top Customer :",
            self.df.groupby("Customer Name")["Sales"].sum().idxmax()
        )

        print(
            "Top Product :",
            self.df.groupby("Product Name")["Sales"].sum().idxmax()
        )

        print(
            "Highest Sales State :",
            self.df.groupby("State")["Sales"].sum().idxmax()
        )