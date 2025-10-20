import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

CSV_FILE = "data/processed/final_cleaned_data.csv"

# load data
df = pd.read_csv(CSV_FILE)

# set target feature and other features
target = 'stars'

numeric_cols = [
    'useful', 'funny', 'cool', 'business_latitude', 'business_longitude',
    'business_stars', 'business_review_count', 'business_is_open',
    'business_attributes.RestaurantsPriceRange2', 'user_review_count',
    'user_useful', 'user_funny', 'user_cool', 'user_fans', 'user_average_stars',
    'user_compliment_hot', 'user_compliment_more', 'user_compliment_profile',
    'user_compliment_cute', 'user_compliment_list', 'user_compliment_note',
    'user_compliment_plain', 'user_compliment_cool', 'user_compliment_funny',
    'user_compliment_writer', 'user_compliment_photos', 'population_density',
    'quality_of_drinks_sentiment', 'quality_of_customer_service_sentiment',
    'cleanliness_of_store_sentiment', 'overall_ambience_sentiment',
    'user_friend_count', 'monday_duration', 'tuesday_duration', 'wednesday_duration',
    'thursday_duration', 'friday_duration', 'saturday_duration', 'sunday_duration',
    'total_hours'
]

# keep only simple categorical features
categorical_cols = ['business_attributes.WiFi']

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
