# AI Healthcare Navigation Assistant
## Dataset Architecture Guide
### Storage Recommendations, RAG Design & Agent Interaction Patterns

---

## 1. Storage Architecture: PostgreSQL vs. Vector Database

### Decision Framework

| Dataset | Primary Store | Secondary Store | Rationale |
|---|---|---|---|
| Visitor Profiles | **PostgreSQL** | None | Structured, relational, exact-match queries (filter by language, insurance type, country). No semantic search needed. |
| Healthcare Scenarios | **Vector DB** | PostgreSQL (metadata) | Core RAG dataset. User symptom descriptions must be semantically matched to the closest scenario. |
| Facility Knowledge Base | **Vector DB** | PostgreSQL (metadata) | Free-text facility descriptions need semantic retrieval ("what's the cheapest option for a minor cut?"). |
| Healthcare Terminology | **Vector DB** | None | Users ask in natural language ("what is that copay thing?"). Semantic similarity is essential. |
| Multilingual Phrases | **PostgreSQL** | Optionally Vector DB | Exact language + category lookup is primary use case. Vector DB optional for fuzzy phrase matching. |

---

### 1.1 PostgreSQL — Recommended For

**Datasets 1 (Visitor Profiles) and 5 (Multilingual Phrases)**

**Why PostgreSQL:**
- Visitor profiles require structured filtering (e.g., `WHERE native_language = 'Arabic' AND travel_insurance = 'No Insurance'`).
- Multilingual phrases require exact language/category lookups (`WHERE language = 'Spanish' AND category = 'Emergency'`).
- Both datasets have well-defined schemas with enumerable field values.
- No semantic interpretation needed — the AI agent uses these as lookup tables.

**Recommended PostgreSQL Setup:**
```
PostgreSQL 15+ with the following extensions:
  - pgcrypto (UUID generation)
  - pg_trgm (fuzzy text search on terminology table if not using vector DB)
  - Full-text search (tsvector) as a fallback for terminology
```

---

### 1.2 Vector Database — Recommended For

**Datasets 2 (Scenarios), 3 (Facilities), and 4 (Terminology)**

**Why a Vector Database:**
- User inputs are unstructured natural language: "I twisted my ankle and it's swollen, what do I do?"
- Semantic similarity search maps user descriptions to the closest matching scenario.
- Embedding-based retrieval significantly outperforms keyword search for healthcare navigation.
- Enables RAG (Retrieval-Augmented Generation) pipeline.

**Recommended Vector DB Options:**

| Option | Best For | Notes |
|---|---|---|
| **Pinecone** | Managed, production-ready | Easiest to deploy; good for startup projects |
| **Weaviate** | Open-source + hybrid search | Supports both vector and keyword search in one query |
| **pgvector** (PostgreSQL extension) | Unified stack | Keep everything in PostgreSQL; good for smaller scale |
| **Qdrant** | High-performance open-source | Excellent filtering + vector search combination |
| **ChromaDB** | Prototyping | Best for local development and testing |

**Recommended Embedding Model:**
```
text-embedding-3-small (OpenAI)  — 1536 dimensions, cost-effective
OR
all-MiniLM-L6-v2 (open-source)  — 384 dimensions, runs locally
```

---

## 2. How Each Dataset is Used During Agent Interaction

### Interaction Flow Overview

```
User Message
     │
     ▼
┌─────────────────────────────────────┐
│   Language Detection                │
│   → Dataset 5 (PostgreSQL lookup)  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Visitor Profile Personalization   │
│   → Dataset 1 (PostgreSQL filter)  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Scenario Matching (RAG)           │
│   → Dataset 2 (Vector DB search)   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Facility Explanation (RAG)        │
│   → Dataset 3 (Vector DB search)   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Terminology Clarification (RAG)   │
│   → Dataset 4 (Vector DB search)   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Multilingual Response Phrases     │
│   → Dataset 5 (PostgreSQL lookup)  │
└─────────────────────────────────────┘
     │
     ▼
AI-Generated Navigation Response (Non-diagnostic)
```

---

### 2.1 Dataset 1 — Visitor Profiles

**When Used:** Session initialization / personalization layer.

**Agent Behavior:**
1. User begins interaction; agent collects minimal context (country of origin, insurance status, language).
2. Agent queries PostgreSQL to load or create a visitor profile.
3. Profile personalizes all subsequent responses:
   - **Language** → determines response language and phrase lookup.
   - **Insurance status** → filters cost information ("You mentioned you have no insurance — community clinics offer sliding-scale fees").
   - **Chronic conditions** → flags relevant medication considerations ("Since you have diabetes, ensure you have sufficient insulin supply").
   - **Accessibility needs** → agent notes accessibility requirements when recommending facilities.

