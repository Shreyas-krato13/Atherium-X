#!/usr/bin/env python3
"""
Generate original futuristic JARVIS-inspired HUD wallpaper for Atherium-X.
1920x1080 dark obsidian + electric-cyan concentric HUD geometry, < 1 MB PNG.
Zero copyrighted logos or imagery.
"""

import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUT_PATH = os.path.join(os.path.dirname(__file__), "atherium-hud.png")

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.axis("off")

# Deep radial dark-obsidian background
y, x = np.mgrid[0:1080:4, 0:1920:4]
cx, cy = 960, 540
dist = np.sqrt(((x - cx) / 960.0) ** 2 + ((y - cy) / 540.0) ** 2)
bg = np.zeros((y.shape[0], y.shape[1], 3))
bg[:, :, 0] = np.clip(0.02 + 0.02 * (1 - dist), 0.01, 0.05)
bg[:, :, 1] = np.clip(0.04 + 0.06 * (1 - dist), 0.02, 0.11)
bg[:, :, 2] = np.clip(0.08 + 0.12 * (1 - dist), 0.04, 0.21)
ax.imshow(bg, extent=[0, 1920, 0, 1080], origin="lower", aspect="auto")

# Subtle HUD coordinate grid
for gx in range(80, 1920, 80):
    ax.plot([gx, gx], [0, 1080], color="#00e5ff", alpha=0.035, linewidth=0.7)
for gy in range(80, 1080, 80):
    ax.plot([0, 1920], [gy, gy], color="#00e5ff", alpha=0.035, linewidth=0.7)

# Concentric geometric HUD rings
ring_specs = [
    (310, 1.2, 0.22, "-"),
    (270, 2.2, 0.38, "--"),
    (220, 1.5, 0.48, "-"),
    (165, 3.0, 0.55, ":"),
    (115, 2.0, 0.72, "-"),
    (68,  1.6, 0.85, "-"),
]
for r, lw, alpha, ls in ring_specs:
    c = patches.Circle((cx, cy), r, fill=False, edgecolor="#00e5ff", linewidth=lw, alpha=alpha, linestyle=ls)
    ax.add_patch(c)

# Segmented arc accents
for start_deg, span_deg, r, lw, col, alpha in [
    (15, 55, 290, 4.5, "#00e5ff", 0.65),
    (130, 70, 290, 4.5, "#38bdf8", 0.55),
    (245, 65, 290, 4.5, "#00e5ff", 0.65),
    (60, 80, 192, 3.2, "#38bdf8", 0.50),
    (200, 95, 192, 3.2, "#00e5ff", 0.55),
]:
    arc = patches.Arc((cx, cy), r * 2, r * 2, angle=0, theta1=start_deg, theta2=start_deg + span_deg,
                      edgecolor=col, linewidth=lw, alpha=alpha)
    ax.add_patch(arc)

# Radial degree ticks
for deg in range(0, 360, 6):
    rad = math.radians(deg)
    r1 = 232 if deg % 30 == 0 else 240
    r2 = 252
    ax.plot([cx + r1 * math.cos(rad), cx + r2 * math.cos(rad)],
            [cy + r1 * math.sin(rad), cy + r2 * math.sin(rad)],
            color="#00e5ff", alpha=0.55 if deg % 30 == 0 else 0.22,
            linewidth=1.6 if deg % 30 == 0 else 0.8)

# Core geometric emblem
ax.add_patch(patches.RegularPolygon((cx, cy), numVertices=6, radius=42, orientation=math.radians(30),
                                    fill=False, edgecolor="#00e5ff", linewidth=2.4, alpha=0.9))
ax.add_patch(patches.Circle((cx, cy), 12, facecolor="#00e5ff", edgecolor="#e0f2fe", linewidth=1.5, alpha=0.85))

# Corner HUD brackets
b = 45
for bx, by, dx, dy in [(50, 50, 1, 1), (1870, 50, -1, 1), (50, 1030, 1, -1), (1870, 1030, -1, -1)]:
    ax.plot([bx, bx + dx * b], [by, by], color="#00e5ff", alpha=0.55, linewidth=2)
    ax.plot([bx, bx], [by, by + dy * b], color="#00e5ff", alpha=0.55, linewidth=2)

# Clean typography
ax.text(cx, cy - 365, "A T H E R I U M - X", color="#e0f2fe", fontsize=22,
        fontfamily="monospace", fontweight="bold", ha="center", va="center", alpha=0.88)
ax.text(cx, cy - 402, "NEURAL HUD INTERFACE // DEBIAN LIVE CORE", color="#38bdf8", fontsize=11,
        fontfamily="monospace", ha="center", va="center", alpha=0.65)
ax.text(72, 72, "SYS.CORE :: ONLINE  |  ARCH :: X86_64  |  HUD :: ACTIVE",
        color="#38bdf8", fontsize=9.5, fontfamily="monospace", ha="left", va="center", alpha=0.55)

fig.savefig(OUT_PATH, dpi=100, facecolor="#050914")
plt.close(fig)
size_kb = os.path.getsize(OUT_PATH) / 1024.0
print(f"Generated {OUT_PATH} ({size_kb:.1f} KB)")
