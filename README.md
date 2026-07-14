# Task-5-Interactive-Business-Dashboard-in-Streamlit

# Interactive Business Dashboard — Global Superstore (Streamlit)

An interactive Streamlit BI dashboard for analyzing sales, profit, and segment-wise
performance across the Global Superstore dataset.

##  Task Objective

Build an interactive dashboard with filters (Region, Category, Sub-Category) that
displays key performance indicators — Total Sales, Profit, and Top 5 Customers by Sales.

##  Approach

1. **Data prep & EDA** (`Superstore_EDA.ipynb`) — cleaned the data, engineered `Month`
   and `Profit Margin %` fields, and explored sales/profit patterns by category, region,
   sub-category, and time.
2. **Dashboard** (`app.py`) — built with Streamlit + Plotly:
   - Sidebar filters for **Region**, **Category**, **Sub-Category**, and **Order Date range**
   - KPI cards: **Total Sales**, **Total Profit**, **Orders**, **Profit Margin %**
   - Charts: Sales & Profit by Category, Sales share by Region (pie), monthly Sales/Profit
     trend, Sub-Category performance, and **Top 5 Customers by Sales**
   - Expandable raw data table for the currently filtered view

## Results & Findings

- Office Supplies drives the highest order volume; Technology contributes disproportionately
  to profit per order.
- Sales fluctuate month-to-month, useful for spotting seasonal peaks.
- A small number of sub-categories account for an outsized share of revenue.
- The top 5 customers by sales form a concentrated, high-value segment worth targeted
  retention efforts.

##  Repository Structure

```
.
├── app.py                  # Streamlit dashboard
├── Superstore_EDA.ipynb    # Data prep & exploratory analysis notebook
├── data/
│   └── superstore.csv      # Dataset (see note below)
├── requirements.txt
└── README.md
```


##  How to Run

```
pip install -r requirements.txt

# Explore the data
jupyter notebook Superstore_EDA.ipynb

# Launch the dashboard
streamlit run app.py
```
