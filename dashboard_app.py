import streamlit as st
import pandas as pd
import os
from src.visualizations import (
    plot_sales_over_time,
    plot_top_products,
    plot_category_distribution,
    plot_monthly_trends,
    plot_heatmap,
    save_figure
)
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
def main():
    st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
    st.title("E-commerce Dashboard: Unveiling Retail Insights")
    st.markdown("""
**Story:**

Welcome to the Online Retail Dashboard! Dive into the journey of a UK-based online giftware retailer from 2009 to 2011. Explore how sales trends, customer behaviors, and product performance shaped the business. Use the interactive filters to uncover insights and drive data-informed decisions.
""")

    # Load processed data
    data_path = os.path.join("data", "processed", "ecommerce_cleaned.csv")
    df = pd.read_csv(data_path, parse_dates=["InvoiceDate"])

    # Sidebar filters
    st.sidebar.header("Filters")
    min_date, max_date = df["InvoiceDate"].min(), df["InvoiceDate"].max()
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        df = df[(df["InvoiceDate"] >= pd.to_datetime(date_range[0])) & (df["InvoiceDate"] <= pd.to_datetime(date_range[1]))]

    products = df["Description"].unique().tolist()
    selected_products = st.sidebar.multiselect("Select Products", options=products, default=products[:10])
    if selected_products:
        df = df[df["Description"].isin(selected_products)]

    countries = df["Country"].unique().tolist()
    selected_countries = st.sidebar.multiselect("Select Countries", options=countries, default=countries)
    if selected_countries:
        df = df[df["Country"].isin(selected_countries)]

    # KPIs
    st.subheader("Key Performance Indicators (KPIs)")
    col1, col2, col3 = st.columns(3)
    total_revenue = df["TotalPrice"].sum()
    total_orders = df["Invoice"].nunique()
    total_customers = df["Customer ID"].nunique()
    col1.metric("Total Revenue", f"£{total_revenue:,.0f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Unique Customers", total_customers)

    st.markdown("---")

    # Monthly Sales Trend
    st.subheader("Monthly Sales Trend")
    if not df.empty:
        monthly_sales = df.groupby([df["InvoiceDate"].dt.to_period("M")])["TotalPrice"].sum().reset_index()
        if not monthly_sales.empty:
            monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)
            fig, ax = plt.subplots(figsize=(10,4))
            sns.lineplot(data=monthly_sales, x="InvoiceDate", y="TotalPrice", marker="o", ax=ax)
            ax.set_title("Monthly Sales Trend")
            ax.set_xlabel("Month")
            ax.set_ylabel("Revenue")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected date range.")
    else:
        st.warning("No data available for the selected date range.")
    st.info("The monthly sales trend highlights periods of peak and low sales activity, helping identify the best times for marketing campaigns and inventory planning.")

    # Top Products by Revenue
    st.subheader("Top 10 Products by Revenue")
    if not df.empty:
        top_products = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)
        if not top_products.empty:
            fig2, ax2 = plt.subplots(figsize=(8,4))
            top_products.plot(kind="bar", ax=ax2, color="skyblue")
            ax2.set_title("Top 10 Products by Revenue")
            ax2.set_ylabel("Revenue")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
        else:
            st.warning("No product data available for the selected date range.")
    else:
        st.warning("No product data available for the selected date range.")
    st.info("The bar chart of top 10 products by revenue shows which items are the biggest contributors to sales. Focusing on these products can maximize revenue and inform inventory and marketing priorities.")

    # Revenue Distribution by Product
    st.subheader("Revenue Distribution by Product")
    if not df.empty:
        revenue_by_desc = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)
        if not revenue_by_desc.empty:
            fig3, ax3 = plt.subplots(figsize=(6,6))
            revenue_by_desc.plot(kind="pie", ax=ax3, autopct="%1.1f%%")
            ax3.set_ylabel("")
            ax3.set_title("Revenue Distribution by Product")
            st.pyplot(fig3)
        else:
            st.warning("No product revenue data available for the selected date range.")
    else:
        st.warning("No product revenue data available for the selected date range.")
    st.info("The revenue distribution pie chart highlights which products dominate total sales. A small number of products may account for a large share of revenue, suggesting opportunities for cross-selling or expanding similar product lines.")

    # Sales Heatmap (Month vs. Day of Week)
    st.subheader("Sales Heatmap: Month vs. Day of Week")
    df["Month"] = df["InvoiceDate"].dt.month
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    heatmap_data = df.pivot_table(index="Month", columns="DayOfWeek", values="TotalPrice", aggfunc="sum", fill_value=0)
    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax4)
    ax4.set_title("Sales Heatmap: Month vs. Day of Week")
    st.pyplot(fig4)
    st.info("The sales heatmap reveals which days of the week and months generate the most revenue. This can uncover patterns such as higher sales on weekends or during specific months, guiding staffing and promotional strategies.")

    # Revenue by Country
    st.subheader("Top 15 Countries by Revenue")
    country_revenue = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(15)
    fig5, ax5 = plt.subplots(figsize=(10,4))
    country_revenue.plot(kind="bar", ax=ax5, color="coral")
    ax5.set_title("Top 15 Countries by Revenue")
    ax5.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig5)
    st.info("The bar chart shows which countries generate the most revenue. This can help prioritize marketing and logistics efforts in high-value regions.")

    # Top Customers by Revenue
    st.subheader("Top 15 Customers by Revenue")
    top_customers = df.groupby("Customer ID")["TotalPrice"].sum().sort_values(ascending=False).head(15)
    fig6, ax6 = plt.subplots(figsize=(10,4))
    top_customers.plot(kind="bar", ax=ax6, color="orange")
    ax6.set_title("Top 15 Customers by Revenue")
    ax6.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig6)
    st.info("A small number of customers often contribute a large share of total revenue. Identifying and nurturing these top customers can drive business growth and loyalty.")

    # Product Return/Cancellation Rates
    st.subheader("Top 10 Products by Return/Cancellation Rate")
    df["IsReturn"] = df["Invoice"].astype(str).str.startswith("C")
    return_rate = df.groupby("Description")["IsReturn"].mean().sort_values(ascending=False).head(10)
    fig7, ax7 = plt.subplots(figsize=(8,4))
    return_rate.plot(kind="bar", ax=ax7, color="red")
    ax7.set_title("Top 10 Products by Return/Cancellation Rate")
    ax7.set_ylabel("Return/Cancellation Rate")
    plt.xticks(rotation=45)
    st.pyplot(fig7)
    st.info("Products with high return or cancellation rates may have quality issues, mismatched customer expectations, or other problems. Investigating these products can help reduce returns and improve customer satisfaction.")

    # Hourly Sales Trends
    st.subheader("Hourly Sales Trend")
    df["Hour"] = df["InvoiceDate"].dt.hour
    hourly_sales = df.groupby("Hour")["TotalPrice"].sum()
    fig8, ax8 = plt.subplots(figsize=(10,4))
    hourly_sales.plot(kind="bar", ax=ax8, color="teal")
    ax8.set_title("Hourly Sales Trend")
    ax8.set_xlabel("Hour of Day")
    ax8.set_ylabel("Total Revenue")
    plt.xticks(rotation=0)
    st.pyplot(fig8)
    st.info("The hourly sales trend reveals peak shopping hours. This can inform staffing, marketing campaigns, and website maintenance schedules to maximize sales during high-traffic periods.")

    # Year-over-Year Revenue and Growth
    st.subheader("Year-over-Year Revenue and Growth")
    df["Year"] = df["InvoiceDate"].dt.year
    sales_by_year = df.groupby("Year")["TotalPrice"].sum()
    yoy_growth = sales_by_year.pct_change() * 100
    fig9, ax9 = plt.subplots(figsize=(8,4))
    sales_by_year.plot(kind="bar", ax=ax9, color="navy", alpha=0.7, label="Revenue")
    ax9.set_ylabel("Revenue")
    ax9.set_title("Year-over-Year Revenue and Growth")
    ax9.legend(loc="upper left")
    ax9_2 = ax9.twinx()
    yoy_growth.plot(ax=ax9_2, color="crimson", marker="o", label="YoY Growth (%)")
    ax9_2.set_ylabel("YoY Growth (%)")
    ax9_2.legend(loc="upper right")
    st.pyplot(fig9)
    st.info("Year-over-year growth visualizations help track business momentum, spot seasonal patterns, and quickly identify periods of acceleration or slowdown. This is crucial for forecasting and strategic planning.")

    # Week-over-Week Revenue and Growth
    st.subheader("Week-over-Week Revenue and Growth")
    df["Week"] = df["InvoiceDate"].dt.isocalendar().week
    weekly_sales = df.groupby(["Year", "Week"])["TotalPrice"].sum().reset_index()
    weekly_sales["YearWeek"] = weekly_sales["Year"].astype(str) + "-W" + weekly_sales["Week"].astype(str)
    weekly_sales["WoW_Growth"] = weekly_sales["TotalPrice"].pct_change() * 100
    fig10, ax10 = plt.subplots(figsize=(14,4))
    ax10.plot(weekly_sales["YearWeek"], weekly_sales["TotalPrice"], label="Weekly Revenue", color="green")
    ax10.set_ylabel("Revenue")
    ax10.set_title("Week-over-Week Revenue and Growth")
    ax10.legend(loc="upper left")
    ax10_2 = ax10.twinx()
    ax10_2.plot(weekly_sales["YearWeek"], weekly_sales["WoW_Growth"], label="WoW Growth (%)", color="purple", alpha=0.5)
    ax10_2.set_ylabel("WoW Growth (%)")
    ax10_2.legend(loc="upper right")
    plt.xticks(rotation=45)
    st.pyplot(fig10)
    st.info("Week-over-week growth visualizations help track short-term business momentum and spot rapid changes in performance.")

    # Average Order Value by Month
    st.subheader("Average Order Value by Month")
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")
    aov_by_month = df.groupby("YearMonth").apply(lambda x: x["TotalPrice"].sum() / x["Invoice"].nunique())
    fig11, ax11 = plt.subplots(figsize=(10,4))
    aov_by_month.plot(ax=ax11, marker="o", color="darkblue")
    ax11.set_title("Average Order Value by Month")
    ax11.set_xlabel("Month")
    ax11.set_ylabel("Average Order Value")
    plt.xticks(rotation=45)
    st.pyplot(fig11)
    st.info("Tracking average order value by month helps identify trends in customer spending and the impact of promotions or seasonality. Increasing AOV is a key lever for revenue growth.")

    # Distribution of Order Sizes
    st.subheader("Distribution of Order Sizes")
    order_sizes = df.groupby("Invoice")["Quantity"].sum()
    fig12, ax12 = plt.subplots(figsize=(10,4))
    order_sizes.plot(kind="hist", bins=30, ax=ax12, color="orchid", edgecolor="black")
    ax12.set_title("Distribution of Order Sizes")
    ax12.set_xlabel("Number of Items per Order")
    ax12.set_ylabel("Frequency")
    st.pyplot(fig12)
    st.info("The order size distribution shows how many items customers typically buy per order. This can inform bundling strategies, minimum order incentives, and inventory planning.")

    # Repeat vs. New Customer Sales
    st.subheader("Sales: Repeat vs. New Customers")
    # Fix: Remove NaN Customer IDs before repeat customer logic
    df_valid_cust = df.dropna(subset=["Customer ID"])
    first_purchase = df_valid_cust.groupby("Customer ID")["InvoiceDate"].min()
    def is_repeat(row):
        cust_id = row["Customer ID"]
        if pd.isna(cust_id):
            return False
        return row["InvoiceDate"] > first_purchase.get(cust_id, row["InvoiceDate"])
    df["IsRepeatCustomer"] = df.apply(is_repeat, axis=1)
    repeat_sales = df.groupby("IsRepeatCustomer")["TotalPrice"].sum()
    labels = ["New Customer", "Repeat Customer"]
    # Ensure both labels are present
    repeat_sales = repeat_sales.reindex([False, True], fill_value=0)
    fig13, ax13 = plt.subplots(figsize=(6,6))
    repeat_sales.plot(kind="pie", labels=labels, autopct="%1.1f%%", ax=ax13, colors=["#66b3ff","#99ff99"])
    ax13.set_ylabel("")
    ax13.set_title("Sales: Repeat vs. New Customers")
    st.pyplot(fig13)
    st.info("Understanding the share of revenue from repeat versus new customers helps guide retention and acquisition strategies. A high proportion of repeat sales indicates strong customer loyalty, while a low proportion may signal a need for improved retention efforts.")

if __name__ == "__main__":
    main()
