"""
Data Cleaning Utilities

Functions to clean and preprocess e-commerce sales data.
"""

import pandas as pd
import numpy as np


def remove_duplicates(df):
    """
    Remove duplicate rows from a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with duplicates removed
    """
    initial_count = len(df)
    df_cleaned = df.drop_duplicates()
    final_count = len(df_cleaned)
    removed = initial_count - final_count
    
    if removed > 0:
        print(f"✓ Removed {removed} duplicate rows")
    else:
        print("✓ No duplicates found")
    
    return df_cleaned


def handle_missing_values(df, strategy='drop', columns=None):
    """
    Handle missing values in a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    strategy : str
        'drop' to drop rows with missing values
        'fill' to fill with appropriate values
    columns : list, optional
        Specific columns to handle. If None, handles all columns
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with missing values handled
    """
    if columns is None:
        columns = df.columns
    
    if strategy == 'drop':
        initial_count = len(df)
        df_cleaned = df.dropna(subset=columns)
        final_count = len(df_cleaned)
        removed = initial_count - final_count
        print(f"✓ Dropped {removed} rows with missing values")
        return df_cleaned
    else:
        df_cleaned = df.copy()
        for col in columns:
            if df_cleaned[col].dtype in ['int64', 'float64']:
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
            else:
                df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
        print("✓ Filled missing values")
        return df_cleaned


def standardize_date_column(df, date_column):
    """
    Convert a column to datetime format.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    date_column : str
        Name of the date column
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with standardized date column
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    print(f"✓ Converted '{date_column}' to datetime format")
    return df


def extract_date_features(df, date_column):
    """
    Extract year, month, day, and day_of_week from a date column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    date_column : str
        Name of the date column
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with extracted date features
    """
    df['Year'] = df[date_column].dt.year
    df['Month'] = df[date_column].dt.month
    df['Day'] = df[date_column].dt.day
    df['DayOfWeek'] = df[date_column].dt.day_name()
    
    print("✓ Extracted date features (Year, Month, Day, DayOfWeek)")
    return df


def remove_outliers(df, column, method='iqr'):
    """
    Remove outliers from a DataFrame using IQR method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Name of the column to check for outliers
    method : str
        'iqr' for Interquartile Range method
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with outliers removed
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    initial_count = len(df)
    df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    final_count = len(df_cleaned)
    removed = initial_count - final_count
    
    print(f"✓ Removed {removed} outliers from '{column}'")
    return df_cleaned


def clean_data(df):
    """
    Perform a complete data cleaning pipeline.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    
    Returns:
    --------
    pd.DataFrame
        Cleaned DataFrame
    """
    print("Starting data cleaning pipeline...")
    print("=" * 60)
    
    df_cleaned = df.copy()
    
    # Remove duplicates
    df_cleaned = remove_duplicates(df_cleaned)
    
    print("=" * 60)
    print("Data cleaning complete!")
    
    return df_cleaned

