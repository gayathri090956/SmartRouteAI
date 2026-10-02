import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# 1. Load the dataset
df = pd.read_csv("data.csv")


# 2. Select input features
X = df[
    [
        "Traffic_Level",
        "Construction",
        "Drainage_Leak",
        "Road_Condition",
        "Weather",
        "Distance_km",
        "Time_of_Day"
    ]
]


# 3. Select what we want to predict
y = df["Travel_Time_min"]


# 4. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 5. Create the Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# 6. Train the model
model.fit(X_train, y_train)


# 7. Make predictions
predictions = model.predict(X_test)


# 8. Check model performance
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


print("================================")
print("   SMARTROUTE AI ML MODEL")
print("================================")

print("Model Training Complete!")

print("Mean Absolute Error:",
      round(mae, 2), "minutes")

print("R2 Score:",
      round(r2, 2))


# 9. Save the trained model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)


print("\nModel saved successfully as model.pkl")