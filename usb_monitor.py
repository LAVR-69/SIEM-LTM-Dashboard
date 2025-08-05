import psycopg2
import pyudev
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

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

def log_event(device, action):
    timestamp = datetime.now()
    device_name = device.get('ID_MODEL', 'Unknown Device')
    cur.execute(
        "INSERT INTO usb_events (device_name, action, log_time) VALUES (%s, %s, %s)",
        (device_name, action, timestamp)
    )
    conn.commit()

for device in iter(monitor.poll, None):
    log_event(device, device.action)

