# Supply Chain Performance Analytics

## Objective

The objective of this project is to demonstrate how Exploratory Data Analysis (EDA) using Python can identify operational inefficiencies and support business decision-making in a supply chain. The project focuses on descriptive analytics and business insights rather than predictive modeling or optimization.

---

## Dataset

- **Source:** Supply Chain Dataset (`data/supply_chain_data.csv`)
- **Size:** 100 rows × 24 columns
- **Scope:** SKU-level supply chain data covering Skincare, Haircare, and Cosmetics product categories.
- **Key Columns Used:**
  - Product Type
  - SKU
  - Price
  - Revenue Generated
  - Manufacturing Costs
  - Manufacturing Lead Time
  - Shipping Costs
  - Shipping Carrier
  - Supplier Name
  - Defect Rate

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Python | Data Analysis |
| Pandas | Data Cleaning, Aggregation & KPI Calculation |
| NumPy | Numerical Operations |
| Matplotlib | Data Visualization |

---

## Business Questions Addressed

### 1. Which product categories generate the highest revenue?
- Revenue comparison across product categories.
- Top 10 revenue-generating SKUs.

### 2. Which products are profitable or loss-making?
- Gross Profit (per unit) = Selling Price − Manufacturing Cost.
- Identification of profitable and loss-making SKUs.

### 3. Which suppliers have the highest defect rates?
- Supplier-wise quality comparison.
- Category-wise defect analysis.

### 4. Which shipping carrier is the most cost-efficient?
- Average shipping cost comparison across carriers.

### 5. Which suppliers have the longest manufacturing lead times?
- Supplier-wise manufacturing lead time comparison.
- Category-wise lead time comparison.

---

## Key Insights

### Revenue Analysis
- Skincare generated the highest total revenue.
- Cosmetics recorded the highest average revenue per SKU.

### Product Profitability
- 44 out of 100 SKUs had negative Gross Profit (per unit), indicating manufacturing costs exceeded selling prices.
- Cosmetics was the only category with a positive average Gross Profit (per unit).

### Supplier Quality
- Supplier 5 recorded the highest average defect rate.
- Supplier 1 had the lowest defect rate among all suppliers.

### Shipping Performance
- Carrier B had the lowest average shipping cost.
- Shipping cost differences between carriers were relatively small.

### Manufacturing Lead Time
- Haircare products had the longest average manufacturing lead time.
- Supplier 5 also showed the highest average manufacturing lead time.

---

## Business Recommendations

- Review pricing or manufacturing costs for loss-making products.
- Prioritize high-performing suppliers with lower defect rates and shorter lead times.
- Audit Supplier 5 to identify quality and production bottlenecks.
- Evaluate opportunities to expand the Cosmetics portfolio due to its stronger profitability.

---

## Visualizations

The project generates the following charts:

- Revenue by Product Category
- Top 10 SKUs by Revenue
- Shipping Cost by Carrier
- Manufacturing Lead Time by Supplier
- Defect Rate by Supplier

All visualizations are saved under:

```
images/charts/
```

---

## Project Structure

```
supply_chain_analytics/
│
├── data/
│   └── supply_chain_data.csv
│
├── images/
│   └── charts/
│       ├── revenue_by_category.png
│       ├── top10_skus_revenue.png
│       ├── shipping_cost_by_carrier.png
│       ├── leadtime_by_supplier.png
│       └── defect_rate_by_supplier.png
│
├── analysis.py
├── supply_chain_notebook.ipynb
├── insights.txt
├── interview_prep.md
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python analysis.py
```

---

## Skills Demonstrated

- Exploratory Data Analysis (EDA)
- Business Analytics
- Supply Chain Analytics
- Data Cleaning
- KPI Analysis
- Data Visualization
- Business Insight Generation
- Python (Pandas, NumPy, Matplotlib)

---

## Future Improvements

- Incorporate historical time-series data for demand forecasting.
- Expand the dataset with additional products and suppliers.
- Build an interactive Power BI dashboard for real-time KPI monitoring.
- Integrate inventory optimization and demand forecasting models using machine learning.