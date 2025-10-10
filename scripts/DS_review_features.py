import pandas as pd

INPUT_FILE = "data/processed/checkpoint_starbucks_reviews_with_features.csv"

df = pd.read_csv(INPUT_FILE)

df = df[
    [
        "text",
        "quality_of_drinks_sentiment",
        "quality_of_customer_service_sentiment",
        "cleanliness_of_store_sentiment",
        "overall_ambience_sentiment",
    ]
]

print(df.describe())
