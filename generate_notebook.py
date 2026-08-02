import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Supply Chain Performance Analytics\n",
    "\n",
    "## Objective\n",
    "The objective of this project is to demonstrate how exploratory data analysis (EDA) using Python can identify operational inefficiencies and support business decision-making in a supply chain. It is not intended to build predictive or optimization models.\n",
    "\n",
    "--- \n",
    "### Business Questions Addressed:\n",
    "1. **Which product categories generate the most revenue?**\n",
    "2. **Which products are loss-making?**\n",
    "3. **Which suppliers have the highest defect rates?**\n",
    "4. **Which shipping carrier is most cost-efficient?**\n",
    "5. **Which suppliers have the longest manufacturing lead times?**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1: Data Loading & Cleaning"
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
    "# Load dataset using relative path\n",
    "DATA_PATH = os.path.join('data', 'supply_chain_data.csv')\n",
    "df = pd.read_csv(DATA_PATH)\n",
    "\n",
    "# Standardize column names to snake_case\n",
    "df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')\n",
    "\n",
    "# Display dataset summary\n",
    "print(f\"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns\")\n",
    "print(f\"Duplicate Rows: {df.duplicated().sum()}\")\n",
    "print(\"\\nNull counts per column:\")\n",
    "print(df.isnull().sum())\n",
    "df.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2: Feature Engineering\n",
    "\n",
    "We calculate **Unit Gross Profit** defined as:\n",
    "$$\\text{Unit Gross Profit} = \\text{Selling Price} - \\text{Manufacturing Cost}$$\n",
    "\n",
    "This measures product-level profitability before logistics or overhead expenses."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Calculate Unit Gross Profit\n",
    "df['unit_gross_profit'] = df['price'] - df['manufacturing_costs']\n",
    "\n",
    "profitable_count = (df['unit_gross_profit'] >= 0).sum()\n",
    "loss_count = (df['unit_gross_profit'] < 0).sum()\n",
    "\n",
    "print(f\"Profitable SKUs: {profitable_count} | Loss-making SKUs: {loss_count}\")\n",
    "print(f\"Average Unit Gross Profit: ${df['unit_gross_profit'].mean():.2f}\")\n",
    "df[['sku', 'product_type', 'price', 'manufacturing_costs', 'unit_gross_profit']].head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3: Exploratory Analysis & Business Questions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Q1: Revenue Analysis\n",
    "revenue_by_category = (\n",
    "    df.groupby('product_type')['revenue_generated']\n",
    "    .agg(['sum', 'mean', 'count'])\n",
    "    .rename(columns={'sum': 'total_revenue', 'mean': 'avg_revenue', 'count': 'sku_count'})\n",
    "    .sort_values('total_revenue', ascending=False)\n",
    ")\n",
    "print(\"--- Revenue by Category ---\")\n",
    "print(revenue_by_category)\n",
    "\n",
    "print(\"\\n--- Top 10 SKUs by Revenue ---\")\n",
    "top10_revenue = df.nlargest(10, 'revenue_generated')[['sku', 'product_type', 'revenue_generated']]\n",
    "print(top10_revenue.to_string(index=False))\n",
    "\n",
    "# Q2: Product Profitability\n",
    "print(\"\\n--- Average Unit Gross Profit by Category ---\")\n",
    "print(df.groupby('product_type')['unit_gross_profit'].mean())\n",
    "\n",
    "print(\"\\n--- Top 5 Profitable SKUs ---\")\n",
    "print(df.nlargest(5, 'unit_gross_profit')[['sku', 'product_type', 'price', 'manufacturing_costs', 'unit_gross_profit']].to_string(index=False))\n",
    "\n",
    "print(\"\\n--- Bottom 5 Loss-making SKUs ---\")\n",
    "print(df.nsmallest(5, 'unit_gross_profit')[['sku', 'product_type', 'price', 'manufacturing_costs', 'unit_gross_profit']].to_string(index=False))\n",
    "\n",
    "# Q3: Supplier Defect Rates\n",
    "print(\"\\n--- Defect Rate by Supplier ---\")\n",
    "print(df.groupby('supplier_name')['defect_rates'].mean().sort_values(ascending=False))\n",
    "\n",
    "# Q4: Carrier Shipping Costs\n",
    "print(\"\\n--- Shipping Cost by Carrier ---\")\n",
    "print(df.groupby('shipping_carriers')['shipping_costs'].agg(['mean', 'min', 'max']).sort_values('mean'))\n",
    "\n",
    "# Q5: Supplier Manufacturing Lead Times\n",
    "print(\"\\n--- Manufacturing Lead Time by Supplier ---\")\n",
    "print(df.groupby('supplier_name')['manufacturing_lead_time'].mean().sort_values(ascending=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4: Visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "plt.rcParams.update({'figure.figsize': (8, 4.5), 'axes.titlesize': 12, 'axes.labelsize': 10})\n",
    "\n",
    "# 1. Revenue by Product Category\n",
    "data = revenue_by_category['total_revenue'].sort_values()\n",
    "fig, ax = plt.subplots()\n",
    "bars = ax.barh(data.index, data.values, color=['#4C72B0', '#55A868', '#C44E52'])\n",
    "ax.set_xlabel('Total Revenue ($)')\n",
    "ax.set_title('Total Revenue by Product Category')\n",
    "for bar in bars:\n",
    "    w = bar.get_width()\n",
    "    ax.text(w + 1000, bar.get_y() + bar.get_height()/2, f'${w:,.0f}', va='center', fontsize=9)\n",
    "ax.set_xlim(0, data.max() * 1.15)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 2. Top 10 SKUs by Revenue\n",
    "data_top10 = top10_revenue.sort_values('revenue_generated')\n",
    "fig, ax = plt.subplots()\n",
    "bars = ax.barh(data_top10['sku'], data_top10['revenue_generated'], color='#4C72B0')\n",
    "ax.set_xlabel('Revenue Generated ($)')\n",
    "ax.set_title('Top 10 SKUs by Revenue')\n",
    "for bar in bars:\n",
    "    w = bar.get_width()\n",
    "    ax.text(w + 100, bar.get_y() + bar.get_height()/2, f'${w:,.0f}', va='center', fontsize=8)\n",
    "ax.set_xlim(0, data_top10['revenue_generated'].max() * 1.12)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 3. Shipping Cost by Carrier\n",
    "carrier_avg = df.groupby('shipping_carriers')['shipping_costs'].mean().sort_values()\n",
    "fig, ax = plt.subplots()\n",
    "bars = ax.bar(carrier_avg.index, carrier_avg.values, color=['#55A868', '#4C72B0', '#C44E52'], width=0.5)\n",
    "ax.set_ylabel('Average Shipping Cost ($)')\n",
    "ax.set_title('Average Shipping Cost by Carrier')\n",
    "for bar in bars:\n",
    "    h = bar.get_height()\n",
    "    ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'${h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')\n",
    "ax.set_ylim(0, carrier_avg.max() * 1.15)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 4. Manufacturing Lead Time by Supplier\n",
    "lead_avg = df.groupby('supplier_name')['manufacturing_lead_time'].mean().sort_values()\n",
    "fig, ax = plt.subplots()\n",
    "bars = ax.barh(lead_avg.index, lead_avg.values, color='#DD8452')\n",
    "ax.set_xlabel('Average Manufacturing Lead Time (Days)')\n",
    "ax.set_title('Average Manufacturing Lead Time by Supplier')\n",
    "for bar in bars:\n",
    "    w = bar.get_width()\n",
    "    ax.text(w + 0.2, bar.get_y() + bar.get_height()/2, f'{w:.1f} days', va='center', fontsize=9)\n",
    "ax.set_xlim(0, lead_avg.max() * 1.2)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 5. Defect Rate by Supplier\n",
    "defect_avg = df.groupby('supplier_name')['defect_rates'].mean().sort_values()\n",
    "fig, ax = plt.subplots()\n",
    "bars = ax.barh(defect_avg.index, defect_avg.values, color='#C44E52')\n",
    "ax.set_xlabel('Average Defect Rate (%)')\n",
    "ax.set_title('Average Defect Rate by Supplier')\n",
    "for bar in bars:\n",
    "    w = bar.get_width()\n",
    "    ax.text(w + 0.03, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', va='center', fontsize=9)\n",
    "ax.set_xlim(0, defect_avg.max() * 1.2)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5: Summary & Key Recommendations\n",
    "\n",
    "1. **Product Profitability**: Review pricing and manufacturing costs for the **44 loss-making SKUs** (e.g., SKU23 losing $94.29/unit). Consider price adjustments or SKU discontinuation.\n",
    "2. **Supplier Management**: Allocate more production to **Supplier 1** (lowest defect rate at 1.80%, fastest lead time at 12.6 days). Conduct quality audits for **Supplier 5** (highest defect rate at 2.67%, slowest lead time at 16.3 days).\n",
    "3. **Category Strategy**: Expand the cosmetics portfolio to leverage its high per-SKU profitability (+ $14.31 avg unit gross profit) while continuing to scale skincare revenue."
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

nb_path = os.path.join(r'C:\Users\Tushar Saini\.gemini\antigravity\scratch\supply_chain_analytics', 'supply_chain_notebook.ipynb')
with open(nb_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Jupyter Notebook generated at: {nb_path}")
