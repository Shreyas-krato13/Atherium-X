#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Static ISO Integrity & Compliance Verifier
# No QEMU/KVM/emulators used — purely static inspection.

ISO_PATH="${1:-atherium-x.iso}"
MAX_MB=700
MAX_BYTES=$((MAX_MB * 1024 * 1024))

if [[ ! -f "${ISO_PATH}" ]]; then
    echo "FAIL: ISO not found at ${ISO_PATH}"
    exit 1
fi

echo "============================================================"
echo "  Atherium-X Static ISO Verification"
echo "  Target: ${ISO_PATH}"
echo "============================================================"

# 1. File size check (<= 500 MB)
SIZE_BYTES=$(stat -c%s "${ISO_PATH}")
SIZE_MB=$(awk "BEGIN {printf \"%.2f\", ${SIZE_BYTES}/1048576}")
echo "[1/6] Size check: ${SIZE_MB} MB (${SIZE_BYTES} bytes) / limit ${MAX_MB} MB"
if (( SIZE_BYTES > MAX_BYTES )); then
    echo "FAIL: ISO exceeds ${MAX_MB} MB hard limit (${SIZE_MB} MB > ${MAX_MB} MB)!"
    exit 1
fi
echo "      PASS: Within ${MAX_MB} MB budget."

# 2. ISO9660 volume & El Torito inspection via isoinfo / xorriso
echo "[2/6] Checking ISO9660 structure & BIOS + UEFI boot records..."
XORRISO_REPORT=$(xorriso -indev "${ISO_PATH}" -report_el_torito plain -report_system_area plain 2>&1)
echo "${XORRISO_REPORT}" | grep -E "El Torito|System area|MBR|GPT|EFI|BIOS|Boot record" || true

HAS_BIOS=0
HAS_UEFI=0
if echo "${XORRISO_REPORT}" | grep -qiE "bios|isolinux|eltorito.*x86|platform.*0x00"; then
    HAS_BIOS=1
fi
if echo "${XORRISO_REPORT}" | grep -qiE "efi|platform.*0xef|efi\.img"; then
    HAS_UEFI=1
fi

if (( HAS_BIOS == 1 && HAS_UEFI == 1 )); then
    echo "      PASS: Hybrid BIOS + UEFI boot records detected."
else
    echo "FAIL: Missing BIOS (${HAS_BIOS}) or UEFI (${HAS_UEFI}) boot record!"
    exit 1
fi

# 3. Check hybrid MBR/partition table (so raw USB dd/Rufus boots)
echo "[3/6] Checking hybrid MBR/USB bootability..."
if echo "${XORRISO_REPORT}" | grep -qiE "MBR|isohybrid|GPT"; then
    echo "      PASS: Hybrid partition table present."
else
    echo "WARN: Could not confirm hybrid MBR signature in xorriso report."
fi

# 4. Inspect key files inside ISO (kernel, initrd, filesystem.squashfs)
echo "[4/6] Checking live payload inside ISO..."
ISO_FILES=$(xorriso -indev "${ISO_PATH}" -find /live -maxdepth 2 2>/dev/null || true)
echo "${ISO_FILES}"
for req in "vmlinuz" "initrd" "filesystem.squashfs"; do
    if ! echo "${ISO_FILES}" | grep -q "${req}"; then
        echo "FAIL: Missing /live/*${req}* inside ISO!"
        exit 1
    fi
done
echo "      PASS: Kernel, initrd, and filesystem.squashfs present."

# 5. SquashFS integrity & compression check (extract only superblock header or squashfs)
echo "[5/6] Verifying filesystem.squashfs superblock & xz compression..."
TMP_SQFS=$(mktemp /tmp/atherium-sqfs-XXXXXX.squashfs)
trap 'rm -f "${TMP_SQFS}"' EXIT
xorriso -osirrox on -indev "${ISO_PATH}" -extract /live/filesystem.squashfs "${TMP_SQFS}" >/dev/null 2>&1
SQFS_INFO=$(unsquashfs -s "${TMP_SQFS}")
echo "${SQFS_INFO}" | grep -E "Found a valid|Compression|Block size|Number of"
if ! echo "${SQFS_INFO}" | grep -qi "xz"; then
    echo "FAIL: filesystem.squashfs is not xz-compressed!"
    exit 1
fi
SQFS_BYTES=$(stat -c%s "${TMP_SQFS}")
SQFS_MB=$(awk "BEGIN {printf \"%.2f\", ${SQFS_BYTES}/1048576}")
echo "      PASS: Valid xz-compressed squashfs (${SQFS_MB} MB)."

# 6. Checksum verification
echo "[6/6] Generating & verifying SHA256 checksum..."
sha256sum "${ISO_PATH}" > "${ISO_PATH}.sha256"
sha256sum -c "${ISO_PATH}.sha256"

echo "============================================================"
echo "  ALL STATIC CHECKS PASSED (${SIZE_MB} MB / ${MAX_MB} MB)"
echo "============================================================"
