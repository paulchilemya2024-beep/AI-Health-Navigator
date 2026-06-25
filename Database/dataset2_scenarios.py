"""
Dataset 2: Healthcare Access Scenarios
AI Healthcare Navigation Assistant - Synthetic Data Generator
Generates 5,000 realistic healthcare navigation scenarios.
"""

import csv
import random
import uuid

random.seed(42)

# ── Scenario templates ────────────────────────────────────────────────────────
# Each tuple: (description_template, care_option, explanation, urgency)

SCENARIO_TEMPLATES = [
    # --- Urgent Care level ---
    ("Visitor has a minor ankle sprain after sightseeing and is experiencing mild swelling and pain.",
     "Urgent Care Center",
     "An urgent care center can assess musculoskeletal injuries like sprains, provide X-rays if needed, and offer wrap/brace support without the long ER wait times or high costs.",
     "Moderate"),

    ("Traveler has had a fever of 101°F for 24 hours with mild body aches and no rash.",
     "Urgent Care Center",
     "Urgent care is appropriate for fevers that are persistent but not dangerously high, allowing evaluation and treatment without ER-level expense.",
     "Moderate"),

    ("Visitor developed a mild rash after eating at a restaurant and is unsure of the cause.",
     "Urgent Care Center",
     "Urgent care can evaluate mild allergic reactions and skin rashes, prescribe antihistamines, and rule out more serious conditions.",
     "Moderate"),

    ("Traveler has a sore throat and difficulty swallowing for two days with no breathing problems.",
     "Urgent Care Center",
     "Urgent care can test for strep throat and prescribe antibiotics if needed, providing faster service than scheduling a primary care visit.",
     "Low-Moderate"),

    ("Visitor has a suspected urinary tract infection with burning sensation and frequent urination.",
     "Urgent Care Center",
     "Urgent care centers can diagnose UTIs with a urine test and prescribe appropriate antibiotics quickly.",
     "Moderate"),

    ("Traveler sustained a small cut on the hand while cooking that may need stitches.",
     "Urgent Care Center",
     "Urgent care can clean wounds and apply sutures or skin glue for lacerations that do not involve tendons or deep tissue.",
     "Moderate"),

    ("Visitor has been vomiting for several hours after eating street food and feels dehydrated.",
     "Urgent Care Center",
     "Food poisoning with mild-to-moderate dehydration can be treated at urgent care with IV fluids if needed. Go to the ER if symptoms worsen severely.",
     "Moderate"),

    ("Traveler has a mild ear infection with pain and muffled hearing but no high fever.",
     "Urgent Care Center",
     "Urgent care can diagnose ear infections and prescribe antibiotic drops or oral antibiotics.",
     "Low-Moderate"),

    ("Visitor slipped on wet floor and has wrist pain with minor swelling, no open wound.",
     "Urgent Care Center",
     "Urgent care can X-ray the wrist to rule out fractures and provide splinting or referral if needed.",
     "Moderate"),

    ("Traveler has a persistent cough lasting 5 days with no shortness of breath or chest pain.",
     "Urgent Care Center",
     "Urgent care can evaluate upper respiratory infections, prescribe cough suppressants, and rule out pneumonia with a chest X-ray.",
     "Low-Moderate"),

    # --- Emergency Room ---
    ("Visitor is experiencing severe chest pain radiating to the left arm with shortness of breath.",
     "Emergency Room (ER)",
     "Chest pain with radiation to the arm may indicate a cardiac emergency. Call 911 or go to the ER immediately. This is a life-threatening situation requiring immediate evaluation.",
     "Critical"),

    ("Traveler has had a sudden onset of severe headache described as 'the worst headache of their life.'",
     "Emergency Room (ER)",
     "A sudden severe headache can indicate a subarachnoid hemorrhage or other serious neurological event. Go to the ER immediately.",
     "Critical"),

    ("Visitor fell and hit their head, briefly losing consciousness and now feeling confused.",
     "Emergency Room (ER)",
     "Loss of consciousness and confusion after a head injury indicates possible concussion or traumatic brain injury requiring immediate ER evaluation.",
     "Critical"),

    ("Traveler is having a severe allergic reaction with throat swelling and difficulty breathing after eating.",
     "Emergency Room (ER)",
     "Anaphylaxis is life-threatening. Call 911 immediately. If an EpiPen is available, use it. Do not wait — go to the ER right away.",
     "Critical"),

    ("Visitor has a deep laceration that is bleeding heavily and not stopping with direct pressure.",
     "Emergency Room (ER)",
     "Uncontrolled bleeding from a deep wound is a medical emergency. Go to the ER or call 911 for immediate wound care and possible surgery.",
     "Critical"),

    ("Traveler is experiencing signs of stroke: face drooping, arm weakness, slurred speech.",
     "Emergency Room (ER)",
     "FAST symptoms (Face drooping, Arm weakness, Speech difficulty, Time to call 911) indicate a stroke. Every minute counts — call 911 immediately.",
     "Critical"),

    ("Visitor has a broken bone with visible deformity after a fall, and extreme pain.",
     "Emergency Room (ER)",
     "Suspected fractures with deformity require ER evaluation for imaging, realignment, and possible casting or surgical intervention.",
     "High"),

    ("Traveler is experiencing a seizure for the first time with no prior history of epilepsy.",
     "Emergency Room (ER)",
     "A first-time seizure requires immediate ER evaluation to identify the underlying cause.",
     "Critical"),

    ("Visitor has a high fever of 104°F with stiff neck and sensitivity to light.",
     "Emergency Room (ER)",
     "High fever with neck stiffness and photophobia are classic signs of meningitis, a life-threatening condition. Go to the ER immediately.",
     "Critical"),

    ("Traveler ingested an unknown substance accidentally and is feeling dizzy and nauseous.",
     "Emergency Room (ER)",
     "Suspected poisoning requires immediate ER evaluation. Also contact Poison Control at 1-800-222-1222.",
     "Critical"),

    # --- Pharmacy ---
    ("Visitor needs to purchase over-the-counter pain relief medication for a mild headache.",
     "Pharmacy",
     "Pharmacies carry a wide range of OTC medications including acetaminophen (Tylenol) and ibuprofen (Advil) for headache relief. No prescription needed.",
     "Low"),

    ("Traveler ran out of daily allergy medication and needs a refill or OTC equivalent.",
     "Pharmacy",
     "Many allergy medications like cetirizine (Zyrtec) and loratadine (Claritin) are available OTC at pharmacies. Ask the pharmacist for guidance.",
     "Low"),

    ("Visitor needs antidiarrheal medication after stomach upset from travel.",
     "Pharmacy",
     "OTC medications like loperamide (Imodium) for diarrhea are available at any pharmacy without a prescription.",
     "Low"),

    ("Traveler needs cold and flu medicine, throat lozenges, and a thermometer.",
     "Pharmacy",
     "Pharmacies stock a full range of OTC cold remedies, sore throat products, and medical devices like thermometers.",
     "Low"),

    ("Visitor wants motion sickness medication before a cruise or long road trip.",
     "Pharmacy",
     "OTC options like dimenhydrinate (Dramamine) or meclizine are available at pharmacies for motion sickness prevention.",
     "Low"),

    ("Traveler needs to purchase bandages, antiseptic cream, and wound dressing supplies.",
     "Pharmacy",
     "Pharmacies carry complete first-aid supplies. A pharmacist can also advise on proper wound care for minor injuries.",
     "Low"),

    ("Visitor needs a prescription transferred from their home country and filled locally.",
     "Pharmacy",
     "Pharmacists can advise on whether foreign prescriptions can be accepted (policies vary by state). A telehealth or urgent care visit may be needed to get a US prescription.",
     "Low-Moderate"),

    # --- Telehealth ---
    ("Traveler needs a prescription renewal for a chronic condition medication they take regularly.",
     "Telehealth Service",
     "Telehealth providers can evaluate ongoing chronic conditions and issue prescription renewals in most states. This is the most convenient option for travelers.",
     "Low-Moderate"),

    ("Visitor wants medical advice about a mild skin rash that appeared during travel.",
     "Telehealth Service",
     "Telehealth dermatology services allow photo-based consultations for skin conditions. A provider can assess and prescribe treatment if needed.",
     "Low"),

    ("Traveler feels anxious and stressed during their trip and wants to speak with a mental health professional.",
     "Telehealth Service",
     "Telehealth platforms offer same-day or next-day mental health counseling via video call. No physical visit required.",
     "Low-Moderate"),

    ("Visitor has mild COVID symptoms and wants a virtual consultation before seeking in-person care.",
     "Telehealth Service",
     "Telehealth providers can assess COVID symptoms, recommend testing, and advise on next steps without requiring an in-person visit.",
     "Moderate"),

    ("Traveler needs medical documentation or a sick note for travel insurance purposes.",
     "Telehealth Service",
     "Telehealth physicians can provide medical documentation, letters, and notes during a virtual consultation.",
     "Low"),

    ("Visitor wants guidance on whether their symptoms warrant an ER visit or can be managed at home.",
     "Telehealth Service",
     "Telehealth triage services help visitors determine the appropriate level of care needed, potentially saving an unnecessary ER visit.",
     "Low-Moderate"),

    # --- Community Clinic ---
    ("Uninsured visitor needs a basic health check and blood pressure evaluation.",
     "Community Health Clinic",
     "Community clinics offer sliding-scale fee services for uninsured patients. They provide basic primary care regardless of insurance status.",
     "Low"),

    ("Traveler without insurance needs to see a doctor for a non-emergency concern and cannot afford ER prices.",
     "Community Health Clinic",
     "Federally Qualified Health Centers (FQHCs) provide care on a sliding fee scale based on income, making them accessible for uninsured visitors.",
     "Low"),

    ("Visitor needs routine vaccinations or travel immunizations not received before departure.",
     "Community Health Clinic",
     "Many community health clinics offer vaccination services, including travel vaccines, often at reduced cost compared to private clinics.",
     "Low"),

    ("Traveler needs blood work or basic lab tests but does not have health insurance.",
     "Community Health Clinic",
     "Community health centers can order and interpret basic lab tests on a sliding fee scale for uninsured patients.",
     "Low"),
]

