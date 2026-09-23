import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "Dataset",
        "tasks.csv"
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.pkl"
)


# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", list(df.columns))


# Features
X = df[
    [
        "severity",
        "population_affected"
    ]
]

# Target
y = df["urgency_score"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Prediction
predictions = model.predict(X_test)


# Evaluation
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation")
print("----------------")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))


# Create models folder
os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


# Save model
joblib.dump(model, MODEL_PATH)

print("\nModel saved at:")
print(MODEL_PATH)