-- Endpoint Device Connections Table
CREATE TABLE endpoint_connections (
    id SERIAL PRIMARY KEY,
    hostname TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    status TEXT NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
