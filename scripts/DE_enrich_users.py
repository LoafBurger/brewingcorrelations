import json

# file paths
REVIEWS_FILE = "data/processed/starbucks_reviews_enriched.json"
USERS_FILE = "data/raw/yelp_academic_dataset_user.json"
OUTPUT_FILE = "data/processed/starbucks_reviews_enriched_with_users.json"


def load_user_data(user_file):
    """Load all user info into a dictionary keyed by user_id."""
    user_lookup = {}
    with open(user_file, "r", encoding="utf-8") as f:
        for line in f:
            user = json.loads(line)
            user_lookup[user["user_id"]] = user
    return user_lookup


def enrich_reviews_with_users(reviews_file, user_lookup, output_file):
    """Add user info to each review (inner join on user_id)."""
    count = 0
    with open(reviews_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            review = json.loads(line)
            user_info = user_lookup.get(review["user_id"])
            if user_info:  # inner join
                review["user_info"] = user_info
                outfile.write(json.dumps(review) + "\n")
                count += 1
    return count


def main():
    print("Loading user data...")
    user_lookup = load_user_data(USERS_FILE)
    print(f"Loaded {len(user_lookup)} users.")

    print("Enriching reviews with user info...")
    total_reviews = enrich_reviews_with_users(REVIEWS_FILE, user_lookup, OUTPUT_FILE)
    print(f"Enriched {total_reviews} reviews. Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
