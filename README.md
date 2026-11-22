# Atherium-X

**Atherium-X** is a custom, Debian-based (`trixie` / Debian 13 stable) hybrid BIOS + UEFI live-USB operating system engineered to fit in **<= 500 MB**, featuring a futuristic JARVIS-inspired HUD desktop, animated arc-reactor Plymouth boot splash, working networking, APT/aptitude, Snap Store support, browser, native lightweight games, and zram/earlyoom memory management.

## Quick Start (Build from Source)

### Host Requirements
- **Linux host:** Debian 12/13 or Ubuntu 22.04/24.04/26.04 (native or **WSL2** on Windows).
- **Disk space:** ~4 GB free in `/var/tmp/atherium-x-build`.
- **Network:** Internet access to `deb.debian.org`.
- **Expected build time:** ~3–8 minutes per phase (depending on internet speed and CPU cores for `xz` squashfs compression).

### 1. Install Host Dependencies (One-Time)
```bash
sudo bash scripts/setup_host.sh
```
*(Installs `debootstrap`, `debian-archive-keyring`, `squashfs-tools`, `xorriso`, `genisoimage`, `mtools`, `dosfstools`, `python3-matplotlib`, and upstream Debian `live-build`.)*

### 2. Build & Verify ISO
```bash
sudo make build PHASE=phase-1
```
This stages the build in `/var/tmp/atherium-x-build` (fast native Linux ext4 FS, avoiding Windows/OneDrive I/O overhead and `/tmp` `nodev` mount issues), runs `lb config && lb build`, copies `atherium-x.iso` to the repo root, generates `atherium-x.iso.sha256`, runs static integrity checks (`scripts/verify_iso.sh`), and writes `docs/size_reports/phase-1.md`.

### 3. Other Makefile Targets
- `make verify` — Run static ISO checks (`xorriso`, BIOS+UEFI El Torito, `unsquashfs -s`, SHA256, <= 500 MB).
- `make size-report PHASE=phase-X` — Generate ISO size + top-20 largest packages report.
- `make checksum` — Regenerate and verify `atherium-x.iso.sha256`.
- `make chart` — Render `docs/boot_times.png` from measured values in `docs/boot_times.csv`.
- `make clean` — Clean build directory and local ISO artifacts.

### 4. Flash to USB
See [docs/USB_FLASHING.md](docs/USB_FLASHING.md) for:
- Guarded Linux/WSL flasher: `sudo bash tools/flash_usb.sh atherium-x.iso`
- Windows Rufus (DD mode) / balenaEtcher instructions
- Dell Vostro BIOS/UEFI (`F12`/`F2`) and Secure Boot instructions

## Documentation
- [docs/PACKAGING.md](docs/PACKAGING.md) — How source code becomes an ISO binary (with Mermaid diagram & 1-slide summary)
- [docs/TESTING.md](docs/TESTING.md) — Real-hardware verification checklist
- [docs/USB_FLASHING.md](docs/USB_FLASHING.md) — USB flashing & Dell Vostro BIOS/UEFI guide
- [docs/boot_times.csv](docs/boot_times.csv) — Real-hardware boot timing log
- [docs/size_reports/](docs/size_reports/) — Per-phase ISO size & top-20 package reports
- [CHANGELOG.md](CHANGELOG.md) — Phase-by-phase build history
