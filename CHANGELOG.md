# Changelog

All notable phases and size/verification milestones for **Atherium-X** are documented here.

## [Phase 9.3] - Stability & Real-Hardware Bugfix Pass (Verified Statically)
- **Fixed disappearing bottom taskbar:** Replaced crashy `tint2` with Debian's rock-solid **`lxpanel`** (`atherium` profile at bottom, 42px dark obsidian + cyan, categorized Start Menu, pinned Browser/Files/Terminal/Store/Games/Wi-Fi, running tasks, tray, battery, clock, Power). Bonus: removing `tint2` eliminated 40 MB of transitive `libgdal`/`proj-data` bloat!
- **Fixed Wi-Fi connection failure:** Added **`lxpolkit`** + `/etc/polkit-1/rules.d/50-atherium-network.rules` and upgraded `atherium-wifi` to unblock `rfkill`, clear stale failed profiles, and connect via `sudo nmcli --wait 20 dev wifi connect` with live progress & IP confirmation.
- **Fixed desktop icon execution prompt:** Added `/etc/skel/.config/libfm/libfm.conf` (`quick_exec=1`) so all Desktop `.desktop` icons launch immediately on double-click.
- **Fixed black wallpaper:** Added `/etc/skel/.config/pcmanfm/default/desktop-items-0.conf` pointing directly to `/usr/share/backgrounds/atherium-x/atherium-hud.png`.
- **Static Verification:** PASS — ISO **651.00 MB** / 700 MB (**-40.00 MB** smaller; 49.00 MB remaining; SquashFS 558.34 MB), BIOS + UEFI hybrid + SHA256 verified. *(Real-hardware verification: NEEDS HARDWARE TEST)*

## [Phase 9.2] - Windows-Style JARVIS HUD UX Upgrade (Verified Statically)
- Replaced minimal top bar with a **44px Windows-style bottom HUD taskbar** (`tint2`): **`◈ START`**, pinned **Browser / Files / Terminal / Store / Games**, running tasks, enlarged `24px` system tray (`nm-applet`), dedicated **`Wi-Fi`** button, **Battery %**, 2-line **Clock/Date**, and **`Power`** (**Shutdown / Reboot / Logout**).
- Upgraded **Start Menu** (`atherium-menu` / `rofi`) to an `82% x 76%` translucent dark-glass **5-column large-icon (52px) app grid** with search bar; fixed `tint2` `~` expansion bug.
- Added one-click GUI Wi-Fi manager (`atherium-wifi` via `zenity` + `nmcli`), GUI Power menu (`atherium-power`), and clickable Desktop app shortcuts (`pcmanfm --desktop` + `/etc/skel/Desktop/*.desktop`).
- Polished `dunst` notifications to `top-center` (no Conky overlap) and fixed GRUB splash footer overlap.
- **Static Verification:** PASS — ISO **691.00 MB** / 700 MB (SquashFS 598.90 MB, 9.00 MB remaining), BIOS + UEFI hybrid + SHA256 verified. *(Real-hardware HUD/Wi-Fi UX: NEEDS HARDWARE TEST)*

## [Phase 9.1] - Real-Hardware Boot Fix (Dell Vostro 3520)
- **Fixed `Authentication failure` on auto-login:** Added `user-setup` (`1.107`) to `01-core.list.chroot` so `live-config` creates the `atherium` user at boot (previously skipped by `--apt-recommends false`).
- **Hardened Xorg + D-Bus desktop launch:** Added `xserver-xorg-legacy`, `dbus-x11`, `/etc/X11/Xwrapper.config`, and `dbus-run-session` in `.xinitrc`.
- **Fixed GRUB/ISOLINUX branding hook:** Updated `0700-brand-bootloaders.hook.binary` to use paths relative to `binary/` (verified `21 KB` Atherium-X splash + `"Atherium-X Live (JARVIS HUD)"` menu entries + cyan theme).
- **Static Verification:** PASS — ISO **685.00 MB** / 700 MB (SquashFS 593.10 MB), BIOS + UEFI hybrid + SHA256 verified. *(Real-hardware login & HUD test: NEEDS HARDWARE TEST)*

## [Phase 9] - Final Optimization & Release Build (Verified Statically)
- Excluded duplicate `boot/initrd.img-*` and `boot/vmlinuz-*` from `filesystem.squashfs` in `auto/build` (live-boot loads `/live/vmlinuz` and `/live/initrd.img` outside squashfs), reclaiming **77.00 MB** with zero feature loss.
- Added final cache/log/backup-db trim in `0990-strip-bloat.hook.chroot`.
- **Final Static Verification:** PASS — ISO **685.00 MB** / 700 MB (SquashFS 592.91 MB, 15.00 MB remaining), BIOS + UEFI hybrid + MBR/GPT + SHA256 verified (`atherium-x.iso: OK`). *(Real-hardware validation on Dell Vostro: NEEDS HARDWARE TEST)*

