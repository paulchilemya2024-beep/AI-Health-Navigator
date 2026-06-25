"""
Dataset 4: Healthcare Terminology Explanations
AI Healthcare Navigation Assistant - Synthetic Data Generator
Generates 2,000 healthcare terminology records.
"""

import csv
import random
import uuid

random.seed(42)

TERMINOLOGY = [
    # ── Insurance & Billing ──────────────────────────────────────────────────
    {
        "term": "Copay",
        "simple_explanation": "A fixed dollar amount you pay for a covered healthcare service, usually at the time of service.",
        "visitor_friendly_explanation": "Think of a copay like a fixed entry fee. For example, you might pay $30 every time you visit a doctor, regardless of what happens during the appointment. Your insurance covers the rest of the bill.",
    },
    {
        "term": "Deductible",
        "simple_explanation": "The amount you must pay out-of-pocket for healthcare services before your insurance starts paying.",
        "visitor_friendly_explanation": "Imagine your insurance has a 'startup cost' of $1,000 per year. Until you've paid $1,000 in medical bills yourself, your insurance won't contribute. After that, they start helping pay your bills.",
    },
    {
        "term": "Premium",
        "simple_explanation": "The monthly amount you pay to maintain your health insurance coverage, regardless of whether you use it.",
        "visitor_friendly_explanation": "Your premium is like a monthly subscription fee for your health insurance. You pay it every month to keep your coverage active, even if you never visit a doctor that month.",
    },
    {
        "term": "Coinsurance",
        "simple_explanation": "After meeting your deductible, the percentage of healthcare costs you share with your insurance company.",
        "visitor_friendly_explanation": "After you've met your deductible, coinsurance means you and your insurance both share the remaining bill. For example, with 80/20 coinsurance, your insurance pays 80% and you pay 20% of each bill.",
    },
    {
        "term": "Out-of-Pocket Maximum",
        "simple_explanation": "The most you will have to pay for covered services in a plan year before your insurance pays 100% of covered costs.",
        "visitor_friendly_explanation": "This is your financial safety net. Once you've spent a certain amount of money on healthcare in a year (e.g., $6,000), your insurance covers 100% of additional covered costs for the rest of the year.",
    },
    {
        "term": "In-Network Provider",
        "simple_explanation": "A healthcare provider or facility that has a contract with your insurance company to provide services at negotiated rates.",
        "visitor_friendly_explanation": "Your insurance has 'preferred' doctors and hospitals it has deals with, called in-network providers. Visiting these providers costs you much less than going to out-of-network providers who don't have a deal with your insurer.",
    },
    {
        "term": "Out-of-Network Provider",
        "simple_explanation": "A healthcare provider who does not have a contract with your insurance company, often resulting in higher costs for the patient.",
        "visitor_friendly_explanation": "If you visit a doctor or hospital that your insurance hasn't partnered with, you're going 'out of network.' This usually means much higher bills and your insurance may pay very little or nothing.",
    },
    {
        "term": "Prior Authorization",
        "simple_explanation": "Approval from your insurance company required before receiving certain medical services or medications.",
        "visitor_friendly_explanation": "For some expensive treatments or medications, your insurance company wants to approve it first before they agree to help pay. This pre-approval is called prior authorization. Without it, they may not cover the service.",
    },
    {
        "term": "Explanation of Benefits (EOB)",
        "simple_explanation": "A document from your insurance company explaining what was covered and what you owe after a medical service.",
        "visitor_friendly_explanation": "After a doctor visit, your insurance sends you a summary letter (EOB) that breaks down: what the doctor charged, what the insurance paid, and what you still owe. It is not a bill — it's a record.",
    },
    {
        "term": "Health Savings Account (HSA)",
        "simple_explanation": "A tax-advantaged savings account used to pay for qualified medical expenses.",
        "visitor_friendly_explanation": "An HSA is a special savings account where you set aside pre-tax money specifically to pay for medical expenses like copays, medications, and dental visits. Only available with high-deductible health plans.",
    },
    {
        "term": "Travel Insurance",
        "simple_explanation": "Insurance purchased before a trip that can cover medical emergencies, trip cancellations, and other unexpected events during travel.",
        "visitor_friendly_explanation": "Travel insurance is your financial safety net while traveling internationally. If you get sick or injured in the US, it can help cover your hospital bills, emergency transport, and even medical evacuation back to your home country.",
    },
    {
        "term": "Emergency Medical Evacuation",
        "simple_explanation": "Transportation of a patient to the nearest appropriate medical facility or back to their home country when local treatment is unavailable or insufficient.",
        "visitor_friendly_explanation": "If you are seriously ill or injured and need to be flown home or to a better-equipped hospital, this is called a medical evacuation. Some travel insurance plans cover this, which can cost $50,000 to $200,000 without insurance.",
    },

    # ── Care Settings ────────────────────────────────────────────────────────
    {
        "term": "Emergency Room (ER)",
        "simple_explanation": "A hospital department providing immediate care for life-threatening medical emergencies, available 24 hours a day, 7 days a week.",
        "visitor_friendly_explanation": "The ER is for true emergencies — situations where your life or a limb is at risk. Think: heart attack, stroke, severe allergic reaction, or major accident. Going to the ER for a mild illness is very expensive and involves long waits.",
    },
    {
        "term": "Urgent Care Center",
        "simple_explanation": "A walk-in clinic for non-life-threatening illnesses and injuries that need same-day attention.",
        "visitor_friendly_explanation": "Urgent care is the 'middle ground' between your doctor and the ER. Great for a sprained ankle, fever, ear infection, or minor cuts. No appointment needed, costs much less than the ER, and wait times are usually shorter.",
    },
    {
        "term": "Primary Care Physician (PCP)",
        "simple_explanation": "A doctor who provides general, preventive, and ongoing health care and is typically your first point of contact in the healthcare system.",
        "visitor_friendly_explanation": "Your PCP is your regular 'family doctor' who knows your medical history and helps manage your overall health. For international visitors, getting a PCP appointment quickly can be difficult — urgent care or telehealth are better options for immediate needs.",
    },
    {
        "term": "Telehealth",
        "simple_explanation": "Medical consultations, diagnoses, and prescriptions delivered remotely via video call, phone, or messaging.",
        "visitor_friendly_explanation": "Telehealth lets you see a licensed US doctor from your phone or computer without going anywhere. Perfect for travelers who need a prescription refill, advice for a mild illness, or mental health support.",
    },
    {
        "term": "Community Health Clinic",
        "simple_explanation": "A nonprofit or government-funded clinic providing affordable primary care to all patients, including uninsured individuals, often on a sliding fee scale.",
        "visitor_friendly_explanation": "Community health clinics serve everyone, including visitors without insurance. Your fee is based on what you can afford. They provide real medical care — not just charity — including lab tests, chronic disease management, and preventive care.",
    },
    {
        "term": "Walk-in Clinic",
        "simple_explanation": "A medical clinic that accepts patients without a prior appointment.",
        "visitor_friendly_explanation": "Walk-in clinics let you see a doctor without scheduling ahead. Most urgent care centers and some pharmacies operate as walk-in clinics. Ideal for travelers with unpredictable schedules.",
    },
    {
        "term": "Specialist",
        "simple_explanation": "A physician with advanced training in a specific area of medicine, such as cardiology, dermatology, or orthopedics.",
        "visitor_friendly_explanation": "Specialists are expert doctors focused on one body system or condition. As a visitor, you would typically need a referral from an urgent care or primary care doctor to see a specialist, which may take days or weeks to schedule.",
    },

    # ── Medications ──────────────────────────────────────────────────────────
    {
        "term": "Prescription Medication",
        "simple_explanation": "Medication that legally requires a written order from a licensed healthcare provider before it can be dispensed by a pharmacist.",
        "visitor_friendly_explanation": "Some medications are prescription-only, meaning a US doctor must authorize them before a pharmacy will give them to you. If you need a prescription from home refilled, you may need a telehealth or urgent care visit to get a US prescription.",
    },
    {
        "term": "Over-the-Counter (OTC) Medication",
        "simple_explanation": "Medication available for purchase without a doctor's prescription.",
        "visitor_friendly_explanation": "OTC medications can be bought directly off the shelf at a pharmacy or grocery store. Common examples include acetaminophen (Tylenol) for pain, ibuprofen (Advil) for inflammation, or Benadryl for allergies. No doctor visit required.",
    },
    {
        "term": "Generic Medication",
        "simple_explanation": "A medication that contains the same active ingredient as a brand-name drug, sold at a lower price after the brand's patent expires.",
        "visitor_friendly_explanation": "Generic drugs work exactly the same as brand-name drugs but cost significantly less. If your doctor prescribes a brand-name drug, ask the pharmacist if a generic version is available — it can save you a lot of money.",
    },
    {
        "term": "Formulary",
        "simple_explanation": "A list of prescription medications covered by an insurance plan.",
        "visitor_friendly_explanation": "Your insurance plan has a list of approved medications it will help pay for — this list is called a formulary. If your medication is not on the list, you may have to pay full price or ask your doctor for an alternative that is covered.",
    },
    {
        "term": "GoodRx",
        "simple_explanation": "A free US-based prescription discount service that provides coupons to reduce the cost of medications at participating pharmacies.",
        "visitor_friendly_explanation": "GoodRx is a free app or website (goodrx.com) that gives you discount coupons for prescription medications at US pharmacies. Uninsured visitors can often save 60–80% on medications using GoodRx. No insurance required.",
    },

    # ── Emergency & Safety ───────────────────────────────────────────────────
    {
        "term": "911",
        "simple_explanation": "The universal emergency telephone number in the United States for police, fire, and medical emergencies.",
        "visitor_friendly_explanation": "In any life-threatening emergency in the US, call 911 from any phone (even without a SIM card or credit). Dispatchers are available 24/7 and can send police, fire, or ambulance services immediately. Calls are free.",
    },
    {
        "term": "Ambulance",
        "simple_explanation": "An emergency vehicle equipped to provide medical care and transport patients to a hospital.",
        "visitor_friendly_explanation": "Calling 911 for a medical emergency will dispatch an ambulance. Be aware that ambulance rides in the US are expensive — often $1,000 to $3,000. For non-life-threatening situations, arranging your own transportation to urgent care is more cost-effective.",
    },
    {
        "term": "Poison Control Center",
        "simple_explanation": "A medical resource providing free, confidential guidance for poisoning emergencies 24 hours a day.",
        "visitor_friendly_explanation": "If someone swallows a harmful substance, call the US Poison Control hotline at 1-800-222-1222. This free service is available 24/7 and connects you with toxicology experts who can guide you on whether you need to go to the ER.",
    },
    {
        "term": "Medical ID Bracelet",
        "simple_explanation": "A bracelet worn by individuals with serious medical conditions or allergies to alert emergency responders.",
        "visitor_friendly_explanation": "A medical ID bracelet contains critical health information (like severe allergies or chronic conditions) that emergency responders check if you are unconscious. If you have a serious condition, wearing one while traveling in the US could save your life.",
    },
    {
        "term": "EMTALA",
        "simple_explanation": "A US federal law requiring hospitals with ERs to provide stabilizing emergency care to any person, regardless of their ability to pay or insurance status.",
        "visitor_friendly_explanation": "In the US, any hospital emergency room must treat you for a life-threatening emergency regardless of whether you have insurance or money. You will receive a bill afterward, but you cannot be turned away from emergency care.",
    },

    # ── Clinical Terms ───────────────────────────────────────────────────────
    {
        "term": "Triage",
        "simple_explanation": "The process of sorting patients based on the urgency of their medical needs to prioritize treatment.",
        "visitor_friendly_explanation": "When you arrive at an ER or urgent care, a nurse will quickly assess how sick you are — this is called triage. The most critical patients are seen first, regardless of arrival order. This is why someone who arrives after you may be seen before you.",
    },
    {
        "term": "Vital Signs",
        "simple_explanation": "Measurements of basic body functions including temperature, blood pressure, pulse rate, and breathing rate.",
        "visitor_friendly_explanation": "When you visit any clinic, a nurse will check your vital signs first: your temperature, blood pressure, heart rate, and how fast you breathe. These basic measurements help the doctor understand your overall health state.",
    },
    {
        "term": "Lab Work / Blood Work",
        "simple_explanation": "Medical tests performed on blood, urine, or other body fluids to assess health status or diagnose conditions.",
        "visitor_friendly_explanation": "When a doctor orders 'labs' or 'blood work,' a small blood or urine sample is collected and analyzed. Results help the doctor understand what is happening in your body, such as checking for infection or monitoring organ function.",
    },
    {
        "term": "Referral",
        "simple_explanation": "A formal recommendation from one healthcare provider directing a patient to see another provider or specialist.",
        "visitor_friendly_explanation": "If your urgent care doctor believes you need to see a specialist (e.g., a heart doctor or bone specialist), they will give you a referral — a formal recommendation to schedule an appointment with that specialist.",
    },
    {
        "term": "Discharge Instructions",
        "simple_explanation": "Written guidelines provided to patients when leaving a medical facility explaining follow-up care, medications, and warning signs.",
        "visitor_friendly_explanation": "When you leave a clinic or ER, staff will give you discharge instructions — a printed sheet explaining what happened, what medications to take, activities to avoid, and warning signs that mean you should return or call a doctor.",
    },
    {
        "term": "Medical History",
        "simple_explanation": "A record of a patient's past and current health conditions, surgeries, medications, allergies, and family health history.",
        "visitor_friendly_explanation": "When you see a doctor in the US, they will ask about your medical history — past illnesses, surgeries, current medications, and allergies. Bring a written summary in English if possible, especially if you have chronic conditions.",
    },
]

