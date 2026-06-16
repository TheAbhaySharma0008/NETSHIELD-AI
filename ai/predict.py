import joblib
import pandas as pd

model = joblib.load("model.pkl")
encoder = joblib.load("encoder.pkl")
features = joblib.load("features.pkl")

sample = pd.read_csv(
    "ai/dataset/02-14-2018.csv",
    nrows=1
)

sample.columns = sample.columns.str.strip()

if "Label" in sample.columns:
    sample = sample.drop("Label", axis=1)

sample = sample.select_dtypes(include=["number"])

# Make columns exactly match training columns
sample = sample.reindex(columns=features, fill_value=0)

print("Feature count:", len(features))
print("Sample shape:", sample.shape)

prediction = model.predict(sample)

attack = encoder.inverse_transform(prediction)

print("\nPredicted Attack:", attack[0])