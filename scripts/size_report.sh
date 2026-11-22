#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Phase Size Report Generator
# Outputs ISO size, squashfs size, remaining 500 MB budget, and top 20 largest packages.

PHASE="${1:-phase-1}"
ISO_PATH="${2:-atherium-x.iso}"
BUILD_DIR="${3:-/var/tmp/atherium-x-build}"
OUT_DIR="docs/size_reports"
OUT_FILE="${OUT_DIR}/${PHASE}.md"
MAX_MB=700

mkdir -p "${OUT_DIR}"

if [[ ! -f "${ISO_PATH}" ]]; then
    echo "ERROR: ISO not found at ${ISO_PATH}"
    exit 1
fi

SIZE_BYTES=$(stat -c%s "${ISO_PATH}")
SIZE_MB=$(awk "BEGIN {printf \"%.2f\", ${SIZE_BYTES}/1048576}")
REMAINING_MB=$(awk "BEGIN {printf \"%.2f\", ${MAX_MB} - (${SIZE_BYTES}/1048576)}")

SQFS_PATH="${BUILD_DIR}/binary/live/filesystem.squashfs"
if [[ -f "${SQFS_PATH}" ]]; then
    SQFS_BYTES=$(stat -c%s "${SQFS_PATH}")
    SQFS_MB=$(awk "BEGIN {printf \"%.2f\", ${SQFS_BYTES}/1048576}")
else
    SQFS_MB="N/A"
fi

# Extract /etc/atherium-packages.tsv from squashfs or chroot
PKG_TSV=""
if [[ -f "${BUILD_DIR}/chroot/etc/atherium-packages.tsv" ]]; then
    PKG_TSV="${BUILD_DIR}/chroot/etc/atherium-packages.tsv"
elif [[ -f "${SQFS_PATH}" ]]; then
    TMP_TSV=$(mktemp /tmp/atherium-pkgs-XXXXXX.tsv)
    trap 'rm -f "${TMP_TSV}"' EXIT
    unsquashfs -cat "${SQFS_PATH}" etc/atherium-packages.tsv > "${TMP_TSV}" 2>/dev/null || true
    if [[ -s "${TMP_TSV}" ]]; then
        PKG_TSV="${TMP_TSV}"
    fi
fi

{
    echo "# Atherium-X Size Report — ${PHASE}"
    echo ""
    echo "- **Generated:** $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "- **ISO File:** \`${ISO_PATH}\`"
    echo "- **ISO Size:** **${SIZE_MB} MB** (${SIZE_BYTES} bytes)"
    echo "- **Hard Limit:** ${MAX_MB} MB"
    echo "- **Budget Remaining:** ${REMAINING_MB} MB"
    echo "- **SquashFS Size (xz):** ${SQFS_MB} MB"
    echo ""
    echo "## Top 20 Largest Installed Packages (Uncompressed Installed-Size)"
    echo ""
    echo "| Rank | Package | Version | Installed Size (MB) |"
    echo "|---:|---|---|---:|"
    if [[ -n "${PKG_TSV}" && -f "${PKG_TSV}" ]]; then
        head -n 20 "${PKG_TSV}" | awk -F'\t' '{printf "| %d | `%s` | `%s` | %.2f |\n", NR, $2, $3, $1/1024}'
    else
        echo "| - | *(Package manifest not found)* | - | - |"
    fi
} > "${OUT_FILE}"

echo "==> Size report written to ${OUT_FILE}"
cat "${OUT_FILE}"
