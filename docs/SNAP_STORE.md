# Atherium-X Snap Store Architecture & Live-Session Caveats (Phase 5)

## Pre-Seeding vs. On-Demand Size Analysis

Pre-seeding `snap-store` inside a live ISO requires bundling the snap itself **plus** all mandatory base and desktop content snaps (each already squashfs-compressed, so `mksquashfs -comp xz` cannot shrink them further):

| Snap Package | Typical Compressed Size |
|---|---:|
| `snapd` (snap) | ~40 MB |
| `core22` | ~75 MB |
| `gnome-42-2204` | ~505 MB |
| `gtk-common-themes` | ~95 MB |
| `snap-store` | ~15 MB |
| **Total Pre-Seeded Overhead** | **~730 MB** |

Adding ~730 MB on top of the 542 MB Phase 4 ISO would produce a **~1,270 MB ISO**, violating both the original 500 MB limit and the raised 700 MB cap.

**Implemented Solution:**
- Ship **`snapd`** + **`apparmor`** + **`squashfs-tools`** + **`fuse3`** inside the ISO (~20 MB compressed).
- Ship the **Atherium Store** launcher (`/usr/local/bin/atherium-store` + desktop entry) which checks connectivity, waits for `snapd` seeding, installs `snap-store` on first online use, and launches it automatically.

---

## Live-Session Technical Caveats (SquashFS-on-SquashFS, AppArmor, RAM)

1. **SquashFS-on-SquashFS via OverlayFS:**
   - `live-boot` mounts `/live/filesystem.squashfs` read-only and merges a writable `tmpfs` upper layer via `overlayfs`.
   - When `snap install` runs, `snapd` downloads `.snap` squashfs archives into `/var/lib/snapd/snaps/` (on the writable `tmpfs`) and loop-mounts them under `/snap/<name>/<rev>`.
   - Debian's stock kernel includes `loop`, `squashfs`, and `overlay` modules, so nested squashfs mounts work cleanly as long as `/var/lib/snapd` is writable.
2. **AppArmor & Seccomp Confinement:**
   - `snap-confine` expects AppArmor to be enabled in the kernel.
   - `auto/config` passes `apparmor=1 security=apparmor` in `--bootappend-live`, and `apparmor.service` is enabled in `0500-snapd.hook.chroot`.
3. **RAM Usage in Live Session:**
   - Because `/var/lib/snapd` lives in `tmpfs` (RAM), installing `snap-store` + `gnome-42-2204` consumes ~750 MB of RAM/zram.
   - Phase 8 enables **zram** compressed swap and **earlyoom** to keep live sessions with 4–8 GB RAM responsive even when installing Snaps.

## Hardware Verification (`NEEDS HARDWARE TEST`)
1. Connect to WiFi/Ethernet (`nettest.sh`).
2. Run `snap version` and `snap find hello-world`.
3. Test `sudo snap install hello-world && hello-world`.
4. Launch **Atherium Store** from the HUD launcher or run `atherium-store`.
