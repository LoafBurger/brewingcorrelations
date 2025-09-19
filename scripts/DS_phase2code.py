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

# 4. value counts / frequency tables for specific columns
"""
i.e if a row in the csv says the following for the 'cool' column:
cool,Count,Frequency
0,17213,0.7918

cool = 0 → these reviews received 0 "cool" votes.

Count = 17213 → there are 17,213 reviews in your dataset where nobody clicked "cool."

Frequency = 0.7918 → about 79.18% of all reviews fall into that category.
"""
columns_to_check = ["useful", "funny", "cool", "business_is_open"]

for col in columns_to_check:
    if col in df.columns:
        print(f"\nValue counts for '{col}':")
        counts = df[col].value_counts(dropna=False)
        freqs = df[col].value_counts(normalize=True, dropna=False)

        print(counts)
        print("\nRelative frequencies:")
        print(freqs)

        # combine counts and frequencies into a single DataFrame
        summary_df = pd.DataFrame({"Count": counts, "Frequency": freqs})

        # save to CSV
        output_file = f"data/processed/value_counts_{col}.csv"
        summary_df.to_csv(output_file)
        print(f"Saved to {output_file}")

    else:
        print(f"\nColumn '{col}' not found in dataset.")
