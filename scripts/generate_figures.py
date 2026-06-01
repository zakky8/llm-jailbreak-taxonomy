"""
Figure generation for Phase 2b simulation results.
Run from repo root: python scripts/generate_figures.py
Outputs publication-ready PNGs to figures/v4/

Color palette: orange accent (#f97316) consistent with web-optimization sibling repo.
Style: clean technical (no chart junk, no gradients, no 3D).
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "figures" / "v4"
OUT.mkdir(parents=True, exist_ok=True)

# Palette
ACC      = "#f97316"
ACC_DARK = "#c2410c"
TEXT     = "#1f2937"
TEXT2    = "#6b7280"
BG       = "#fafafa"
GRID     = "#e5e7eb"
RED      = "#dc2626"
GREEN    = "#16a34a"
YELLOW   = "#ca8a04"

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.edgecolor': TEXT2,
    'axes.linewidth': 0.8,
    'axes.labelcolor': TEXT,
    'axes.titlecolor': TEXT,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.titlepad': 14,
    'xtick.color': TEXT2,
    'ytick.color': TEXT2,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.dpi': 160,
})

# ─────────────────────────────────────────────────────────────────────────────
def load_csv(path):
    with open(ROOT / path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

cat_rows   = load_csv("data/results/phase2b_summary_by_category.csv")
model_rows = load_csv("data/results/phase2b_cross_model_comparison.csv")
trial_rows = load_csv("data/results/phase2b_controlled_results.csv")

# ─────────────────────────────────────────────────────────────────────────────
# FIG 1 — Cross-model ASR bar chart (the headline number)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.5))
models = [r['model'] for r in model_rows]
asrs   = [float(r['asr_percent'].rstrip('%')) for r in model_rows]
crits  = [float(r['critical_pct'].rstrip('%')) for r in model_rows]

x = range(len(models))
bars1 = ax.bar([i - 0.2 for i in x], asrs,  width=0.4, color=ACC,       label="Overall ASR",          edgecolor='white')
bars2 = ax.bar([i + 0.2 for i in x], crits, width=0.4, color=ACC_DARK,  label="Critical-tier (sev 3)", edgecolor='white')

for b, v in zip(bars1, asrs):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.2, f"{v:.1f}%",
            ha='center', fontsize=9, color=TEXT, fontweight='bold')
for b, v in zip(bars2, crits):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.2, f"{v:.0f}%",
            ha='center', fontsize=9, color=TEXT2)

ax.set_xticks(list(x))
ax.set_xticklabels(models, rotation=15, ha='right')
ax.set_ylabel("Attack Success Rate (%)")
ax.set_title("Phase 2b Simulated ASR — 2026 Frontier Models  (1,600 trials, seed 42)")
ax.set_ylim(0, max(asrs) + 12)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.legend(loc='upper left', frameon=False, fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "fig1_cross_model_asr.png")
plt.close()
print(f"OK: {OUT}/fig1_cross_model_asr.png")

# ─────────────────────────────────────────────────────────────────────────────
# FIG 2 — Per-category ASR (horizontal bars, color-coded by severity)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5.5))
cats = [r['category'].replace('_', ' ').title() for r in cat_rows]
cat_asrs = [float(r['asr_percent'].rstrip('%')) for r in cat_rows]
cat_crits = [int(r['critical']) for r in cat_rows]
cat_trials = [int(r['total_trials']) for r in cat_rows]
crit_pct = [100*c/t if t else 0 for c, t in zip(cat_crits, cat_trials)]

# Color by criticality risk
def color_for(c):
    if c >= 60: return RED
    if c >= 30: return YELLOW
    if c >= 10: return ACC
    return GREEN

colors = [color_for(c) for c in crit_pct]
# Sort by ASR
order = sorted(range(len(cats)), key=lambda i: cat_asrs[i])
cats_s   = [cats[i] for i in order]
asrs_s   = [cat_asrs[i] for i in order]
colors_s = [colors[i] for i in order]
crits_s  = [crit_pct[i] for i in order]

bars = ax.barh(cats_s, asrs_s, color=colors_s, edgecolor='white', height=0.7)
for b, v, c in zip(bars, asrs_s, crits_s):
    ax.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2,
            f"{v:.1f}%  ·  critical {c:.0f}%",
            va='center', fontsize=9, color=TEXT)

ax.set_xlabel("Attack Success Rate (%)")
ax.set_title("Phase 2b Simulated ASR by Taxonomy Category")
ax.set_xlim(0, 115)
ax.grid(axis='x', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend for severity color coding
legend_items = [
    Patch(facecolor=RED,    label='Critical-tier ≥ 60% (paramount risk)'),
    Patch(facecolor=YELLOW, label='Critical-tier 30–59% (high risk)'),
    Patch(facecolor=ACC,    label='Critical-tier 10–29% (moderate)'),
    Patch(facecolor=GREEN,  label='Critical-tier < 10% (low)'),
]
ax.legend(handles=legend_items, loc='lower right', frameon=False, fontsize=8.5)
plt.tight_layout()
plt.savefig(OUT / "fig2_per_category_asr.png")
plt.close()
print(f"OK: {OUT}/fig2_per_category_asr.png")

# ─────────────────────────────────────────────────────────────────────────────
# FIG 3 — Severity distribution heatmap (model × category)
# ─────────────────────────────────────────────────────────────────────────────
import numpy as np
cat_set = sorted(set(r['category'] for r in trial_rows),
                 key=lambda c: int([r['pattern_id'] for r in trial_rows if r['category']==c][0].split('-')[1] if '-' in [r['pattern_id'] for r in trial_rows if r['category']==c][0] else 0))
model_set = sorted(set(r['model'] for r in trial_rows))
matrix = np.zeros((len(model_set), len(cat_set)))
counts = np.zeros((len(model_set), len(cat_set)))
for r in trial_rows:
    m = model_set.index(r['model'])
    c = cat_set.index(r['category'])
    matrix[m, c] += float(r['severity_score'])
    counts[m, c] += 1
mean_sev = np.divide(matrix, counts, out=np.zeros_like(matrix), where=counts!=0)

fig, ax = plt.subplots(figsize=(10, 4))
im = ax.imshow(mean_sev, cmap='YlOrRd', aspect='auto', vmin=0, vmax=3)
ax.set_xticks(range(len(cat_set)))
ax.set_xticklabels([c.replace('_', '\n') for c in cat_set], fontsize=8.5)
ax.set_yticks(range(len(model_set)))
ax.set_yticklabels(model_set, fontsize=9)
for i in range(len(model_set)):
    for j in range(len(cat_set)):
        v = mean_sev[i,j]
        ax.text(j, i, f"{v:.2f}", ha='center', va='center',
                color='white' if v > 1.5 else TEXT, fontsize=8)
ax.set_title("Mean Severity Score by Model × Category  (0 = safe refusal, 3 = critical bypass)")
cbar = plt.colorbar(im, ax=ax, shrink=0.7)
cbar.set_label("Mean Severity", fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "fig3_severity_heatmap.png")
plt.close()
print(f"OK: {OUT}/fig3_severity_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# FIG 4 — Response type breakdown stacked bars
# ─────────────────────────────────────────────────────────────────────────────
resp_types = ['explicit_refusal','redirect','safety_acknowledgment',
              'partial_bypass','full_bypass','complete_bypass']
resp_colors = ['#16a34a','#22c55e','#84cc16','#fde047','#fb923c','#dc2626']
buckets = {m: {rt: 0 for rt in resp_types} for m in model_set}
for r in trial_rows:
    rt = r['response_type']
    if rt in buckets[r['model']]:
        buckets[r['model']][rt] += 1

fig, ax = plt.subplots(figsize=(8, 4.5))
bottoms = np.zeros(len(model_set))
for rt, color in zip(resp_types, resp_colors):
    vals = np.array([buckets[m][rt] for m in model_set])
    # normalize to percent
    totals = np.array([sum(buckets[m].values()) for m in model_set])
    vals_pct = (vals / totals) * 100
    ax.bar(model_set, vals_pct, bottom=bottoms, label=rt.replace('_',' '),
           color=color, edgecolor='white', width=0.65)
    bottoms += vals_pct

ax.set_ylabel("Trial Outcome (%)")
ax.set_title("Response Outcome Distribution by Model")
ax.set_ylim(0, 100)
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=8.5)
ax.grid(axis='y', color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.setp(ax.get_xticklabels(), rotation=15, ha='right')
plt.tight_layout()
plt.savefig(OUT / "fig4_response_outcome.png")
plt.close()
print(f"OK: {OUT}/fig4_response_outcome.png")

print("\nAll figures written to figures/v4/")
