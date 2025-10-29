"""
Visualization Utilities

Functions to create common plots for e-commerce sales analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_sales_over_time(df, date_column, value_column, title="Sales Over Time"):
    """
    Create a line plot showing sales over time.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    date_column : str
        Name of the date column
    value_column : str
        Name of the value column to plot
    title : str
        Plot title
    
    Returns:
    --------
    fig, ax : matplotlib objects
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    df_sorted = df.sort_values(date_column)
    ax.plot(df_sorted[date_column], df_sorted[value_column], linewidth=2)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(date_column)
    ax.set_ylabel(value_column)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig, ax


def plot_top_products(df, product_column, value_column, top_n=10, title="Top Products by Sales"):
    """
    Create a horizontal bar chart of top products.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    product_column : str
        Name of the product column
    value_column : str
        Name of the value column
    top_n : int
        Number of top products to show
    title : str
        Plot title
    
    Returns:
    --------
    fig, ax : matplotlib objects
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top_products = df.groupby(product_column)[value_column].sum().nlargest(top_n)
    
    bars = ax.barh(range(len(top_products)), top_products.values, color='steelblue')
    ax.set_yticks(range(len(top_products)))
    ax.set_yticklabels(top_products.index)
    ax.set_xlabel(value_column)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels on bars
    for i, (idx, val) in enumerate(top_products.items()):
        ax.text(val, i, f'${val:,.0f}', va='center', fontsize=10)
    
    plt.tight_layout()
    return fig, ax


def plot_category_distribution(df, category_column, value_column, title="Category Distribution"):
    """
    Create a pie chart showing category distribution.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    category_column : str
        Name of the category column
    value_column : str
        Name of the value column
    title : str
        Plot title
    
    Returns:
    --------
    fig, ax : matplotlib objects
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    category_sales = df.groupby(category_column)[value_column].sum()
    
    ax.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%',
           startangle=90, textprops={'fontsize': 12})
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    return fig, ax


def plot_monthly_trends(df, date_column, value_column, title="Monthly Sales Trends"):
    """
    Create a bar chart showing monthly sales trends.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    date_column : str
        Name of the date column
    value_column : str
        Name of the value column
    title : str
        Plot title
    
    Returns:
    --------
    fig, ax : matplotlib objects
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    df['Month'] = pd.to_datetime(df[date_column]).dt.month
    monthly_sales = df.groupby('Month')[value_column].sum()
    
    bars = ax.bar(monthly_sales.index, monthly_sales.values, color='coral')
    ax.set_xlabel('Month')
    ax.set_ylabel(value_column)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(1, 13))
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for month, val in monthly_sales.items():
        ax.text(month, val, f'${val:,.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    return fig, ax


def plot_heatmap(df, pivot_columns, value_column, title="Sales Heatmap"):
    """
    Create a heatmap of sales data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    pivot_columns : tuple
        (row_column, col_column) for pivot table
    value_column : str
        Name of the value column
    title : str
        Plot title
    
    Returns:
    --------
    fig, ax : matplotlib objects
    """
    pivot_df = df.pivot_table(
        values=value_column,
        index=pivot_columns[0],
        columns=pivot_columns[1],
        aggfunc='sum',
        fill_value=0
    )
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_df, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': value_column})
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig, ax


def save_figure(fig, filename, directory='reports/visualizations'):
    """
    Save a matplotlib figure to a file.
    
    Parameters:
    -----------
    fig : matplotlib figure
        Figure to save
    filename : str
        Name of the file
    directory : str
        Directory to save the figure
    """
    import os
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure to {filepath}")

