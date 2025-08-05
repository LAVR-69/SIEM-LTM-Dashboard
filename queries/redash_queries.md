Redash Queries for SIEM-LT Dashboard Monitoring


Postgresql Queries for Redash UI-

1. USB Device Events 

SELECT
  log_time AS "Time",
  device_name AS "Device",
  action AS "Action"
FROM usb_events
ORDER BY log_time DESC
LIMIT 50;


2. Endpoint Device Connections – Active Connections
sql
Copy
Edit
SELECT
  log_time AS "Time",
  hostname AS "Hostname",
  ip_address AS "Remote IP",
  status AS "Status"
FROM endpoint_connections
WHERE status = 'ESTABLISHED'
ORDER BY log_time DESC
LIMIT 50;


3. Network Interfaces Statistics – Interface Usage
Copy
Edit
SELECT
  log_time AS "Time",
  interface_name AS "Interface",
  rx_bytes AS "RX Bytes",
  tx_bytes AS "TX Bytes",
  status AS "Status"
FROM network_interfaces
ORDER BY log_time DESC
LIMIT 50;


4. KPI – Active Network Interfaces Count
SELECT COUNT(DISTINCT interface_name) AS "Active Interfaces"
FROM network_interfaces
WHERE status = 'UP'


5. KPI – Connected Endpoint Devices Count
SELECT COUNT(*) AS "Active Endpoints"
FROM endpoint_connections
WHERE status = 'ESTABLISHED'
AND log_time > NOW() - INTERVAL '10 minutes';


6. KPI – USB Devices Connected (Last 10 Minutes)
SELECT COUNT(*) AS "USB Devices Connected (10 min)"
FROM usb_events
WHERE action = 'add'
AND log_time > NOW() - INTERVAL '10 minutes';


7. Network Interfaces RX/TX Table View
SELECT
  log_time AS "Time",
  interface_name AS "Interface",
  rx_bytes AS "RX Bytes",
  tx_bytes AS "TX Bytes"
FROM network_interfaces
ORDER BY log_time DESC
LIMIT 50;


8. Total USB Events Count
SELECT COUNT(*) AS "Total USB Events" FROM usb_events;