VISITOR_CONTEXTS = [
    "on a 2-week vacation", "attending a business conference", "visiting family",
    "on a student exchange program", "on a cruise stopover", "during a road trip",
    "at a hotel", "at an Airbnb rental", "sightseeing in the city",
    "at an amusement park", "at a national park", "at a shopping mall",
    "after a long-haul flight", "during a layover", "at a beach resort",
]

VISITOR_DEMOGRAPHICS = [
    "A 28-year-old traveler from Brazil", "A 45-year-old visitor from Japan",
    "A 62-year-old tourist from Germany", "A 19-year-old student from Mexico",
    "A 35-year-old business traveler from France", "A 55-year-old visitor from China",
    "A 72-year-old retiree from Canada", "A 30-year-old tourist from Australia",
    "A 40-year-old visitor from Saudi Arabia", "A 25-year-old traveler from India",
    "A 50-year-old visitor from the UK", "A 33-year-old tourist from Spain",
    "A 68-year-old visitor from Italy", "A 22-year-old student from South Korea",
    "A 47-year-old traveler from Portugal",
]

URGENCY_LEVELS = ["Low", "Low-Moderate", "Moderate", "High", "Critical"]


def generate_scenarios(n=5000):
    records = []
    for i in range(n):
        template = random.choice(SCENARIO_TEMPLATES)
        desc_base, care_option, explanation, urgency = template
        demographic = random.choice(VISITOR_DEMOGRAPHICS)
        context = random.choice(VISITOR_CONTEXTS)

        # Enrich description with demographic + context
        full_description = f"{demographic} {context}. {desc_base}"

        records.append({
            "scenario_id": str(uuid.uuid4()),
            "scenario_description": full_description,
            "recommended_care_option": care_option,
            "explanation": explanation,
            "urgency_level": urgency,
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
    data = generate_scenarios(5000)
    write_csv(data, "/mnt/user-data/outputs/healthcare_scenarios.csv")
