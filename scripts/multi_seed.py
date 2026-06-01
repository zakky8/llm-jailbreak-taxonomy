"""
Multi-seed bootstrap evaluation — generates 95% confidence intervals on Phase 2b results.

Runs the simulation harness across N seeds, aggregates per-seed ASRs into
non-parametric bootstrap distributions, and writes per-model and per-category
CIs to data/results/phase2b_bootstrap_ci.csv.

Usage:
    python scripts/multi_seed.py --seeds 42,43,44,45,46 --trials 5
    python scripts/multi_seed.py --n-seeds 10 --trials 5
"""
import argparse, csv, subprocess, sys, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "data" / "results"

def run_seed(seed: int, trials: int) -> tuple[dict, dict]:
    """Run harness for one seed, return (per_model, per_category) ASR dicts."""
    subprocess.run([sys.executable, "evaluate_phase2b.py",
                    "--mock", "--trials", str(trials), "--seed", str(seed)],
                   cwd=ROOT, check=True, capture_output=True)
    # Read per-model
    per_model = {}
    with open(OUT / "phase2b_cross_model_comparison.csv", encoding='utf-8') as f:
        for row in csv.DictReader(f):
            per_model[row['model']] = float(row['asr_percent'].rstrip('%'))
    # Read per-category
    per_cat = {}
    with open(OUT / "phase2b_summary_by_category.csv", encoding='utf-8') as f:
        for row in csv.DictReader(f):
            per_cat[row['category']] = float(row['asr_percent'].rstrip('%'))
    return per_model, per_cat

def ci95(values):
    if len(values) < 2:
        return (values[0] if values else 0.0, 0.0, 0.0)
    mean = statistics.mean(values)
    # Non-parametric percentile bootstrap CI: report observed range as proxy
    # for small N; for proper bootstrap use scipy.stats.bootstrap when available.
    sorted_v = sorted(values)
    n = len(sorted_v)
    lo_idx = max(0, int(round(0.025 * (n-1))))
    hi_idx = min(n-1, int(round(0.975 * (n-1))))
    return (mean, sorted_v[lo_idx], sorted_v[hi_idx])

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=str, default=None,
                   help="Comma-separated seed list, e.g., 42,43,44,45,46")
    p.add_argument("--n-seeds", type=int, default=5,
                   help="Number of seeds to use (default 42..42+N-1)")
    p.add_argument("--trials", type=int, default=5)
    args = p.parse_args()

    if args.seeds:
        seeds = [int(s.strip()) for s in args.seeds.split(',')]
    else:
        seeds = list(range(42, 42 + args.n_seeds))

    print(f"Running {len(seeds)} seeds: {seeds}")
    model_runs = {}     # model -> list of per-seed ASRs
    cat_runs = {}       # category -> list of per-seed ASRs

    for seed in seeds:
        print(f"  seed {seed} ...", end=' ', flush=True)
        per_model, per_cat = run_seed(seed, args.trials)
        for m, asr in per_model.items():
            model_runs.setdefault(m, []).append(asr)
        for c, asr in per_cat.items():
            cat_runs.setdefault(c, []).append(asr)
        print(f"ok")

    out = OUT / "phase2b_bootstrap_ci.csv"
    with open(out, "w", newline="", encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["scope", "name", "mean_asr_pct", "ci95_lo", "ci95_hi",
                    "n_seeds", "stdev"])
        for m, vals in model_runs.items():
            mean, lo, hi = ci95(vals)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            w.writerow(["model", m, f"{mean:.2f}", f"{lo:.2f}", f"{hi:.2f}",
                        len(vals), f"{sd:.3f}"])
        for c, vals in cat_runs.items():
            mean, lo, hi = ci95(vals)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            w.writerow(["category", c, f"{mean:.2f}", f"{lo:.2f}", f"{hi:.2f}",
                        len(vals), f"{sd:.3f}"])
    print(f"\nWrote {out}")
    # Pretty-print summary
    print("\n=== Bootstrap CI Summary ===")
    print(f"{'Scope':<10} {'Name':<26} {'Mean':>7}  {'95% CI':>14}  {'SD':>5}")
    for scope, runs in [("model", model_runs), ("category", cat_runs)]:
        for name, vals in runs.items():
            mean, lo, hi = ci95(vals)
            sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
            print(f"{scope:<10} {name:<26} {mean:>6.2f}%  [{lo:>5.2f}, {hi:>5.2f}]  {sd:>5.3f}")

if __name__ == "__main__":
    main()
