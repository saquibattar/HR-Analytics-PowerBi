import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
RAW_PATH = r"E:\Power BI\hr-analytics-powerbi\archive\WA_Fn-UseC_-HR-Employee-Attrition.csv"
PROCESSED_DIR = r"E:\Power BI\hr-analytics-powerbi\processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ─────────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────────
print("Loading raw data...")
df = pd.read_csv(RAW_PATH)
print(f"  Shape: {df.shape}")

# ─────────────────────────────────────────
# 2. CLEAN
# ─────────────────────────────────────────
print("Cleaning data...")

# Drop constant/useless columns
df.drop(columns=["EmployeeCount", "Over18", "StandardHours"], inplace=True)

# Fix data types
df["Attrition"] = df["Attrition"].str.strip()
df["OverTime"] = df["OverTime"].str.strip()
df["Gender"] = df["Gender"].str.strip()

# Check for nulls (IBM dataset is clean, but good practice)
null_counts = df.isnull().sum()
if null_counts.any():
    print(f"  Nulls found:\n{null_counts[null_counts > 0]}")
    df.dropna(inplace=True)
else:
    print("  No nulls found.")

# ─────────────────────────────────────────
# 3. FEATURE ENGINEERING
# ─────────────────────────────────────────
print("Engineering features...")

# Binary attrition flag
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

# Tenure bands
bins = [-1, 2, 5, 10, 100]
labels = ["0-2 yrs", "3-5 yrs", "6-10 yrs", "10+ yrs"]
df["TenureBand"] = pd.cut(df["YearsAtCompany"], bins=bins, labels=labels)

# Age bands
age_bins = [17, 25, 35, 45, 55, 100]
age_labels = ["18-25", "26-35", "36-45", "46-55", "55+"]
df["AgeBand"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

# Salary bands based on quartiles
quartiles = df["MonthlyIncome"].quantile([0.33, 0.66])
def salary_band(income):
    if income <= quartiles[0.33]:
        return "Low"
    elif income <= quartiles[0.66]:
        return "Mid"
    else:
        return "High"
df["SalaryBand"] = df["MonthlyIncome"].apply(salary_band)

# Overall satisfaction score (avg of 4 satisfaction metrics)
satisfaction_cols = [
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "RelationshipSatisfaction",
    "WorkLifeBalance"
]
df["OverallSatisfaction"] = df[satisfaction_cols].mean(axis=1).round(2)

# Satisfaction label
def satisfaction_label(score):
    if score < 2.0:
        return "Low"
    elif score < 3.0:
        return "Medium"
    else:
        return "High"
df["SatisfactionLevel"] = df["OverallSatisfaction"].apply(satisfaction_label)

# High risk flag: attrited + working overtime
df["HighRisk"] = ((df["Attrition"] == "Yes") & (df["OverTime"] == "Yes")).astype(int)

# Years since last promotion band
df["PromotionRecency"] = pd.cut(
    df["YearsSinceLastPromotion"],
    bins=[-1, 1, 3, 6, 100],
    labels=["Recent (0-1yr)", "1-3 yrs", "3-6 yrs", "6+ yrs"]
)

print(f"  Features added: AttritionFlag, TenureBand, AgeBand, SalaryBand, OverallSatisfaction, SatisfactionLevel, HighRisk, PromotionRecency")

# ─────────────────────────────────────────
# 4. EXPORT — Main cleaned dataset
# ─────────────────────────────────────────
print("Exporting processed files...")

main_path = os.path.join(PROCESSED_DIR, "hr_clean.csv")
df.to_csv(main_path, index=False)
print(f"  ✔ hr_clean.csv saved ({len(df)} rows, {len(df.columns)} columns)")

# ─────────────────────────────────────────
# 5. EXPORT — Attrition summary
# ─────────────────────────────────────────
attrition_summary = df.groupby(
    ["Department", "JobRole", "TenureBand", "AgeBand", "OverTime"]
).agg(
    TotalEmployees=("EmployeeNumber", "count"),
    AttritionCount=("AttritionFlag", "sum"),
    AvgSatisfaction=("OverallSatisfaction", "mean"),
    AvgMonthlyIncome=("MonthlyIncome", "mean")
).reset_index()
attrition_summary["AttritionRate"] = (
    attrition_summary["AttritionCount"] / attrition_summary["TotalEmployees"] * 100
).round(2)
attrition_summary["AvgSatisfaction"] = attrition_summary["AvgSatisfaction"].round(2)
attrition_summary["AvgMonthlyIncome"] = attrition_summary["AvgMonthlyIncome"].round(2)

attrition_path = os.path.join(PROCESSED_DIR, "attrition_summary.csv")
attrition_summary.to_csv(attrition_path, index=False)
print(f"  ✔ attrition_summary.csv saved ({len(attrition_summary)} rows)")

# ─────────────────────────────────────────
# 6. EXPORT — Salary bands summary
# ─────────────────────────────────────────
salary_summary = df.groupby(
    ["Department", "JobRole", "SalaryBand", "Gender", "EducationField"]
).agg(
    EmployeeCount=("EmployeeNumber", "count"),
    AvgMonthlyIncome=("MonthlyIncome", "mean"),
    AvgJobLevel=("JobLevel", "mean"),
    AvgPerformanceRating=("PerformanceRating", "mean")
).reset_index()
salary_summary["AvgMonthlyIncome"] = salary_summary["AvgMonthlyIncome"].round(2)
salary_summary["AvgJobLevel"] = salary_summary["AvgJobLevel"].round(2)
salary_summary["AvgPerformanceRating"] = salary_summary["AvgPerformanceRating"].round(2)

salary_path = os.path.join(PROCESSED_DIR, "salary_bands.csv")
salary_summary.to_csv(salary_path, index=False)
print(f"  ✔ salary_bands.csv saved ({len(salary_summary)} rows)")

# ─────────────────────────────────────────
# 7. QUICK STATS SUMMARY
# ─────────────────────────────────────────
print("\n── Dataset Summary ──────────────────────")
print(f"  Total Employees   : {len(df)}")
print(f"  Attrition Rate    : {df['AttritionFlag'].mean()*100:.1f}%")
print(f"  Avg Monthly Income: ${df['MonthlyIncome'].mean():,.0f}")
print(f"  Avg Tenure        : {df['YearsAtCompany'].mean():.1f} yrs")
print(f"  Avg Age           : {df['Age'].mean():.1f}")
print(f"  OT + Attrition    : {df['HighRisk'].sum()} high-risk employees")
print("─────────────────────────────────────────")
print("\nETL complete. Files saved to data/processed/")