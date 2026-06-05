CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS csc_knowledge (
    id BIGSERIAL PRIMARY KEY,
    service_name TEXT NOT NULL,
    category TEXT,
    purpose TEXT,
    eligibility TEXT,
    prerequisites TEXT,
    fee_information TEXT,
    required_documents TEXT,
    dsp_navigation TEXT,
    form_filling_steps TEXT,
    validation_rules TEXT,
    upload_requirements TEXT,
    workflow TEXT,
    status_tracking TEXT,
    approval_process TEXT,
    download_print_process TEXT,
    common_errors TEXT,
    policies_circulars TEXT,
    comparison TEXT,
    faq TEXT,
    official_url TEXT NOT NULL,
    official_helpdesk TEXT,
    official_tracking_url TEXT,
    response_modes TEXT,
    service_keywords TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS csc_knowledge_embedding_idx
ON csc_knowledge
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS csc_knowledge_service_name_idx
ON csc_knowledge (service_name);

CREATE INDEX IF NOT EXISTS csc_knowledge_category_idx
ON csc_knowledge (category);
