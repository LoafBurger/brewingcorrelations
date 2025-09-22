import pandas as pd

ENRICHED_JSON = "data/processed/starbucks_reviews_enriched_with_users.json"
OUTPUT_CSV = "data/processed/starbucks_reviews_flat_all.csv"


def load_and_flatten(json_file):
    """Load enriched JSON and flatten business_info and user_info with readable prefixes."""
    df = pd.read_json(json_file, lines=True)

    # flatten business info
    biz_df = pd.json_normalize(df["business_info"]).add_prefix("business_")
    df = df.drop(columns=["business_info"]).join(biz_df)

    # flatten user info
    user_df = pd.json_normalize(df["user_info"]).add_prefix("user_")
    df = df.drop(columns=["user_info"]).join(user_df)

    return df


def main():
    print("Loading and flattening JSON...")
    df = load_and_flatten(ENRICHED_JSON)

    print(f"Saving flattened CSV to {OUTPUT_CSV}...")
    df.to_csv(OUTPUT_CSV, index=False)
    print("Done!")
    print(f"Final table shape: {df.shape}")


if __name__ == "__main__":
    main()
