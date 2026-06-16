import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

folder = "ai/dataset"

all_data = []

print("Loading CSV files...")

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)

        print("Reading:", file)

        try:

            df = pd.read_csv(
                path,
                low_memory=False,
                nrows=10000
            )

            all_data.append(df)

        except Exception as e:

            print(f"Skipping {file}: {e}")

print("\nCombining datasets...")

dataset = pd.concat(
    all_data,
    ignore_index=True
)

print("Dataset loaded.")
print("Rows:", len(dataset))

dataset.columns = dataset.columns.str.strip()

# Remove duplicate header rows
dataset = dataset[
    dataset["Label"] != "Label"
]

# Replace inf values
dataset = dataset.replace(
    [np.inf, -np.inf],
    np.nan
)

dataset = dataset.fillna(0)

# Features
X = dataset.drop(
    "Label",
    axis=1
)

# Convert every column to numeric
for col in X.columns:

    X[col] = pd.to_numeric(
        X[col],
        errors="coerce"
    )

# Clean again after conversion
X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

# Prevent huge values causing float32 overflow
X = X.clip(
    lower=-1e10,
    upper=1e10
)

X = X.astype("float32")

# Labels
y = dataset["Label"]

print("\nUnique Labels:")
print(y.unique())

print("\nFeature Count:")
print(len(X.columns))

# Encode labels
encoder = LabelEncoder()

y = encoder.fit_transform(y)

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nChecking dataset...")

print("Infinite values:",
      np.isinf(X_train.values).sum())

print("NaN values:",
      np.isnan(X_train.values).sum())

print("\nTraining model...")

model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

accuracy = model.score(
    X_test,
    y_test
)

print(f"\nAccuracy: {accuracy:.4f}")

joblib.dump(
    model,
    "model.pkl"
)

joblib.dump(
    encoder,
    "encoder.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "features.pkl"
)

print("\nClasses Learned:")
print(encoder.classes_)

print("\nModel saved successfully.")