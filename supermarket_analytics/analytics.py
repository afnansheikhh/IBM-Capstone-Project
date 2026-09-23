import pandas as pd
import numpy as np

def calculate_sales(df):
    """
    Calculates Sales = Quantity * Unit Price and validates against existing column.
    """
    df_calc = df.copy()
    df_calc['Calculated_Sales'] = (df_calc['Quantity'] * df_calc['Unit Price']).round(2)
    
    if 'Sales' in df_calc.columns:
        diff = (df_calc['Calculated_Sales'] - df_calc['Sales'].round(2)).abs()
        discrepancies_count = int((diff > 0.05).sum())
        df_calc['Sales_Discrepancy'] = diff > 0.05
    else:
        discrepancies_count = 0
        df_calc['Sales'] = df_calc['Calculated_Sales']
        
    return df_calc, discrepancies_count

def get_kpi_metrics(df):
    """
    Calculates high-level business KPI metrics.
    """
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    total_sales = float(df[sales_col].sum())
    total_units = int(df['Quantity'].sum())
    total_orders = len(df)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    avg_rating = float(df['Rating'].mean()) if 'Rating' in df.columns else 0.0
    max_order = float(df[sales_col].max()) if total_orders > 0 else 0.0
    min_order = float(df[sales_col].min()) if total_orders > 0 else 0.0
    
    return {
        'total_revenue': total_sales,
        'total_units_sold': total_units,
        'total_transactions': total_orders,
        'avg_order_value': avg_order_value,
        'avg_rating': avg_rating,
        'max_order_value': max_order,
        'min_order_value': min_order
    }

