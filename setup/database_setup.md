# Database Setup Guide – SIEM-LTM Dashboard Monitoring Project

---

## Objective:
This document provides a **step-by-step guide** to set up the **PostgreSQL database (network_monitor)** which serves as the backend data store for the SIEM-LT Dashboard Project. This includes user creation, schema loading, network access configurations via Tailscale, and error troubleshooting during implementation.

---

## PostgreSQL Installation & Initial Configuration

### Step 1: Install PostgreSQL (Skip if Already Installed)

$ sudo apt update
$ sudo apt install postgresql postgresql-contrib

### Step 2: Verify PostgreSQL Service is Active
$ sudo systemctl status postgresql
#Ensure it's Active (Running).

## Database and User Creation
### Step 3: Switch to PostgreSQL Superuser
$ sudo -i -u postgres

### Step 4: Access PostgreSQL Interactive Shell
> psql

### Step 5: Create Database & User
#Execute the following commands inside psql shell:
> CREATE DATABASE network_monitor;
> CREATE USER monitor_user WITH ENCRYPTED PASSWORD 'lavr123';
> GRANT ALL PRIVILEGES ON DATABASE network_monitor TO monitor_user;

### Step 6: Verify Database & User Creation
> \l         -- Lists all databases
> \du        -- Lists all users/roles

### Step 7: Exit PostgreSQL Shell
> \q
#And exit from postgres user:
> exit

## Database Schema Execution
### Step 8: Execute Schema Script
#Ensure you’re inside the project directory:
$ cd ~/live-system-monitor
$ psql -U monitor_user -d network_monitor -f sql/schema.sql

# What This Creates:
Table	                            Purpose
usb_events	Logs USB device events: Insert/remove
endpoint_connections:	            Logs active device IP connections
network_interfaces:	                Tracks RX/TX byte counts per interface

## Configuring PostgreSQL for Remote Access (Tailscale)
### Step 9: Edit pg_hba.conf to Allow Tailscale IPs
$ sudo nano /etc/postgresql/12/main/pg_hba.conf
# Add this line at the bottom
host    all             all             100.0.0.0/8             md5

### Step 10: Edit postgresql.conf to Listen on All IPs
$ sudo nano /etc/postgresql/12/main/postgresql.conf
#Uncomment and set:
listen_addresses = '*'

### Step 11: Restart PostgreSQL Service
$ sudo systemctl restart postgresql

## Python Script Database Connection (Example)
# Ensure all scripts connecting to DB (usb_monitor.py, endpoint_monitor.py, network_monitor.py) have this structure:
conn = psycopg2.connect(
    dbname='network_monitor',
    user='monitor_user',
    password='lavr123',
    host='100.X.X.X',  # Replace with actual Tailscale IP of DB Server
    port='5432'
)

### Verification Steps
#Ensure Tailscale VPN is up and devices are connected.
On the agent device, test DB connection:
$ psql -U monitor_user -d network_monitor -h 100.X.X.X -W

You should be inside the DB shell if Tailscale connection is good.
Check Tables:
> \dt
