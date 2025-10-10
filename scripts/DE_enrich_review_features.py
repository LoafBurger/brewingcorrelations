import pandas as pd
import litellm
import json
from tqdm import tqdm
import time
import random
import re

INPUT_FILE = "data/processed/starbucks_reviews_flat_with_density.csv"
OUTPUT_FILE = "data/processed/starbucks_reviews_flat_with_review_features.csv"
CHECKPOINT_FILE = "data/processed/checkpoint_starbucks_reviews_with_features.csv"

# [0, 1] range for the following features, 0 = very poor, 1 = excellent
# Quality of food & drinks
# Quality of customer service
# Cleanliness of store
# Overall ambience


def enrich_review_features():
    df_input = pd.read_csv(INPUT_FILE)

    # If checkpoint exists, resume
    try:
        df_checkpoint = pd.read_csv(CHECKPOINT_FILE)
        start_idx = len(df_checkpoint)
        df_input = df_input.iloc[start_idx:]
        print(f"Resuming from checkpoint: {start_idx} rows already processed.")
        all_results = df_checkpoint
    except FileNotFoundError:
        print("No checkpoint found. Starting fresh.")
        all_results = pd.DataFrame()

    quality_of_food_drinks_scores = []
    quality_of_customer_service_scores = []
    cleanliness_of_store_scores = []
    overall_ambience_scores = []

    for i, review in tqdm(enumerate(df_input["text"].tolist()), total=len(df_input)):
        prompt = f"""
        You are a helpful assistant that analyzes Starbucks reviews. 
        Given the following review, rate the following features on a scale from 0 to 1, where 0 is very poor and 1 is excellent:
        1. Quality of food & drinks
        2. Quality of customer service
        3. Cleanliness of store
        4. Overall ambience

        If the feature is not mentioned in the review, give a neutral score of 0.5.

        Review: "{review}"

        Provide your response in JSON format:
        {{
            "Quality of food & drinks": float,
            "Quality of customer service": float,
            "Cleanliness of store": float,
            "Overall ambience": float
        }}
        """

        # retry loop with exponential backoff
        for attempt in range(5):
            try:
                response = litellm.completion(
                    model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
                )
                result = response["choices"][0]["message"]["content"].strip()

                result = re.sub(
                    r"^```(?:json)?", "", result.strip(), flags=re.IGNORECASE
                )
                result = re.sub(r"```$", "", result.strip())
                result = json.loads(result)
                break
            except Exception as e:
                wait = (2**attempt) + random.random()
                print(f"Error on row {i}: {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
        else:
            # failed all attempts
            result = {
                "Quality of food & drinks": 0.5,
                "Quality of customer service": 0.5,
                "Cleanliness of store": 0.5,
                "Overall ambience": 0.5,
            }

        # append results
        quality_of_food_drinks_scores.append(
            result.get("Quality of food & drinks", 0.5)
        )
        quality_of_customer_service_scores.append(
            result.get("Quality of customer service", 0.5)
        )
        cleanliness_of_store_scores.append(result.get("Cleanliness of store", 0.5))
        overall_ambience_scores.append(result.get("Overall ambience", 0.5))

        # Save progress every 50 rows (checkpoint)
        if (i + 1) % 50 == 0 or (i + 1) == len(df_input):
            temp_df = df_input.iloc[: i + 1].copy()
            temp_df["quality_of_drinks_sentiment"] = quality_of_food_drinks_scores
            temp_df["quality_of_customer_service_sentiment"] = (
                quality_of_customer_service_scores
            )
            temp_df["cleanliness_of_store_sentiment"] = cleanliness_of_store_scores
            temp_df["overall_ambience_sentiment"] = overall_ambience_scores

            combined = pd.concat([all_results, temp_df])
            combined.to_csv(CHECKPOINT_FILE, index=False)
            print(f"Checkpoint saved at row {i+1}.")

    # Final save
    df_input["quality_of_drinks_sentiment"] = quality_of_food_drinks_scores
    df_input["quality_of_customer_service_sentiment"] = (
        quality_of_customer_service_scores
    )
    df_input["cleanliness_of_store_sentiment"] = cleanliness_of_store_scores
    df_input["overall_ambience_sentiment"] = overall_ambience_scores

    final_df = pd.concat([all_results, df_input])
    final_df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    enrich_review_features()
