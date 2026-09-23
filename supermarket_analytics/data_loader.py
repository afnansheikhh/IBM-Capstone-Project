import os
import pandas as pd

DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'SUPER MARKET DATA - supermarket_sales_500_rows.csv'
)

def load_data(uploaded_file=None):
    """
    Loads dataset from uploaded file buffer or fallback default CSV path.
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            pass
            
    if os.path.exists(DEFAULT_CSV_PATH):
        return pd.read_csv(DEFAULT_CSV_PATH)
    raise FileNotFoundError(f"Default dataset not found at {DEFAULT_CSV_PATH}")

def check_data_quality(df):
    """
    Audits the dataset for missing values, data types, and duplicates.
    """
    total_records = len(df)
    audit_rows = []
    
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        null_pct = round((null_count / total_records) * 100, 2) if total_records > 0 else 0.0
        audit_rows.append({
            'Column': col,
            'Data Type': str(df[col].dtype),
            'Missing Count': null_count,
            'Missing %': f"{null_pct}%",
            'Sample Value': str(df[col].iloc[0]) if total_records > 0 else ''
        })
        
    audit_df = pd.DataFrame(audit_rows)
    duplicates_count = int(df.duplicated().sum())
    
    return {
        'total_records': total_records,
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'audit_df': audit_df,
        'has_missing': audit_df['Missing Count'].sum() > 0,
        'duplicate_rows': duplicates_count
    }

def clean_data(df):
    """
    Cleans, standardizes and enriches the dataset.
    """
    df_clean = df.copy()
    
    # Strip string columns
    str_cols = df_clean.select_dtypes(include=['object']).columns
    for col in str_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        
    # Standardize Date column
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
        df_clean['Month_Year'] = df_clean['Date'].dt.strftime('%Y-%m')
        df_clean['Month_Name'] = df_clean['Date'].dt.strftime('%B')
        df_clean['Day_Name'] = df_clean['Date'].dt.strftime('%A')
        df_clean['Is_Weekend'] = df_clean['Date'].dt.dayofweek.isin([5, 6]).map({True: 'Weekend', False: 'Weekday'})

    # Ensure numeric columns
    numeric_cols = {
        'Quantity': 'int64',
        'Unit Price': 'float64',
        'Rating': 'float64',
        'Sales': 'float64'
    }
    for col, dtype in numeric_cols.items():
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype(dtype)
            
    return df_clean
