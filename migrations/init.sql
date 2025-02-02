CREATE TABLE IF NOT EXISTS scheduled_triggers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    interval_minutes INT,
    fire_in_minutes INT,
    recurring BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS api_triggers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    payload JSON NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS executions (
    id SERIAL PRIMARY KEY,
    trigger_id INT NOT NULL,
    executed_at TIMESTAMP NOT NULL,
    is_test BOOLEAN NOT NULL,
    trigger_type TEXT NOT NULL,
    is_archived BOOLEAN DEFAULT FALSE
);
