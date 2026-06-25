"""
AI Healthcare Navigation Assistant
Master Data Generation Script
Generates all 5 synthetic datasets and writes CSVs to /mnt/user-data/outputs/
"""

import sys
import os

# Ensure the scripts directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from dataset1_visitor_profiles import generate_visitor_profiles, write_csv as write1
from dataset2_scenarios        import generate_scenarios,        write_csv as write2
from dataset3_facilities       import generate_facility_kb,      write_csv as write3
from dataset4_terminology      import generate_terminology,       write_csv as write4
from dataset5_multilingual     import generate_multilingual_phrases, write_csv as write5

OUTPUT_DIR = "/mnt/user-data/outputs"

def main():
    print("\n" + "="*60)
    print("  AI Healthcare Navigation Assistant")
    print("  Synthetic Dataset Generation")
    print("="*60 + "\n")

    print("📋  Dataset 1: Visitor Profiles (10,000 records)")
    d1 = generate_visitor_profiles(10000)
    write1(d1, f"{OUTPUT_DIR}/visitor_profiles.csv")

    print("\n📋  Dataset 2: Healthcare Access Scenarios (5,000 records)")
    d2 = generate_scenarios(5000)
    write2(d2, f"{OUTPUT_DIR}/healthcare_scenarios.csv")

    print("\n📋  Dataset 3: Facility Knowledge Base (1,000 records)")
    d3 = generate_facility_kb(1000)
    write3(d3, f"{OUTPUT_DIR}/facility_knowledge_base.csv")

    print("\n📋  Dataset 4: Healthcare Terminology (2,000 records)")
    d4 = generate_terminology(2000)
    write4(d4, f"{OUTPUT_DIR}/healthcare_terminology.csv")

    print("\n📋  Dataset 5: Multilingual Phrases (5,000 records)")
    d5 = generate_multilingual_phrases(5000)
    write5(d5, f"{OUTPUT_DIR}/multilingual_phrases.csv")

    print("\n" + "="*60)
    print("  ✅  All datasets generated successfully!")
    print(f"  📁  Output directory: {OUTPUT_DIR}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
