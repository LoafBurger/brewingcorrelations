import json

# file paths
INPUT_FILE = "data/raw/yelp_academic_dataset_business.json"
OUTPUT_FILE = "data/processed/starbucks_businesses.json"


def filter_starbucks_businesses(input_file, output_file):
    """Filter Starbucks businesses from the Yelp business dataset."""
    count = 0
    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:  # reads business dataset line by line, loads each json
            business = json.loads(line)
            if "Starbucks" in business["name"]:  # keeps only Starbucks
                outfile.write(json.dumps(business) + "\n")
                count += 1
    return count


def main():
    print("Filtering Starbucks businesses...")
    total = filter_starbucks_businesses(INPUT_FILE, OUTPUT_FILE)
    print(f"Filtered {total} Starbucks businesses into {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