**Example Query:**
```sql
SELECT native_language, travel_insurance, chronic_conditions, allergies, accessibility_needs
FROM visitor_profiles
WHERE visitor_id = $1;
```

---

### 2.2 Dataset 2 — Healthcare Access Scenarios

**When Used:** Core triage step — mapping user-described symptoms to recommended care.

**Agent Behavior:**
1. User describes their situation: "I have a bad headache and I've been vomiting for 3 hours."
2. Agent embeds the user message using the embedding model.
3. Vector DB performs semantic similarity search across 5,000 scenario descriptions.
4. Top 3–5 matching scenarios are retrieved with their recommended care options and explanations.
5. Agent uses the retrieved scenarios as RAG context to generate its navigation response.
6. The `urgency_level` field triggers safety guardrails:
   - **Critical** → agent immediately responds with 911/ER instruction before anything else.
   - **High** → agent emphasizes time sensitivity.
   - **Low** → agent calmly explains pharmacy or telehealth options.

**Example RAG Prompt Injection:**
```
Retrieved scenarios suggest: Recommended care = "Emergency Room (ER)"
Urgency level: Critical
Explanation: "High fever with neck stiffness and photophobia are classic signs of
meningitis, a life-threatening condition."

Instruction to LLM: Do not diagnose. Navigate the user to the ER immediately.
```

---

### 2.3 Dataset 3 — Facility Knowledge Base

**When Used:** After care option is determined — explaining what that facility is and what to expect.

**Agent Behavior:**
1. Once the agent determines the recommended care option (e.g., "Urgent Care Center"), it queries the facility knowledge base.
2. Vector DB retrieves relevant facility descriptions matching the user's concern.
3. Agent explains: cost range, wait times, whether appointment is needed, insurance acceptance.
4. PostgreSQL metadata filtering allows the agent to filter by facility type.

**Example Use Case:**
> User: "What is urgent care and how much will it cost me?"
>
> Agent retrieves: `facility_type = "Urgent Care Center"` → pulls description, cost range ($100–$350), wait time (15–45 min), no appointment needed → explains in plain language.

**Example Hybrid Query (pgvector or Weaviate):**
```python
results = vector_db.query(
    query_embedding=embed("what is an urgent care center"),
    filter={"facility_type": "Urgent Care Center"},
    top_k=3
)
```

---

### 2.4 Dataset 4 — Healthcare Terminology

**When Used:** On-demand education when user is confused by a term.

**Agent Behavior:**
1. User asks: "What is a deductible?" or "I don't understand what copay means."
2. Agent embeds the question and queries the terminology vector store.
3. Retrieves the matching term with both `simple_explanation` and `visitor_friendly_explanation`.
4. Agent delivers the `visitor_friendly_explanation` — written in accessible, non-clinical language.
5. Proactively triggered when agent response contains a term the user may not know (e.g., agent says "triage" → auto-appends a brief explanation).

**Example RAG Context:**
```
Term: "Copay"
Visitor-friendly explanation: "Think of a copay like a fixed entry fee. For example,
you might pay $30 every time you visit a doctor, regardless of what happens during
the appointment. Your insurance covers the rest of the bill."
```

---

### 2.5 Dataset 5 — Multilingual Healthcare Communication

**When Used:** Language detection, multilingual response generation, phrase lookup.

**Agent Behavior:**
1. **Language detection:** Agent identifies user's language from their message.
2. **Phrase lookup:** Agent retrieves pre-translated healthcare phrases for that language from PostgreSQL.
3. **Critical phrase delivery:** For emergency situations, agent immediately provides key phrases in the user's native language (e.g., "Here is how to say 'I need emergency help' in Japanese: 緊急の助けが必要です。").
4. **Category filtering:** Agent retrieves Emergency, Symptom, or Navigation phrases based on context.

**Example Query:**
```sql
SELECT phrase, english_translation, category
FROM multilingual_phrases
WHERE language = 'Arabic'
  AND category IN ('Emergency', 'Navigation')
ORDER BY category;
```

---

## 3. RAG Pipeline Architecture

