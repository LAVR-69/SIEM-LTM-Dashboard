import psutil
import psycopg2
import socket
import time
from datetime import datetime

conn = psycopg2.connect(
    dbname='network_monitor',
    user='monitor_user',
    password='lavr123',
    host='100.124.209.58',  # This is fine since you're using Tailscale IP
    port='5432'
)
cur = conn.cursor()

hostname = socket.gethostname()

def get_connected_endpoints():
    connections = psutil.net_connections(kind='inet')
    for conn_data in connections:
        if conn_data.raddr:  # Only log active connections
            ip_address = conn_data.raddr.ip
            status = conn_data.status
            timestamp = datetime.now()
            cur.execute(
                "INSERT INTO endpoint_connections (hostname, ip_address, status, log_time) VALUES (%s, %s, %s, %s)",
                (hostname, ip_address, status, timestamp)
            )
    conn.commit()

while True:
    get_connected_endpoints()
    time.sleep(5)

