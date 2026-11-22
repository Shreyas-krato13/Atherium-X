# Atherium-X Hardware & Firmware Justification (Phase 2)

Target primary hardware: **Dell Vostro** (typically Intel Core + Intel UHD/Iris Xe graphics or AMD Ryzen + Radeon, Intel/Realtek/Qualcomm Atheros WiFi, Realtek Gigabit Ethernet, Intel HDA/SOF audio).

## Included Firmware Packages (Justified)

| Package | Purpose | Justification |
|---|---|---|
| `firmware-iwlwifi` | Intel WiFi (AX200/AX201/AX210/AC9560/etc.) | Primary wireless chipset across Dell Vostro laptops. |
| `firmware-realtek` | Realtek WiFi (RTL8821CE/RTL8852BE), Bluetooth & Ethernet (`r8169`) | Common Ethernet and budget WiFi chipset in Dell Vostro models. |
| `firmware-atheros` | Qualcomm Atheros WiFi/BT (`ath10k`/`ath11k`) | Used in several Dell Vostro / Qualcomm Wireless 1810/1820 configurations. |
| `firmware-brcm80211` | Broadcom WiFi (`brcmfmac`) | Broad laptop compatibility for secondary test machines. |
| `firmware-sof-signed` | Intel Sound Open Firmware (SOF) DSP | Required for internal speakers/microphones on modern (10th+ gen Intel) Dell Vostro laptops. |
| `intel-microcode` | Intel CPU security/stability microcode | Primary CPU vendor for Dell Vostro. |
| `amd64-microcode` | AMD CPU microcode | Supports Dell Vostro AMD Ryzen editions. |

## Pruned Firmware Packages (Excluded to Stay <= 500 MB)

- `firmware-linux` / `firmware-misc-nonfree` (meta-bundles containing hundreds of server/NIC/GPU/DSP blobs)
- `firmware-nvidia-graphics` / `firmware-amd-graphics` (large discrete GPU blobs; `nouveau`/`modesetting`/`amdgpu` KMS cover standard desktop display; can be added selectively if `hwcheck.sh` reports a missing GPU blob on your specific Vostro)
- `firmware-qcom-soc`, `firmware-netronome`, `firmware-cavium`, `firmware-marvell-prestera`, `firmware-ti-connectivity` (enterprise/embedded hardware irrelevant to x86 laptops)

## Verification on Real Hardware
Boot Atherium-X on your Dell Vostro and run:
```bash
hwcheck.sh
```
Check section `[7] dmesg Firmware Failure Summary` — if any specific blob is reported missing, add only that targeted package.
