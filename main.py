from analysis import DataAnalyzer
from visualization import DataVisualizer
from report import ReportGenerator
from dashboard import Dashboard

def main():

    print("=" * 60)
    print("SUPERSTORE BUSINESS INTELLIGENCE ANALYSIS")
    print("=" * 60)

    # Load & Clean Data
    analyzer = DataAnalyzer()

    analyzer.load_data()
    analyzer.clean_data()

    # KPI
    analyzer.calculate_kpi()

    # Analysis
    analyzer.category_analysis()
    analyzer.region_analysis()
    analyzer.customer_analysis()
    analyzer.product_analysis()
    analyzer.insights()

    # Charts
    visualizer = DataVisualizer(analyzer.df)
    visualizer.create_all()

    # Report
    report = ReportGenerator(analyzer.df)
    report.generate_report()
    dashboard = Dashboard(analyzer.df)
    dashboard.create_dashboard()

    print("\n" + "=" * 60)
    print("PROJECT COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nGenerated Files:")
    print("✔ outputs/cleaned_data.xlsx")
    print("✔ outputs/business_report.txt")
    print("✔ outputs/charts/")


if __name__ == "__main__":
    main()