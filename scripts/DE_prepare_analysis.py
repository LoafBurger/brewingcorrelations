import json
import pandas as pd

ENRICHED_JSON = "data/processed/starbucks_reviews_enriched.json"
OUTPUT_CSV = "data/processed/starbucks_reviews_flat.csv"


def load_and_flatten(json_file):
    """Load enriched JSON and flatten business_info with readable prefix."""
    df = pd.read_json(json_file, lines=True)

    # Flatten business_info with 'business_' prefix
    biz_df = pd.json_normalize(df["business_info"]).add_prefix("business_")

    # Drop original column and join
    df = df.drop(columns=["business_info"]).join(biz_df)

    return df


def main():
    print("Loading and flattening JSON...")
    df = load_and_flatten(ENRICHED_JSON)

    print(f"Saving flattened CSV to {OUTPUT_CSV}...")
    df.to_csv(OUTPUT_CSV, index=False)
    print("Done!")


if __name__ == "__main__":
    main()
