"""
Supply Chain Performance Analytics
===================================
A business analytics project analyzing supply chain data for 100 SKUs
across skincare, haircare, and cosmetics categories.

Business Questions Addressed:
1. Which product categories generate the most revenue?
2. Which products are loss-making?
3. Which suppliers have the highest defect rates?
4. Which shipping carrier is most cost-efficient?
5. Which suppliers have the longest manufacturing lead times?

Tools: Python, Pandas, NumPy, Matplotlib
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving charts
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'supply_chain_data.csv')
CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'images', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

# Consistent chart styling
plt.rcParams.update({
    'figure.figsize': (9, 5),
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 150,
})

# =========================================================================
# STEP 1: DATA LOADING & CLEANING
# =========================================================================
print("=" * 70)
print("STEP 1: DATA LOADING & CLEANING")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

# Standardize column names to snake_case for consistency
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"\nNull counts per column:")
print(df.isnull().sum().to_string())
print(f"\nProduct types: {sorted(df['product_type'].unique())}")
print(f"Suppliers: {sorted(df['supplier_name'].unique())}")
print(f"Carriers: {sorted(df['shipping_carriers'].unique())}")

# =========================================================================
# STEP 2: FEATURE ENGINEERING
# =========================================================================
print("\n" + "=" * 70)
print("STEP 2: FEATURE ENGINEERING")
print("=" * 70)

# Unit Gross Profit = Selling Price - Manufacturing Cost
# This is a standard business metric: how much profit each unit generates
# before logistics, overhead, or other costs.
df['unit_gross_profit'] = df['price'] - df['manufacturing_costs']

print("Created: unit_gross_profit = price - manufacturing_costs")
print(f"  Mean: ${df['unit_gross_profit'].mean():.2f}")
print(f"  Min:  ${df['unit_gross_profit'].min():.2f}")
print(f"  Max:  ${df['unit_gross_profit'].max():.2f}")

profitable_count = (df['unit_gross_profit'] >= 0).sum()
loss_count = (df['unit_gross_profit'] < 0).sum()
print(f"\nProfitable SKUs: {profitable_count} | Loss-making SKUs: {loss_count}")

# =========================================================================
# STEP 3: EXPLORATORY ANALYSIS & BUSINESS QUESTIONS
# =========================================================================
print("\n" + "=" * 70)
print("STEP 3: EXPLORATORY ANALYSIS")
print("=" * 70)

# --- Q1: Which product categories generate the most revenue? ---
print("\n--- Q1: Revenue by Product Category ---")
revenue_by_category = (
    df.groupby('product_type')['revenue_generated']
    .agg(['sum', 'mean', 'count'])
    .rename(columns={'sum': 'total_revenue', 'mean': 'avg_revenue', 'count': 'sku_count'})
    .sort_values('total_revenue', ascending=False)
)
print(revenue_by_category.to_string())

print("\n  Top 10 SKUs by Revenue:")
top10_revenue = df.nlargest(10, 'revenue_generated')[['sku', 'product_type', 'revenue_generated']]
print(top10_revenue.to_string(index=False))

# --- Q2: Which products are loss-making? ---
print("\n--- Q2: Product Profitability (Unit Gross Profit) ---")
print("\n  Average Unit Gross Profit by Category:")
profit_by_category = (
    df.groupby('product_type')['unit_gross_profit']
    .mean()
    .sort_values(ascending=False)
)
print(profit_by_category.to_string())

print("\n  Top 5 SKUs by Unit Gross Profit:")
top5_profit = df.nlargest(5, 'unit_gross_profit')[['sku', 'product_type', 'price', 'manufacturing_costs', 'unit_gross_profit']]
print(top5_profit.to_string(index=False))

print("\n  Bottom 5 SKUs by Unit Gross Profit (Loss-makers):")
bottom5_profit = df.nsmallest(5, 'unit_gross_profit')[['sku', 'product_type', 'price', 'manufacturing_costs', 'unit_gross_profit']]
print(bottom5_profit.to_string(index=False))

# --- Q3: Which suppliers have the highest defect rates? ---
print("\n--- Q3: Defect Rate by Supplier ---")
defect_by_supplier = (
    df.groupby('supplier_name')['defect_rates']
    .mean()
    .sort_values(ascending=False)
)
print(defect_by_supplier.to_string())

print("\n  Average Defect Rate by Product Category:")
defect_by_category = (
    df.groupby('product_type')['defect_rates']
    .mean()
    .sort_values(ascending=False)
)
print(defect_by_category.to_string())

# --- Q4: Which shipping carrier is most cost-efficient? ---
print("\n--- Q4: Shipping Cost by Carrier ---")
shipping_by_carrier = (
    df.groupby('shipping_carriers')['shipping_costs']
    .agg(['mean', 'min', 'max'])
    .rename(columns={'mean': 'avg_cost', 'min': 'min_cost', 'max': 'max_cost'})
    .sort_values('avg_cost')
)
print(shipping_by_carrier.to_string())

# --- Q5: Which suppliers have the longest manufacturing lead times? ---
print("\n--- Q5: Manufacturing Lead Time by Supplier ---")
leadtime_by_supplier = (
    df.groupby('supplier_name')['manufacturing_lead_time']
    .mean()
    .sort_values(ascending=False)
)
print(leadtime_by_supplier.to_string())

print("\n  Average Manufacturing Lead Time by Product Category:")
leadtime_by_category = (
    df.groupby('product_type')['manufacturing_lead_time']
    .mean()
    .sort_values(ascending=False)
)
print(leadtime_by_category.to_string())

# =========================================================================
# STEP 4: VISUALIZATIONS
# =========================================================================
print("\n" + "=" * 70)
print("STEP 4: VISUALIZATIONS")
print("=" * 70)

# --- Chart 1: Revenue by Product Category ---
fig, ax = plt.subplots()
data = revenue_by_category['total_revenue'].sort_values()
bars = ax.barh(data.index, data.values, color=['#4C72B0', '#55A868', '#C44E52'])
ax.set_xlabel('Total Revenue ($)')
ax.set_title('Total Revenue by Product Category')
# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 500, bar.get_y() + bar.get_height()/2,
            f'${width:,.0f}', va='center', fontsize=9)
ax.set_xlim(0, data.max() * 1.15)
fig.tight_layout()
path1 = os.path.join(CHARTS_DIR, 'revenue_by_category.png')
plt.savefig(path1)
plt.close()
print(f"  Saved: {path1}")

# --- Chart 2: Top 10 SKUs by Revenue ---
fig, ax = plt.subplots()
data = top10_revenue.sort_values('revenue_generated')
bars = ax.barh(data['sku'], data['revenue_generated'], color='#4C72B0')
ax.set_xlabel('Revenue Generated ($)')
ax.set_title('Top 10 SKUs by Revenue')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 100, bar.get_y() + bar.get_height()/2,
            f'${width:,.0f}', va='center', fontsize=8)
ax.set_xlim(0, data['revenue_generated'].max() * 1.12)
fig.tight_layout()
path2 = os.path.join(CHARTS_DIR, 'top10_skus_revenue.png')
plt.savefig(path2)
plt.close()
print(f"  Saved: {path2}")

# --- Chart 3: Average Shipping Cost by Carrier ---
fig, ax = plt.subplots()
data = shipping_by_carrier['avg_cost'].sort_values()
bars = ax.bar(data.index, data.values, color=['#55A868', '#4C72B0', '#C44E52'], width=0.5)
ax.set_ylabel('Average Shipping Cost ($)')
ax.set_title('Average Shipping Cost by Carrier')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.05,
            f'${height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylim(0, data.max() * 1.15)
fig.tight_layout()
path3 = os.path.join(CHARTS_DIR, 'shipping_cost_by_carrier.png')
plt.savefig(path3)
plt.close()
print(f"  Saved: {path3}")

# --- Chart 4: Average Manufacturing Lead Time by Supplier ---
fig, ax = plt.subplots()
data = leadtime_by_supplier.sort_values()
bars = ax.barh(data.index, data.values, color='#DD8452')
ax.set_xlabel('Average Manufacturing Lead Time (Days)')
ax.set_title('Average Manufacturing Lead Time by Supplier')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
            f'{width:.1f} days', va='center', fontsize=9)
ax.set_xlim(0, data.max() * 1.2)
fig.tight_layout()
path4 = os.path.join(CHARTS_DIR, 'leadtime_by_supplier.png')
plt.savefig(path4)
plt.close()
print(f"  Saved: {path4}")

# --- Chart 5: Average Defect Rate by Supplier ---
fig, ax = plt.subplots()
data = defect_by_supplier.sort_values()
bars = ax.barh(data.index, data.values, color='#C44E52')
ax.set_xlabel('Average Defect Rate (%)')
ax.set_title('Average Defect Rate by Supplier')
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.03, bar.get_y() + bar.get_height()/2,
            f'{width:.2f}%', va='center', fontsize=9)
ax.set_xlim(0, data.max() * 1.2)
fig.tight_layout()
path5 = os.path.join(CHARTS_DIR, 'defect_rate_by_supplier.png')
plt.savefig(path5)
plt.close()
print(f"  Saved: {path5}")

# =========================================================================
# STEP 5: SUMMARY
# =========================================================================
print("\n" + "=" * 70)
print("STEP 5: SUMMARY OF KEY FINDINGS")
print("=" * 70)

total_rev = df['revenue_generated'].sum()
top_category = revenue_by_category['total_revenue'].idxmax()
top_cat_rev = revenue_by_category.loc[top_category, 'total_revenue']
top_cat_pct = (top_cat_rev / total_rev) * 100

print(f"\n1. REVENUE: Total revenue across all SKUs is ${total_rev:,.2f}.")
print(f"   {top_category.title()} leads with ${top_cat_rev:,.2f} ({top_cat_pct:.1f}% of total).")

print(f"\n2. PROFITABILITY: {loss_count} out of 100 SKUs are loss-making (unit_gross_profit < 0).")
worst_sku = df.loc[df['unit_gross_profit'].idxmin()]
print(f"   Worst: {worst_sku['sku']} loses ${abs(worst_sku['unit_gross_profit']):.2f} per unit")
print(f"   (Price: ${worst_sku['price']:.2f}, Manufacturing Cost: ${worst_sku['manufacturing_costs']:.2f}).")

worst_supplier = defect_by_supplier.idxmax()
best_supplier = defect_by_supplier.idxmin()
print(f"\n3. DEFECT RATES: {worst_supplier} has the highest average defect rate ({defect_by_supplier.max():.2f}%).")
print(f"   {best_supplier} has the lowest ({defect_by_supplier.min():.2f}%).")

cheapest_carrier = shipping_by_carrier['avg_cost'].idxmin()
costliest_carrier = shipping_by_carrier['avg_cost'].idxmax()
print(f"\n4. SHIPPING: {cheapest_carrier} is the most cost-efficient (avg ${shipping_by_carrier.loc[cheapest_carrier, 'avg_cost']:.2f}).")
print(f"   {costliest_carrier} is the most expensive (avg ${shipping_by_carrier.loc[costliest_carrier, 'avg_cost']:.2f}).")

slowest_supplier = leadtime_by_supplier.idxmax()
fastest_supplier = leadtime_by_supplier.idxmin()
print(f"\n5. LEAD TIME: {slowest_supplier} has the longest avg manufacturing lead time ({leadtime_by_supplier.max():.1f} days).")
print(f"   {fastest_supplier} has the shortest ({leadtime_by_supplier.min():.1f} days).")

print("\nAnalysis complete. Charts saved to images/charts/")