## [Phase 8] - Apps, Browser, Games & Memory Management (Pre-Optimization Build)
- Added `config/package-lists/08-apps-memory.list.chroot`: `firefox-esr` (Debian repo), `pcmanfm`, `lxterminal`, `mousepad`, `mpv`, `htop`, native tiny games (`ninvaders`, `moon-buggy`, `bastet`, `2048` — < 2 MB total), `systemd-zram-generator`, `earlyoom`.
- Configured zram (`zstd`, `min(ram/2, 4096)`), sysctl (`vm.swappiness=100`, `vm.page-cluster=0`), `earlyoom`, `atherium-games` HUD launcher, `atherium-monitor` desktop entry, `COMPRESS=xz` for `initrd.img`, and documented live-boot `tmpfs`/`overlayfs` RAM behavior in `docs/APPS_AND_MEMORY.md`.
- **Measured Pre-Optimization ISO Size:** **762.00 MB** (SquashFS 670.10 MB) — identified **79 MB** of duplicate `/boot/initrd.img-*` + `/boot/vmlinuz-*` inside SquashFS to eliminate in Phase 9.

## [Phase 7] - Boot Animation & Branding (Verified Statically)
- Added `config/package-lists/07-boot-branding.list.chroot` (`plymouth`, `plymouth-label`) and `splash` boot flag in `auto/config`.
- Built script-based Plymouth `atherium-x` theme (`43.5 KB` total PNG sprites): counter-rotating geometric neon rings, pulsing core, `"ATHERIUM-X // INITIALIZING"`, and sequentially fading-in system-check lines.
- Added binary bootloader branding hook (`0700-brand-bootloaders.hook.binary`) for cyan/obsidian GRUB-EFI + ISOLINUX menus and `640x480` splash image.
- **Static Verification:** PASS — ISO **632.00 MB** / 700 MB (**+25.00 MB**; 68.00 MB remaining; SquashFS 539.83 MB). *(Animation timing & handoff: NEEDS HARDWARE TEST)*

## [Phase 6] - Desktop & JARVIS-Style HUD Interface (Verified Statically)
- Added `config/package-lists/06-desktop.list.chroot` (`xinit`, `openbox`, `picom`, `tint2`, `rofi`, `conky-std`, `dunst`, `libnotify-bin`, `feh`, `fonts-dejavu-core`, `fonts-hack`, `dmz-cursor-theme`).
- Built custom dark-glass & electric-cyan Openbox + GTK3 themes (`Atherium-X`), `picom.conf`, `tint2rc`, `rofi/atherium.rasi`, `conky.conf` telemetry HUD, and `dunstrc`.
- Created original neon line-art SVG icon theme `Atherium-X-Icons` (8 core icons + app icon symlinks), 1920x1080 HUD wallpaper (`168.3 KB` < 1 MB), and startup greeting `"Welcome back. Atherium-X online."`.
- **Static Verification:** PASS — ISO **607.00 MB** / 700 MB (**+37.00 MB**; 93.00 MB remaining; SquashFS 527.11 MB). *(Visual HUD: NEEDS HARDWARE TEST)*

## [Phase 5] - In-Built Store: Snap Store (Verified Statically)
- Added `config/package-lists/05-snap.list.chroot` (`snapd`, `apparmor`, `apparmor-utils`, `squashfs-tools`, `fuse3`), enabled `snapd`/`apparmor` services, and added `apparmor=1 security=apparmor` to `--bootappend-live`.
- Added `/usr/local/bin/atherium-store` + desktop entry for on-demand `snap-store` installation (pre-seeding `snap-store` + `core22` + `gnome-42-2204` + `gtk-common-themes` would add ~730 MB).
- Documented squashfs-on-squashfs, AppArmor, and RAM/tmpfs caveats in `docs/SNAP_STORE.md`.
- **Static Verification:** PASS — ISO **570.00 MB** / 700 MB (**+28.00 MB**; 130.00 MB remaining; SquashFS 490.15 MB). *(Live `snap install`: NEEDS HARDWARE TEST)*

## [Phase 4] - Package Manager: APT / aptitude (Verified Statically)
- Added `config/package-lists/04-apt.list.chroot` (`apt`, `aptitude`, `debian-archive-keyring`, `ca-certificates`, `gnupg`) and chroot verification hook `0400-verify-apt.hook.chroot`.
- Verified `sources.list` (`trixie main contrib non-free-firmware`) while keeping `/var/lib/apt/lists/*` stripped in the ISO.
- **Static Verification:** PASS — ISO **542.00 MB** / 700 MB (**+4.00 MB**; 158.00 MB remaining; SquashFS 462.55 MB). *(Online `apt update/install`: NEEDS HARDWARE TEST)*

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
