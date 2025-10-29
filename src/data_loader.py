"""
Data Loading Utilities

Functions to load and inspect e-commerce sales data from various formats.
"""

import pandas as pd
import os
from pathlib import Path


def load_csv(file_path, encoding='utf-8'):
    """
    Load a CSV file into a pandas DataFrame.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    encoding : str, optional
        File encoding (default 'utf-8')
    
    Returns:
    --------
    pd.DataFrame
        Loaded data as a DataFrame
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"✓ Successfully loaded data from {file_path}")
        print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        raise


def load_excel(file_path, sheet_name=0):
    """
    Load an Excel file into a pandas DataFrame.
    
    Parameters:
    -----------
    file_path : str
        Path to the Excel file
    sheet_name : int or str
        Sheet name or index to read
    
    Returns:
    --------
    pd.DataFrame
        Loaded data as a DataFrame
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"✓ Successfully loaded data from {file_path}")
        print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        raise


def inspect_dataframe(df):
    """
    Print basic information about a DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to inspect
    """
    print("=" * 60)
    print("DATA INSPECTION")
    print("=" * 60)
    
    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"\n📋 Columns:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        print(f"  - {col} ({dtype}) - {null_count} nulls")
    
    print(f"\n📈 Summary Statistics:")
    print(df.describe())
    
    print(f"\n🔍 First Few Rows:")
    print(df.head())


def get_raw_data_path(filename):
    """
    Get the full path to a file in the raw data directory.
    
    Parameters:
    -----------
    filename : str
        Name of the file
    
    Returns:
    --------
    str
        Full path to the file
    """
    project_root = Path(__file__).parent.parent
    return os.path.join(project_root, "data", "raw", filename)


def get_processed_data_path(filename):
    """
    Get the full path to a file in the processed data directory.
    
    Parameters:
    -----------
    filename : str
        Name of the file
    
    Returns:
    --------
    str
        Full path to the file
    """
    project_root = Path(__file__).parent.parent
    return os.path.join(project_root, "data", "processed", filename)

