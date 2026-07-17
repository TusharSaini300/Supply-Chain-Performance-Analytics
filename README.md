# Supply Chain Performance Analytics

A data-driven Business Analytics (BA) and Exploratory Data Analysis (EDA) project focusing on portfolio profitability, supplier reliability, and logistics optimization. Built using Python (**pandas**, **numpy**, and **matplotlib**), this project serves as a resume-ready portfolio demonstration of analytical rigor, data auditing, and business intelligence reporting.

---

## Project Structure

```
supply_chain_analytics/
├── data/
│   └── supply_chain_data.csv       # Source dataset (100 rows, 24 columns)
├── images/
│   └── charts/                     # Generated business charts
│       ├── revenue_vs_volume.png
│       ├── carrier_performance.png
│       ├── supplier_quality_leadtime.png
│       └── correlation_matrix.png
├── analysis.py                     # Main Python execution script
├── supply_chain_notebook.ipynb     # Jupyter Notebook version of the analysis
├── insights.txt                    # Quantitative business insights report
├── requirements.txt                # Python dependencies and versions
└── interview_prep.md               # Behavioral and technical Q&A prep
```

---

## Technical Stack & Dependencies

- **Python 3.11+**
- **pandas** (v3.0.3) - Data cleaning, manipulation, and KPI aggregations
- **numpy** (v1.26.4) - Mathematical modeling and array vectorization
- **matplotlib** (v3.11.0) - Custom static visualizations (no Seaborn for maximum layout control)

To install dependencies, run:
```bash
pip install -r requirements.txt
```

To run the analysis:
```bash
python analysis.py
```

---

## Key Business Insights & Findings

### 1. Product Profitability Crisis
- **44% of SKUs** operate with a negative gross unit profit (manufacturing cost > list price).
- **49% of SKUs** have a negative net unit profit when unit shipping costs are included.
- *Action:* Recommend immediate price increases or manufacturing re-negotiations for negative-margin SKUs like **SKU4** (losing $87.26 per unit) and **SKU2** (losing $19.37 per unit).

### 2. Supply Chain Leakage (COGS vs. Revenue)
- The business generated **$577,604.82** in total revenue, but incurred **$2,208,830.61** in total manufacturing costs of goods sold.
- Aggregate net profit is **-$1,943,445.72** with a profit margin of **-336.47%**.
- *Data Audit Note:* There is a major mathematical inconsistency in this synthetic dataset: the `Revenue generated` column is 74% lower than `Price * Number of products sold`. This discrepancy is flagged as a key data quality finding.

### 3. Shipping Carrier Performance
- **Carrier B** is the top-performing carrier: average shipping time of **5.30 days** and the lowest late delivery rate of **23.26%** (defined as shipping times > 7 days).
- **Carrier C** is the worst: highest average cost (**$5.60**), slow transit time (**6.03 days**), and the highest late delivery rate (**41.38%**).
- *Recommendation:* Transition shipments from Carrier C to Carrier B to reduce transit times and improve reliability.

### 4. Inventory Velocity
- **Skincare** is the fastest-moving category with an average Stock-to-Sales ratio of **0.1282**.
- **Haircare** is the slowest-moving category with a Stock-to-Sales ratio of **0.3251** (moving 2.5 times slower than skincare).
- *Recommendation:* Reallocate warehouse storage from Haircare to Skincare to improve holding efficiency.

---

## Visualizations Generated

All visualizations are stored in [images/charts/](file:///C:/Users/Tushar%20Saini/.gemini/antigravity/scratch/supply_chain_analytics/images/charts):
1. **`revenue_vs_volume.png`**: Dual-axis bar/line chart highlighting volume sold and revenue generated across categories.
2. **`carrier_performance.png`**: Side-by-side comparison of shipping times/costs and late delivery rates by carrier.
3. **`supplier_quality_leadtime.png`**: Bubble chart (bubble size = production volume) plotting average manufacturing lead time vs. defect rate.
4. **`correlation_matrix.png`**: Correlation heatmap of all numerical features, with values annotated inside cells.

---

## Career Alignment (Resume Ready)
This project is built to demonstrate core business analyst skills:
- **Data Auditing**: Discovering and documenting systematic inconsistencies between columns.
- **KPI Design**: Defining clear formulas for unit margins, stock-to-sales ratios, and carrier late delivery rates.
- **Actionable Reporting**: Converting raw data metrics into clear business recommendations.

For typical interview questions and technical walkthroughs of the decisions made in this project, refer to the [interview_prep.md](file:///C:/Users/Tushar%20Saini/.gemini/antigravity/scratch/supply_chain_analytics/interview_prep.md) file.
