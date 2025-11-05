import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn import tree as sktree

CSV_FILE = "data/processed/final_cleaned_data.csv"

# load data
df = pd.read_csv(CSV_FILE)

# aggregate by business_id 
df = df.groupby('business_id').agg({
    'business_attributes.WiFi': 'first', 
    'business_attributes.RestaurantsTakeOut': 'first', 
    'business_attributes.DriveThru': 'first', 
    'business_attributes.RestaurantsDelivery': 'first', 
    'business_attributes.OutdoorSeating': 'first', 
    'business_attributes.BusinessAcceptsCreditCards': 'first', 
    'business_attributes.BikeParking': 'first',
    'business_stars': 'first',
    'business_latitude': 'first',
    'business_longitude': 'first',
    'business_review_count': 'mean',
    'business_is_open': 'first',
    'business_attributes.RestaurantsPriceRange2': 'mean',
    'population_density': 'mean',
    'monday_duration': 'first', 
    'tuesday_duration': 'first', 
    'wednesday_duration': 'first',
    'thursday_duration': 'first', 
    'friday_duration': 'first', 
    'saturday_duration': 'first', 
    'sunday_duration': 'first',
    'total_hours': 'mean', 
    'quality_of_drinks_sentiment': 'mean', 
    'quality_of_customer_service_sentiment': 'mean',
    'cleanliness_of_store_sentiment': 'mean', 
    'overall_ambience_sentiment': 'mean'
}).reset_index()

# set target feature and other features
target = 'business_stars'

numeric_cols = [
    'business_latitude', 'business_longitude',
    'business_review_count', 'business_is_open',
    'business_attributes.RestaurantsPriceRange2', 'population_density',
    'monday_duration', 'tuesday_duration', 'wednesday_duration',
    'thursday_duration', 'friday_duration', 'saturday_duration', 'sunday_duration',
    'total_hours', 'quality_of_drinks_sentiment', 'quality_of_customer_service_sentiment',
    'cleanliness_of_store_sentiment', 'overall_ambience_sentiment'
]

# keep only simple categorical features
categorical_cols = ['business_attributes.WiFi', 'business_attributes.RestaurantsTakeOut', 'business_attributes.DriveThru', 'business_attributes.RestaurantsDelivery', 'business_attributes.OutdoorSeating', 'business_attributes.BusinessAcceptsCreditCards', 'business_attributes.BikeParking']

# filter existing columns
numeric_cols = [c for c in numeric_cols if c in df.columns]
categorical_cols = [c for c in categorical_cols if c in df.columns]

X = df[numeric_cols + categorical_cols]
y = df[target]

# train and test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# preprocessing since decision trees don’t need scaling but just need to handle missing values and encode categories
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='mean'))
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_cols),
    ('cat', categorical_transformer, categorical_cols)
])

# decision tree model
dt_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', DecisionTreeRegressor(
        max_depth=5,
        min_samples_leaf=10,
        random_state=42
    ))
])

# train model
dt_pipeline.fit(X_train, y_train)

# evaluate model
y_pred = dt_pipeline.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("\n===== Decision Tree Model =====")
print(f"RMSE: {rmse:.3f}")

# calculate the R^2 value
r2 = dt_pipeline.score(X_test, y_test)
print(f"R^2: {r2:.3f}")

# interpret results
feature_names_cat = []
if categorical_cols:
    feature_names_cat = dt_pipeline.named_steps['preprocessor'] \
        .named_transformers_['cat'] \
        .named_steps['onehot'] \
        .get_feature_names_out(categorical_cols)

all_feature_names = np.concatenate([numeric_cols, feature_names_cat])
importances = dt_pipeline.named_steps['regressor'].feature_importances_

importance_df = pd.DataFrame({
    'Feature': all_feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\n===== Top 10 Most Important Features =====")
print(importance_df.head(10).to_string(index=False))

# save results for further analysis
importance_df.to_csv("models/feature_importance.csv", index=False)
print("\nFeature importance saved to models/feature_importance.csv")

# ----- Decision tree visualization -----
try:
    # the trained decision tree is the 'regressor' step in the pipeline
    reg = dt_pipeline.named_steps['regressor']

    # all_feature_names already computed above and corresponds to transformed features
    # Plot and save a PNG of the full tree (may be large). We limit depth for readability.
    fig = plt.figure(figsize=(36, 16))
    sktree.plot_tree(
        reg,
        feature_names=all_feature_names,
        filled=True,
        rounded=True,
        max_depth=5,
        fontsize=10
    )
    fig.tight_layout()
    out_path = "models/dt_tree.png"
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"\nDecision tree visualization saved to {out_path}")
except Exception as e:
    print(f"\nCould not produce decision tree visualization: {e}")
    print("If you want a prettier image, install graphviz and use export_graphviz + pydot or dtreeviz.")
