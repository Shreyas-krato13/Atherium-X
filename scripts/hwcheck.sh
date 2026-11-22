#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Hardware Verification Script (source copy; installed to /usr/local/bin/hwcheck.sh in ISO)

echo "============================================================"
echo "  Atherium-X Hardware Check (hwcheck.sh)"
echo "  Host: $(hostname) | Kernel: $(uname -r)"
echo "  Date: $(date)"
echo "============================================================"

echo ""
echo "[1] DMI / System Model:"
if [[ -r /sys/class/dmi/id/product_name ]]; then
    echo "    Vendor : $(cat /sys/class/dmi/id/sys_vendor 2>/dev/null || echo 'N/A')"
    echo "    Product: $(cat /sys/class/dmi/id/product_name 2>/dev/null || echo 'N/A')"
else
    echo "    (DMI info unavailable)"
fi

echo ""
echo "[2] CPU & Microcode:"
grep -m1 "model name" /proc/cpuinfo || true
grep -m1 "microcode" /proc/cpuinfo || true

echo ""
echo "[3] PCI Devices (GPU / Network / Audio):"
lspci -nnk | grep -EA3 "VGA|3D|Display|Network|Ethernet|Audio" || lspci

echo ""
echo "[4] USB Devices:"
lsusb || echo "(lsusb unavailable)"

echo ""
echo "[5] Audio (ALSA / PipeWire):"
aplay -l 2>/dev/null | head -n 15 || echo "    No ALSA playback devices found."

echo ""
echo "[6] Backlight / Brightness & Battery:"
ls -1 /sys/class/backlight 2>/dev/null || echo "    No backlight interfaces found."
acpi -b 2>/dev/null || echo "    No battery detected (or acpi unavailable)."

echo ""
echo "[7] dmesg Firmware Failure Summary:"
FW_ERRS=$(dmesg 2>/dev/null | grep -iE "firmware.*(fail|error|missing|direct-load|unable)|failed to load" || true)
if [[ -z "${FW_ERRS}" ]]; then
    echo "    PASS: No firmware load failures detected in dmesg."
else
    echo "    WARNING: Firmware messages found in dmesg:"
    echo "${FW_ERRS}"
fi

echo ""
echo "============================================================"
echo "  Hardware check complete."
echo "============================================================"
