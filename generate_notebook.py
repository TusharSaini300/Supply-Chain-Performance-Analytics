import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Supply Chain Performance Analytics\n",
    "\n",
    "This notebook contains the Exploratory Data Analysis (EDA) and Business KPI reporting for a 100-SKU supply chain dataset. \n",
    "The analysis is structured in five phases:\n",
    "- **Phase 1: Load & Clean**\n",
    "- **Phase 2: Feature Engineering**\n",
    "- **Phase 3: EDA & KPIs**\n",
    "- **Phase 4: Visualizations**\n",
    "- **Phase 5: Insights & Deliverables**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 0: Working Assumptions & Data Dictionary\n",
    "\n",
    "Given the lack of official documentation, we establish the following working assumptions:\n",
    "1. **Lead Time Columns**:\n",
    "   - `lead_times`: Supplier-to-warehouse delivery lead time (in days).\n",
    "   - `lead_time`: End-to-end customer order-to-delivery fulfillment lead time (in days).\n",
    "   - `manufacturing_lead_time`: Supplier production lead time (in days).\n",
    "2. **Cost Columns**:\n",
    "   - `manufacturing_costs`: Unit-level direct manufacturing cost.\n",
    "   - `shipping_costs`: Unit-level transport cost.\n",
    "   - `costs`: Route-level logistics freight cost (transaction/lane cost, not unit-level).\n",
    "3. **Data Limitations**:\n",
    "   - No product-name column (analysis conducted at SKU level).\n",
    "   - No temporal column (no time-series trends possible)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 1: Load & Clean"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "DATA_PATH = r'data/supply_chain_data.csv'\n",
    "\n",
    "# Load data\n",
    "print(f\"Loading data from: {DATA_PATH}\")\n",
    "df = pd.read_csv(DATA_PATH)\n",
    "\n",
    "# Check shape and duplicates\n",
    "print(f\"Shape: {df.shape[0]} rows, {df.shape[1]} columns\")\n",
    "print(f\"Duplicate Rows: {df.duplicated().sum()}\")\n",
    "\n",
    "# Check nulls\n",
    "print(\"\\nNull count per column:\")\n",
    "print(df.isnull().sum())\n",
    "\n",
    "# Standardize columns\n",
    "original_cols = list(df.columns)\n",
    "df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')\n",
    "print(\"\\nColumns standardized to snake_case.\")\n",
    "\n",
    "df.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 2: Feature Engineering"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create copy\n",
    "df_feat = df.copy()\n",
    "\n",
    "# 1. Realized price per unit\n",
    "df_feat['revenue_per_unit'] = df_feat['revenue_generated'] / df_feat['number_of_products_sold']\n",
    "\n",
    "# 2. Gross Unit Profit (listed price)\n",
    "df_feat['gross_unit_profit'] = df_feat['price'] - df_feat['manufacturing_costs']\n",
    "\n",
    "# 3. Gross Profit Margin (%)\n",
    "df_feat['gross_profit_margin_pct'] = df_feat['gross_unit_profit'] / df_feat['price']\n",
    "\n",
    "# 4. Net Unit Profit (including unit shipping)\n",
    "df_feat['net_unit_profit'] = df_feat['price'] - df_feat['manufacturing_costs'] - df_feat['shipping_costs']\n",
    "\n",
    "# 5. Net Profit Margin (%)\n",
    "df_feat['net_profit_margin_pct'] = df_feat['net_unit_profit'] / df_feat['price']\n",
    "\n",
    "# 6. Total Mfg Cost\n",
    "df_feat['total_manufacturing_cost'] = df_feat['manufacturing_costs'] * df_feat['production_volumes']\n",
    "\n",
    "# 7. Stock-to-Sales Ratio\n",
    "df_feat['stock_to_sales_ratio'] = df_feat['stock_levels'] / df_feat['number_of_products_sold']\n",
    "\n",
    "# 8. Late Delivery Flag\n",
    "df_feat['is_late_delivery'] = (df_feat['shipping_times'] > 7).astype(int)\n",
    "\n",
    "print(\"Engineered Features Summary:\")\n",
    "print(df_feat[['revenue_per_unit', 'gross_unit_profit', 'gross_profit_margin_pct', 'net_unit_profit', 'net_profit_margin_pct', 'stock_to_sales_ratio', 'is_late_delivery']].describe())\n",
    "\n",
    "# Discrepancy Checks\n",
    "neg_gross = df_feat[df_feat['gross_unit_profit'] < 0]\n",
    "print(f\"\\nSKUs with manufacturing cost exceeding list price: {len(neg_gross)} out of {len(df_feat)}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 3: EDA & KPIs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"--- 1. FINANCIAL KPIs ---\")\n",
    "total_rev = df_feat['revenue_generated'].sum()\n",
    "total_mfg_sold = (df_feat['manufacturing_costs'] * df_feat['number_of_products_sold']).sum()\n",
    "total_ship_sold = (df_feat['shipping_costs'] * df_feat['number_of_products_sold']).sum()\n",
    "total_route_freight = df_feat['costs'].sum()\n",
    "total_cost = total_mfg_sold + total_ship_sold + total_route_freight\n",
    "net_profit = total_rev - total_cost\n",
    "margin_pct = (net_profit / total_rev) * 100\n",
    "\n",
    "print(f\"Total Revenue: ${total_rev:,.2f}\")\n",
    "print(f\"Total COGS (Manufacturing): ${total_mfg_sold:,.2f}\")\n",
    "print(f\"Total Shipping Cost (Sold Units): ${total_ship_sold:,.2f}\")\n",
    "print(f\"Total Route Freight Cost: ${total_route_freight:,.2f}\")\n",
    "print(f\"Total Supply Chain Cost: ${total_cost:,.2f}\")\n",
    "print(f\"Net Supply Chain Profit: ${net_profit:,.2f}\")\n",
    "print(f\"Overall Profit Margin: {margin_pct:.2f}%\")\n",
    "\n",
    "print(\"\\n--- 2. INVENTORY KPIs ---\")\n",
    "print(f\"Average Stock Level: {df_feat['stock_levels'].mean():.2f} units\")\n",
    "print(f\"Average Product Availability: {df_feat['availability'].mean():.2f}%\")\n",
    "print(f\"Average Stock-to-Sales Ratio: {df_feat['stock_to_sales_ratio'].mean():.4f}\")\n",
    "\n",
    "print(\"\\nInventory Metrics by Product Type:\")\n",
    "print(df_feat.groupby('product_type')[['stock_levels', 'availability', 'stock_to_sales_ratio']].mean())\n",
    "\n",
    "print(\"\\n--- 3. SUPPLIER PERFORMANCE ---\")\n",
    "print(df_feat.groupby('supplier_name').agg(\n",
    "    avg_defect_rate=('defect_rates', 'mean'),\n",
    "    avg_lead_times=('lead_times', 'mean'),\n",
    "    total_production_volume=('production_volumes', 'sum'),\n",
    "    sku_count=('sku', 'count')\n",
    "))\n",
    "\n",
    "print(\"\\n--- 4. CARRIER & ROUTE PERFORMANCE ---\")\n",
    "carrier_stats = df_feat.groupby('shipping_carriers').agg(\n",
    "    avg_shipping_cost=('shipping_costs', 'mean'),\n",
    "    avg_shipping_time=('shipping_times', 'mean'),\n",
    "    late_delivery_rate=('is_late_delivery', 'mean')\n",
    ")\n",
    "carrier_stats['late_delivery_rate'] *= 100\n",
    "print(carrier_stats)\n",
    "\n",
    "print(\"\\nRoute & Mode Logistics Cost Analysis:\")\n",
    "print(df_feat.groupby(['routes', 'transportation_modes'])['costs'].mean().unstack())\n",
    "\n",
    "print(\"\\n--- 5. QUALITY CONTROL ANALYSIS ---\")\n",
    "print(\"Inspection Results Counts:\")\n",
    "print(df_feat['inspection_results'].value_counts())\n",
    "print(\"\\nAverage Defect Rate by Inspection Result:\")\n",
    "print(df_feat.groupby('inspection_results')['defect_rates'].mean())\n",
    "\n",
    "print(\"\\n--- 6. CORRELATION NOISE DETECTION ---\")\n",
    "numeric_corr = df_feat.select_dtypes(include='number').corr()\n",
    "corr_pairs = numeric_corr.unstack().sort_values(ascending=False)\n",
    "corr_pairs = corr_pairs[corr_pairs < 1.0].drop_duplicates()\n",
    "print(\"Top Positive Correlations:\")\n",
    "print(corr_pairs.head(3))\n",
    "print(\"\\nTop Negative Correlations:\")\n",
    "print(corr_pairs.tail(3))\n",
    "weak_corrs = corr_pairs[corr_pairs.abs() < 0.2]\n",
    "print(f\"\\nStatistical Noise Flag: There are {len(weak_corrs)} correlation pairs with |r| < 0.2. With N=100, these are likely noise.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Phase 4: Visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12})\n",
    "\n",
    "# Chart 1: Revenue vs Volume Sold\n",
    "product_stats = df_feat.groupby('product_type').agg(\n",
    "    total_sales=('number_of_products_sold', 'sum'),\n",
    "    total_revenue=('revenue_generated', 'sum')\n",
    ").reset_index()\n",
    "\n",
    "fig, ax1 = plt.subplots(figsize=(8, 4.5))\n",
    "color = '#1f77b4'\n",
    "ax1.set_xlabel('Product Type')\n",
    "ax1.set_ylabel('Total Units Sold', color=color)\n",
    "bars = ax1.bar(product_stats['product_type'], product_stats['total_sales'], color=color, alpha=0.7, width=0.4)\n",
    "ax1.tick_params(axis='y', labelcolor=color)\n",
    "\n",
    "ax2 = ax1.twinx()\n",
    "color = '#d62728'\n",
    "ax2.set_ylabel('Total Revenue ($)', color=color)\n",
    "line = ax2.plot(product_stats['product_type'], product_stats['total_revenue'], color=color, marker='o', linewidth=2)\n",
    "ax2.tick_params(axis='y', labelcolor=color)\n",
    "\n",
    "plt.title('Product Performance: Sales Volume vs Revenue')\n",
    "plt.show()\n",
    "\n",
    "# Chart 2: Correlation Heatmap\n",
    "cols_to_corr = ['price', 'number_of_products_sold', 'revenue_generated', 'stock_levels', 'lead_times', 'shipping_times', 'shipping_costs', 'lead_time', 'production_volumes', 'manufacturing_lead_time', 'manufacturing_costs', 'defect_rates', 'costs']\n",
    "corr_matrix = df_feat[cols_to_corr].corr()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 7))\n",
    "cax = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)\n",
    "fig.colorbar(cax)\n",
    "ticks = np.arange(len(cols_to_corr))\n",
    "ax.set_xticks(ticks)\n",
    "ax.set_yticks(ticks)\n",
    "ax.set_xticklabels([c.replace('_', ' ').title() for c in cols_to_corr], rotation=90)\n",
    "ax.set_yticklabels([c.replace('_', ' ').title() for c in cols_to_corr])\n",
    "plt.title('Correlation Matrix of Key Numerical Variables')\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open(r'C:\Users\Tushar Saini\.gemini\antigravity\scratch\supply_chain_analytics\supply_chain_notebook.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("Jupyter Notebook file generated successfully.")
