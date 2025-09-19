"""
Code for Phase 2 Report:
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load the flattened CSV
csv_file = "data/processed/starbucks_reviews_flat.csv"
df = pd.read_csv(csv_file)

# getting the timeline of the data, how many years of history (for the report)
earliest_date = df["date"].min()
latest_date = df["date"].max()

print("\nDate range of the dataset:")
print(f"Earliest: {earliest_date}")
print(f"Latest:   {latest_date}")

# 1. check attribute types
# basic info about the dataset
print(df.info())  # shows data types and missing values

# identify numeric columns
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
print("\nNumeric columns:")
print(numeric_cols)

# identify categorical columns (object/string types)
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
print("\nCategorical columns:")
print(categorical_cols)

# identify datetime columns
# convert 'date' to datetime first if not already
df["date"] = pd.to_datetime(df["date"], errors="coerce")
datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()
print("\nDatetime columns:")
print(datetime_cols)

# 2. check attribute value ranges
# numeric attributes summary
print("\nNumeric attribute ranges:")
summary = df[numeric_cols].describe()

print(summary)  # still prints to screen

# save to CSV
summary.to_csv("data/processed/numeric_attribute_summary.csv")

# keep it as a DataFrame for later use
summary_table = summary

# categorical attributes summary
print("\nCategorical attribute value counts (top 5 for each):")
for col in categorical_cols:
    print(f"\nColumn: {col}")
    print(df[col].value_counts().head())

# 3. check attribute correlations
# compute correlation matrix for numeric attributes
correlation_matrix = df[numeric_cols].corr()

print("\nCorrelation matrix (numeric attributes):")
print(correlation_matrix)

# visualize using a heatmap

plt.figure(figsize=(16, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix of Numeric Attributes")
plt.tight_layout()
plt.show()