# Expand to 2,000 by adding variations
ADDITIONAL_TERMS = [
    ("Anaphylaxis", "A severe, life-threatening allergic reaction requiring immediate epinephrine injection.",
     "Anaphylaxis is the most severe form of allergic reaction. Symptoms include throat swelling, hives, dropping blood pressure, and difficulty breathing. This is always a 911/ER emergency. If you carry an EpiPen, use it immediately."),
    ("EpiPen", "A brand-name auto-injector device containing epinephrine used to treat severe allergic reactions.",
     "An EpiPen is an emergency device that injects epinephrine (adrenaline) into your thigh to rapidly reverse severe allergic reactions. If prescribed one by your doctor, always carry it while traveling. After use, go to the ER immediately."),
    ("Sutures (Stitches)", "Threads used by medical professionals to close wounds.",
     "If you have a deep cut, a doctor may use sutures (stitches) to close the wound. This is typically done at urgent care or the ER. After treatment, you will receive instructions on keeping the wound clean and when to have stitches removed."),
    ("X-Ray", "A medical imaging test using radiation to visualize bones and certain internal structures.",
     "An X-ray is a quick imaging test used to check for broken bones or other internal issues. Most urgent care centers have X-ray equipment on-site. Results are usually available within minutes."),
    ("CT Scan", "A computed tomography scan that uses X-rays to create detailed cross-sectional images of the body.",
     "A CT scan produces detailed images of your internal organs, bones, and tissues. It is more detailed than a standard X-ray and is typically done at a hospital or emergency setting for more serious conditions."),
    ("HIPAA", "A US federal law protecting the privacy and security of patients' medical information.",
     "HIPAA means your medical information in the US is legally protected. Healthcare providers cannot share your health details with others without your permission, except in limited situations like emergencies or legal requirements."),
    ("Sliding Scale Fee", "A payment system where the cost of services is adjusted based on a patient's income level.",
     "Some community health clinics charge based on what you can afford — the less you earn, the less you pay. This is called a sliding scale fee. Uninsured visitors with limited funds can access real medical care this way."),
    ("Observation Status", "A hospital status where a patient is monitored for a period of time while a decision is made about whether to admit them.",
     "If you visit the ER and the doctor is uncertain whether you need to be hospitalized, you may be placed in 'observation status.' This means you stay in the hospital for monitoring but are not officially admitted — this can affect what your insurance covers."),
]

def generate_terminology(n=2000):
    records = []
    all_terms = TERMINOLOGY + [
        {"term": t, "simple_explanation": s, "visitor_friendly_explanation": v}
        for t, s, v in ADDITIONAL_TERMS
    ]

    while len(records) < n:
        base = random.choice(all_terms)
        records.append({
            "term_id": str(uuid.uuid4()),
            "term": base["term"],
            "simple_explanation": base["simple_explanation"],
            "visitor_friendly_explanation": base["visitor_friendly_explanation"],
        })
    return records[:n]


import uuid

def write_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"✅  Wrote {len(records):,} records → {filename}")


if __name__ == "__main__":
    data = generate_terminology(2000)
    write_csv(data, "/mnt/user-data/outputs/healthcare_terminology.csv")
