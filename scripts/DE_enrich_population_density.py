import pandas as pd

INPUT_FILE = "data/processed/starbucks_reviews_flat_all.csv"
DENSITY_FILE = "data/raw/Population-Density-Final.xlsx"
OUTPUT_FILE = "data/processed/starbucks_reviews_flat_with_density.csv"


def enrich_population_density():
    df_input = pd.read_csv(INPUT_FILE)
    df_density = pd.read_excel(DENSITY_FILE)

    # get only zipcode and density from df_density
    df_density = df_density[["Zip", "density"]]

    # covert zip to integer
    df_density["Zip"] = df_density["Zip"].astype(str)

    # merge on zipcode
    df_merged = pd.merge(
        df_input, df_density, left_on="business_postal_code", right_on="Zip", how="left"
    )
    df_merged = df_merged.drop(columns=["Zip"])

    # rename density column to population density
    df_merged = df_merged.rename(columns={"density": "population_density"})

    df_merged.to_csv(OUTPUT_FILE, index=False)


def count_missing_density():
    df = pd.read_csv(OUTPUT_FILE)

    # get zipcodes with missing density values
    missing_density = df[df["population_density"].isnull()][
        "business_postal_code"
    ].unique()
    print(missing_density)


if __name__ == "__main__":
    enrich_population_density()
    # count_missing_density()
