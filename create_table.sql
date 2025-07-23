CREATE TABLE IF NOT EXISTS image_classification_results (
    id SERIAL PRIMARY KEY,
    claim_id VARCHAR(255) NOT NULL,
    image_name VARCHAR(255) NOT NULL,
    classification INTEGER NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
