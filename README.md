# HR Analytics Dashboard — Power BI

## Overview
An end-to-end HR Analytics project built on the IBM HR Employee Attrition dataset.
The goal is to identify key drivers of employee attrition and provide actionable
insights across departments, salary bands, job roles, and satisfaction levels.

## Dataset
- Source: IBM HR Analytics Employee Attrition & Performance (Kaggle)
- Records: 1,470 employees, 35 features
- Link: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

## Tools Used
- Python (pandas, numpy) — ETL & feature engineering
- Power BI Desktop — data modelling, DAX, dashboard design

## Project Structure
```
hr-analytics-powerbi/
│
├── data/
│   ├── raw/                        # Original IBM HR dataset
│   └── processed/                  # Cleaned & feature-engineered CSVs
│       ├── hr_clean.csv
│       ├── attrition_summary.csv
│       └── salary_bands.csv
│
├── scripts/
│   └── etl.py                      # Python ETL pipeline
│
├── report/
│   └── HR_Analytics_PowerBI.pbix   # Power BI report file
│
├── screenshots/
│   ├── home.png
│   ├── overview.png
│   ├── attrition_analysis.png
│   ├── department_performance.png
│   └── salary_compensation.png
│
└── README.md
```

## ETL Pipeline
The Python script (scripts/etl.py) performs the following:
- Drops constant/irrelevant columns (EmployeeCount, Over18, StandardHours)
- Engineers 8 new features:
  - AttritionFlag — binary encoding of attrition (1/0)
  - TenureBand — grouped years at company (0-2, 3-5, 6-10, 10+)
  - AgeBand — grouped age ranges (18-25, 26-35, 36-45, 46-55, 55+)
  - SalaryBand — income quartile grouping (Low, Mid, High)
  - OverallSatisfaction — average of 4 satisfaction metrics
  - SatisfactionLevel — labeled satisfaction tier (Low, Medium, High)
  - HighRisk — employees who left AND worked overtime (1/0)
  - PromotionRecency — years since last promotion, grouped
- Exports 3 processed CSVs for Power BI consumption

## How to Run the ETL
1. Download the dataset from Kaggle and place it in data/raw/hr_data.csv
2. Install dependencies:
   pip install pandas numpy
3. Run the script:
   python scripts/etl.py
4. Processed files will appear in data/processed/

## Dashboard Pages
1. Home — navigation hub with key stats (1,470 employees, 16.1% attrition, 127 high risk)
2. Overview — KPI cards, attrition split donut, attrition by age band and department
3. Attrition Analysis — attrition by job role, tenure, overtime, and business travel
4. Department Performance — headcount, satisfaction scores, and distribution by department
5. Salary & Compensation — income by role, department, gender, and salary band vs attrition

## Key DAX Measures
- Attrition Rate = DIVIDE(attrited employees, total employees)
- OT Attrition Rate = attrition rate among overtime workers only
- Income Gap = avg income of active employees minus avg income of attrited employees
- High Risk Employees = employees who left AND worked overtime
- Avg Satisfaction = average of overall satisfaction score across selected filters

## Key Insights
- Overall attrition rate is 16.1% (237 out of 1,470 employees)
- Sales Representatives have the highest attrition rate at ~40%
- Employees in the 18-25 age group leave at nearly 35% — highest of any age band
- Overtime workers attrite at 30.5% vs 10% for non-overtime employees
- Low salary band employees leave at 27% vs ~11% for mid and high bands
- 127 employees are classified as high risk (attrited + worked overtime)
- Gender pay gap is minimal — Female avg $6,560 vs Male avg $6,381
- Satisfaction levels are consistent across departments (~2.73 avg out of 4)

## How to Open the Report
1. Download and install Power BI Desktop (free):
   https://powerbi.microsoft.com/desktop
2. Clone or download this repository
3. Open report/HR_Analytics_PowerBI.pbix
4. If prompted about data source, re-point to the processed CSVs in data/processed/

## Screenshots
### Home
![Home](https://github.com/saquibattar/HR-Analytics-PowerBi/blob/main/Screenshots/Home.png)

### Overview
![Overview](https://github.com/saquibattar/HR-Analytics-PowerBi/blob/main/Screenshots/Overview.png)

### Attrition Analysis
![Attrition Analysis](https://github.com/saquibattar/HR-Analytics-PowerBi/blob/main/Screenshots/Attrition%20Analysis.png)

### Department Performance
![Department Performance](https://github.com/saquibattar/HR-Analytics-PowerBi/blob/main/Screenshots/Department%20Performance.png)

### Salary & Compensation
![Salary & Compensation](https://github.com/saquibattar/HR-Analytics-PowerBi/blob/main/Screenshots/Salary%20%26%20Compensation.png)

## Author
Saquib Attar
M.Eng Information Technology — Frankfurt University of Applied Sciences
https://www.linkedin.com/in/saquib-attar-0404/