```python
# Simplified RAG pipeline pseudocode

def handle_user_message(user_message: str, visitor_id: str) -> str:

    # Step 1: Load visitor profile (PostgreSQL)
    profile = postgres.query(
        "SELECT * FROM visitor_profiles WHERE visitor_id = %s", visitor_id
    )

    # Step 2: Embed user message
    query_embedding = embed_model.encode(user_message)

    # Step 3: Semantic scenario retrieval (Vector DB)
    scenarios = vector_db.query(
        collection="healthcare_scenarios",
        embedding=query_embedding,
        top_k=5,
        filter={}  # optionally filter by urgency_level
    )

    # Step 4: Check urgency — safety guardrail
    top_urgency = max(s["urgency_level"] for s in scenarios)
    if top_urgency == "Critical":
        return emergency_response(profile["native_language"])

    # Step 5: Retrieve facility explanation (Vector DB)
    care_option = scenarios[0]["recommended_care_option"]
    facilities = vector_db.query(
        collection="facility_knowledge_base",
        embedding=query_embedding,
        top_k=3,
        filter={"facility_type": care_option}
    )

    # Step 6: Retrieve terminology if needed (Vector DB)
    terminology = vector_db.query(
        collection="healthcare_terminology",
        embedding=query_embedding,
        top_k=2
    )

    # Step 7: Retrieve multilingual phrases (PostgreSQL)
    phrases = postgres.query(
        "SELECT phrase, english_translation FROM multilingual_phrases "
        "WHERE language = %s AND category = %s",
        profile["native_language"], "Navigation"
    )

    # Step 8: Compose RAG prompt and call LLM
    rag_context = build_context(scenarios, facilities, terminology, phrases, profile)
    response = llm.complete(
        system_prompt=NAVIGATION_SYSTEM_PROMPT,
        context=rag_context,
        user_message=user_message
    )

    return response
```

---

## 4. CSV Schema Summary

### Dataset 1: visitor_profiles.csv
| Column | Type | Example |
|---|---|---|
| visitor_id | UUID | `3f2a1b4c-...` |
| country_of_origin | String | `Brazil` |
| native_language | String | `Portuguese` |
| age_group | String | `35-44` |
| travel_type | String | `Tourism` |
| travel_insurance | String | `Travel Insurance (Comprehensive)` |
| chronic_conditions | String | `Diabetes Type 2` |
| allergies | String | `Penicillin` |
| accessibility_needs | String | `None` |

### Dataset 2: healthcare_scenarios.csv
| Column | Type | Example |
|---|---|---|
| scenario_id | UUID | `7c8d9e0f-...` |
| scenario_description | Text | `A 45-year-old visitor from Japan...` |
| recommended_care_option | String | `Urgent Care Center` |
| explanation | Text | `Urgent care can assess...` |
| urgency_level | String | `Moderate` |

### Dataset 3: facility_knowledge_base.csv
| Column | Type | Example |
|---|---|---|
| facility_id | UUID | `a1b2c3d4-...` |
| facility_type | String | `Urgent Care Center` |
| facility_description | Text | `A walk-in medical clinic...` |
| common_use_cases | Text | `Minor fractures; sprains...` |
| average_cost_range | String | `$100 – $200 (basic visit)` |
| average_wait_time | String | `15 – 45 minutes` |
| appointment_required | String | `No — walk-in available` |
| insurance_typically_accepted | Text | `Most major US insurance...` |

### Dataset 4: healthcare_terminology.csv
| Column | Type | Example |
|---|---|---|
| term_id | UUID | `d5e6f7a8-...` |
| term | String | `Copay` |
| simple_explanation | Text | `A fixed dollar amount...` |
| visitor_friendly_explanation | Text | `Think of a copay like a fixed entry fee...` |

### Dataset 5: multilingual_phrases.csv
| Column | Type | Example |
|---|---|---|
| phrase_id | UUID | `b9c0d1e2-...` |
| language | String | `Japanese` |
| phrase | Text | `緊急の助けが必要です。` |
| english_translation | Text | `I need emergency help.` |
| category | String | `Emergency` |

---

## 5. Safety & Compliance Notes

1. **Non-diagnostic guardrail:** The system prompt must explicitly instruct the LLM to navigate (not diagnose). Include a disclaimer in every response.
2. **Critical urgency override:** Any scenario with `urgency_level = Critical` must bypass RAG and immediately output the emergency response template.
3. **EMTALA awareness:** Agent should always mention that US ERs cannot legally turn away patients in genuine emergencies, regardless of insurance.
4. **Poison Control:** Agent should proactively mention 1-800-222-1222 for any poisoning/ingestion scenario.
5. **Data privacy:** No real patient data in these datasets. Visitor profiles are synthetic.
6. **Audit trail:** Log which scenarios and facilities were retrieved for each interaction for quality review.
