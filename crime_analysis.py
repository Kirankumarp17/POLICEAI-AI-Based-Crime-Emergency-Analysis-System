import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(
    "data/crime_data.csv"
)

print()
print("=" * 50)
print("🚔 POLICEAI CRIME ANALYSIS")
print("=" * 50)

# Dataset information
print("\nTotal Records:", len(data))

print(
    "Number of Areas:",
    data["Area"].nunique()
)

print(
    "Number of Crime Types:",
    data["Crime_Type"].nunique()
)

# Crime type statistics
print("\n===== CRIME TYPES =====")

print(
    data["Crime_Type"].value_counts()
)

# Average crime count
print("\n===== AVERAGE CRIME COUNT =====")

print(
    data["Crime_Count"].mean()
)

# Highest crime area
print("\n===== AREA ANALYSIS =====")

area_crimes = data.groupby(
    "Area"
)["Crime_Count"].sum()

print(
    area_crimes.sort_values(
        ascending=False
    )
)

# Crime type graph
plt.figure(
    figsize=(10, 6)
)

data["Crime_Type"].value_counts().plot(
    kind="bar"
)

plt.title(
    "POLICEAI - Crime Type Distribution"
)

plt.xlabel(
    "Crime Type"
)

plt.ylabel(
    "Number of Incidents"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.show()