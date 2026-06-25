-- =============================================================================
-- AI Healthcare Navigation Assistant
-- SQL Table Schemas (PostgreSQL)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- DATASET 1: Visitor Profiles
-- Storage: PostgreSQL (structured, filterable, relational)
-- -----------------------------------------------------------------------------
CREATE TABLE visitor_profiles (
    visitor_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    country_of_origin   VARCHAR(100)    NOT NULL,
    native_language     VARCHAR(80)     NOT NULL,
    age_group           VARCHAR(20)     NOT NULL
                            CHECK (age_group IN ('18-24','25-34','35-44','45-54','55-64','65+')),
    travel_type         VARCHAR(60)     NOT NULL,
    travel_insurance    VARCHAR(100)    NOT NULL,
    chronic_conditions  VARCHAR(150)    NOT NULL DEFAULT 'None',
    allergies           VARCHAR(150)    NOT NULL DEFAULT 'None',
    accessibility_needs VARCHAR(150)    NOT NULL DEFAULT 'None',
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_vp_country        ON visitor_profiles (country_of_origin);
CREATE INDEX idx_vp_language       ON visitor_profiles (native_language);
CREATE INDEX idx_vp_travel_type    ON visitor_profiles (travel_type);
CREATE INDEX idx_vp_insurance      ON visitor_profiles (travel_insurance);

COMMENT ON TABLE  visitor_profiles IS
    'Synthetic international visitor profiles used for personalizing healthcare navigation advice.';
COMMENT ON COLUMN visitor_profiles.travel_insurance IS
    'Type of insurance coverage the visitor carries while in the US.';


-- -----------------------------------------------------------------------------
-- DATASET 2: Healthcare Access Scenarios
-- Storage: VECTOR DATABASE (semantic similarity search for RAG)
-- Metadata columns kept here for hybrid filtering.
-- -----------------------------------------------------------------------------
CREATE TABLE healthcare_scenarios (
    scenario_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_description    TEXT            NOT NULL,
    recommended_care_option VARCHAR(80)     NOT NULL,
    explanation             TEXT            NOT NULL,
    urgency_level           VARCHAR(20)     NOT NULL
                                CHECK (urgency_level IN
                                    ('Low','Low-Moderate','Moderate','High','Critical')),
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_hs_care_option ON healthcare_scenarios (recommended_care_option);
CREATE INDEX idx_hs_urgency     ON healthcare_scenarios (urgency_level);

COMMENT ON TABLE healthcare_scenarios IS
    'Synthetic scenarios describing situations international visitors may face, '
    'mapped to appropriate US healthcare access options. '
    'Primary store: vector DB. This table holds metadata for hybrid filtering.';


-- -----------------------------------------------------------------------------
-- DATASET 3: Healthcare Facility Knowledge Base
-- Storage: VECTOR DATABASE (semantic retrieval) + PostgreSQL (metadata/filtering)
-- -----------------------------------------------------------------------------
CREATE TABLE facility_knowledge_base (
    facility_id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_type               VARCHAR(80)  NOT NULL,
    facility_description        TEXT         NOT NULL,
    common_use_cases            TEXT         NOT NULL,
    average_cost_range          VARCHAR(100) NOT NULL,
    average_wait_time           VARCHAR(80)  NOT NULL,
    appointment_required        VARCHAR(120) NOT NULL,
    insurance_typically_accepted TEXT        NOT NULL,
    created_at                  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_fkb_type ON facility_knowledge_base (facility_type);

COMMENT ON TABLE facility_knowledge_base IS
    'Knowledge base describing US healthcare facility types, their use cases, '
    'costs, and insurance acceptance. Used for RAG retrieval.';


-- -----------------------------------------------------------------------------
-- DATASET 4: Healthcare Terminology
-- Storage: VECTOR DATABASE (semantic search on explanations)
-- -----------------------------------------------------------------------------
CREATE TABLE healthcare_terminology (
    term_id                         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    term                            VARCHAR(120) NOT NULL,
    simple_explanation              TEXT         NOT NULL,
    visitor_friendly_explanation    TEXT         NOT NULL,
    created_at                      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_ht_term ON healthcare_terminology (term);

COMMENT ON TABLE healthcare_terminology IS
    'Plain-language explanations of US healthcare terms targeted at '
    'international visitors unfamiliar with the US health system.';


-- -----------------------------------------------------------------------------
-- DATASET 5: Multilingual Healthcare Communication
-- Storage: PostgreSQL (exact-match lookup by language + category)
--          Optionally mirrored to vector DB for fuzzy phrase matching.
-- -----------------------------------------------------------------------------
CREATE TABLE multilingual_phrases (
    phrase_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    language                VARCHAR(30)  NOT NULL,
    phrase                  TEXT         NOT NULL,
    english_translation     TEXT         NOT NULL,
    category                VARCHAR(60)  NOT NULL,
    created_at              TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_mp_language ON multilingual_phrases (language);
CREATE INDEX idx_mp_category ON multilingual_phrases (category);
CREATE INDEX idx_mp_lang_cat ON multilingual_phrases (language, category);

COMMENT ON TABLE multilingual_phrases IS
    'Multilingual healthcare communication phrases for 7 languages '
    'used to help international visitors communicate with US providers.';


-- =============================================================================
-- SUPPORTING LOOKUP TABLES
-- =============================================================================

CREATE TABLE care_option_reference (
    option_id       SERIAL PRIMARY KEY,
    option_name     VARCHAR(80)  UNIQUE NOT NULL,
    short_code      VARCHAR(20)  UNIQUE NOT NULL,
    is_emergency    BOOLEAN      NOT NULL DEFAULT FALSE,
    requires_rx     BOOLEAN      NOT NULL DEFAULT FALSE,
    typical_hours   VARCHAR(60),
    cost_tier       VARCHAR(20)  CHECK (cost_tier IN ('Low','Moderate','High','Variable'))
);

INSERT INTO care_option_reference
    (option_name, short_code, is_emergency, requires_rx, typical_hours, cost_tier)
VALUES
    ('Emergency Room (ER)',      'ER',          TRUE,  TRUE,  '24/7',                   'High'),
    ('Urgent Care Center',       'URGENT',      FALSE, TRUE,  '8am–10pm most days',     'Moderate'),
    ('Pharmacy',                 'PHARMACY',    FALSE, FALSE, 'Varies; 24hr available', 'Low'),
    ('Telehealth Service',       'TELEHEALTH',  FALSE, TRUE,  '24/7 on-demand',         'Low'),
    ('Community Health Clinic',  'COMMUNITY',   FALSE, TRUE,  'By appointment',         'Low');


CREATE TABLE urgency_level_reference (
    level_id        SERIAL PRIMARY KEY,
    level_name      VARCHAR(20) UNIQUE NOT NULL,
    level_rank      SMALLINT    NOT NULL,   -- 1 = lowest urgency
    default_action  TEXT        NOT NULL
);

INSERT INTO urgency_level_reference (level_name, level_rank, default_action) VALUES
    ('Low',          1, 'Self-care or pharmacy visit appropriate.'),
    ('Low-Moderate', 2, 'Telehealth or urgent care recommended within 24 hours.'),
    ('Moderate',     3, 'Urgent care visit recommended same day.'),
    ('High',         4, 'Go to urgent care immediately or consider ER.'),
    ('Critical',     5, 'Call 911 or go to the nearest ER immediately.');
