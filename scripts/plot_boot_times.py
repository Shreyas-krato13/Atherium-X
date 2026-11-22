#!/usr/bin/env python3
"""
Generate a boot time vs. phase/components chart from docs/boot_times.csv.
Skips placeholder rows that have not yet been measured on real hardware.
"""

import csv
import os
import re
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "docs/boot_times.csv"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "docs/boot_times.png"


def parse_seconds(val: str):
    if not val or "NEEDS" in val.upper() or "ENTER" in val.upper() or val.strip() in ("", "N/A"):
        return None
    val = val.strip()
    m_min = re.match(r"^(\d+(?:\.\d+)?)min\s*(\d+(?:\.\d+)?)s$", val)
    if m_min:
        return float(m_min.group(1)) * 60.0 + float(m_min.group(2))
    m_ms = re.match(r"^(\d+(?:\.\d+)?)ms$", val)
    if m_ms:
        return float(m_ms.group(1)) / 1000.0
    m_s = re.match(r"^(\d+(?:\.\d+)?)s?$", val)
    if m_s:
        return float(m_s.group(1))
    return None


def main():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: {CSV_PATH} not found.")
        sys.exit(1)

    phases = []
    systemd_totals = []
    stopwatch_totals = []
    iso_sizes = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sys_t = parse_seconds(row.get("systemd_total", ""))
            sw_t = parse_seconds(row.get("stopwatch_total_sec", ""))
            iso_mb = parse_seconds(row.get("iso_size_mb", ""))
            if sys_t is not None or sw_t is not None:
                label = f"{row['phase']}\n({row['components_added'][:22]})"
                phases.append(label)
                systemd_totals.append(sys_t if sys_t is not None else 0.0)
                stopwatch_totals.append(sw_t if sw_t is not None else 0.0)
                iso_sizes.append(iso_mb if iso_mb is not None else 0.0)

    if not phases:
        print("INFO: No real-hardware boot measurements in docs/boot_times.csv yet.")
        print("      Populate measured values from your Dell Vostro laptop, then run `make chart`.")
        sys.exit(0)

    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor("#0b0f19")
    ax1.set_facecolor("#111827")

    x = range(len(phases))
    ax1.plot(x, systemd_totals, marker="o", color="#00e5ff", linewidth=2.2, label="systemd-analyze total (s)")
    if any(stopwatch_totals):
        ax1.plot(x, stopwatch_totals, marker="s", color="#38bdf8", linestyle="--", linewidth=2.0, label="Stopwatch total (s)")

    ax1.set_ylabel("Boot Time (seconds)", color="#e2e8f0", fontsize=11)
    ax1.set_title("Atherium-X — Boot Time vs. Components Added (Real Hardware)", color="#00e5ff", fontsize=13, pad=14)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(phases, rotation=20, ha="right", color="#cbd5e1", fontsize=8.5)
    ax1.tick_params(axis="y", colors="#cbd5e1")
    ax1.grid(True, color="#1e293b", linestyle=":", linewidth=0.8)

    if any(iso_sizes):
        ax2 = ax1.twinx()
        ax2.bar(x, iso_sizes, alpha=0.22, color="#22d3ee", width=0.45, label="ISO Size (MB)")
        ax2.set_ylabel("ISO Size (MB)", color="#67e8f9", fontsize=11)
        ax2.tick_params(axis="y", colors="#67e8f9")
        ax2.set_ylim(0, 750)
        ax2.axhline(700, color="#ef4444", linestyle=":", linewidth=1.2, label="700 MB Budget")

    lines1, labels1 = ax1.get_legend_handles_labels()
    if any(iso_sizes):
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0")
    else:
        ax1.legend(loc="upper left", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0")

    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=160)
    print(f"Chart saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
