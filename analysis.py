import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define file paths
DATA_PATH = r"C:\Users\Tushar Saini\.gemini\antigravity\scratch\supply_chain_analytics\data\supply_chain_data.csv"
CHARTS_DIR = r"C:\Users\Tushar Saini\.gemini\antigravity\scratch\supply_chain_analytics\images\charts"

os.makedirs(CHARTS_DIR, exist_ok=True)

def run_phase_1():
    print("="*80)
    print("PHASE 1: LOAD & CLEAN")
    print("="*80)
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("Data loaded and cleaned.")
    return df

def run_phase_2(df):
    print("\n" + "="*80)
    print("PHASE 2: FEATURE ENGINEERING")
    print("="*80)
    df = df.copy()
    df['revenue_per_unit'] = df['revenue_generated'] / df['number_of_products_sold']
    df['gross_unit_profit'] = df['price'] - df['manufacturing_costs']
    df['gross_profit_margin_pct'] = (df['price'] - df['manufacturing_costs']) / df['price']
    df['net_unit_profit'] = df['price'] - df['manufacturing_costs'] - df['shipping_costs']
    df['net_profit_margin_pct'] = (df['price'] - df['manufacturing_costs'] - df['shipping_costs']) / df['price']
    df['total_manufacturing_cost'] = df['manufacturing_costs'] * df['production_volumes']
    df['stock_to_sales_ratio'] = df['stock_levels'] / df['number_of_products_sold']
    df['is_late_delivery'] = (df['shipping_times'] > 7).astype(int)
    print("Features engineered.")
    return df

def run_phase_3(df):
    print("\n" + "="*80)
    print("PHASE 3: EDA & KPIs")
    print("="*80)
    
    total_revenue = df['revenue_generated'].sum()
    total_mfg_cost_sold = (df['manufacturing_costs'] * df['number_of_products_sold']).sum()
    total_ship_cost_sold = (df['shipping_costs'] * df['number_of_products_sold']).sum()
    total_route_cost = df['costs'].sum()
    total_sc_cost = total_mfg_cost_sold + total_ship_cost_sold + total_route_cost
    net_sc_profit = total_revenue - total_sc_cost
    profit_margin_pct = (net_sc_profit / total_revenue) * 100
    
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total SC Cost: ${total_sc_cost:,.2f}")
    print(f"Net SC Profit: ${net_sc_profit:,.2f}")
    print(f"Overall Profit Margin: {profit_margin_pct:.2f}%")
    return df

