#!/usr/bin/env python3
"""
Generate a plain, clean academic black-and-white A4 PDF for Atherium-X submission:
- GitHub Source Code URL
- Hugging Face ISO URL
- Brief steps explaining how source code is converted into a bootable ISO binary
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

OUT_PDF = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "Atherium-X_Submission.pdf")

fig = plt.figure(figsize=(8.27, 11.69), dpi=200)  # A4 portrait
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 141.4)
ax.axis("off")
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

# Plain academic title
ax.text(9.0, 130.0, "Atherium-X — Custom Linux Live Operating System",
        color="#000000", fontsize=15, fontweight="bold", fontfamily="DejaVu Serif")
ax.plot([9.0, 91.0], [127.8, 127.8], color="#000000", linewidth=0.9)

# Section 1: Links
y = 122.0
ax.text(9.0, y, "1. Project Links", color="#000000", fontsize=11.5, fontweight="bold", fontfamily="DejaVu Serif")
y -= 4.2
ax.text(9.0, y, "GitHub Repository (Source Code):", color="#000000", fontsize=10, fontweight="bold", fontfamily="DejaVu Serif")
y -= 3.0
ax.text(9.0, y, "https://github.com/Shreyas-krato13/Atherium-X", color="#000000", fontsize=9.8, fontfamily="DejaVu Sans Mono")

y -= 4.8
ax.text(9.0, y, "Hugging Face Repository (Bootable ISO — 651.00 MB):", color="#000000", fontsize=10, fontweight="bold", fontfamily="DejaVu Serif")
y -= 3.0
ax.text(9.0, y, "https://huggingface.co/datasets/warrior-kratos13/Atherium-X-ISO/tree/main", color="#000000", fontsize=9.2, fontfamily="DejaVu Sans Mono")

# Section 2: Brief Steps
y -= 7.5
ax.text(9.0, y, "2. Steps to Convert Source Code into a Bootable ISO",
        color="#000000", fontsize=11.5, fontweight="bold", fontfamily="DejaVu Serif")
y -= 4.2

steps = [
    ("Step 1: Source Configuration (live-build)",
     "All OS definitions are written as plain-text files in the Git repository: auto/config (Debian 13 trixie, amd64, hybrid BIOS+UEFI, xz compression), package lists (config/package-lists/), configuration overlays (config/includes.chroot/), build hooks, icons, and boot splash assets."),
    ("Step 2: Base System Bootstrap (debootstrap)",
     "live-build runs debootstrap to download and unpack a minimal Debian stable root filesystem into an isolated chroot/ working directory."),
    ("Step 3: Chroot Customization",
     "Inside chroot/, APT installs all required packages with --no-install-recommends (Debian stock kernel, laptop firmware, Mesa 3D, NetworkManager, APT/aptitude, snapd, desktop HUD, Plymouth, Firefox ESR, games, zram). Custom hooks enable services, rebuild initramfs, and strip documentation, manpages, non-English locales, and APT caches."),
    ("Step 4: Filesystem Compression (mksquashfs)",
     "The customized chroot/ (~1.4 GB uncompressed) is compressed using XZ compression (-comp xz -b 1M -Xbcj x86) into a single read-only image: /live/filesystem.squashfs (558.34 MB), excluding duplicate kernel/initrd files from /boot."),
    ("Step 5: Bootloader and Kernel Staging",
     "The stock Linux kernel (/live/vmlinuz), initial RAM disk (/live/initrd.img containing live-boot and Plymouth), ISOLINUX (for Legacy BIOS), and GRUB-EFI (with an embedded FAT EFI image efi.img for UEFI) are placed outside the SquashFS image."),
    ("Step 6: Hybrid ISO9660 Creation (xorriso)",
     "xorriso combines /live/* and both bootloaders into atherium-x.iso (651.00 MB) with El Torito BIOS and UEFI boot records plus an isohybrid MBR/GPT partition table in the first 32 KB. A SHA256 checksum file is generated to verify integrity."),
    ("Step 7: Flashing to USB and Booting",
     "The ISO is written raw sector-by-sector to a USB drive using Rufus (DD Image mode) or dd. At startup, the PC firmware loads GRUB/ISOLINUX -> kernel + initrd -> live-boot mounts filesystem.squashfs (read-only) with a RAM tmpfs layer (read-write) via overlayfs -> systemd -> Plymouth -> Desktop."),
]

for title, body in steps:
    ax.text(9.0, y, title, color="#000000", fontsize=10, fontweight="bold", fontfamily="DejaVu Serif")
    y -= 2.8
    words = body.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= 92:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        ax.text(11.0, y, ln, color="#111111", fontsize=8.8, fontfamily="DejaVu Serif")
        y -= 2.35
    y -= 1.35

# Footer SHA256
ax.plot([9.0, 91.0], [8.5, 8.5], color="#666666", linewidth=0.5)
ax.text(9.0, 5.8, "ISO SHA256: e7d15856716df13957ec61e8ff0f6fb44b8a113d112fab51f63ac2c37f85fe33",
        color="#333333", fontsize=7.6, fontfamily="DejaVu Sans Mono")

os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
with PdfPages(OUT_PDF) as pdf:
    pdf.savefig(fig, dpi=200)
plt.close(fig)
print(f"Generated plain PDF: {OUT_PDF} ({os.path.getsize(OUT_PDF) / 1024.0:.1f} KB)")
