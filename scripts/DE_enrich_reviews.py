import json

# File paths
BUSINESS_FILE = "data/processed/starbucks_businesses.json"
REVIEWS_FILE = "data/processed/starbucks_reviews.json"
OUTPUT_FILE = "data/processed/starbucks_reviews_enriched.json"

def load_business_info(business_file):
    """Load selected business info into a dictionary keyed by business_id."""
    lookup = {}
    with open(business_file, "r", encoding="utf-8") as f:
        for line in f:
            business_entry = json.loads(line)
            attributes = business_entry.get("attributes") or {}
            lookup[business_entry["business_id"]] = {
                "name": business_entry.get("name"),
                "address": business_entry.get("address"),
                "city": business_entry.get("city"),
                "state": business_entry.get("state"),
                "postal_code": business_entry.get("postal_code"),
                "latitude": business_entry.get("latitude"),
                "longitude": business_entry.get("longitude"),
                "stars": business_entry.get("stars"),
                "review_count": business_entry.get("review_count"),
                "is_open": business_entry.get("is_open"),
                "categories": business_entry.get("categories"),
                "hours": business_entry.get("hours"),
                "attributes": {
                    "WiFi": attributes.get("WiFi"),
                    "DriveThru": attributes.get("DriveThru"),
                    "RestaurantsTakeOut": attributes.get("RestaurantsTakeOut"),
                    "RestaurantsDelivery": attributes.get("RestaurantsDelivery"),
                    "OutdoorSeating": attributes.get("OutdoorSeating"),
                    "RestaurantsPriceRange2": attributes.get("RestaurantsPriceRange2"),
                    "BusinessAcceptsCreditCards": attributes.get("BusinessAcceptsCreditCards"),
                    "BikeParking": attributes.get("BikeParking"),
                }
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

