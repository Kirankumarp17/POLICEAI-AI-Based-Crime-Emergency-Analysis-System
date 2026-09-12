import pandas as pd
import joblib
from datetime import datetime


# ==========================================
# 🚔 POLICEAI - INTERACTIVE CRIME PREDICTOR
# ==========================================

print()
print("=" * 60)
print("🚔 POLICEAI - CRIME RISK PREDICTOR")
print("=" * 60)


# ==========================================
# Load dataset
# ==========================================

data = pd.read_csv(
    "data/crime_data.csv"
)


# ==========================================
# Load trained model
# ==========================================

model = joblib.load(
    "models/policeai_crime_model.pkl"
)

crime_encoder = joblib.load(
    "models/crime_encoder.pkl"
)

weather_encoder = joblib.load(
    "models/weather_encoder.pkl"
)

density_encoder = joblib.load(
    "models/density_encoder.pkl"
)

area_encoder = joblib.load(
    "models/area_encoder.pkl"
)


# ==========================================
# Select Area
# ==========================================

areas = sorted(
    data["Area"].unique()
)

print()
print("📍 AVAILABLE AREAS")

for i, area in enumerate(areas, 1):
    print(f"{i}. {area}")

while True:

    try:

        area_choice = int(
            input("\nSelect area number: ")
        )

        if 1 <= area_choice <= len(areas):
            break

        print("❌ Invalid area number.")

    except ValueError:

        print("❌ Please enter a number.")


area = areas[
    area_choice - 1
]


# ==========================================
# Date
# ==========================================

while True:

    date_input = input(
        "\n📅 Enter date (YYYY-MM-DD): "
    )

    try:

        selected_date = datetime.strptime(
            date_input,
            "%Y-%m-%d"
        )

        break

    except ValueError:

        print(
            "❌ Invalid date. Example: 2026-09-15"
        )


day_number = (
    selected_date.weekday() + 1
)

month_number = (
    selected_date.month
)


# ==========================================
# Time
# ==========================================

while True:

    time_input = input(
        "\n🕐 Enter time (HH:MM): "
    )

    try:

        selected_time = datetime.strptime(
            time_input,
            "%H:%M"
        )

        break

    except ValueError:

        print(
            "❌ Invalid time. Example: 22:30"
        )


hour = selected_time.hour


# ==========================================
# Crime Type
# ==========================================

crime_types = list(
    crime_encoder.classes_
)

print()
print("🚨 CRIME TYPES")

for i, crime in enumerate(
    crime_types,
    1
):

    print(f"{i}. {crime}")


while True:

    try:

        crime_choice = int(
            input("\nSelect crime type number: ")
        )

        if 1 <= crime_choice <= len(crime_types):
            break

        print("❌ Invalid choice.")

    except ValueError:

        print("❌ Please enter a number.")


crime_type = crime_types[
    crime_choice - 1
]


# ==========================================
# Weather
# ==========================================

weather_types = list(
    weather_encoder.classes_
)

print()
print("🌦️ WEATHER")

for i, weather in enumerate(
    weather_types,
    1
):

    print(f"{i}. {weather}")


while True:

    try:

        weather_choice = int(
            input("\nSelect weather number: ")
        )

        if 1 <= weather_choice <= len(weather_types):
            break

        print("❌ Invalid choice.")

    except ValueError:

        print("❌ Please enter a number.")


weather = weather_types[
    weather_choice - 1
]


# ==========================================
# Population Density
# ==========================================

density_types = list(
    density_encoder.classes_
)

print()
print("👥 POPULATION DENSITY")

for i, density in enumerate(
    density_types,
    1
):

    print(f"{i}. {density}")


while True:

    try:

        density_choice = int(
            input("\nSelect density number: ")
        )

        if 1 <= density_choice <= len(density_types):
            break

        print("❌ Invalid choice.")

    except ValueError:

        print("❌ Please enter a number.")


density = density_types[
    density_choice - 1
]


# ==========================================
# Encode values
# ==========================================

crime_code = crime_encoder.transform(
    [crime_type]
)[0]

weather_code = weather_encoder.transform(
    [weather]
)[0]

density_code = density_encoder.transform(
    [density]
)[0]

area_code = area_encoder.transform(
    [area]
)[0]


# ==========================================
# Get coordinates for selected area
# ==========================================

area_data = data[
    data["Area"] == area
]

latitude = area_data[
    "Latitude"
].mean()

longitude = area_data[
    "Longitude"
].mean()


# ==========================================
# Create prediction input
# ==========================================

input_data = pd.DataFrame(
    [[
        latitude,
        longitude,
        hour,
        day_number,
        month_number,
        crime_code,
        weather_code,
        density_code,
        area_code
    ]],
    columns=[
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
)


# ==========================================
# Prediction
# ==========================================

prediction = model.predict(
    input_data
)[0]


prediction = max(
    0,
    prediction
)


# ==========================================
# Risk Level
# ==========================================

if prediction >= 12:

    risk = "🔴 CRITICAL"

elif prediction >= 8:

    risk = "🟠 HIGH"

elif prediction >= 4:

    risk = "🟡 MEDIUM"

else:

    risk = "🟢 LOW"


# ==========================================
# Display Result
# ==========================================

print()
print("=" * 60)
print("🚔 POLICEAI ANALYSIS RESULT")
print("=" * 60)

print()
print("📍 Area:", area)

print(
    "📅 Date:",
    selected_date.strftime("%d-%m-%Y")
)

print(
    "🕐 Time:",
    time_input
)

print(
    "🚨 Crime Type:",
    crime_type
)

print(
    "🌦️ Weather:",
    weather
)

print(
    "👥 Population Density:",
    density
)

print()
print("-" * 60)

print(
    "🤖 Predicted Crime Count:",
    round(prediction, 2)
)

print(
    "⚠️ Risk Level:",
    risk
)

print("-" * 60)

print()
print(
    "⚠️ This is an experimental prediction "
    "based on synthetic project data."
)

print()
print("=" * 60)