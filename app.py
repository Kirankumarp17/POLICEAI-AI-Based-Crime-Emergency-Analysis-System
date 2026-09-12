import streamlit as st
import pandas as pd
import joblib
import folium

from folium.plugins import HeatMap

from streamlit_folium import st_folium

from database import (
    add_incident,
    get_incidents,
    update_status,
    add_emergency_alert,
    get_emergency_alerts,
    update_emergency_status
)

from complaint_classifier import classify_complaint

df = pd.read_csv("data/crime_data.csv")

# =========================================================
# 🚔 POLICEAI
# AI-Based Crime & Emergency Analysis System
# =========================================================

st.set_page_config(
    page_title="POLICEAI",
    page_icon="🚔",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/crime_data.csv"
    )


data = load_data()


# =========================================================
# LOAD ML MODEL
# =========================================================

@st.cache_resource
def load_model():

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
    performance = joblib.load(
        "models/model_performance.pkl"
    )

    return (
        model,
        crime_encoder,
        weather_encoder,
        density_encoder,
        area_encoder,
        performance
    )


(
    model,
    crime_encoder,
    weather_encoder,
    density_encoder,
    area_encoder,
    performance
) = load_model()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚔 POLICEAI")

st.sidebar.write(
    "AI Crime & Emergency Analysis"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🤖 Crime Risk Prediction",
        "📝 Complaint Analysis",
        "📊 Crime Analytics",
        "🗺️ Crime Hotspot Map",
        "📋 Incident Management",
        "📹 CCTV AI Monitoring",
        "🚨 Emergency Alerts",
        "🚨 Emergency Management",
        "ℹ️ About"
    ]
)
# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🚔 POLICEAI COMMAND CENTER")

    st.subheader(
        "AI-Based Crime & Emergency Analysis System"
    )

    st.write(
        "Centralized dashboard for crime analytics, "
        "AI predictions and incident management."
    )

    st.divider()

    # =========================================
    # DATASET STATISTICS
    # =========================================

    total_records = len(data)

    total_crime_types = data[
        "Crime_Type"
    ].nunique()

    total_areas = data[
        "Area"
    ].nunique()

    total_crimes = data[
        "Crime_Count"
    ].sum()

    # =========================================
    # DATABASE INCIDENT STATISTICS
    # =========================================

    incidents = get_incidents()

    total_incidents = len(incidents)

    pending_incidents = sum(
        1 for incident in incidents
        if incident[7] == "Pending"
    )

    resolved_incidents = sum(
        1 for incident in incidents
        if incident[7] == "Resolved"
    )

    # =========================================
    # TOP METRICS
    # =========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🚨 Total Crime Records",
            f"{total_records:,}"
        )

    with col2:

        st.metric(
            "📋 Registered Incidents",
            total_incidents
        )

    with col3:

        st.metric(
            "⏳ Pending Incidents",
            pending_incidents
        )

    with col4:

        st.metric(
            "✅ Resolved Incidents",
            resolved_incidents
        )

    st.divider()

    # =========================================
    # DATASET INFORMATION
    # =========================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🚨 Crime Distribution"
        )

        crime_chart = (
            data["Crime_Type"]
            .value_counts()
        )

        st.bar_chart(
            crime_chart
        )

    with col2:

        st.subheader(
            "📍 Crime by Area"
        )

        area_chart = (
            data.groupby("Area")[
                "Crime_Count"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            area_chart
        )

    st.divider()

    # =========================================
    # DATABASE INCIDENTS
    # =========================================

    st.subheader(
        "🚨 Recent Police Incidents"
    )

    if not incidents:

        st.info(
            "📭 No incidents registered yet."
        )

    else:

        incident_df = pd.DataFrame(
            incidents,
            columns=[
                "ID",
                "Complaint",
                "Crime Type",
                "Priority",
                "Location",
                "Date",
                "Time",
                "Status"
            ]
        )

        st.dataframe(
            incident_df.head(10),
            width="stretch",
            hide_index=True
        )

    st.divider()

    # =========================================
    # SYSTEM INFORMATION
    # =========================================

    st.subheader(
        "🤖 POLICEAI System"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🔴 Crime Types",
            total_crime_types
        )

    with col2:

        st.metric(
            "📍 Monitored Areas",
            total_areas
        )

    with col3:

        st.metric(
            "📊 Total Crime Count",
            f"{total_crimes:,}"
        )

    st.info(
        "⚠️ POLICEAI is an academic prototype "
        "using synthetic crime data. AI results "
        "are experimental and require human review."
    )

# =========================================================
# CRIME RISK PREDICTION
# =========================================================

elif page == "🤖 Crime Risk Prediction":

    st.title(
        "🤖 AI Crime Risk Prediction"
    )

    st.write(
        "Enter the conditions below to "
        "estimate the expected crime count."
    )

    st.divider()

    # ---------------------------------------------
    # Area
    # ---------------------------------------------

    areas = sorted(
        data["Area"].unique()
    )

    area = st.selectbox(
        "📍 Select Area",
        areas
    )

    # ---------------------------------------------
    # Date
    # ---------------------------------------------

    selected_date = st.date_input(
        "📅 Select Date"
    )

    # ---------------------------------------------
    # Time
    # ---------------------------------------------

    selected_hour = st.slider(
        "🕐 Select Hour",
        min_value=0,
        max_value=23,
        value=20
    )

    # ---------------------------------------------
    # Crime Type
    # ---------------------------------------------

    crime_types = list(
        crime_encoder.classes_
    )

    crime_type = st.selectbox(
        "🚨 Crime Type",
        crime_types
    )

    # ---------------------------------------------
    # Weather
    # ---------------------------------------------

    weather_types = list(
        weather_encoder.classes_
    )

    weather = st.selectbox(
        "🌦️ Weather",
        weather_types
    )

    # ---------------------------------------------
    # Population Density
    # ---------------------------------------------

    density_types = list(
        density_encoder.classes_
    )

    density = st.selectbox(
        "👥 Population Density",
        density_types
    )

    st.divider()

    # ---------------------------------------------
    # Model Performance
    # ---------------------------------------------

    st.subheader(
        "🧠 AI Model Performance"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📉 Mean Absolute Error",
            round(
                performance["mae"],
                3
            )
        )

    with col2:

        st.metric(
            "📈 R² Score",
            round(
                performance["r2"],
                3
            )
        )

    st.caption(
        "Performance calculated on the test portion "
        "of the synthetic project dataset."
    )

    st.divider()

    # ---------------------------------------------
    # Feature Importance
    # ---------------------------------------------

    st.subheader(
        "🧠 What Influences the Prediction?"
    )

    feature_names = [
        "Latitude",
        "Longitude",
        "Hour",
        "Day",
        "Month",
        "Crime Type",
        "Weather",
        "Population Density",
        "Area"
    ]

    importance_data = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance_data = (
        importance_data
        .sort_values(
            "Importance",
            ascending=False
        )
        .set_index("Feature")
    )

    st.bar_chart(
        importance_data
    )

    st.caption(
        "Feature importance shows how strongly each "
        "input contributes to the Random Forest model's "
        "predictions. It does not imply causation."
    )

    st.divider()   
    # ---------------------------------------------
    # Prediction Button
    # ---------------------------------------------

    predict_button = st.button(
        "🔮 PREDICT CRIME RISK",
        type="primary",
        width="stretch"
    )

    if predict_button:

        # Get area coordinates

        area_data = data[
            data["Area"] == area
        ]

        latitude = area_data[
            "Latitude"
        ].mean()

        longitude = area_data[
            "Longitude"
        ].mean()

        # Date information

        day_number = (
            selected_date.weekday() + 1
        )

        month_number = (
            selected_date.month
        )

        # Encode categorical values

        crime_code = (
            crime_encoder
            .transform([crime_type])[0]
        )

        weather_code = (
            weather_encoder
            .transform([weather])[0]
        )

        density_code = (
            density_encoder
            .transform([density])[0]
        )

        area_code = (
            area_encoder
            .transform([area])[0]
        )

        # Create model input

        input_data = pd.DataFrame(
            [[
                latitude,
                longitude,
                selected_hour,
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

        # Prediction

        prediction = model.predict(
            input_data
        )[0]

        prediction = max(
            0,
            prediction
        )

        # Risk level

        if prediction >= 12:

            risk = "🔴 CRITICAL"

        elif prediction >= 8:

            risk = "🟠 HIGH"

        elif prediction >= 4:

            risk = "🟡 MEDIUM"

        else:

            risk = "🟢 LOW"

        # -----------------------------------------
        # Display Result
        # -----------------------------------------

        st.divider()

        st.subheader(
            "🚔 POLICEAI Prediction Result"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🤖 Predicted Crime Count",
                round(prediction, 2)
            )

        with col2:

            st.metric(
                "⚠️ Risk Level",
                risk
            )

        st.divider()

        st.write(
            f"**📍 Area:** {area}"
        )

        st.write(
            f"**🚨 Crime Type:** {crime_type}"
        )

        st.write(
            f"**📅 Date:** "
            f"{selected_date}"
        )

        st.write(
            f"**🕐 Hour:** "
            f"{selected_hour}:00"
        )

        st.write(
            f"**🌦️ Weather:** {weather}"
        )

        st.write(
            f"**👥 Population Density:** "
            f"{density}"
        )

        st.info(
            "This prediction is experimental "
            "and is based on synthetic project data. "
            "It should not be used to make real-world "
            "law-enforcement decisions."
        )


# =========================================================
# COMPLAINT ANALYSIS
# =========================================================

elif page == "📝 Complaint Analysis":

    st.title("🚨 AI Complaint Analysis")

    st.write(
        "Enter a complaint and POLICEAI will "
        "classify the reported incident and "
        "assign a priority for human review."
    )

    st.divider()

    complaint = st.text_area(
        "📝 Enter Complaint",
        placeholder=(
            "Example: Someone stole my mobile phone "
            "near the bus stop."
        ),
        height=150
    )

    analyze_button = st.button(
        "🔍 ANALYZE COMPLAINT",
        type="primary",
        width="stretch"
    )

    if analyze_button:

        if not complaint.strip():

            st.error(
                "Please enter a complaint."
            )

        else:

            # =========================================
            # AI Complaint Classification
            # =========================================

            detected_crime, confidence, priority = (
                classify_complaint(complaint)
            )

            # =========================================
            # Display Result
            # =========================================

            st.divider()

            st.subheader(
                "🤖 POLICEAI Analysis Result"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🚨 Detected Crime",
                    detected_crime
                )

            with col2:

                st.metric(
                    "📊 Confidence",
                    f"{confidence}%"
                )

            with col3:

                st.metric(
                    "⚠️ Priority",
                    priority
                )

            st.divider()

            st.write(
                "**📝 Complaint:**"
            )

            st.info(
                complaint
            )

            # =========================================
            # Result Message
            # =========================================

            if detected_crime == "Unknown":

                st.warning(
                    "⚠️ The complaint could not be "
                    "confidently classified. "
                    "Please review it manually."
                )

            else:

                st.success(
                  "✅ Complaint classified successfully."
              )

                st.info(
                    "Human review is recommended before "
                  "any operational decision."
              )

            if detected_crime == "Unknown":

                st.warning(
                    "⚠️ The complaint could not be "
                    "confidently classified. "
                    "Please review it manually."
                )

            else:

                st.success(
                    "✅ Complaint classified successfully."
                )

                st.info(
                    "Human review is recommended before "
                    "any operational decision."
                )

                # =========================================
                # SAVE INCIDENT TO DATABASE
                # =========================================

                incident_id = add_incident(
                    complaint=complaint,
                    crime_type=detected_crime,
                    priority=priority,
                    location=""
                )

                st.success(
                    f"💾 Incident saved successfully! "
                    f"Incident ID: #{incident_id}"
                )               



# =========================================================
# INCIDENT MANAGEMENT
# =========================================================

elif page == "📋 Incident Management":

    st.title("📋 Incident Management")

    st.write(
        "View and manage complaints registered "
        "in the POLICEAI incident database."
    )

    st.divider()

    # Get incidents from database

    incidents = get_incidents()

    # =========================================
    # No incidents
    # =========================================

    if not incidents:

        st.info(
            "📭 No incidents have been registered yet."
        )

    else:

        # =====================================
        # Convert database records to DataFrame
        # =====================================

        incidents_df = pd.DataFrame(
            incidents,
            columns=[
                "ID",
                "Complaint",
                "Crime Type",
                "Priority",
                "Location",
                "Date",
                "Time",
                "Status"
            ]
        )

        # =====================================
        # Statistics
        # =====================================

        total_incidents = len(incidents_df)

        pending_count = len(
            incidents_df[
                incidents_df["Status"] == "Pending"
            ]
        )

        investigation_count = len(
            incidents_df[
                incidents_df["Status"]
                == "Under Investigation"
            ]
        )

        resolved_count = len(
            incidents_df[
                incidents_df["Status"] == "Resolved"
            ]
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🚨 Total Incidents",
                total_incidents
            )

        with col2:

            st.metric(
                "⏳ Pending",
                pending_count
            )

        with col3:

            st.metric(
                "🔎 Investigation",
                investigation_count
            )

        with col4:

            st.metric(
                "✅ Resolved",
                resolved_count
            )

        st.divider()

        # =====================================
        # Incident Table
        # =====================================

        st.subheader(
            "📋 Registered Incidents"
        )

        st.dataframe(
            incidents_df,
            width="stretch",
            hide_index=True
        )

        st.divider()

        # =====================================
        # Update Incident Status
        # =====================================

        st.subheader(
            "🔄 Update Incident Status"
        )

        incident_ids = incidents_df[
            "ID"
        ].tolist()

        selected_id = st.selectbox(
            "🆔 Select Incident",
            incident_ids
        )

        new_status = st.selectbox(
            "📌 Select New Status",
            [
                "Pending",
                "Under Investigation",
                "Resolved",
                "Closed"
            ]
        )

        if st.button(
            "🔄 UPDATE STATUS",
            type="primary"
        ):

            update_status(
                selected_id,
                new_status
            )

            st.success(
                f"✅ Incident #{selected_id} "
                f"updated to '{new_status}'."
            )

            st.rerun()


# =========================================================
# CRIME ANALYTICS
# =========================================================

elif page == "📊 Crime Analytics":

    st.title("📊 Crime Analytics")

    st.subheader("📈 Crime Statistics")

    # Crime type distribution
    crime_counts = df["Crime_Type"].value_counts()

    st.write("### 🚨 Crime Type Distribution")
    st.bar_chart(crime_counts)

    # Area-wise crime analysis
    area_counts = df["Area"].value_counts()

    st.write("### 📍 Area-wise Crime Distribution")
    st.bar_chart(area_counts)

    # Hour-wise crime analysis
    hour_counts = df["Hour"].value_counts().sort_index()

    st.write("### 🕒 Crime Distribution by Hour")
    st.line_chart(hour_counts)

    # Monthly crime analysis
    month_counts = df["Month"].value_counts().sort_index()

    st.write("### 📅 Monthly Crime Distribution")
    st.line_chart(month_counts)

    # Most common crime
    if len(crime_counts) > 0:

        most_common_crime = crime_counts.idxmax()
        highest_count = crime_counts.max()

        st.success(
            f"🚨 Most Common Crime: **{most_common_crime}** "
            f"({highest_count} records)"
        )

    # Highest crime area
    if len(area_counts) > 0:

        highest_area = area_counts.idxmax()
        highest_area_count = area_counts.max()

        st.warning(
            f"📍 Highest Crime Area: **{highest_area}** "
            f"({highest_area_count} records)"
        )

# =========================================================
# CRIME HOTSPOT MAP
# =========================================================

elif page == "🗺️ Crime Hotspot Map":

    st.title("🗺️ Crime Hotspot Map")

    st.write(
        "Interactive geographical visualization "
        "of crime activity across Bengaluru."
    )

    st.divider()

    # =========================================
    # FILTERS
    # =========================================

    col1, col2 = st.columns(2)

    with col1:

        crime_filter = st.selectbox(
            "🚨 Select Crime Type",
            ["All"] +
            sorted(
                data["Crime_Type"]
                .unique()
                .tolist()
            )
        )

    with col2:

        area_filter = st.selectbox(
            "📍 Select Area",
            ["All"] +
            sorted(
                data["Area"]
                .unique()
                .tolist()
            )
        )

    # =========================================
    # APPLY FILTERS
    # =========================================

    filtered_data = data.copy()

    if crime_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Crime_Type"]
            == crime_filter
        ]

    if area_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Area"]
            == area_filter
        ]

    # =========================================
    # FILTER RESULT
    # =========================================

    st.info(
        f"📊 Showing {len(filtered_data):,} "
        f"crime records"
    )

    if filtered_data.empty:

        st.warning(
            "⚠️ No crime records found "
            "for the selected filters."
        )

    else:

        # =====================================
        # CREATE MAP
        # =====================================

        crime_map = folium.Map(
            location=[
                12.9716,
                77.5946
            ],
            zoom_start=11,
            tiles="OpenStreetMap"
        )

        # =====================================
        # HEATMAP
        # =====================================

        heat_data = filtered_data[
            [
                "Latitude",
                "Longitude",
                "Crime_Count"
            ]
        ].values.tolist()

        HeatMap(
            heat_data,
            radius=20,
            blur=25,
            min_opacity=0.4,
            max_zoom=13
        ).add_to(
            crime_map
        )

        # =====================================
        # INCIDENT MARKERS
        # =====================================

        marker_data = filtered_data.sample(
            min(150, len(filtered_data)),
            random_state=42
        )

        for _, row in marker_data.iterrows():

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
                radius=5,
                popup=folium.Popup(
                    popup_text,
                    max_width=300
                ),
                tooltip=(
                    f"{row['Crime_Type']} - "
                    f"{row['Area']}"
                ),
                fill=True
            ).add_to(
                crime_map
            )

        # =====================================
        # MAP
        # =====================================

        st_folium(
            crime_map,
            width=None,
            height=650
        )

# =========================================================
# ABOUT
# =========================================================
elif page == "📹 CCTV AI Monitoring":

    st.title("📹 CCTV AI Monitoring")
    st.write("AI-powered real-time object detection using YOLO.")

    st.warning(
        "⚠️ This system detects objects such as people and vehicles. "
        "It does not identify people as criminals."
    )

    if st.button("▶️ Start CCTV Monitoring"):

        import subprocess
        import sys

        subprocess.run(
            [sys.executable, "cctv_detection.py"]
        )

elif page == "🚨 Emergency Alerts":

    st.title("🚨 Emergency Alert System")
    st.write("Register and prioritize emergency situations.")

    emergency_type = st.selectbox(
        "Emergency Type",
        [
            "Accident",
            "Fire",
            "Medical Emergency",
            "Suspicious Activity",
            "Missing Person"
        ]
    )

    location = st.text_input(
        "Location",
        placeholder="Enter emergency location"
    )

    description = st.text_area(
        "Description",
        placeholder="Describe the emergency..."
    )

    if st.button("🚨 Create Emergency Alert"):

        if location and description:

            emergency_priority = {
                "Accident": "HIGH",
                "Fire": "CRITICAL",
                "Medical Emergency": "CRITICAL",
                "Suspicious Activity": "MEDIUM",
                "Missing Person": "HIGH"
            }

            priority = emergency_priority[emergency_type]

            st.error(
                f"🚨 {priority} PRIORITY EMERGENCY"
            )

            st.write(f"**Type:** {emergency_type}")
            st.write(f"**Location:** {location}")
            st.write(f"**Description:** {description}")
            st.write(f"**Priority:** {priority}")
            alert_id = add_emergency_alert(
                emergency_type,
                location,
                description,
                priority
            )

            st.success(
                f"✅ Emergency Alert #{alert_id} saved successfully!"
            )

        else:
            st.warning(
                "Please enter both location and description."
            )

elif page == "🚨 Emergency Management":

    st.title("🚨 Emergency Alert Management")

    alerts = get_emergency_alerts()

    if not alerts:

        st.info("No emergency alerts found.")

    else:

        st.write(f"Total Emergency Alerts: **{len(alerts)}**")

        for alert in alerts:

            alert_id = alert[0]
            emergency_type = alert[1]
            location = alert[2]
            description = alert[3]
            priority = alert[4]
            status = alert[5]
            created_at = alert[6]

            with st.expander(
                f"🚨 Alert #{alert_id} | {emergency_type} | {priority}"
            ):

                st.write(f"**Location:** {location}")
                st.write(f"**Description:** {description}")
                st.write(f"**Priority:** {priority}")
                st.write(f"**Current Status:** {status}")
                st.write(f"**Created:** {created_at}")

                new_status = st.selectbox(
                    "Update Status",
                    [
                        "Active",
                        "Under Investigation",
                        "Resolved",
                        "Closed"
                    ],
                    index=[
                        "Active",
                        "Under Investigation",
                        "Resolved",
                        "Closed"
                    ].index(status),
                    key=f"status_{alert_id}"
                )

                if st.button(
                    "💾 Update Status",
                    key=f"update_{alert_id}"
                ):

                    update_emergency_status(
                        alert_id,
                        new_status
                    )

                    st.success(
                        f"Alert #{alert_id} updated to {new_status}"
                    )

                    st.rerun()


elif page == "ℹ️ About":

    st.title(
        "ℹ️ About POLICEAI"
    )

    st.subheader(
        "🚔 AI-Based Crime & Emergency "
        "Analysis System"
    )

    st.write(
        """
        POLICEAI is an experimental Python-based
        platform designed to demonstrate how
        Machine Learning, Computer Vision,
        Natural Language Processing and
        geospatial analytics can be combined
        in a crime-analysis workflow.
        """
    )

    st.divider()

    st.subheader(
        "🧠 Technologies"
    )

    technologies = [
        "Python",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Random Forest",
        "OpenCV",
        "YOLO",
        "Streamlit",
        "Folium",
        "SQLite"
    ]

    for technology in technologies:

        st.write(
            f"• {technology}"
        )

    st.divider()

    st.warning(
        "POLICEAI is an academic prototype. "
        "The crime dataset is synthetic and "
        "the predictions are experimental. "
        "The system must not be used for "
        "real-world policing or decisions "
        "about individuals."
    )

    st.subheader("⚠️ Project Disclaimer")

st.info(
    "POLICEAI is an academic prototype developed for demonstration "
    "and educational purposes. Crime data used in this project may be "
    "synthetic and should not be treated as official police statistics. "
    "AI predictions and CCTV detections require human verification."
    )

st.markdown("---")

st.caption(
    "🚔 POLICEAI | AI-Based Crime & Emergency Analysis System | "
    "Academic Prototype"
)