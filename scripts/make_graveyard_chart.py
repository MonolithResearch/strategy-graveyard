"""
make_graveyard_chart.py
=======================
Regenerates the branded "strategy graveyard" chart from the public, sanitized
gate ranking. One horizontal bar per strategy = the honest blind out-of-sample
Deflated Sharpe (DSR) it faces, drawn against the firm's promotion gate at 0.50.

Zero strategies clear the gate. The two longest bars (Gold timing 0.686, Core
legacy 0.668) are NOT alpha — they are gold buy-and-hold beta in a 2023-26 bull,
which is exactly the failure mode the gate exists to reject.

Brand: Monolith Research. Palette Ink #0E0C14 / Plum #A78AA3 / Paper #F3EFE8.
Run:  py -3.14 scripts/make_graveyard_chart.py
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --- Monolith palette --------------------------------------------------------
INK = "#0E0C14"      # near-black
PLUM = "#A78AA3"     # accent
PAPER = "#F3EFE8"    # light
GATE_C = "#C24B4B"   # gate line / fail red

# Tier colours (kept muted and on-brand)
TIER_C = {
    0: "#2E7D5B",  # PASS (none clear it)
    1: "#8C7BB0",  # beta mirage
    2: "#C9A23A",  # real but undeployable (funding-grade)
    3: "#9A6B5A",  # overfit / sign-flip noise
    4: "#5A5560",  # structurally dead
}
TIER_LABEL = {
    1: "Beta mirage (high DSR = market beta, no alpha)",
    2: "Real signal, undeployable (funding-grade)",
    3: "Overfit / sign-flips out-of-sample (noise)",
    4: "Structurally dead (multi-confirmed)",
}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_IN = os.path.join(ROOT, "data", "gate_ranking_public.csv")
OUT_DIR = os.path.join(ROOT, "charts")
GATE = 0.50

# Cormorant if installed, else a clean serif fallback. Mono for the axes labels.
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = [
    "Cormorant Garamond", "Cormorant", "Garamond", "Georgia", "DejaVu Serif",
]


def load_rows():
    rows = []
    with open(CSV_IN, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            dsr = r["blind_OOS_DSR"].strip()
            if dsr == "":
                continue  # rows with no gate-applicable DSR are off-chart
            rows.append({
                "name": r["name"],
                "tier": int(r["tier"]),
                "dsr": float(dsr),
            })
    # smallest at the bottom -> largest at the top (descending visually)
    rows.sort(key=lambda x: x["dsr"])
    return rows


def main():
    rows = load_rows()
    names = [r["name"] for r in rows]
    dsrs = [r["dsr"] for r in rows]
    colors = [TIER_C[r["tier"]] for r in rows]

    fig, ax = plt.subplots(figsize=(11, 12))
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)

    y = range(len(rows))
    ax.barh(list(y), dsrs, color=colors, edgecolor=INK, linewidth=0.6, height=0.72)

    # gate line
    ax.axvline(GATE, color=GATE_C, linewidth=2.0, linestyle="-", zorder=5)
    ax.text(
        GATE + 0.02, len(rows) * 0.32,
        "PROMOTION GATE  ·  DSR ≥ 0.50", color=GATE_C, fontsize=10.5,
        fontweight="bold", fontfamily="DejaVu Sans", rotation=90,
        va="center", ha="center", zorder=6,
        bbox=dict(facecolor=PAPER, edgecolor="none", pad=2.0, alpha=0.85),
    )

    # value labels at the end of each bar
    for i, v in enumerate(dsrs):
        ax.text(
            max(v, 0) + 0.004, i, f"{v:.3f}",
            va="center", ha="left", fontsize=8.5, color=INK,
        )

    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=9.5, color=INK)
    ax.set_xlim(0, max(GATE + 0.10, max(dsrs) + 0.10))
    ax.set_xlabel("Honest blind out-of-sample Deflated Sharpe (DSR)",
                  fontsize=12, color=INK)

    # Sigma + title block
    fig.text(0.063, 0.962, "Σ", fontsize=34, color=PLUM, style="italic",
             ha="center", va="center")
    fig.text(0.105, 0.972, "M O N O L I T H   R E S E A R C H", fontsize=12,
             color=INK, fontweight="bold", va="center")
    fig.text(0.105, 0.951, "Evidence over narrative", fontsize=10, color="#7A6177",
             style="italic", va="center")
    fig.text(0.063, 0.918,
             "The Strategy Graveyard — 34 ideas graded on honest out-of-sample evidence",
             fontsize=15, color=INK, fontweight="bold", va="center")
    fig.text(0.063, 0.898,
             "Ranked by the most honest gate-applicable DSR a deployable version "
             "faces. The two longest bars are gold beta, not skill.",
             fontsize=9.5, color="#4A4652", va="center")

    # legend by tier (only tiers present)
    present = []
    seen = set()
    for r in rows:
        if r["tier"] not in seen:
            seen.add(r["tier"])
            present.append(r["tier"])
    handles = [Patch(facecolor=TIER_C[t], edgecolor=INK, label=TIER_LABEL[t])
               for t in sorted(present)]
    handles.append(Patch(facecolor="none", edgecolor=GATE_C, label="Promotion gate (DSR ≥ 0.50)"))
    ax.legend(handles=handles, loc="lower right", fontsize=8.5, frameon=True,
              facecolor=PAPER, edgecolor=INK)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(INK)
    ax.tick_params(colors=INK)
    ax.grid(axis="x", color=INK, alpha=0.08, linewidth=0.6)

    plt.subplots_adjust(left=0.30, right=0.965, top=0.875, bottom=0.055)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_png = os.path.join(OUT_DIR, "dsr_graveyard.png")
    fig.savefig(out_png, dpi=150, facecolor=PAPER)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
