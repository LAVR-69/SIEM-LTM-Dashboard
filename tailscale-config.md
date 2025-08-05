# Tailscale Configuration Guide

## Purpose:
Tailscale is used to establish a secure VPN tunnel between distributed endpoints and the central SIEM-LT Dashboard server for telemetry and monitoring data transmission.

## Installation (Linux Mint OS):

curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey <YOUR-AUTH-KEY>

Steps to Enable Tailscale:

1. Install Tailscale:
sudo apt update
sudo apt install tailscale

2. Authenticate & Connect:
sudo tailscale up --authkey <YOUR-AUTH-KEY>

3. Exit Node (Optional):
sudo tailscale up --advertise-exit-node

4. Check Connection:
tailscale status

5. Ensure Tailscale Hijacking does not overide the system, if it does then proceed with this:
sudo tailscale up --accept-dns=false --reset 

Notes:
Ensure Tailscale daemon starts on boot.

Devices communicate over Tailscale IPs (e.g., 100.x.x.x).

Exit nodes are not mandatory for dashboard access unless tunneling external internet.


