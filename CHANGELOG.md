# Changelog

All notable phases and size/verification milestones for **Atherium-X** are documented here.

## [Phase 3] - Network Connectivity (Verified Statically)
- Updated ISO size budget cap to **700 MB** per user decision (keeping all Dell Vostro/laptop firmware unpruned + full Mesa 3D + `firefox-esr` + `snapd` + full JARVIS HUD).
- Added `config/package-lists/03-network.list.chroot`: `network-manager`, `network-manager-applet`, `wpasupplicant`, `wireless-regdb`, `rfkill`, `systemd-resolved`, `libnss-resolve`, `iputils-ping`, `dnsutils`, `curl`.
- Added `/etc/NetworkManager/conf.d/10-atherium-network.conf`, service-enable hook `0300-network.hook.chroot`, and `nettest.sh`.
- **Static Verification:** PASS — ISO **538.00 MB** / 700 MB (SquashFS 458.70 MB, 162.00 MB remaining), BIOS + UEFI hybrid + SHA256 verified. *(WiFi/LAN/DNS: NEEDS HARDWARE TEST)*

## [Phase 2] - Hardware Compatibility (Verified Statically — Size Budget Alert)
- Added `config/package-lists/02-hardware.list.chroot`: `firmware-iwlwifi`, `firmware-realtek`, `firmware-atheros`, `firmware-brcm80211`, `firmware-sof-signed`, `intel-microcode`, `amd64-microcode`, Xorg + Mesa (`libgl1-mesa-dri`, `intel`/`amdgpu`/`nouveau`/`modesetting`/`vesa`/`fbdev`), `libinput`, PipeWire/ALSA, `acpid`/`upower`/`brightnessctl`.
- Added Dell Vostro touchpad configuration (`/etc/X11/xorg.conf.d/40-libinput.conf`), `hwcheck.sh`, and `docs/HARDWARE.md`.
- **Static Verification:** PASS — ISO **456.00 MB** (SquashFS 375.88 MB, **only 44.00 MB remaining** out of 500 MB), BIOS + UEFI hybrid + SHA256 verified. *(Real-hardware drivers & timing: NEEDS HARDWARE TEST)*
- **Budget Conflict Flagged:** Only 44.00 MB remains for Phases 3–8 (NetworkManager, APT/aptitude, snapd, JARVIS HUD, Plymouth, Browser, Apps, Games, zram). Paused to confirm pruning/budget strategy with user.

## [Phase 1] - Minimal Bootable Core (Verified Statically)
- Initialized Git repository, `Makefile`, `auto/config`, `auto/build`, `auto/clean` targeting Debian 13 (`trixie`) `amd64` with `live-build 20250814`, `xz` squashfs (`-b 1M -Xbcj x86`), and hybrid BIOS (`syslinux`) + UEFI (`grub-efi`) boot.
- Added `config/package-lists/01-core.list.chroot` (`linux-image-amd64`, `systemd-sysv`, `live-boot`, `live-config`, minimal CLI tools, auto-login).
- Added bloat-stripping and package-size recording hooks.
- Added `scripts/verify_iso.sh`, `scripts/size_report.sh`, `scripts/plot_boot_times.py`, `scripts/setup_host.sh`, `tools/flash_usb.sh`, and `bootlog.sh`.
- Added `docs/PACKAGING.md`, `docs/USB_FLASHING.md`, `docs/TESTING.md`, `docs/boot_times.csv`, and `README.md`.
- **Static Verification:** PASS — ISO **252.00 MB** (SquashFS 186.84 MB, 248.00 MB remaining), BIOS + UEFI El Torito + hybrid MBR/GPT verified, SHA256 verified. *(Real-hardware boot & timing: NEEDS HARDWARE TEST)*
