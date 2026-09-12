# ==========================================
# 🚔 POLICEAI - Complaint Classifier
# ==========================================

import re


# ==========================================
# Crime Keywords
# ==========================================

complaints = {

    "Theft": [
        "mobile stolen",
        "phone stolen",
        "someone stole",
        "wallet stolen",
        "money stolen",
        "stolen phone",
        "stolen wallet",
        "stolen money",
        "theft"
    ],

    "Robbery": [
        "robbery",
        "robbed",
        "gun robbery",
        "threatened me",
        "threatened",
        "snatched",
        "gunpoint",
        "weapon"
    ],

    "Assault": [
        "fight",
        "attacked me",
        "attack",
        "someone hit me",
        "physical attack",
        "beaten",
        "assault"
    ],

  "Burglary": [
    "burglary",
    "break in",
    "break-in",
    "broken into",
    "broke into",
    "house broken",
    "house was broken into",
    "entered my house",
    "someone entered my house",
    "someone broke into my house",
    "house theft"
],

    "Vehicle Theft": [
        "bike stolen",
        "car stolen",
        "vehicle stolen",
        "motorcycle stolen",
        "scooter stolen"
    ],

    "Cyber Crime": [
        "hacked",
        "hacking",
        "cyber crime",
        "online scam",
        "account hacked",
        "instagram hacked",
        "otp fraud"
    ],

    "Fraud": [
        "fraud",
        "scam",
        "cheated",
        "fake payment",
        "money fraud",
        "financial fraud"
    ],

    "Missing Person": [
        "missing",
        "disappeared",
        "cannot find",
        "not returned",
        "missing person"
    ],

    "Accident": [
        "accident",
        "collision",
        "crash",
        "vehicle collision",
        "road accident"
    ],

    "Vandalism": [
        "damaged",
        "damage",
        "destroyed",
        "vandalism",
        "property damage"
    ],

    "Fire": [
        "fire",
        "building burning",
        "house burning",
        "burning",
        "smoke"
    ]
}


# ==========================================
# Priority Rules
# ==========================================

critical_crimes = [
    "Accident",
    "Assault",
    "Robbery",
    "Missing Person",
    "Fire"
]

high_crimes = [
    "Burglary",
    "Vehicle Theft",
    "Cyber Crime"
]

medium_crimes = [
    "Theft",
    "Fraud",
    "Vandalism"
]


# ==========================================
# Clean Text
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# Classify Complaint
# ==========================================

def classify_complaint(text):

    text = clean_text(text)

    scores = {}

    for crime_type, keywords in complaints.items():

        score = 0

        for keyword in keywords:

            keyword = clean_text(keyword)

            if keyword in text:
                score += 1

        if score > 0:
            scores[crime_type] = score


    # No match

    if not scores:

        return "Unknown", 0, "🟢 LOW"


    # Highest matching crime

    detected_crime = max(
        scores,
        key=scores.get
    )

    highest_score = scores[
        detected_crime
    ]


    # ======================================
    # Simple confidence calculation
    # ======================================

    confidence = min(
        60 + (highest_score * 15),
        95
    )


    # ======================================
    # Priority
    # ======================================

    if detected_crime in critical_crimes:

        priority = "🔴 CRITICAL"

    elif detected_crime in high_crimes:

        priority = "🟠 HIGH"

    elif detected_crime in medium_crimes:

        priority = "🟡 MEDIUM"

    else:

        priority = "🟢 LOW"


    return (
        detected_crime,
        confidence,
        priority
    )


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    complaint = input(
        "Enter your complaint: "
    )

    crime, confidence, priority = (
        classify_complaint(complaint)
    )

    print()
    print("=" * 50)
    print("🚔 POLICEAI ANALYSIS")
    print("=" * 50)

    print(
        "🚨 Crime:",
        crime
    )

    print(
        "📊 Confidence:",
        f"{confidence}%"
    )

    print(
        "⚠️ Priority:",
        priority
    )

    print("=" * 50)