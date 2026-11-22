#!/usr/bin/env python3
"""
Generate a clean, presentation-ready 1-page A4 PDF submission document for Atherium-X:
- GitHub Source Code URL
- Hugging Face ISO Binary URL
- Brief, technically accurate steps: How Source Code Becomes a Bootable ISO Binary
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages

OUT_PDF = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "Atherium-X_Submission.pdf")

fig = plt.figure(figsize=(8.27, 11.69), dpi=200)  # A4 portrait
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 141.4)
ax.axis("off")
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

# Top Header Banner (Dark Obsidian + Electric Cyan accent)
ax.add_patch(patches.Rectangle((0, 123.5), 100, 17.9, facecolor="#070d1a", edgecolor="none"))
ax.add_patch(patches.Rectangle((0, 123.0), 100, 0.7, facecolor="#00c8e8", edgecolor="none"))

ax.text(5.5, 134.8, "ATHERIUM-X  //  CUSTOM LINUX LIVE OS", color="#00e5ff",
        fontsize=17, fontweight="bold", fontfamily="DejaVu Sans")
ax.text(5.5, 129.8, "Debian 13 (Trixie) Hybrid BIOS + UEFI Live-USB Operating System  |  JARVIS-Style HUD",
        color="#e2e8f0", fontsize=9.2, fontfamily="DejaVu Sans")
ax.text(5.5, 125.8, "Final Verified ISO: 651.00 MB (XZ SquashFS)   |   Hardware Verified: Dell Vostro 3520",
        color="#7dd3fc", fontsize=8.3, fontfamily="DejaVu Sans Mono")

# Section 1: Project Repositories & Download Links
ax.text(5.5, 118.2, "1. PROJECT REPOSITORIES & LINKS", color="#070d1a",
        fontsize=11.5, fontweight="bold", fontfamily="DejaVu Sans")
ax.add_patch(patches.FancyBboxPatch((5.5, 100.8), 89.0, 15.5,
                                    boxstyle="round,pad=0.6,rounding_size=1.2",
                                    facecolor="#f0f9ff", edgecolor="#0284c7", linewidth=1.2))

ax.text(7.5, 113.4, "GitHub Source Code Repository:", color="#0369a1",
        fontsize=9.2, fontweight="bold", fontfamily="DejaVu Sans")
ax.text(7.5, 110.2, "https://github.com/Shreyas-krato13/Atherium-X", color="#0f172a",
        fontsize=9.2, fontfamily="DejaVu Sans Mono")

ax.text(7.5, 106.2, "Hugging Face Bootable ISO Repository (651.00 MB):", color="#0369a1",
        fontsize=9.2, fontweight="bold", fontfamily="DejaVu Sans")
ax.text(7.5, 103.0, "https://huggingface.co/datasets/warrior-kratos13/Atherium-X-ISO/tree/main", color="#0f172a",
        fontsize=8.6, fontfamily="DejaVu Sans Mono")

# Section 2: Visual Build Pipeline Strip
ax.text(5.5, 95.8, "2. HOW SOURCE CODE BECOMES A BOOTABLE ISO BINARY", color="#070d1a",
        fontsize=11.5, fontweight="bold", fontfamily="DejaVu Sans")

flow_boxes = [
    ("1. Source", "live-build\nconfigs"),
    ("2. Bootstrap", "debootstrap\nrootfs"),
    ("3. Chroot", "APT + HUD\n+ hooks"),
    ("4. Compress", "mksquashfs\n(xz)"),
    ("5. Boot Files", "vmlinuz +\ninitrd + GRUB"),
    ("6. Hybrid ISO", "xorriso\nBIOS + UEFI"),
]
bx = 5.5
bw = 13.6
gap = 1.48
for i, (title, sub) in enumerate(flow_boxes):
    x0 = bx + i * (bw + gap)
    ax.add_patch(patches.FancyBboxPatch((x0, 84.5), bw, 9.0,
                                        boxstyle="round,pad=0.3,rounding_size=0.9",
                                        facecolor="#0f172a", edgecolor="#00b8d4", linewidth=1.0))
    ax.text(x0 + bw / 2, 91.0, title, color="#00e5ff", fontsize=7.6,
            fontweight="bold", ha="center", va="center", fontfamily="DejaVu Sans")
    ax.text(x0 + bw / 2, 87.0, sub, color="#e2e8f0", fontsize=6.8,
            ha="center", va="center", fontfamily="DejaVu Sans")
    if i < len(flow_boxes) - 1:
        ax.annotate("", xy=(x0 + bw + gap - 0.15, 89.0), xytext=(x0 + bw + 0.15, 89.0),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.4))

# Section 2 Details: Concise 7-Step Breakdown
steps = [
    ("Step 1 — Source Layer (Git Repository)",
     "All OS definitions live as plain-text files: auto/config (Debian 13 trixie, amd64, hybrid BIOS+UEFI, xz compression), "
     "declarative package lists (config/package-lists/), rootfs overlays (config/includes.chroot/ for HUD, Wi-Fi, zram, scripts), "
     "chroot/binary hooks, custom SVG icons, and Plymouth animation sprites."),
    ("Step 2 — Bootstrap (debootstrap)",
     "live-build runs debootstrap to download and unpack a minimal Debian base root filesystem into an isolated chroot/ directory."),
    ("Step 3 — Customization (Chroot Stage)",
     "Inside chroot/, APT installs all phased packages with --no-install-recommends (stock kernel, Dell Vostro firmware, Mesa 3D, "
     "NetworkManager, snapd, Openbox/LXPanel/Rofi HUD, Plymouth, Firefox ESR, games, zram). Hooks configure services, rebuild initrd, "
     "and strip docs, manpages, non-English locales, and APT caches."),
    ("Step 4 — SquashFS Compression (mksquashfs)",
     "The entire customized chroot/ (~1.4 GB uncompressed) is compressed with XZ + x86 BCJ filter (-comp xz -b 1M -Xbcj x86) into "
     "a single read-only filesystem image: /live/filesystem.squashfs (558.34 MB), excluding duplicate /boot kernel/initrd files."),
    ("Step 5 — Boot Components Extraction",
     "The stock Linux kernel (/live/vmlinuz), initial RAM disk (/live/initrd.img with live-boot + Plymouth splash), ISOLINUX (Legacy BIOS), "
     "and GRUB-EFI (bootx64.efi inside an embedded FAT EFI image efi.img) are staged outside SquashFS."),
    ("Step 6 — Hybrid ISO9660 Assembly (xorriso)",
     "xorriso packages /live/* and both bootloaders into atherium-x.iso (651.00 MB) with El Torito BIOS + UEFI boot catalogs and an "
     "isohybrid MBR + GPT partition header in the first 32 KB, then generates atherium-x.iso.sha256."),
    ("Step 7 — USB Flash & Hardware Boot Flow",
     "Written raw sector-by-sector via Rufus (DD Image mode) or dd. At power-on: UEFI/BIOS -> GRUB/ISOLINUX -> vmlinuz + initrd -> "
     "live-boot mounts filesystem.squashfs (read-only) + RAM tmpfs (read-write) via overlayfs -> systemd -> Plymouth -> JARVIS HUD."),
]

y = 81.2
for heading, body in steps:
    ax.text(5.8, y, heading, color="#0369a1", fontsize=8.6, fontweight="bold", fontfamily="DejaVu Sans")
    y -= 2.05
    # Wrap body cleanly to ~108 chars per line
    words = body.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= 108:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        ax.text(6.8, y, ln, color="#1e293b", fontsize=7.6, fontfamily="DejaVu Sans")
        y -= 2.0
    y -= 0.95

# Section 3: Compact Source vs Binary Summary Box at bottom
ax.add_patch(patches.FancyBboxPatch((5.5, 4.2), 89.0, 11.4,
                                    boxstyle="round,pad=0.5,rounding_size=1.0",
                                    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0))
ax.text(7.5, 13.4, "SOURCE vs. BINARY SUMMARY", color="#070d1a", fontsize=8.6, fontweight="bold", fontfamily="DejaVu Sans")
ax.text(7.5, 10.6, "• Source (GitHub): ~2 MB of human-readable live-build configs, hooks, shell scripts, and SVG/PNG assets.",
        color="#334155", fontsize=7.6, fontfamily="DejaVu Sans")
ax.text(7.5, 8.1, "• Binary (Hugging Face): 651.00 MB immutable hybrid ISO9660 image (BIOS + UEFI bootable, XZ SquashFS).",
        color="#334155", fontsize=7.6, fontfamily="DejaVu Sans")
ax.text(7.5, 5.5, "• SHA256: e7d15856716df13957ec61e8ff0f6fb44b8a113d112fab51f63ac2c37f85fe33",
        color="#0369a1", fontsize=7.3, fontfamily="DejaVu Sans Mono")

os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
with PdfPages(OUT_PDF) as pdf:
    pdf.savefig(fig, dpi=200)
plt.close(fig)
print(f"Generated {OUT_PDF} ({os.path.getsize(OUT_PDF) / 1024.0:.1f} KB)")
