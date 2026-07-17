# Interview Prep Q&A: Supply Chain Performance Analytics

This document covers the technical mechanics (pandas/numpy/matplotlib) and critical design decisions made during this project, formatted for role-play and interview preparation.

---

### Q1: How did you resolve the ambiguity of having three separate lead-time columns (`Lead times`, `Lead time`, and `Manufacturing lead time`)?
**Answer:**
Given the lack of official documentation, I audited the range and distributions of these columns:
- **`Manufacturing lead time`** (Column 18) ranged from 1 to 30 days. This represents the production lead time at the supplier facility.
- **`Lead times`** (Column 9) ranged from 1 to 30 days. I assumed this represents the **Supplier-to-Warehouse Delivery Lead Time** (the time taken for a supplier to ship and deliver products to our warehouse).
- **`Lead time`** (Column 16) also ranged from 1 to 30 days. I assumed this represents the **Total End-to-End Fulfillment Lead Time** (customer-facing lead time from order placement to final delivery).

*Statistical Validation:*
I checked the correlation of these columns with defect rates. End-to-end `Lead time` (fulfillment) had a moderate positive correlation with defect rates ($r = 0.297$), which suggests that quality control issues or defects delay final delivery to customers.

---

### Q2: How did you distinguish between `Costs`, `Manufacturing costs`, and `Shipping costs`?
**Answer:**
I analyzed the magnitude and correlation structure of these columns:
- **`Manufacturing costs`** (mean ~$47.27, range $1–$99) and **`Shipping costs`** (mean ~$5.55, range $1–$10) represent **unit-level costs** because they are small and scale linearly with units.
- **`Costs`** (mean ~$529.25, range $103–$997) was significantly higher. I hypothesized that this represents the **Route-level Freight Logistics Cost** (the macro cost of running that specific shipping lane/route).
- I validated this by grouping `Costs` by transportation mode and route: Air ($561.71) and Road ($553.38) were significantly higher than Sea ($417.81). Similarly, Route B was the most expensive route ($595.66) compared to Route A ($485.48). This confirmed `Costs` represents route freight expenses, not unit-level costs.

---

### Q3: What major financial anomaly did you discover in the dataset, and how would you explain it to a business stakeholder?
**Answer:**
I found a severe structural discrepancy between the columns:
- Theoretical Revenue (`Price * Number of products sold`) sums to **$2.24M**.
- The reported **`Revenue generated`** column only sums to **$577.6k** (a 74% reduction).
- If we calculate the Cost of Goods Sold (COGS) as `Manufacturing costs * Number of products sold` ($2.21M) and shipping costs ($259k), the business shows a massive net loss of **-$1.94M** (a profit margin of **-336.47%**).
- This discrepancy indicates that either:
  1. The business is discounting products by an average of 74% or selling wholesale at a massive loss.
  2. Or, more likely, this is a **synthetic data generation error** where the columns were generated independently without maintaining mathematical coherence.
- *Why this matters:* Pointing this out demonstrates that I don't just run code blindly. I perform data auditing to ensure the mathematical integrity of the database before making recommendations.

---

### Q4: How did you implement the "Late Delivery Flag" in pandas? What threshold did you use and why?
**Answer:**
The `shipping_times` column consists of discrete integers ranging from 1 to 10 days. I set the threshold for a "late delivery" at **> 7 days** (which represents the 75th percentile of transit times).
- In pandas, I created this Boolean flag using:
  ```python
  df['is_late_delivery'] = (df['shipping_times'] > 7).astype(int)
  ```
- This resulted in an overall late delivery rate of **33%** (33 out of 100 shipments), which provided a balanced target for analyzing carrier reliability.

---

### Q5: How did you create the dual-axis chart in Matplotlib to compare units sold and revenue?
**Answer:**
To overlay a line chart (Revenue) on top of a bar chart (Units Sold) with different scales, I used Matplotlib's `twinx()` function to create a secondary y-axis.
```python
fig, ax1 = plt.subplots(figsize=(8, 5))
# Plot bars for Units Sold on ax1
bars = ax1.bar(df['product_type'], df['total_sales'], color='blue', alpha=0.7)
ax1.set_ylabel('Total Units Sold', color='blue')

# Create secondary axis sharing the x-axis
ax2 = ax1.twinx()
# Plot line for Revenue on ax2
line = ax2.plot(df['product_type'], df['total_revenue'], color='red', marker='o')
ax2.set_ylabel('Total Revenue ($)', color='red')
```
I also adjusted tick parameters and color-coded labels to ensure the dual-axis was readable and clear.

---

### Q6: How did you handle statistical noise in your correlation analysis?
**Answer:**
With a small dataset of only 100 rows ($N=100$), weak correlation coefficients (e.g., $|r| < 0.2$) are highly likely to be statistical noise rather than actual business patterns.
- I computed the correlation matrix using:
  ```python
  corr_matrix = df.select_dtypes(include='number').corr()
  ```
- I flagged that **220 out of 228 correlation pairs (96%)** had coefficients $|r| < 0.2$. I advised against using these weak correlations for business decision-making.
- I only highlighted moderate correlations, such as `Price` vs. `Manufacturing lead time` ($-0.301$) and `Lead time` vs. `Defect rates` ($0.297$), and noted that even these should be monitored closely as they could be driven by a few outlier rows in a small dataset.

---

### Q7: Explain the pandas code you used to analyze Route Costs by Transportation Mode.
**Answer:**
To analyze how average logistics costs vary across combinations of routes and transportation modes, I used a multi-column groupby followed by an `unstack()` operation to pivot the index into columns:
```python
route_mode_cost = df.groupby(['routes', 'transportation_modes'])['costs'].mean().unstack()
```
- The `groupby(['routes', 'transportation_modes'])` groups the data by both categories.
- `['costs'].mean()` calculates the average freight cost for each combination, yielding a multi-indexed Series.
- `.unstack()` pivots the inner index (`transportation_modes`) into columns, creating a clean, matrix-style DataFrame where rows are Routes and columns are Transportation Modes (Air, Rail, Road, Sea). This is much easier to read and present in reports.
