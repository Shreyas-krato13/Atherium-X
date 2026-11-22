# Flashing Atherium-X to a USB Drive & Booting on Dell Vostro

## Option 1: Linux / WSL2 (Guarded Script)

Use the included guarded script `tools/flash_usb.sh`. It refuses to touch mounted disks, system disks, or non-removable drives, verifies the ISO SHA256 before writing, writes with `dd`, and reads back the USB drive to confirm the checksum.

```bash
sudo bash tools/flash_usb.sh atherium-x.iso
```

*(Note: Never run this without double-checking the target `/dev/sdX` device shown by `lsblk`.)*

---

## Option 2: Windows (Recommended on a Windows Host)

### Method A: Rufus (DD Image Mode)
1. Download and open **Rufus** (https://rufus.ie).
2. Under **Device**, select your USB flash drive (all data on it will be erased).
3. Click **SELECT** and choose `atherium-x.iso`.
4. Verify the SHA256 checksum matches `atherium-x.iso.sha256` (in PowerShell: `Get-FileHash atherium-x.iso -Algorithm SHA256`).
5. Click **START**. When Rufus prompts **"ISOHybrid image detected"**, choose **"Write in DD Image mode"** (recommended for exact hybrid BIOS+UEFI compatibility).
6. Wait for **READY**, then safely eject the USB drive.

### Method B: balenaEtcher
1. Open **balenaEtcher** (https://etcher.balena.io).
2. Click **Flash from file** -> select `atherium-x.iso`.
3. Click **Select target** -> choose your USB drive.
4. Click **Flash!** — Etcher writes in raw DD mode and automatically verifies the write.

---

## Booting on Dell Vostro (BIOS / UEFI & Secure Boot)

1. Insert the Atherium-X USB drive and power on (or restart) your Dell Vostro.
2. **One-time Boot Menu:** Tap **`F12`** repeatedly at the Dell logo to open the Boot Menu, then select your USB drive (under **UEFI Boot** preferred, or **Legacy Boot** if BIOS mode is enabled).
3. **BIOS Setup & Secure Boot (if needed):**
   - Tap **`F2`** at the Dell logo to enter **BIOS/UEFI Setup**.
   - **Secure Boot status:** Atherium-X is configured with `--uefi-secure-boot auto` (signed `shim-signed` + `grub-efi-amd64-signed` when present in the build). If your Dell Vostro reports a Secure Boot violation or refuses to load the unsigned kernel/initrd, go to **Boot Configuration -> Secure Boot** and set **Secure Boot** to **Disabled**, then save and reboot.
   - *(Optional)* To make USB boot first permanently, adjust **Boot Sequence** under **Boot Configuration**.
4. **Recording Boot Time (for your presentation):**
   - Start a stopwatch the instant you press **Enter** on the Atherium-X boot menu.
   - Stop the stopwatch when the CLI prompt (Phase 1–5) or JARVIS HUD desktop (Phase 6–9) is usable.
   - Run `bootlog.sh` in the live terminal to capture `systemd-analyze` and `systemd-analyze blame` numbers, and record them in `docs/boot_times.csv`.
