import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==========================================
# 🚔 POLICEAI - AI CRIME PREDICTION
# ==========================================

print()
print("=" * 60)
print("🚔 POLICEAI - AI CRIME PREDICTION SYSTEM")
print("=" * 60)


# ==========================================
# 1. Load Dataset
# ==========================================

data = pd.read_csv(
    "data/crime_data.csv"
)

print()
print("📊 Dataset loaded")
print("Total records:", len(data))


# ==========================================
# 2. Create Encoders
# ==========================================

crime_encoder = LabelEncoder()
weather_encoder = LabelEncoder()
density_encoder = LabelEncoder()
area_encoder = LabelEncoder()


data["Crime_Type_Code"] = crime_encoder.fit_transform(
    data["Crime_Type"]
)

data["Weather_Code"] = weather_encoder.fit_transform(
    data["Weather"]
)

data["Density_Code"] = density_encoder.fit_transform(
    data["Population_Density"]
)

data["Area_Code"] = area_encoder.fit_transform(
    data["Area"]
)


# ==========================================
# 3. Select Features
# ==========================================

features = [
    "Latitude",
    "Longitude",
    "Hour",
    "Day_Number",
    "Month_Number",
    "Crime_Type_Code",
    "Weather_Code",
    "Density_Code",
    "Area_Code"
]


X = data[features]

y = data["Crime_Count"]


# ==========================================
# 4. Split Dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print()
print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 5. Create AI Model
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 6. Train Model
# ==========================================

print()
print("🤖 Training POLICEAI model...")

model.fit(
    X_train,
    y_train
)

print("✅ Model training completed!")


# ==========================================
# 7. Test Model
# ==========================================

predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print()
print("=" * 60)
print("📈 MODEL PERFORMANCE")
print("=" * 60)

print(
    "Mean Absolute Error:",
    round(mae, 3)
)

print(
    "R² Score:",
    round(r2, 3)
)

# ==========================================
# Save Model Performance
# ==========================================

joblib.dump(
    {
        "mae": mae,
        "r2": r2
    },
    "models/model_performance.pkl"
)


# ==========================================
# 8. Create Models Folder
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)


# ==========================================
# 9. Save Model
# ==========================================

joblib.dump(
    model,
    "models/policeai_crime_model.pkl"
)

joblib.dump(
    crime_encoder,
    "models/crime_encoder.pkl"
)

joblib.dump(
    weather_encoder,
    "models/weather_encoder.pkl"
)

joblib.dump(
    density_encoder,
    "models/density_encoder.pkl"
)

joblib.dump(
    area_encoder,
    "models/area_encoder.pkl"
)


# ==========================================
# 10. Completion Message
# ==========================================

print()
print("=" * 60)
print("🎉 POLICEAI MODEL READY!")
print("=" * 60)

print()
print("Saved files:")

print("✅ models/policeai_crime_model.pkl")
print("✅ models/crime_encoder.pkl")
print("✅ models/weather_encoder.pkl")
print("✅ models/density_encoder.pkl")
print("✅ models/area_encoder.pkl")

print()
print("🚔 AI model is ready for prediction.")