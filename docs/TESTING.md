# Atherium-X Real-Hardware Testing Checklist (Dell Vostro)

> All items below are marked **NEEDS HARDWARE TEST** until verified on your physical Dell Vostro laptop (no QEMU/KVM emulators are used in this project).

## Boot & Firmware (Phase 1 & 7)
- [ ] **NEEDS HARDWARE TEST:** USB boots cleanly in **UEFI mode** (Dell `F12` boot menu).
- [ ] **NEEDS HARDWARE TEST:** USB boots cleanly in **Legacy BIOS mode** (if enabled).
- [ ] **NEEDS HARDWARE TEST:** GRUB / ISOLINUX menu displays "Atherium-X" branding.
- [ ] **NEEDS HARDWARE TEST:** Plymouth arc-reactor boot animation plays smoothly and hands off to desktop without flicker.
- [ ] **NEEDS HARDWARE TEST:** Auto-login succeeds without password prompt (`atherium`).
- [ ] **NEEDS HARDWARE TEST:** Run `bootlog.sh` and record `systemd-analyze` + stopwatch timing in `docs/boot_times.csv`.

## Hardware Compatibility (Phase 2)
- [ ] **NEEDS HARDWARE TEST:** Run `hwcheck.sh` — verify zero critical missing firmware errors in `dmesg`.
- [ ] **NEEDS HARDWARE TEST:** Display native resolution and hardware acceleration (Mesa/Xorg) work cleanly.
- [ ] **NEEDS HARDWARE TEST:** Touchpad (tap-to-click, two-finger scroll) and keyboard function keys work.
- [ ] **NEEDS HARDWARE TEST:** Screen brightness keys / backlight control work.
- [ ] **NEEDS HARDWARE TEST:** Audio output (speakers + headphone jack) works via PipeWire/ALSA.
- [ ] **NEEDS HARDWARE TEST:** Battery status and AC adapter detection work (ACPI).

## Networking (Phase 3)
- [ ] **NEEDS HARDWARE TEST:** Run `nettest.sh` — Ethernet DHCP acquires IP + DNS automatically.
- [ ] **NEEDS HARDWARE TEST:** WiFi scan detects nearby SSIDs; connecting via tray applet / `nmtui` succeeds.
- [ ] **NEEDS HARDWARE TEST:** `ping -c 3 deb.debian.org` succeeds (IP + DNS verified).

## Package Management & Snap Store (Phase 4 & 5)
- [ ] **NEEDS HARDWARE TEST:** `sudo apt update && sudo apt install -y sl` succeeds over network.
- [ ] **NEEDS HARDWARE TEST:** `aptitude` launches and queries Debian `trixie` repos cleanly.
- [ ] **NEEDS HARDWARE TEST:** `snap version` and `snap find` work; **Atherium Store** launcher installs/runs Snap Store cleanly.

## Desktop HUD, Apps, Games & Memory (Phase 6 & 8)
- [ ] **NEEDS HARDWARE TEST:** Openbox + `picom` + `tint2` HUD bar + `rofi` launcher render cleanly with `Atherium-X-Icons`.
- [ ] **NEEDS HARDWARE TEST:** Startup greeting `"Welcome back. Atherium-X online."` appears.
- [ ] **NEEDS HARDWARE TEST:** Browser loads web pages with audio/video playback.
- [ ] **NEEDS HARDWARE TEST:** `pcmanfm`, terminal, text editor, image viewer, `mpv`, system monitor, and Games launcher all work.
- [ ] **NEEDS HARDWARE TEST:** `zramctl` shows active zram swap; `systemctl status earlyoom` is active.
