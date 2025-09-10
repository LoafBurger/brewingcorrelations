import json

# file paths
STARBUCKS_BUSINESS_FILE = "data/processed/starbucks_businesses.json"
REVIEWS_FILE = "data/raw/yelp_academic_dataset_review.json"
OUTPUT_FILE = "data/processed/starbucks_reviews.json"


def load_starbucks_ids(business_file):
    """Load all Starbucks business IDs into a set."""
    starbucks_ids = set()
    with open(business_file, "r", encoding="utf-8") as f:
        for line in f:
            business = json.loads(line)
            starbucks_ids.add(business["business_id"])
    return starbucks_ids


def filter_reviews(reviews_file, starbucks_ids, output_file):
    """Filter reviews for Starbucks businesses only."""
    with open(reviews_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            review = json.loads(line)
            if review["business_id"] in starbucks_ids:
                outfile.write(json.dumps(review) + "\n")


def main():
    print("Loading Starbucks business IDs...")
    starbucks_ids = load_starbucks_ids(STARBUCKS_BUSINESS_FILE)
    print(f"Found {len(starbucks_ids)} Starbucks locations.")

    print("Filtering reviews...")
    filter_reviews(REVIEWS_FILE, starbucks_ids, OUTPUT_FILE)
    print(f"Filtered reviews saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
