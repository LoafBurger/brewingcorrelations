import pandas as pd

CSV_FILE = "data/processed/starbucks_reviews_flat.csv"

df = pd.read_csv(CSV_FILE)


# get the unique values from each column
def print_unique_values():
    for column in df.columns:
        unique_values = df[column].unique()
        print(
            f"Column '{column}' has {len(unique_values)} unique values: {unique_values}"
        )


# figure out the num of missing values in each column and their percentage
def print_missing_values():
    print("\nMissing values per column:")
    missing_info = {}
    for column in df.columns:
        num_missing = df[column].isnull().sum()
        percent_missing = (num_missing / len(df)) * 100
        missing_info[column] = (num_missing, percent_missing)

    # format mssing_info as a pandas DataFrame for better visualization
    missing_df = pd.DataFrame.from_dict(
        missing_info, orient="index", columns=["Num Missing", "Percent Missing"]
    )
    print(missing_df)


# check if any columns have a high occurence of a singular value
def check_plausibility():
    threshold = 90.0  # percentage threshold to flag
    print(f"\nColumns with more than {threshold}% of a single value:")
    for column in df.columns:
        value_counts = df[column].value_counts(normalize=True, dropna=False) * 100
        if not value_counts.empty and value_counts.iloc[0] > threshold:
            print(
                f"Column '{column}' has {value_counts.iloc[0]:.2f}% of value '{value_counts.index[0]}'"
            )


if __name__ == "__main__":
    print_unique_values()
    print_missing_values()
    check_plausibility()
