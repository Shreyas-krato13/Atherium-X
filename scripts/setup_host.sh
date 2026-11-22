#!/usr/bin/env bash
set -euo pipefail

# Atherium-X Host Setup Script (Debian / Ubuntu / WSL2)
# Installs build dependencies and upstream Debian live-build.

if [[ $EUID -ne 0 ]]; then
    echo "Please run as root (e.g., sudo $0)"
    exit 1
fi

echo "==> Checking Debian stable release..."
curl -fsSL https://deb.debian.org/debian/dists/stable/Release | grep -E '^(Suite|Version|Codename):'

echo "==> Installing base build dependencies..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    debootstrap \
    debian-archive-keyring \
    squashfs-tools \
    xorriso \
    genisoimage \
    mtools \
    dosfstools \
    cpio \
    xz-utils \
    curl \
    ca-certificates \
    rsync \
    make \
    python3 \
    python3-matplotlib

# On Ubuntu hosts, the repo's live-build is an old 3.0~a57 fork.
# Install upstream Debian live-build (Architecture: all shell scripts) for full Debian stable support.
echo "==> Installing upstream Debian live-build..."
DEB_FILE=$(curl -fsSL https://deb.debian.org/debian/pool/main/l/live-build/ \
    | grep -oE 'live-build_[^"<>]+_all\.deb' \
    | sort -V \
    | tail -n 1)

if [[ -z "${DEB_FILE}" ]]; then
    echo "ERROR: Could not locate Debian live-build .deb"
    exit 1
fi

echo "==> Downloading ${DEB_FILE}..."
curl -fsSL "https://deb.debian.org/debian/pool/main/l/live-build/${DEB_FILE}" -o /tmp/live-build.deb
dpkg -i /tmp/live-build.deb || apt-get install -f -y
rm -f /tmp/live-build.deb

echo "==> Installed live-build version: $(lb --version)"
