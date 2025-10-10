import pandas as pd

# load the flattened CSV
INPUT_CSV = "data/processed/starbucks_reviews_flat_all.csv"
OUTPUT_CSV = "data\processed\starbucks_reviews_cleaned.csv"
df = pd.read_csv(INPUT_CSV)


# Fill missing values and drop irrelevant columns
df['business_attributes.DriveThru'] = df['business_attributes.DriveThru'].fillna(False)
df['business_attributes.OutdoorSeating'] = df['business_attributes.OutdoorSeating'].fillna(False)
df['business_attributes.OutdoorSeating'] = df['business_attributes.OutdoorSeating'].fillna(False)
df = df.drop('business_hours', axis=1)

df['business_attributes.BusinessAcceptsCreditCards'] = df['business_attributes.BusinessAcceptsCreditCards'].fillna(True)
df['business_attributes.BikeParking'] = df['business_attributes.BikeParking'].fillna(False)
df = df.drop('business_categories', axis=1)

# TODO
# PriceRange --> fill with the majority value
# User_friends --> covert None to ?  or add numerical amount
# Remove rows with strings in int columns
# Use Business_hours to derive hours per day and Fill empty with median time
# Derive a decision rule to decide what a troll review is based on “helpful” votes / user attributes


df.to_csv(OUTPUT_CSV, index=False)

# Missing columns
print(df.isna().sum())



