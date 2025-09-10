"""
Order of running scripts:
- extract, filter, enrich, prepare, tinker
    ├── DE_extract_starbucks.py
    ├── DE_filter_reviews.py
    ├── DE_enrich_reviews.py
    ├── DE_prepare_analysis.py
    └── DS_tinkering_with_data.py
"""

import pandas as pd

# load the flattened CSV
csv_file = "data/processed/starbucks_reviews_flat.csv"
df = pd.read_csv(csv_file)

# see the first few rows
print("First 5 rows of the dataset:")
print(df.head())

# list all columns
print("\nColumns in the dataset:")
print(df.columns.tolist())
print(f"Number of Columns: {len(df.columns)}")


# get average review stars per city
avg_stars_by_city = (
    df.groupby("business_city")["stars"].mean().sort_values(ascending=False)
)
print("\nAverage review stars by city:")
print(avg_stars_by_city)

# see distribution of review stars
print("\nReview stars value counts:")
print(df["stars"].value_counts())

print()
row = df.iloc[0]
print(row)

# getting the timeline of the data, how many years of history (for the report)
earliest_date = df["date"].min()
latest_date = df["date"].max()

print("\nDate range of the dataset:")
print(f"Earliest: {earliest_date}")
print(f"Latest:   {latest_date}")