def run_phase_4(df):
    print("\n" + "="*80)
    print("PHASE 4: VISUALIZATIONS")
    print("="*80)
    
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'figure.titlesize': 14
    })
    
    # -------------------------------------------------------------
    # Chart 1: Revenue vs Volume Sold by Product Type (Dual-Axis)
    # -------------------------------------------------------------
    print("Generating Chart 1: Revenue vs Volume Sold by Product Type...")
    product_stats = df.groupby('product_type').agg(
        total_sales=('number_of_products_sold', 'sum'),
        total_revenue=('revenue_generated', 'sum')
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    color = '#1f77b4'
    ax1.set_xlabel('Product Type')
    ax1.set_ylabel('Total Units Sold', color=color)
    bars = ax1.bar(product_stats['product_type'], product_stats['total_sales'], color=color, alpha=0.7, width=0.4, label='Units Sold')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, height + 500, f'{int(height):,}', ha='center', va='bottom', color=color, fontweight='bold')
        
    ax2 = ax1.twinx()  
    color = '#d62728'
    ax2.set_ylabel('Total Revenue Generated ($)', color=color)
    line = ax2.plot(product_stats['product_type'], product_stats['total_revenue'], color=color, marker='o', linewidth=2, label='Revenue')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Add values on line points
    for i, txt in enumerate(product_stats['total_revenue']):
        ax2.annotate(f"${txt:,.0f}", (product_stats['product_type'][i], product_stats['total_revenue'][i]), textcoords="offset points", xytext=(0,10), ha='center', color=color, fontweight='bold')
        
    plt.title('Product Category Performance: Total Units Sold vs. Revenue Generated', pad=20)
    fig.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, "revenue_vs_volume.png")
    plt.savefig(chart1_path, dpi=150)
    plt.close()
    print(f"  Saved: {chart1_path}")
    
    # -------------------------------------------------------------
    # Chart 2: Carrier Performance (Cost, Speed & Reliability)
    # -------------------------------------------------------------
    print("Generating Chart 2: Carrier Performance Analysis...")
    carrier_stats = df.groupby('shipping_carriers').agg(
        avg_cost=('shipping_costs', 'mean'),
        avg_time=('shipping_times', 'mean'),
        late_rate=('is_late_delivery', 'mean')
    ).reset_index()
    carrier_stats['late_rate'] *= 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left subplot: Cost vs Speed
    x = np.arange(len(carrier_stats['shipping_carriers']))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, carrier_stats['avg_cost'], width, label='Avg Shipping Cost ($)', color='#2ca02c')
    rects2 = ax1.bar(x + width/2, carrier_stats['avg_time'], width, label='Avg Shipping Time (Days)', color='#ff7f0e')
    
    ax1.set_title('Carrier Cost vs. Delivery Speed Tradeoff')
    ax1.set_xticks(x)
    ax1.set_xticklabels(carrier_stats['shipping_carriers'])
    ax1.legend()
    
    # Add labels on bars
    for rect in rects1:
        height = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2.0, height + 0.1, f'${height:.2f}', ha='center', va='bottom', fontsize=8)
    for rect in rects2:
        height = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2.0, height + 0.1, f'{height:.1f}d', ha='center', va='bottom', fontsize=8)
        
    # Right subplot: Late Delivery Rate
    bars_late = ax2.bar(carrier_stats['shipping_carriers'], carrier_stats['late_rate'], color='#9467bd', alpha=0.85, width=0.5)
    ax2.set_title('Late Delivery Rate by Carrier (> 7 Days)')
    ax2.set_ylabel('Late Delivery Rate (%)')
    ax2.set_ylim(0, 50)
    
    for bar in bars_late:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, height + 1, f'{height:.1f}%', ha='center', va='bottom', color='#4b0082', fontweight='bold')
        
    plt.suptitle('Shipping Carrier Performance Evaluation', y=0.98)
    fig.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, "carrier_performance.png")
    plt.savefig(chart2_path, dpi=150)
    plt.close()
    print(f"  Saved: {chart2_path}")
    
    # -------------------------------------------------------------
    # Chart 3: Supplier Quality vs Production Lead Time
    # -------------------------------------------------------------
    print("Generating Chart 3: Supplier Performance Plot...")
    supplier_stats = df.groupby('supplier_name').agg(
        avg_defect_rate=('defect_rates', 'mean'),
        avg_mfg_lead_time=('manufacturing_lead_time', 'mean'),
        sku_count=('sku', 'count'),
        total_prod=('production_volumes', 'sum')
    ).reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    # Plot bubble chart
    scatter = ax.scatter(
        supplier_stats['avg_mfg_lead_time'],
        supplier_stats['avg_defect_rate'],
        s=supplier_stats['total_prod']/20.0, # size represents production volume
        alpha=0.6,
        c=supplier_stats['avg_defect_rate'],
        cmap='YlOrRd',
        edgecolors='black'
    )
    
    # Annotate suppliers
    for i, row in supplier_stats.iterrows():
        ax.annotate(row['supplier_name'], (row['avg_mfg_lead_time'], row['avg_defect_rate']), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')
        
    ax.set_xlabel('Average Manufacturing Lead Time (Days)')
    ax.set_ylabel('Average Defect Rate (%)')
    ax.set_title('Supplier Analysis: Quality vs. Lead Time (Bubble Size = Production Volume)')
    
    # Grid and tight layout
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    chart3_path = os.path.join(CHARTS_DIR, "supplier_quality_leadtime.png")
    plt.savefig(chart3_path, dpi=150)
    plt.close()
    print(f"  Saved: {chart3_path}")
    
    # -------------------------------------------------------------
    # Chart 4: Correlation Matrix Heatmap
    # -------------------------------------------------------------
    print("Generating Chart 4: Correlation Matrix Heatmap...")
    cols_to_corr = [
        'price', 'number_of_products_sold', 'revenue_generated', 
        'stock_levels', 'lead_times', 'shipping_times', 'shipping_costs', 
        'lead_time', 'production_volumes', 'manufacturing_lead_time', 
        'manufacturing_costs', 'defect_rates', 'costs'
    ]
    corr_matrix = df[cols_to_corr].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax)
    
    # Set labels
    ticks = np.arange(len(cols_to_corr))
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    
    # Clean variable names for labels
    clean_labels = [col.replace('_', ' ').title() for col in cols_to_corr]
    ax.set_xticklabels(clean_labels, rotation=90)
    ax.set_yticklabels(clean_labels)
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(cols_to_corr)):
        for j in range(len(cols_to_corr)):
            text = ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                           ha="center", va="center", color="black" if abs(corr_matrix.iloc[i, j]) < 0.5 else "white", fontsize=8)
            
    plt.title('Correlation Matrix of Key Numerical Variables', pad=20)
    fig.tight_layout()
    chart4_path = os.path.join(CHARTS_DIR, "correlation_matrix.png")
    plt.savefig(chart4_path, dpi=150)
    plt.close()
    print(f"  Saved: {chart4_path}")
    
    print("\nPhase 4 Completed Successfully.")
    return df

if __name__ == "__main__":
    df = run_phase_1()
    df = run_phase_2(df)
    df = run_phase_3(df)
    df = run_phase_4(df)
