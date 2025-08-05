-- USB Events Table
CREATE TABLE usb_events (
    id SERIAL PRIMARY KEY,
    device_name TEXT NOT NULL,
    action TEXT NOT NULL,  -- Added/Removed
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
