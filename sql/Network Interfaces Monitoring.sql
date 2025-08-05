-- Network Interfaces Monitoring Table
CREATE TABLE network_interfaces (
    id SERIAL PRIMARY KEY,
    interface_name TEXT NOT NULL,
    status TEXT NOT NULL,  -- UP/DOWN
    rx_bytes BIGINT NOT NULL,
    tx_bytes BIGINT NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
