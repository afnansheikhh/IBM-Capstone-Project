# 🛒 IBM Capstone Project: Supermarket Sales Analytics & Intelligence

![IBM](https://img.shields.io/badge/IBM-SkillsBuild-0F62FE?style=for-the-badge&logo=ibm&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

An end-to-end Exploratory Data Analysis (EDA), KPI Intelligence Dashboard, and Strategic Decision Framework built for the **IBM Capstone Project (Supermarket Sales Analytics)**.

---

## 📌 Project Objectives & Workflow

1. **Collect and Load Dataset**: Ingested 500 validated supermarket transaction records across 4 major Indian metropolitan branches (`Mumbai`, `Delhi`, `Bengaluru`, `Jaipur`).
2. **Data Quality & Audit**: Verified data integrity — 0 missing values, 0 schema errors, and 0 duplicate records.
3. **Formula Calculation**: Programmatically computed and verified $\text{Sales} = \text{Quantity} \times \text{Unit Price}$ across 100% of rows.
4. **Group & Summarize**: Aggregated totals, counts, and averages across Categories, Cities/Branches, Customer Types, Payment Methods, and Dates.
5. **Interactive Data Visualizations**: Built high-contrast Neo-Brutalist IBM Blue dashboards and comparative charts.
6. **Data-Driven Business Decisions**: Formulated 4 strategic executive recommendations to optimize retail inventory, customer loyalty, and digital checkout operations.

---

## 🗂️ Project Repository Structure

```
IBM Capstone Project/
├── app.py                                        # Main Streamlit 7-Tab Interactive Dashboard
├── requirements.txt                              # Python Dependencies
├── Project_Report.md                             # Comprehensive Capstone Project Report
├── Project_Report.html                           # Printable Executive Report (PDF-ready)
├── README.md                                     # Project Documentation & Guide
├── SUPER MARKET DATA - supermarket_sales_500_rows.csv  # 500-Row Primary Dataset
├── supermarket_analysis.py                       # Standalone Python CLI Analysis Script
├── category_summary.csv                          # Exported Category Metrics
├── branch_summary.csv                            # Exported Branch Metrics
└── supermarket_analytics/                        # Core Python Analytics Package
    ├── __init__.py                               # Package Initializer
    ├── data_loader.py                            # Data Ingestion & Quality Audit
    └── analytics.py                              # Calculations, Aggregations & Scenarios
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14
- `pip` package manager

### 1. Clone or Download the Repository
Navigate to the project root directory:
```bash
cd "IBM Capstone Project"
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 📊 Key Findings & Store Performance Summary

| Metric | Result | Insight |
| :--- | :---: | :--- |
| **Total Revenue** | **₹244,411.08** | Across 500 invoices and 2,768 units sold |
| **Average Order Value (Ticket)** | **₹488.82** | Consistent median basket spend |
| **Average Customer Rating** | **3.99 / 5.0★** | High customer satisfaction |
| **Top Category** | **Beverages** | **₹56,108.24** (23.0% revenue share) |
| **Top Performing Branch** | **Mumbai (Branch C)** | **₹72,469.45** (29.6% revenue share, 4.05★) |
| **Top Payment Method** | **UPI** | **27.8%** of total revenue |
| **Customer Type Split** | **Members (58.5%)** | 296 transactions vs. 204 normal shoppers |

---

## 💡 Strategic Executive Recommendations

1. **Cross-Selling Combo Deals**:
   - *Finding*: Beverages has high average basket size (₹684.25), while Snacks has high frequency (75 transactions) but low basket size (₹226.57).
   - *Action*: Launch combo bundles (*"Coffee/Tea + Snacks at 15% discount"*) to expand basket values.
2. **Branch Benchmarking (Jaipur Turnaround)**:
   - *Finding*: Jaipur (Branch A) lags at ₹52.4K with the lowest rating (3.84★), whereas Mumbai delivers ₹72.5K with 4.05★.
   - *Action*: Replicate Mumbai's store layout and align Jaipur stock with top Dairy & Beverage items.
3. **Loyalty Program Conversion**:
   - *Finding*: Normal non-members spend more per ticket on average (₹497 vs ₹483 for members).
   - *Action*: Offer cashiers incentives to enroll normal shoppers into membership with instant 5% welcome cashback.
4. **Digital POS Express Lanes**:
   - *Finding*: Digital payment methods (UPI, Net Banking, Cards) represent 77.9% of transactions.
   - *Action*: Deploy dedicated fast-track QR payment lanes to eliminate weekend checkout congestion.

---

## 👨‍💻 Author & Acknowledgements
- **Author**: Afnan Sheikh
- **Program**: IBM SkillsBuild / BharatCares Capstone Project
- **Topic**: Business Solutions with Data Analytics
