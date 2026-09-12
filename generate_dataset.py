import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ==========================================
# 🚔 POLICEAI
# Synthetic Crime Dataset Generator
# ==========================================

# Number of records
NUMBER_OF_RECORDS = 5000

# Bengaluru demo areas
areas = {
    "Indiranagar": (12.9784, 77.6408),
    "Whitefield": (12.9698, 77.7500),
    "Electronic City": (12.8452, 77.6602),
    "Koramangala": (12.9352, 77.6245),
    "Jayanagar": (12.9250, 77.5937),
    "Malleshwaram": (13.0035, 77.5700),
    "Rajajinagar": (12.9916, 77.5550),
    "Yeshwanthpur": (13.0280, 77.5400),
    "BTM Layout": (12.9166, 77.6101),
    "Hebbal": (13.0358, 77.5970),
    "Banashankari": (12.9255, 77.5468),
    "Marathahalli": (12.9591, 77.6974),
    "HSR Layout": (12.9116, 77.6389),
    "Basavanagudi": (12.9416, 77.5750),
    "Kengeri": (12.9141, 77.4820)
}

# Crime types
crime_types = [
    "Theft",
    "Robbery",
    "Assault",
    "Burglary",
    "Vehicle Theft",
    "Cyber Crime",
    "Fraud",
    "Missing Person",
    "Accident",
    "Vandalism"
]

# Weather conditions
weather_conditions = [
    "Sunny",
    "Cloudy",
    "Rainy",
    "Partly Cloudy"
]

# Population density categories
population_density = [
    "Low",
    "Medium",
    "High",
    "Very High"
]


# ==========================================
# Generate records
# ==========================================

records = []

start_date = datetime(2025, 1, 1)

for i in range(NUMBER_OF_RECORDS):

    # Random date
    random_days = random.randint(0, 729)

    date = start_date + timedelta(
        days=random_days
    )

    # Random time
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    time = f"{hour:02d}:{minute:02d}"

    # Select area
    area = random.choice(
        list(areas.keys())
    )

    base_latitude, base_longitude = areas[area]

    # Add small random location variation
    latitude = base_latitude + random.uniform(
        -0.008, 0.008
    )

    longitude = base_longitude + random.uniform(
        -0.008, 0.008
    )

    # Select crime
    crime_type = random.choice(
        crime_types
    )

    # Select weather
    weather = random.choice(
        weather_conditions
    )

    # Select population density
    density = random.choice(
        population_density
    )

    # --------------------------------------
    # Generate crime count
    # --------------------------------------

    crime_count = random.randint(1, 5)

    # Night-time incidents slightly higher
    if hour >= 20 or hour <= 4:
        crime_count += random.randint(1, 4)

    # Weekend effect
    if date.weekday() >= 5:
        crime_count += random.randint(0, 2)

    # High population areas
    if density == "High":
        crime_count += random.randint(1, 2)

    elif density == "Very High":
        crime_count += random.randint(2, 4)

    # Some crimes naturally get higher counts
    if crime_type in [
        "Theft",
        "Vehicle Theft",
        "Fraud"
    ]:
        crime_count += random.randint(0, 2)

    # Limit count
    crime_count = min(
        crime_count,
        20
    )

    # --------------------------------------
    # Create record
    # --------------------------------------

    record = {
        "Date": date.strftime("%Y-%m-%d"),
        "Time": time,
        "Hour": hour,
        "Day": date.strftime("%A"),
        "Day_Number": date.weekday() + 1,
        "Month": date.strftime("%B"),
        "Month_Number": date.month,
        "Latitude": round(latitude, 6),
        "Longitude": round(longitude, 6),
        "Area": area,
        "Crime_Type": crime_type,
        "Crime_Count": crime_count,
        "Weather": weather,
        "Population_Density": density
    }

    records.append(record)


# ==========================================
# Convert to DataFrame
# ==========================================

data = pd.DataFrame(records)


# ==========================================
# Create data folder
# ==========================================

os.makedirs(
    "data",
    exist_ok=True
)


# ==========================================
# Save CSV
# ==========================================

file_path = "data/crime_data.csv"

data.to_csv(
    file_path,
    index=False
)


# ==========================================
# Display information
# ==========================================

print()
print("=" * 50)
print("🚔 POLICEAI DATASET GENERATOR")
print("=" * 50)

print()
print("✅ Dataset created successfully!")

print()
print("📊 Number of records:", len(data))

print()
print("📁 File created:")
print(file_path)

print()
print("📋 Columns:")
print(list(data.columns))

print()
print("🔎 Crime types:")
print(data["Crime_Type"].value_counts())

print()
print("📍 Areas:")
print(data["Area"].nunique())

print()
print("🎯 Sample records:")
print(data.head(10))

print()
print("=" * 50)