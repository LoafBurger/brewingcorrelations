import json

# File paths
BUSINESS_FILE = "data/processed/starbucks_businesses.json"
REVIEWS_FILE = "data/processed/starbucks_reviews.json"
OUTPUT_FILE = "data/processed/starbucks_reviews_enriched.json"

def load_business_info(business_file):
    """Load business info into a dictionary keyed by business_id."""
    lookup = {}
    with open(business_file, "r", encoding="utf-8") as f:
        for line in f:
            biz = json.loads(line)
            lookup[biz["business_id"]] = {
                "name": biz["name"],
                "address": biz["address"],
                "city": biz["city"],
                "state": biz["state"],
                "postal_code": biz["postal_code"],
                "stars": biz["stars"],
                "review_count": biz["review_count"],
                "is_open": biz["is_open"],
                "attributes": biz.get("attributes", {})
            }
    return lookup

def enrich_reviews(reviews_file, business_lookup, output_file):
    """Add business info to each review."""
    count = 0
    with open(reviews_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            review = json.loads(line)
            biz_info = business_lookup.get(review["business_id"], {})
            review["business_info"] = biz_info
            outfile.write(json.dumps(review) + "\n")
            count += 1
    return count

def main():
    print("Loading business info...")
    business_lookup = load_business_info(BUSINESS_FILE)
    print(f"Loaded info for {len(business_lookup)} Starbucks locations.")

    print("Enriching reviews...")
    total_reviews = enrich_reviews(REVIEWS_FILE, business_lookup, OUTPUT_FILE)
    print(f"Enriched {total_reviews} reviews. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

