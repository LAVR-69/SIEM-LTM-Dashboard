import psutil
import psycopg2
import time
from datetime import datetime

conn = psycopg2.connect(
    dbname='network_monitor',
    user='monitor_user',
    password='lavr123',
    host='100.124.209.58',
    port='5432'
)
cur = conn.cursor()

def get_interface_stats():
    net_io = psutil.net_io_counters(pernic=True)
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()

    for interface in net_io:
        status = 'UP' if net_if_stats[interface].isup else 'DOWN'
        rx_bytes = net_io[interface].bytes_recv
        tx_bytes = net_io[interface].bytes_sent
        timestamp = datetime.now()

        cur.execute(
            "INSERT INTO network_interfaces (interface_name, status, rx_bytes, tx_bytes, log_time) VALUES (%s, %s, %s, %s, %s)",
            (interface, status, rx_bytes, tx_bytes, timestamp)
        )
    conn.commit()

while True:
    get_interface_stats()
    time.sleep(5)