def get_category_summary(df):
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    grouped = df.groupby('Category').agg(
        Transactions=('Invoice ID', 'count'),
        Total_Units=('Quantity', 'sum'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Ticket=(sales_col, 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    total_revenue = df[sales_col].sum()
    grouped['Revenue_Share_%'] = (grouped['Total_Sales'] / total_revenue * 100).round(2)
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Ticket'] = grouped['Avg_Ticket'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Total_Sales', ascending=False).reset_index(drop=True)

def get_branch_summary(df):
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    grouped = df.groupby(['Branch', 'City']).agg(
        Transactions=('Invoice ID', 'count'),
        Total_Units=('Quantity', 'sum'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Ticket=(sales_col, 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    total_revenue = df[sales_col].sum()
    grouped['Revenue_Share_%'] = (grouped['Total_Sales'] / total_revenue * 100).round(2)
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Ticket'] = grouped['Avg_Ticket'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Total_Sales', ascending=False).reset_index(drop=True)

def get_customer_summary(df):
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    grouped = df.groupby(['Customer Type', 'Gender']).agg(
        Transactions=('Invoice ID', 'count'),
        Total_Units=('Quantity', 'sum'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Ticket=(sales_col, 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    total_revenue = df[sales_col].sum()
    grouped['Revenue_Share_%'] = (grouped['Total_Sales'] / total_revenue * 100).round(2)
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Ticket'] = grouped['Avg_Ticket'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Total_Sales', ascending=False).reset_index(drop=True)

def get_payment_summary(df):
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    grouped = df.groupby('Payment').agg(
        Transactions=('Invoice ID', 'count'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Ticket=(sales_col, 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    total_revenue = df[sales_col].sum()
    grouped['Revenue_Share_%'] = (grouped['Total_Sales'] / total_revenue * 100).round(2)
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Ticket'] = grouped['Avg_Ticket'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Total_Sales', ascending=False).reset_index(drop=True)

def get_product_summary(df):
    """
    Summarizes individual product performance.
    """
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    grouped = df.groupby(['Product', 'Category']).agg(
        Transactions=('Invoice ID', 'count'),
        Total_Units=('Quantity', 'sum'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Price=('Unit Price', 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    total_revenue = df[sales_col].sum()
    grouped['Revenue_Share_%'] = (grouped['Total_Sales'] / total_revenue * 100).round(2)
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Price'] = grouped['Avg_Price'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Total_Sales', ascending=False).reset_index(drop=True)

def get_monthly_summary(df):
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in df.columns else 'Sales'
    df_temp = df.copy()
    if 'Month_Year' not in df_temp.columns and 'Date' in df_temp.columns:
        df_temp['Month_Year'] = pd.to_datetime(df_temp['Date']).dt.strftime('%Y-%m')
        
    grouped = df_temp.groupby('Month_Year').agg(
        Transactions=('Invoice ID', 'count'),
        Total_Units=('Quantity', 'sum'),
        Total_Sales=(sales_col, 'sum'),
        Avg_Ticket=(sales_col, 'mean'),
        Avg_Rating=('Rating', 'mean')
    ).reset_index()
    
    grouped['Total_Sales'] = grouped['Total_Sales'].round(2)
    grouped['Avg_Ticket'] = grouped['Avg_Ticket'].round(2)
    grouped['Avg_Rating'] = grouped['Avg_Rating'].round(2)
    
    return grouped.sort_values(by='Month_Year').reset_index(drop=True)

def simulate_growth_scenario(df, price_delta_pct=0.0, member_lift_pct=0.0, snack_cross_sell_lift_pct=0.0):
    """
    What-If Business Scenario Simulator:
    - price_delta_pct: change in general unit prices (-20% to +20%)
    - member_lift_pct: conversion of normal shoppers to members with estimated +10% order frequency
    - snack_cross_sell_lift_pct: lift in snack basket quantity through combos
    """
    sim_df = df.copy()
    sales_col = 'Calculated_Sales' if 'Calculated_Sales' in sim_df.columns else 'Sales'
    
    # 1. Price adjustment
    sim_df['Sim_Unit_Price'] = sim_df['Unit Price'] * (1 + price_delta_pct / 100.0)
    
    # 2. Snack cross sell lift
    is_snack = sim_df['Category'] == 'Snacks'
    sim_df['Sim_Quantity'] = sim_df['Quantity'].astype(float)
    sim_df.loc[is_snack, 'Sim_Quantity'] = sim_df.loc[is_snack, 'Quantity'] * (1 + snack_cross_sell_lift_pct / 100.0)
    
    # Base simulated sales
    sim_df['Sim_Sales'] = sim_df['Sim_Quantity'] * sim_df['Sim_Unit_Price']
    
    # 3. Membership conversion lift (boost Normal customer sales by member_lift_pct)
    is_normal = sim_df['Customer Type'] == 'Normal'
    membership_revenue_boost = (sim_df.loc[is_normal, 'Sim_Sales'].sum()) * (member_lift_pct / 100.0) * 0.12
    
    base_revenue = float(df[sales_col].sum())
    projected_revenue = float(sim_df['Sim_Sales'].sum()) + membership_revenue_boost
    revenue_delta = projected_revenue - base_revenue
    revenue_growth_pct = (revenue_delta / base_revenue) * 100 if base_revenue > 0 else 0.0
    
    return {
        'base_revenue': round(base_revenue, 2),
        'projected_revenue': round(projected_revenue, 2),
        'revenue_delta': round(revenue_delta, 2),
        'revenue_growth_pct': round(revenue_growth_pct, 2)
    }

def get_business_recommendations():
    return [
        {
            'title': '1. Product Bundling & Basket Optimization',
            'finding': 'Beverages (₹56.1K) and Personal Care (₹45.9K) drive high ticket sizes (>₹620), while Snacks has high transaction volume (75) with lower average spend (₹226.57).',
            'recommendation': 'Deploy high-margin snack displays at beverage coolers and checkout counters. Launch combo bundling promotions (e.g., Tea/Coffee + Biscuit/Chips combo at 15% discount) to elevate overall basket size.'
        },
        {
            'title': '2. Regional Strategy & Branch Turnaround',
            'finding': 'Mumbai (Branch C) leads sales at ₹72.5K (29.6% share) and 4.05★ rating, while Jaipur (Branch A) lags at ₹52.4K (21.4% share) with the lowest rating (3.84★).',
            'recommendation': "Conduct service audits and customer feedback sessions in Jaipur. Replicate Mumbai's merchandising layout and align Jaipur stock with top-selling Dairy and Beverage products."
        },
        {
            'title': '3. Loyalty Program & Customer Conversion',
            'finding': 'Members generate 58.5% of total revenue (₹143.0K), but Normal non-member shoppers spend more per transaction on average (₹497 vs ₹483).',
            'recommendation': 'Incentivize cashiers to convert Normal customers into Members during checkout by offering instant 5% welcome cashback or points towards their next purchase.'
        },
        {
            'title': '4. Digital Point-of-Sale Acceleration',
            'finding': 'Digital payment methods (UPI, Net Banking, and Cards) capture 77.9% of total store revenue (UPI leading at 27.8%).',
            'recommendation': 'Upgrade in-store QR code scanners and deploy quick-pay self-service terminals to eliminate queue bottlenecks during peak weekend traffic.'
        }
    ]
