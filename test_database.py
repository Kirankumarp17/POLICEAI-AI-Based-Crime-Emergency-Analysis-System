from database import (
    add_incident,
    get_incidents
)


# Add test incident

incident_id = add_incident(
    complaint="Someone stole my mobile phone",
    crime_type="Theft",
    priority="Medium",
    location="Indiranagar"
)

print(
    "Incident created:",
    incident_id
)


# Get incidents

incidents = get_incidents()

print()
print("===== INCIDENTS =====")

for incident in incidents:

    print(incident)