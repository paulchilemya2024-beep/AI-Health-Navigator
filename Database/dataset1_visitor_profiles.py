"""
Dataset 1: Visitor Profiles
AI Healthcare Navigation Assistant - Synthetic Data Generator
Generates 10,000 synthetic international visitor profiles.
"""

import csv
import random
import uuid

random.seed(42)

# ── Reference data ────────────────────────────────────────────────────────────

COUNTRIES_LANGUAGES = [
    ("Mexico", "Spanish"), ("Spain", "Spanish"), ("Colombia", "Spanish"),
    ("Argentina", "Spanish"), ("Brazil", "Portuguese"), ("Portugal", "Portuguese"),
    ("France", "French"), ("Belgium", "French"), ("Canada", "French"),
    ("China", "Chinese"), ("Japan", "Japanese"), ("South Korea", "Korean"),
    ("Saudi Arabia", "Arabic"), ("Egypt", "Arabic"), ("UAE", "Arabic"),
    ("Germany", "German"), ("Italy", "Italian"), ("India", "Hindi"),
    ("India", "English"), ("Philippines", "Filipino"), ("Nigeria", "English"),
    ("Australia", "English"), ("UK", "English"), ("Ireland", "English"),
    ("Russia", "Russian"), ("Poland", "Polish"), ("Netherlands", "Dutch"),
    ("Sweden", "Swedish"), ("Turkey", "Turkish"), ("Israel", "Hebrew"),
    ("Thailand", "Thai"), ("Vietnam", "Vietnamese"), ("Indonesia", "Indonesian"),
]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
AGE_WEIGHTS = [0.15, 0.28, 0.22, 0.17, 0.11, 0.07]

TRAVEL_TYPES = ["Tourism", "Business", "Student", "Medical Tourism",
                "Family Visit", "Conference", "Transit"]
TRAVEL_WEIGHTS = [0.38, 0.22, 0.12, 0.05, 0.13, 0.06, 0.04]

INSURANCE_OPTIONS = [
    "Travel Insurance (Comprehensive)", "Travel Insurance (Basic)",
    "Home Country Insurance Only", "No Insurance", "Employer Insurance",
    "Student Health Insurance",
]
INSURANCE_WEIGHTS = [0.20, 0.18, 0.25, 0.22, 0.10, 0.05]

CHRONIC_CONDITIONS = [
    "None", "None", "None", "None",  # weighted toward None
    "Hypertension", "Diabetes Type 2", "Asthma", "Arthritis",
    "Heart Disease", "Thyroid Disorder", "Epilepsy", "COPD",
    "Migraine", "Anxiety Disorder", "Depression", "None",
]

ALLERGIES = [
    "None", "None", "None",
    "Penicillin", "Sulfa Drugs", "Aspirin", "Ibuprofen",
    "Latex", "Shellfish", "Peanuts", "Tree Nuts",
    "Bee Stings", "Contrast Dye", "None",
]

ACCESSIBILITY_NEEDS = [
    "None", "None", "None", "None",
    "Wheelchair Accessible", "Sign Language Interpreter",
    "Visual Assistance", "Hearing Loop", "Mobility Aid",
    "Language Interpreter Needed",
]


def generate_visitor_profiles(n=10000):
    records = []
    for _ in range(n):
        country, language = random.choice(COUNTRIES_LANGUAGES)
        records.append({
            "visitor_id": str(uuid.uuid4()),
            "country_of_origin": country,
            "native_language": language,
            "age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS)[0],
            "travel_type": random.choices(TRAVEL_TYPES, weights=TRAVEL_WEIGHTS)[0],
            "travel_insurance": random.choices(INSURANCE_OPTIONS,
                                               weights=INSURANCE_WEIGHTS)[0],
            "chronic_conditions": random.choice(CHRONIC_CONDITIONS),
            "allergies": random.choice(ALLERGIES),
            "accessibility_needs": random.choice(ACCESSIBILITY_NEEDS),
        })
    return records


def write_csv(records, filename):
    if not records:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"✅  Wrote {len(records):,} records → {filename}")


if __name__ == "__main__":
    data = generate_visitor_profiles(10000)
    write_csv(data, "/mnt/user-data/outputs/visitor_profiles.csv")
