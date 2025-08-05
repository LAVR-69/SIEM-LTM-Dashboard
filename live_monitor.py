import time
import threading
import psycopg2
import pyudev
import psutil
import subprocess

# PostgreSQL Configuration
DB_CONFIG = {
    'dbname': network_monitor,
    'user': afryn,
    'password': 1234,
    'host': 172.18.0.2,
    'port': 5432
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# USB Monitoring Function
def usb_monitor():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        action = device.action  # 'add' or 'remove'
        device_name = device.get('ID_MODEL', 'Unknown')
        cursor.execute("""
            INSERT INTO usb_events (device_name, action, log_time)
            VALUES (%s, %s, NOW())
        """, (device_name, action))
        conn.commit()
        print(f"USB {action}: {device_name}")

# Network Interface Monitoring Function
def network_interface_monitor():
    while True:
        net_if_stats = psutil.net_if_stats()
        net_io_counters = psutil.net_io_counters(pernic=True)

        for iface, stats in net_if_stats.items():
            is_up = stats.isup
            rx_bytes = net_io_counters[iface].bytes_recv
            tx_bytes = net_io_counters[iface].bytes_sent

            cursor.execute("""
                INSERT INTO network_interface_status (interface, is_up, rx_bytes, tx_bytes, log_time)
                VALUES (%s, %s, %s, %s, NOW())
            """, (iface, is_up, rx_bytes, tx_bytes))
        conn.commit()
        print("Pushed Network Interface Status")
        time.sleep(5)

# Network Device Connection Monitoring Function
def endpoint_connection_monitor():
    known_devices = set()
    while True:
        result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.split('\n'):
            if 'ether' in line:
                parts = line.split()
                ip = parts[1].strip('()')
                mac = parts[3]
                device_id = f"{ip}-{mac}"
                if device_id not in known_devices:
                    cursor.execute("""
                        INSERT INTO endpoint_connections (device_ip, mac_address, status, log_time)
                        VALUES (%s, %s, 'connected', NOW())
                    """, (ip, mac))
                    known_devices.add(device_id)
                    print(f"New Network Device Connected: {ip} {mac}")
        conn.commit()
        time.sleep(10)

# Thread Launchers
usb_thread = threading.Thread(target=usb_monitor)
net_iface_thread = threading.Thread(target=network_interface_monitor)
endpoint_thread = threading.Thread(target=endpoint_connection_monitor)

usb_thread.start()
net_iface_thread.start()
endpoint_thread.start()

usb_thread.join()
net_iface_thread.join()
endpoint_thread.join()
