# Interview Prep Guide: Supply Chain Performance Analytics

This document contains practical Q&A designed for business analytics and consulting interviews (e.g., Bain, ZS, BCN, McKinsey, corporate BA roles). It focuses on defending project decisions, explaining methodologies, and communicating insights concisely.

---

### Q1: Can you give a 2-minute summary of this project?
**Answer:**
"I analyzed a supply chain dataset of 100 SKUs across skincare, haircare, and cosmetics to identify key operational inefficiencies and revenue drivers. 

I focused on five core business questions around revenue distribution, product profitability, supplier quality, shipping costs, and manufacturing lead times. 

Key findings include:
1. **Skincare drives 41.8% of total revenue** ($241.6k), but cosmetics generates the highest revenue per SKU ($6.2k vs. $5.1k for haircare).
2. **44 out of 100 SKUs are loss-making** on a unit gross profit basis (`Selling Price - Manufacturing Cost`), with the worst product losing $94.29 per unit.
3. **Supplier 1 is the clear operational leader**, delivering both the lowest defect rate (1.80%) and the fastest manufacturing lead time (12.6 days), while Supplier 5 performs worst on both metrics (2.67% defects, 16.3 days lead time).

My core recommendations are to review pricing or discontinue the 44 loss-making SKUs, shift production volume toward Supplier 1, and evaluate expanding the cosmetics lineup given its high per-SKU revenue."

---

### Q2: Why did you define Unit Gross Profit as `Selling Price - Manufacturing Cost` rather than calculating Net Profit Margin % or including shipping costs?
**Answer:**
"I kept the metric to `Unit Gross Profit = Selling Price - Manufacturing Cost` for three reasons:
1. **Data Defensibility**: Manufacturing cost is a direct unit cost. Mixing unit-level shipping costs or route-level freight fees into a 'net unit profit' requires undocumented assumptions about how logistics costs are allocated to individual products.
2. **Standard Terminology**: Unit Gross Profit is a standard, unambiguous metric in business operations. It evaluates whether a product's bill of materials makes fundamental economic sense before overlaying transport or overhead.
3. **Actionability**: It immediately separates product-level design/cost issues from carrier/logistics negotiation issues. If a product costs $98 to manufacture but sells for $4, no shipping optimization can fix that product—it requires price or BOM intervention."

---

### Q3: Why did you exclude inventory metrics like Stock-to-Sales Ratio or Inventory Turnover from your analysis?
**Answer:**
"I excluded inventory metrics because the dataset contains `availability` and `stock_levels` without documented timestamps, historical turnover data, or time horizons. 

In a real supply chain, inventory turnover requires Cost of Goods Sold over a specific time period (e.g., annual COGS / average inventory). Calculating ratios using static snapshot numbers without knowing the time period leads to misleading figures that cannot be confidently defended in an interview. 

Instead, I focused strictly on metrics directly supported by the data: revenue, unit gross profit, lead times, carrier costs, and defect rates."

---

### Q4: Why did you choose `manufacturing_lead_time` over `lead_times` or `lead_time`?
**Answer:**
"The dataset contains three ambiguous lead time columns (`lead_times`, `lead_time`, `manufacturing_lead_time`). 

`manufacturing_lead_time` is the only column whose scope is explicit—it represents the supplier's production time. The other two columns do not specify whether they refer to shipping transit, supplier dispatch, or customer fulfillment. 

Rather than inventing unsupported assumptions about what the ambiguous columns mean, I chose `manufacturing_lead_time` to evaluate supplier performance cleanly."

---

### Q5: Why didn't you build predictive models or run correlation heatmaps?
**Answer:**
"With a sample size of only 100 SKUs, running complex statistical correlations or machine learning models creates a high risk of overfitting to statistical noise. 

The goal of this project was not model building, but demonstrating how clean exploratory data analysis (EDA) using Python can answer fundamental business questions and guide strategic decisions. In consulting, a clear, defensible analysis of core business metrics is always preferred over overly complex models built on small or noisy datasets."

---

### Q6: Walk me through the Python code you used to analyze category revenue and supplier metrics.
**Answer:**
"I used Pandas `groupby()` paired with aggregation methods:

1. **Category Revenue**:
   ```python
   revenue_by_category = (
       df.groupby('product_type')['revenue_generated']
       .agg(['sum', 'mean', 'count'])
       .sort_values('sum', ascending=False)
   )
   ```
   This groups the data by product category, sums total revenue, computes average SKU revenue, and counts SKUs per category.

2. **Top / Bottom Profitable SKUs**:
   ```python
   df['unit_gross_profit'] = df['price'] - df['manufacturing_costs']
   top5 = df.nlargest(5, 'unit_gross_profit')
   bottom5 = df.nsmallest(5, 'unit_gross_profit')
   ```
   Using `nlargest()` and `nsmallest()` allows efficient filtering of extreme performers for executive reporting."

---

### Q7: If a client gave you this dataset in a real consulting engagement, what next steps would you recommend?
**Answer:**
"I would recommend three next steps:
1. **Obtain Temporal Data**: Request time-stamped sales and inventory data to perform actual time-series forecasting, seasonality analysis, and true inventory turnover calculations.
2. **Audit Supplier Contracts**: Meet with Supplier 5 to investigate the root causes of their high defect rates (2.67%) and long lead times (16.3 days), using Supplier 1 (1.80% defects, 12.6 days) as a benchmark.
3. **Conduct SKU Rationalization**: Perform a deep-dive on the 44 loss-making SKUs to determine whether price elasticity allows price increases, or if these products should be phased out entirely."
