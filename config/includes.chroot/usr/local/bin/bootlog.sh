#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Boot Timing Logger
# Run on real hardware after booting the live USB.
# Appends a CSV row to docs/boot_times.csv (or specified output file).
#
# Usage:
#   bootlog.sh <phase> <components_added> <iso_size_mb> [stopwatch_sec] [csv_path]
# Example:
#   bootlog.sh "Phase 1" "Core CLI + systemd + live-boot" "210.4" "18.5" /tmp/boot_times.csv

PHASE="${1:-Phase ?}"
COMPONENTS="${2:-Unspecified}"
ISO_SIZE_MB="${3:-UNKNOWN}"
STOPWATCH_SEC="${4:-<ENTER_STOPWATCH_SEC>}"
CSV_PATH="${5:-./boot_times.csv}"

if ! command -v systemd-analyze >/dev/null 2>&1; then
    echo "ERROR: systemd-analyze not found."
    exit 1
fi

RAW_TIME=$(systemd-analyze time 2>&1 || true)
echo "=== systemd-analyze ==="
echo "${RAW_TIME}"
echo ""
echo "=== systemd-analyze blame (top 15) ==="
systemd-analyze blame 2>/dev/null | head -n 15 || true
echo ""

# Parse kernel, initrd, userspace, total from systemd-analyze output
# Typical format: "Startup finished in 3.120s (firmware) + 1.200s (loader) + 2.450s (kernel) + 4.100s (userspace) = 10.870s"
extract_field() {
    local label="$1"
    echo "${RAW_TIME}" | grep -oE "[0-9]+(\.[0-9]+)?(ms|s|min) \(${label}\)" | head -n 1 | awk '{print $1}' || echo "N/A"
}

FIRMWARE=$(extract_field "firmware")
KERNEL=$(extract_field "kernel")
INITRD=$(extract_field "initrd")
USERSPACE=$(extract_field "userspace")
TOTAL=$(echo "${RAW_TIME}" | grep -oE "= [0-9]+(\.[0-9]+)?(ms|s|min)" | head -n 1 | awk '{print $2}' || echo "N/A")

FW_KERNEL="fw:${FIRMWARE:-N/A} + kern:${KERNEL:-N/A}"
if [[ -n "${INITRD}" && "${INITRD}" != "N/A" ]]; then
    FW_KERNEL="${FW_KERNEL} + initrd:${INITRD}"
fi

if [[ ! -f "${CSV_PATH}" ]]; then
    echo "phase,components_added,firmware_kernel_time,userspace_time,systemd_total,stopwatch_total_sec,iso_size_mb" > "${CSV_PATH}"
fi

printf '"%s","%s","%s","%s","%s","%s","%s"\n' \
    "${PHASE}" \
    "${COMPONENTS}" \
    "${FW_KERNEL}" \
    "${USERSPACE:-N/A}" \
    "${TOTAL:-N/A}" \
    "${STOPWATCH_SEC}" \
    "${ISO_SIZE_MB}" >> "${CSV_PATH}"

echo "Appended boot timing row to: ${CSV_PATH}"
tail -n 1 "${CSV_PATH}"
