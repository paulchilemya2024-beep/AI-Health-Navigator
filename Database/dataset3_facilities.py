"""
Dataset 3: Healthcare Facility Knowledge Base
AI Healthcare Navigation Assistant - Synthetic Data Generator
Generates 1,000 facility knowledge base records.
"""

import csv
import random
import uuid

random.seed(42)

# ── Facility templates ────────────────────────────────────────────────────────

FACILITY_TEMPLATES = {
    "Emergency Room (ER)": {
        "descriptions": [
            "A hospital-based department providing immediate medical care for life-threatening or severe medical emergencies, staffed 24/7 by emergency physicians and nurses.",
            "The emergency department (ED) of a hospital, designed to handle critical conditions, trauma, and severe illnesses that require immediate intervention and hospital-level resources.",
            "A fully equipped medical facility within a hospital that operates around the clock, equipped with advanced diagnostic tools including CT scanners, MRI, and surgical suites.",
        ],
        "use_cases": [
            "Chest pain or suspected heart attack; stroke symptoms; severe allergic reactions (anaphylaxis); major trauma or broken bones; uncontrolled bleeding; loss of consciousness",
            "Difficulty breathing; severe abdominal pain; high fever with stiff neck; seizures; overdose or poisoning; severe burns; eye injuries with vision loss",
            "Suspected appendicitis; psychiatric emergencies; severe infections; deep lacerations requiring surgery; head injuries with loss of consciousness",
        ],
        "cost_ranges": ["$1,500 – $3,000 (basic visit)", "$2,000 – $5,000 (with imaging)", "$3,000 – $10,000+ (complex cases)"],
        "wait_times": ["30 min – 4 hours (non-critical)", "Immediate (life-threatening)", "1 – 6 hours (moderate urgency)"],
        "appointment_required": ["No — walk-in or 911 arrival"],
        "insurance": ["Most major US insurance plans accepted; Medicare; Medicaid; international travel insurance (verify coverage before visit)"],
    },

    "Urgent Care Center": {
        "descriptions": [
            "A walk-in medical clinic providing care for non-life-threatening illnesses and injuries that require same-day attention but are not severe enough for an emergency room visit.",
            "A freestanding outpatient clinic offering extended hours and walk-in availability for acute medical conditions, minor injuries, and illnesses.",
            "A convenient alternative to the ER for moderate health concerns, offering services such as X-rays, lab tests, stitches, and prescription services at a fraction of the ER cost.",
        ],
        "use_cases": [
            "Minor fractures; sprains; cuts requiring stitches; ear infections; strep throat; UTIs; mild fevers; skin rashes; respiratory infections",
            "Flu symptoms; eye infections (pink eye); minor burns; animal bites; STI testing; sports injuries; nausea and vomiting; back pain",
            "Allergy symptoms; sinus infections; mild asthma flare-ups; minor lacerations; medication refills for short-term conditions",
        ],
        "cost_ranges": ["$100 – $200 (basic visit)", "$150 – $350 (with X-ray)", "$200 – $500 (with lab tests and procedures)"],
        "wait_times": ["15 – 45 minutes", "30 – 60 minutes (peak hours)", "Under 30 minutes (off-peak)"],
        "appointment_required": ["No — walk-in available; appointments preferred at some locations"],
        "insurance": ["Most major US insurance; many international travel insurance plans; self-pay options available"],
    },

    "Pharmacy": {
        "descriptions": [
            "A retail pharmacy providing prescription dispensing services, over-the-counter medications, health products, and pharmacist consultation services.",
            "A community pharmacy where licensed pharmacists dispense prescription medications and advise customers on OTC drug selection and drug interactions.",
            "A full-service pharmacy offering prescription services, vaccinations, health screenings, and a comprehensive selection of over-the-counter remedies.",
        ],
        "use_cases": [
            "Filling prescriptions from US physicians; purchasing OTC pain relievers, allergy medication, cold remedies; purchasing first aid supplies",
            "Receiving flu shots and other vaccinations; blood pressure screenings; purchasing diabetic supplies; contraception; vitamins and supplements",
            "Medication counseling; medication synchronization; refilling maintenance medications; purchasing medical devices (thermometers, glucometers)",
        ],
        "cost_ranges": ["$0 – $20 (OTC medications)", "$10 – $100 (generic prescriptions)", "$50 – $500+ (brand-name medications without insurance)"],
        "wait_times": ["Immediate (OTC purchases)", "15 – 30 minutes (prescription fill)", "Up to 1 hour (new prescriptions with insurance verification)"],
        "appointment_required": ["No — walk-in for OTC; no appointment for prescription drop-off"],
        "insurance": ["US health insurance; GoodRx discount card (no insurance needed); self-pay accepted at all pharmacies"],
    },

    "Telehealth Service": {
        "descriptions": [
            "A virtual healthcare platform connecting patients with licensed physicians, nurse practitioners, and mental health professionals via video, phone, or secure messaging.",
            "An online medical service providing remote consultations, diagnosis support for minor conditions, prescription services, and care coordination without requiring an in-person visit.",
            "A digital health platform offering 24/7 access to US-licensed healthcare providers for non-emergency medical consultations, mental health support, and prescription management.",
        ],
        "use_cases": [
            "Prescription renewals for chronic conditions; mental health counseling; minor illness evaluation; COVID-19 symptom assessment; medical advice",
            "Cold and flu symptom management; skin condition consultations (photo-based); sleep issues; anxiety and depression support; medication questions",
            "Travel health advice; triage guidance (should I go to the ER?); follow-up care after urgent care; second opinions; lab result interpretation",
        ],
        "cost_ranges": ["$40 – $75 (basic video visit)", "$50 – $100 (with prescription)", "$60 – $150 (specialist telehealth)"],
        "wait_times": ["On-demand: under 15 minutes", "Scheduled: same day or next day", "Mental health: within 24-48 hours"],
        "appointment_required": ["On-demand visits: no appointment needed; Scheduled visits: appointment preferred"],
        "insurance": ["Many US insurance plans cover telehealth; some international travel insurance plans cover virtual visits; self-pay available"],
    },

    "Community Health Clinic": {
        "descriptions": [
            "A federally qualified health center (FQHC) or nonprofit clinic providing affordable primary care, preventive services, and basic medical care on a sliding-fee scale regardless of insurance status.",
            "A community-based health center serving underinsured and uninsured patients, offering comprehensive primary care with fees adjusted based on income level.",
            "A nonprofit or government-funded health center that provides accessible healthcare to all community members, including international visitors, with reduced or no-cost services available.",
        ],
        "use_cases": [
            "General health check-ups; management of chronic conditions; vaccinations; family planning; dental care (at some locations); mental health services",
            "Basic lab tests; blood pressure monitoring; diabetes management; prenatal care; pediatric care; prescription assistance programs",
            "Health education; social services referrals; sliding-scale fee primary care; care for uninsured patients; language interpreter services",
        ],
        "cost_ranges": ["$0 – $30 (sliding scale for uninsured)", "$20 – $80 (low-income scale)", "$80 – $180 (full pay, still below private rates)"],
        "wait_times": ["Same-day (urgent slots)", "1 – 3 days (scheduled appointments)", "Walk-in availability varies by location"],
        "appointment_required": ["Recommended; walk-in availability varies; call ahead to confirm"],
        "insurance": ["Accepts uninsured patients; Medicaid; Medicare; some private insurance; sliding-fee scale for all income levels"],
    },
}


def generate_facility_kb(n=1000):
    records = []
    facility_types = list(FACILITY_TEMPLATES.keys())
    # Weight distribution across 1,000 records
    weights = [0.20, 0.30, 0.20, 0.18, 0.12]

    for _ in range(n):
        ftype = random.choices(facility_types, weights=weights)[0]
        tmpl = FACILITY_TEMPLATES[ftype]

        records.append({
            "facility_id": str(uuid.uuid4()),
            "facility_type": ftype,
            "facility_description": random.choice(tmpl["descriptions"]),
            "common_use_cases": random.choice(tmpl["use_cases"]),
            "average_cost_range": random.choice(tmpl["cost_ranges"]),
            "average_wait_time": random.choice(tmpl["wait_times"]),
            "appointment_required": random.choice(tmpl["appointment_required"]),
            "insurance_typically_accepted": random.choice(tmpl["insurance"]),
        })
    return records


def write_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"✅  Wrote {len(records):,} records → {filename}")


if __name__ == "__main__":
    data = generate_facility_kb(1000)
    write_csv(data, "/mnt/user-data/outputs/facility_knowledge_base.csv")
