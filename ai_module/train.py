import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("data/synthetic_tasks.csv")

X = df[[
    "severity_score",
    "population_affected",
    "hours_since_reported"
]]

y = df["urgency_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


predictions = model.predict(X_test)


mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model Performance")
print("------------------")
print(f"Mean Absolute Error : {mae:.2f}")
print(f"R² Score            : {r2:.2f}")


joblib.dump(model, "models/model.pkl")

print("\nModel saved successfully!")