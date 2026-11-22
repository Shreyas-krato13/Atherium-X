# Atherium-X Apps, Browser, Games & Live-OS Memory Architecture (Phase 8)

## Browser Selection (`firefox-esr` from Debian Repo)
- **Choice:** `firefox-esr` (Debian stable package, **not** Snap).
- **Justification:** Full modern web standards, hardware-accelerated video/WebGL via Mesa, zero Snap runtime overhead (~700 MB saved vs. Snap), and full compatibility with YouTube, GitHub, Google Docs, and web apps. Lighter alternatives (`epiphany-browser`/`netsurf`) either lack extension/media parity or still pull in WebKitGTK (~45 MB).

## Basic Apps & Native Games
- **File Manager:** `pcmanfm`
- **Terminal:** `lxterminal`
- **Text Editor:** `mousepad`
- **Image Viewer:** `feh` (CLI/desktop image viewer)
- **Media Player:** `mpv`
- **System Monitor:** `htop` (`Atherium System Monitor` desktop entry + Conky HUD telemetry widget)
- **Games (< 2 MB total, well under the 30 MB budget):** `ninvaders`, `moon-buggy`, `bastet`, `2048`, accessible via the **Atherium Games** HUD launcher (`atherium-games`).

---

## How `live-boot` Uses `tmpfs` + `overlayfs` and How It Affects RAM

When Atherium-X boots from USB:
1. `/live/filesystem.squashfs` is mounted **read-only** as the lower layer (`lowerdir`).
2. `live-boot` creates an in-RAM **`tmpfs`** filesystem (by default up to 50% of physical RAM) as the writable upper layer (`upperdir`).
3. **`overlayfs`** merges both into `/` so every write (browser cache, `apt install`, `snap install`, downloaded files) goes into RAM without touching the USB stick or internal SSD.
4. **RAM Impact:** Because both running applications **and** newly written files share physical RAM, a live OS can run out of memory faster than an installed OS (especially during `firefox-esr` multi-tab browsing or `snap install snap-store`).

### Memory Protections Enabled in Atherium-X
- **`systemd-zram-generator` (`/etc/systemd/zram-generator.conf`):** Automatically creates a `zstd`-compressed in-RAM swap device (`min(ram/2, 4096)` MB) at priority 100. Cold memory pages compress ~2.5x–3.5x in RAM, effectively expanding usable memory on 4–8 GB laptops without needing a disk swap partition.
- **Sysctl tuning (`/etc/sysctl.d/99-atherium-memory.conf`):** `vm.swappiness=100`, `vm.page-cluster=0`, `vm.vfs_cache_pressure=50` — tuned specifically for zero-seek zram swap.
- **`earlyoom` (`/etc/default/earlyoom`):** Monitors free RAM (< 5%) and free zram swap (< 10%) and gracefully terminates runaway tabs/processes *before* the kernel OOM-killer freezes the desktop, while explicitly protecting `systemd`, `Xorg`, `openbox`, `picom`, and `tint2`.
- **Memory HUD Widget:** Conky's right-side HUD panel continuously displays live `RAM` and `ZRAM` usage bars.
