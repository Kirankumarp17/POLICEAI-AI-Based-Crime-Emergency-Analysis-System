import pandas as pd
import folium
from folium.plugins import HeatMap

# ==========================================
# 🚔 POLICEAI - CRIME HOTSPOT MAP
# ==========================================

# Load dataset
data = pd.read_csv("data/crime_data.csv")

# Create Bengaluru map
crime_map = folium.Map(
    location=[12.9716, 77.5946],
    zoom_start=11,
    tiles=None
)

# ==========================================
# Add Esri World Street Map
# ==========================================

folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri World Street Map",
    overlay=False,
    control=True
).add_to(crime_map)

# ==========================================
# Prepare heatmap
# ==========================================

heat_data = data[
    [
        "Latitude",
        "Longitude",
        "Crime_Count"
    ]
].values.tolist()

# Add heatmap
HeatMap(
    heat_data,
    radius=20,
    blur=25,
    min_opacity=0.4,
    max_zoom=13
).add_to(crime_map)

# ==========================================
# Add incident markers
# ==========================================

sample_data = data.sample(
    min(100, len(data)),
    random_state=42
)

for _, row in sample_data.iterrows():

    popup_text = f"""
    <div style="width:250px">

    <h4>🚔 POLICEAI INCIDENT</h4>

    <b>Area:</b> {row['Area']}<br>
    <b>Crime:</b> {row['Crime_Type']}<br>
    <b>Date:</b> {row['Date']}<br>
    <b>Time:</b> {row['Time']}<br>
    <b>Weather:</b> {row['Weather']}<br>
    <b>Population Density:</b>
    {row['Population_Density']}<br>
    <b>Crime Count:</b>
    {row['Crime_Count']}

    </div>
    """

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=4,
        popup=folium.Popup(
            popup_text,
            max_width=300
        ),
        tooltip=row["Crime_Type"],
        fill=True
    ).add_to(crime_map)

# ==========================================
# Add layer control
# ==========================================

folium.LayerControl().add_to(crime_map)

# ==========================================
# Save
# ==========================================

crime_map.save(
    "crime_heatmap.html"
)

print("==========================================")
print("🚔 POLICEAI CRIME HOTSPOT MAP")
print("==========================================")
print("✅ Map created successfully!")
print()
print("Run:")
print("python -m http.server 8000")
print()
print("Then open:")
print("http://localhost:8000/crime_heatmap.html")