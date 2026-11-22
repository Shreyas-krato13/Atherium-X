#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Network Diagnostics Script (source copy; installed to /usr/local/bin/nettest.sh in ISO)

echo "============================================================"
echo "  Atherium-X Network Test (nettest.sh)"
echo "  Date: $(date)"
echo "============================================================"

echo ""
echo "[1] RFKill Radio State:"
rfkill list 2>/dev/null || echo "    (rfkill unavailable)"

echo ""
echo "[2] Network Interfaces & Links:"
ip -br link

echo ""
echo "[3] IP Addresses:"
ip -br addr

echo ""
echo "[4] Default Route:"
ip route | head -n 10

echo ""
echo "[5] NetworkManager Device Status:"
nmcli -f DEVICE,TYPE,STATE,CONNECTION device status 2>/dev/null || echo "    (nmcli unavailable)"

echo ""
echo "[6] WiFi Scan (top 15 networks):"
nmcli -f IN-USE,SSID,SIGNAL,SECURITY dev wifi list 2>/dev/null | head -n 16 || echo "    (No WiFi device or scan unavailable)"

echo ""
echo "[7] DNS Resolution Check (deb.debian.org):"
if getent hosts deb.debian.org >/dev/null 2>&1; then
    getent hosts deb.debian.org | head -n 3
    echo "    PASS: DNS resolution working."
else
    echo "    FAIL: DNS resolution failed (check WiFi/Ethernet connection)."
fi

echo ""
echo "[8] Connectivity Ping (1.1.1.1 & deb.debian.org):"
ping -c 3 -W 3 1.1.1.1 && echo "    PASS: IPv4 reachability OK." || echo "    FAIL: Cannot ping 1.1.1.1."
ping -c 3 -W 3 deb.debian.org && echo "    PASS: Hostname ping OK." || echo "    FAIL: Cannot ping deb.debian.org."

echo ""
echo "============================================================"
echo "  Network test complete."
echo "============================================================"
