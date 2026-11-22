#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Guarded USB Flasher (Linux / WSL with USB passthrough)
# SAFETY: Refuses to touch mounted disks, system/root disks, or non-removable/non-USB disks.
# Requires exact device name confirmation, verifies ISO SHA256 before writing,
# writes via dd, and verifies the written USB by reading back and comparing SHA256.

ISO_PATH="${1:-atherium-x.iso}"
SHA_PATH="${ISO_PATH}.sha256"

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Please run as root (e.g., sudo $0 ${ISO_PATH})"
    exit 1
fi

if [[ ! -f "${ISO_PATH}" ]]; then
    echo "ERROR: ISO file not found: ${ISO_PATH}"
    exit 1
fi

# 1. Verify ISO checksum BEFORE touching any disk
echo "==> Verifying ISO SHA256 checksum..."
if [[ -f "${SHA_PATH}" ]]; then
    sha256sum -c "${SHA_PATH}"
    EXPECTED_SHA=$(awk '{print $1}' "${SHA_PATH}")
else
    EXPECTED_SHA=$(sha256sum "${ISO_PATH}" | awk '{print $1}')
    echo "    Computed SHA256: ${EXPECTED_SHA}"
fi

ISO_BYTES=$(stat -c%s "${ISO_PATH}")
echo "    ISO size: ${ISO_BYTES} bytes"
echo ""

# 2. List ONLY removable / USB block devices
echo "==> Available removable/USB disks:"
lsblk -d -o NAME,SIZE,MODEL,TRAN,RM,MOUNTPOINT | awk 'NR==1 || ($4=="usb" || $5=="1")'
echo ""

read -r -p "Enter the EXACT target device name (e.g., /dev/sdb): " TARGET_DEV

if [[ ! -b "${TARGET_DEV}" ]]; then
    echo "ABORT: '${TARGET_DEV}' is not a valid block device."
    exit 1
fi

# Strip partition suffix check (must be whole disk, not /dev/sdb1)
DEV_TYPE=$(lsblk -dn -o TYPE "${TARGET_DEV}" | tr -d '[:space:]')
if [[ "${DEV_TYPE}" != "disk" ]]; then
    echo "ABORT: '${TARGET_DEV}' has TYPE='${DEV_TYPE}', expected whole 'disk'."
    exit 1
fi

# 3. Safety check: must be removable OR USB transport
RM_FLAG=$(lsblk -dn -o RM "${TARGET_DEV}" | tr -d '[:space:]')
TRAN_FLAG=$(lsblk -dn -o TRAN "${TARGET_DEV}" | tr -d '[:space:]')
if [[ "${RM_FLAG}" != "1" && "${TRAN_FLAG}" != "usb" ]]; then
    echo "ABORT: '${TARGET_DEV}' is NOT removable (RM=${RM_FLAG}) and NOT USB (TRAN=${TRAN_FLAG})."
    exit 1
fi

# 4. Safety check: refuse if it is the root/system disk
ROOT_SRC=$(findmnt -no SOURCE / || true)
ROOT_DISK=$(lsblk -no PKNAME "${ROOT_SRC}" 2>/dev/null | head -n 1 || true)
if [[ -n "${ROOT_DISK}" && "/dev/${ROOT_DISK}" == "${TARGET_DEV}" ]]; then
    echo "ABORT: '${TARGET_DEV}' is the system root disk!"
    exit 1
fi

# 5. Safety check: refuse if ANY partition on the disk is currently mounted
MOUNTED=$(lsblk -nr -o MOUNTPOINT "${TARGET_DEV}" | grep -v '^$' || true)
if [[ -n "${MOUNTED}" ]]; then
    echo "ABORT: '${TARGET_DEV}' has mounted partition(s):"
    echo "${MOUNTED}"
    echo "Unmount them manually first, then re-run."
    exit 1
fi

# 6. Final explicit confirmation
echo ""
echo "WARNING: ALL DATA ON ${TARGET_DEV} WILL BE PERMANENTLY ERASED!"
lsblk -o NAME,SIZE,MODEL,TRAN,RM "${TARGET_DEV}"
echo ""
read -r -p "Type the exact device path '${TARGET_DEV}' again to confirm: " CONFIRM_DEV
if [[ "${CONFIRM_DEV}" != "${TARGET_DEV}" ]]; then
    echo "ABORT: Confirmation did not match."
    exit 1
fi

# 7. Flash ISO with dd
echo "==> Writing ${ISO_PATH} to ${TARGET_DEV}..."
dd if="${ISO_PATH}" of="${TARGET_DEV}" bs=4M status=progress conv=fsync
sync

# 8. Read-back verification
echo "==> Verifying written bytes by reading back ${ISO_BYTES} bytes..."
WRITTEN_SHA=$(head -c "${ISO_BYTES}" "${TARGET_DEV}" | sha256sum | awk '{print $1}')
echo "    Expected SHA256: ${EXPECTED_SHA}"
echo "    Written  SHA256: ${WRITTEN_SHA}"

if [[ "${WRITTEN_SHA}" != "${EXPECTED_SHA}" ]]; then
    echo "FAIL: Checksum mismatch after write! Do NOT boot this USB; retry with another drive."
    exit 1
fi

echo "SUCCESS: Atherium-X live USB written and verified cleanly on ${TARGET_DEV}."
