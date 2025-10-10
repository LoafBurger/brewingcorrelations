import pandas as pd
from datetime import datetime, timedelta

# load the flattened CSV
INPUT_CSV = "data/processed/starbucks_reviews_flat_all.csv"
OUTPUT_CSV = "data/processed/starbucks_reviews_cleaned.csv"
df = pd.read_csv(INPUT_CSV)


def hours_from_range(time_range):
    try:
        start_str, end_str = time_range.split("-")
        start = datetime.strptime(start_str.strip(), "%H:%M")
        end = datetime.strptime(end_str.strip(), "%H:%M")
        if end < start:  # crosses midnight
            end += timedelta(days=1)
        diff = (end - start).seconds / 3600
        return diff
    except Exception:
        return None


# df['hours'] = df['time_range'].apply(hours_from_range)
# print(df)


# Fill missing values and drop irrelevant columns
df["business_attributes.DriveThru"] = df["business_attributes.DriveThru"].fillna(False)
df["business_attributes.OutdoorSeating"] = df[
    "business_attributes.OutdoorSeating"
].fillna(False)
df["business_attributes.RestaurantsTakeOut"] = df[
    "business_attributes.RestaurantsTakeOut"
].fillna(True)

df = df.drop("business_hours", axis=1)
df["business_attributes.BusinessAcceptsCreditCards"] = df[
    "business_attributes.BusinessAcceptsCreditCards"
].fillna(True)
df["business_attributes.BikeParking"] = df["business_attributes.BikeParking"].fillna(
    False
)

# Fill with majority value
df = df.drop("business_categories", axis=1)
df["business_attributes.RestaurantsPriceRange2"] = df[
    "business_attributes.RestaurantsPriceRange2"
].fillna(df["business_attributes.RestaurantsPriceRange2"].value_counts().idxmax())

# Add column to count number of friends
df["user_friend_count"] = df["user_friends"].apply(
    lambda x: len(str(x).split(",")) if pd.notnull(x) else 0
)


# Derive hours for each day
df["monday_duration"] = df["business_hours.Monday"].apply(hours_from_range)
median_val = df["monday_duration"].median(skipna=True)
df["monday_duration"] = df["monday_duration"].fillna(median_val)

df["tuesday_duration"] = df["business_hours.Tuesday"].apply(hours_from_range)
median_val = df["tuesday_duration"].median(skipna=True)
df["tuesday_duration"] = df["tuesday_duration"].fillna(median_val)

df["wednesday_duration"] = df["business_hours.Wednesday"].apply(hours_from_range)
median_val = df["wednesday_duration"].median(skipna=True)
df["wednesday_duration"] = df["wednesday_duration"].fillna(median_val)

df["thursday_duration"] = df["business_hours.Thursday"].apply(hours_from_range)
median_val = df["thursday_duration"].median(skipna=True)
df["thursday_duration"] = df["thursday_duration"].fillna(median_val)

df["friday_duration"] = df["business_hours.Friday"].apply(hours_from_range)
median_val = df["friday_duration"].median(skipna=True)
df["friday_duration"] = df["friday_duration"].fillna(median_val)

df["saturday_duration"] = df["business_hours.Saturday"].apply(hours_from_range)
median_val = df["saturday_duration"].median(skipna=True)
df["saturday_duration"] = df["saturday_duration"].fillna(median_val)

df["sunday_duration"] = df["business_hours.Sunday"].apply(hours_from_range)
median_val = df["sunday_duration"].median(skipna=True)
df["sunday_duration"] = df["sunday_duration"].fillna(median_val)

# Get total hours
df["total_hours"] = (
    df["monday_duration"]
    + df["tuesday_duration"]
    + df["wednesday_duration"]
    + df["thursday_duration"]
    + df["friday_duration"]
    + df["saturday_duration"]
    + df["sunday_duration"]
)


print("Cleaning...")
df.to_csv(OUTPUT_CSV, index=False)
print("Done!")
