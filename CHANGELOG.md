# Changelog

All notable phases and size/verification milestones for **Atherium-X** are documented here.

## [Phase 1] - Minimal Bootable Core (Verified Statically)
- Initialized Git repository, `Makefile`, `auto/config`, `auto/build`, `auto/clean` targeting Debian 13 (`trixie`) `amd64` with `live-build 20250814`, `xz` squashfs (`-b 1M -Xbcj x86`), and hybrid BIOS (`syslinux`) + UEFI (`grub-efi`) boot.
- Added `config/package-lists/01-core.list.chroot` (`linux-image-amd64`, `systemd-sysv`, `live-boot`, `live-config`, minimal CLI tools, auto-login).
- Added bloat-stripping and package-size recording hooks.
- Added `scripts/verify_iso.sh`, `scripts/size_report.sh`, `scripts/plot_boot_times.py`, `scripts/setup_host.sh`, `tools/flash_usb.sh`, and `bootlog.sh`.
- Added `docs/PACKAGING.md`, `docs/USB_FLASHING.md`, `docs/TESTING.md`, `docs/boot_times.csv`, and `README.md`.
- **Static Verification:** PASS — ISO **252.00 MB** (SquashFS 186.84 MB, 248.00 MB remaining), BIOS + UEFI El Torito + hybrid MBR/GPT verified, SHA256 verified. *(Real-hardware boot & timing: NEEDS HARDWARE TEST)*
