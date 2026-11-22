#!/usr/bin/env python3
"""
Generate lightweight PNG sprites for the Atherium-X Plymouth boot animation
and the 640x480 GRUB/ISOLINUX bootloader splash screen.
Original geometric neon cyan design (zero copyrighted assets).
"""

import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE = os.path.dirname(__file__)
THEME_DIR = os.path.join(BASE, "atherium-x")
os.makedirs(THEME_DIR, exist_ok=True)


def save_ring(filename, size_px, draw_fn):
    fig = plt.figure(figsize=(size_px / 100.0, size_px / 100.0), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.axis("off")
    ax.set_facecolor("none")
    draw_fn(ax)
    out = os.path.join(THEME_DIR, filename)
    fig.savefig(out, dpi=100, transparent=True)
    plt.close(fig)
    print(f"Generated {out} ({os.path.getsize(out) / 1024.0:.1f} KB)")


def draw_outer_ring(ax):
    ax.add_patch(patches.Circle((0, 0), 86, fill=False, edgecolor="#00e5ff", linewidth=2.2, alpha=0.45))
    for start, span in [(0, 48), (90, 52), (180, 48), (270, 52)]:
        ax.add_patch(patches.Arc((0, 0), 156, 156, angle=0, theta1=start, theta2=start + span,
                                 edgecolor="#00e5ff", linewidth=6.0, alpha=0.92))
    for deg in range(0, 360, 15):
        r = math.radians(deg)
        ax.plot([86 * math.cos(r), 94 * math.cos(r)], [86 * math.sin(r), 94 * math.sin(r)],
                color="#38bdf8", linewidth=1.8, alpha=0.75)


def draw_inner_ring(ax):
    ax.add_patch(patches.Circle((0, 0), 54, fill=False, edgecolor="#38bdf8", linewidth=2.0, linestyle="--", alpha=0.8))
    for start, span in [(20, 75), (140, 75), (260, 75)]:
        ax.add_patch(patches.Arc((0, 0), 92, 92, angle=0, theta1=start, theta2=start + span,
                                 edgecolor="#00e5ff", linewidth=4.5, alpha=0.95))


def draw_core(ax):
    ax.add_patch(patches.RegularPolygon((0, 0), numVertices=6, radius=26, orientation=math.radians(30),
                                        fill=False, edgecolor="#00e5ff", linewidth=2.8, alpha=0.95))
    ax.add_patch(patches.Circle((0, 0), 11, facecolor="#00e5ff", edgecolor="#e0f2fe", linewidth=1.8, alpha=0.9))


def generate_boot_splash():
    fig = plt.figure(figsize=(6.4, 4.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 640)
    ax.set_ylim(0, 480)
    ax.axis("off")
    fig.patch.set_facecolor("#050914")
    ax.set_facecolor("#050914")

    # Subtle grid
    for gx in range(32, 640, 32):
        ax.plot([gx, gx], [0, 480], color="#00e5ff", alpha=0.05, linewidth=0.6)
    for gy in range(32, 480, 32):
        ax.plot([0, 640], [gy, gy], color="#00e5ff", alpha=0.05, linewidth=0.6)

    # Top-right geometric rings
    cx, cy = 530, 380
    ax.add_patch(patches.Circle((cx, cy), 58, fill=False, edgecolor="#00e5ff", linewidth=2.0, alpha=0.45))
    ax.add_patch(patches.Circle((cx, cy), 38, fill=False, edgecolor="#38bdf8", linewidth=1.5, linestyle="--", alpha=0.6))
    ax.add_patch(patches.RegularPolygon((cx, cy), numVertices=6, radius=18, orientation=math.radians(30),
                                        fill=False, edgecolor="#00e5ff", linewidth=2.0, alpha=0.8))

    # Header bar (keep bottom clear so GRUB timeout bar never overlaps)
    ax.plot([24, 616], [428, 428], color="#00e5ff", linewidth=1.5, alpha=0.7)
    ax.text(28, 444, "ATHERIUM-X // LIVE BOOTLOADER", color="#00e5ff", fontsize=13,
            fontfamily="monospace", fontweight="bold")
    ax.text(28, 412, "DEBIAN STABLE HYBRID BIOS+UEFI  |  JARVIS HUD EDITION", color="#38bdf8",
            fontsize=8.5, fontfamily="monospace", alpha=0.7)

    out = os.path.join(BASE, "splash_640x480.png")
    fig.savefig(out, dpi=100, facecolor="#050914")
    plt.close(fig)
    print(f"Generated {out} ({os.path.getsize(out) / 1024.0:.1f} KB)")


save_ring("outer_ring.png", 260, draw_outer_ring)
save_ring("inner_ring.png", 260, draw_inner_ring)
save_ring("core.png", 260, draw_core)
generate_boot_splash()
