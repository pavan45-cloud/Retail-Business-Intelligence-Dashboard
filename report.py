import os


class ReportGenerator:

    def __init__(self, df):
        self.df = df
        self.output_file = "outputs/business_report.txt"

    def generate_report(self):

        total_sales = self.df["Sales"].sum()
        total_profit = self.df["Profit"].sum()
        total_orders = self.df["Order ID"].nunique()
        total_customers = self.df["Customer ID"].nunique()

        highest_category = (
            self.df.groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )

        highest_region = (
            self.df.groupby("Region")["Profit"]
            .sum()
            .idxmax()
        )

        highest_state = (
            self.df.groupby("State")["Sales"]
            .sum()
            .idxmax()
        )

        top_customer = (
            self.df.groupby("Customer Name")["Sales"]
            .sum()
            .idxmax()
        )

        top_product = (
            self.df.groupby("Product Name")["Sales"]
            .sum()
            .idxmax()
        )

        highest_month = (
            self.df.groupby(self.df["Order Date"].dt.month_name())["Sales"]
            .sum()
            .idxmax()
        )

        report = f"""
==========================================================
          SUPERSTORE BUSINESS ANALYTICS REPORT
==========================================================

BUSINESS KPIs
----------------------------------------------------------

Total Sales          : ${total_sales:,.2f}
Total Profit         : ${total_profit:,.2f}
Total Orders         : {total_orders}
Total Customers      : {total_customers}

----------------------------------------------------------
TOP BUSINESS INSIGHTS
----------------------------------------------------------

Highest Revenue Category : {highest_category}

Most Profitable Region   : {highest_region}

Highest Sales State      : {highest_state}

Top Customer             : {top_customer}

Best Selling Product     : {top_product}

Highest Sales Month      : {highest_month}

----------------------------------------------------------
BUSINESS RECOMMENDATIONS
----------------------------------------------------------

• Increase inventory for the highest revenue category.

• Focus marketing campaigns on the most profitable region.

• Reward loyal customers with personalized offers.

• Monitor discounts to improve profit margins.

• Promote top-selling products across all regions.

==========================================================
Report Generated Automatically using Python
==========================================================
"""

        os.makedirs("outputs", exist_ok=True)

        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(report)

        print("\nBusiness report generated successfully.")
        print(f"Saved to: {self.output_file}")