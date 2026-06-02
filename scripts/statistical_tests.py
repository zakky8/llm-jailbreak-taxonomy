"""
Statistical-test computations on Phase 2b output data.

⚠ v4.2.1 honesty: When run against the SIMULATION outputs (the default state
of the repo until Phase 2b live executes), the tests below are NOT valid as
hypothesis tests about real model behaviour. They are computed for two reasons:

  1. Pipeline validation — verify the test script produces the expected schema
     and integrates cleanly with the downstream analysis.
  2. Reuse readiness — when live Phase 2b data arrives, the same script runs
     unchanged and produces tests that ARE valid.

Specific assumption violations on the simulated data:

  - Cochran's Q requires matched subjects (same stimulus across conditions).
    The simulation produces independent random draws per (model, pattern,
    trial), not matched measurements. Q is computable but its p-value is
    NOT interpretable on simulated data.
  - McNemar p-values on simulated data reflect the parameterization of
    `evaluate_phase2b.py` — they would be near-identical under any prior
    that preserves the same model ordering.

Both tests become valid the moment they are computed on the live API harness
output (evaluate_live.py), because the live trials produce real responses
to controlled stimuli.

Implements:
  - 95% binomial Wilson CIs per (model, category) cell — valid on either
    simulated or live data (Wilson CI is a property of the count itself)
  - Pairwise McNemar's test between models on per-pattern outcomes
    (assumption-valid on live, NOT on simulated)
  - Effect size (Cohen's h) between model pairs
  - Per-category Cochran's Q (k-way agreement)
    (assumption-valid on live, NOT on simulated)

Run:  python scripts/statistical_tests.py
Output: data/results/phase2b_statistical_tests.csv
"""
import csv
import math
import statistics
from pathlib import Path
from collections import defaultdict
from itertools import combinations

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "data" / "results"

# ─── Stdlib statistical helpers ────────────────────────────────────────────────
def wilson_ci(success, n, z=1.96):
    """95% Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = success / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    margin = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return (p, max(0.0, center - margin), min(1.0, center + margin))

def mcnemar_chi2(b, c):
    """Continuity-corrected McNemar χ² statistic and p-value approximation.

    b: count of items model A bypassed, model B refused
    c: count of items model A refused, model B bypassed

    Returns (statistic, two-sided p-value approximation).
    For (b+c) < 25, the exact binomial p-value is more reliable.
    """
    if b + c == 0:
        return (0.0, 1.0)
    if b + c < 25:
        # Exact: P(X >= max(b,c)) under Binomial(b+c, 0.5), two-sided
        n = b + c
        k = max(b, c)
        # Two-sided exact: 2 * sum_{i=k}^{n} C(n,i) * 0.5^n
        def comb(n, k):
            if k < 0 or k > n: return 0
            return math.comb(n, k)
        tail = sum(comb(n, i) for i in range(k, n+1)) * (0.5 ** n)
        return (float('nan'), min(1.0, 2 * tail))
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    # χ² with 1 df → two-sided p via complementary error function
    p = math.erfc(math.sqrt(chi2 / 2))
    return (chi2, p)

def cohens_h(p1, p2):
    """Cohen's h effect size for two proportions."""
    phi1 = 2 * math.asin(math.sqrt(max(0.0, min(1.0, p1))))
    phi2 = 2 * math.asin(math.sqrt(max(0.0, min(1.0, p2))))
    return phi1 - phi2

def cochran_q(table):
    """Cochran's Q test for k-way agreement on binary outcomes.

    table: list of rows, each a list of {0,1} for k conditions.
    Returns (Q, df=k-1, p-value approximation).
    """
    if not table:
        return (0.0, 0, 1.0)
    k = len(table[0])
    n = len(table)
    col_sums = [sum(row[j] for row in table) for j in range(k)]
    row_sums = [sum(row) for row in table]
    T = sum(col_sums)
    sum_col_sq = sum(s*s for s in col_sums)
    sum_row_sq = sum(s*s for s in row_sums)
    denom = (k*T - sum_row_sq)
    if denom == 0:
        return (0.0, k-1, 1.0)
    Q = (k - 1) * (k * sum_col_sq - T*T) / denom
    # χ² with k-1 df → p value approximation via series
    # For df=3 (k=4 models): use complementary chi-square approximation
    df = k - 1
    # Wilson–Hilferty approximation
    if df > 0 and Q > 0:
        wh = ((Q/df) ** (1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
        # Two-sided via normal complementary
        p = 0.5 * math.erfc(wh / math.sqrt(2))
    else:
        p = 1.0
    return (Q, df, max(0.0, min(1.0, p)))

# ─── Load trial-level data ─────────────────────────────────────────────────────
def load_trials():
    rows = []
    with open(OUT / "phase2b_controlled_results.csv", encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({
                'pattern_id': r['pattern_id'],
                'category': r['category'],
                'model': r['model'],
                'temperature': float(r['temperature']),
                'trial_number': int(r['trial_number']),
                'severity_score': int(r['severity_score']),
                'bypass_observed': r['bypass_observed'] == 'TRUE',
            })
    return rows

# ─── Output rows ───────────────────────────────────────────────────────────────
def main():
    trials = load_trials()
    print(f"Loaded {len(trials)} trials")
    out_rows = []

    # 1. Wilson CIs per (model, category)
    print("\n=== Per-cell Wilson 95% CIs ===")
    cells = defaultdict(list)
    for t in trials:
        cells[(t['model'], t['category'])].append(t['bypass_observed'])
    for (m, c), bs in sorted(cells.items()):
        s = sum(bs); n = len(bs)
        p, lo, hi = wilson_ci(s, n)
        out_rows.append({
            'test': 'wilson_ci_95',
            'scope': f'{m}|{c}',
            'metric_value': f'{p*100:.2f}%',
            'ci_low': f'{lo*100:.2f}%',
            'ci_high': f'{hi*100:.2f}%',
            'n': n,
            'p_value': '',
            'effect_size': '',
            'notes': f'binomial Wilson; bypass rate'
        })
    print(f"  Computed Wilson CIs for {len(cells)} cells")

    # 2. McNemar pairwise tests on per-pattern outcomes
    print("\n=== Pairwise McNemar tests (per-pattern bypass agreement) ===")
    # For each (pattern, temperature, trial) combo, get each model's outcome
    by_key = defaultdict(dict)
    for t in trials:
        key = (t['pattern_id'], t['temperature'], t['trial_number'])
        by_key[key][t['model']] = t['bypass_observed']
    models = sorted({t['model'] for t in trials})
    for m1, m2 in combinations(models, 2):
        b = c = 0  # b: m1 bypass, m2 refuse; c: vice versa
        for k, results in by_key.items():
            if m1 not in results or m2 not in results: continue
            o1, o2 = results[m1], results[m2]
            if o1 and not o2: b += 1
            elif not o1 and o2: c += 1
        stat, p = mcnemar_chi2(b, c)
        h = cohens_h(b/(b+c) if b+c else 0.5, c/(b+c) if b+c else 0.5)
        out_rows.append({
            'test': 'mcnemar_pairwise',
            'scope': f'{m1} vs {m2}',
            'metric_value': f'b={b}, c={c}',
            'ci_low': '',
            'ci_high': '',
            'n': b + c,
            'p_value': f'{p:.4g}',
            'effect_size': f'h={h:.3f}',
            'notes': 'two-sided; b=m1-only, c=m2-only bypass counts'
        })
        print(f"  {m1:24} vs {m2:24}: b={b:>4}, c={c:>4}, p={p:.4g}, h={h:+.3f}")

    # 3. Cochran's Q across 4 models per category
    print("\n=== Cochran's Q (cross-model agreement per category) ===")
    by_cat = defaultdict(lambda: defaultdict(dict))
    for t in trials:
        key = (t['pattern_id'], t['temperature'], t['trial_number'])
        by_cat[t['category']][key][t['model']] = 1 if t['bypass_observed'] else 0
    for cat, keys_dict in sorted(by_cat.items()):
        table = []
        for k, row_dict in keys_dict.items():
            if len(row_dict) == len(models):
                table.append([row_dict[m] for m in models])
        Q, df, p = cochran_q(table)
        out_rows.append({
            'test': 'cochran_q',
            'scope': cat,
            'metric_value': f'Q={Q:.2f}',
            'ci_low': '',
            'ci_high': '',
            'n': len(table),
            'p_value': f'{p:.4g}',
            'effect_size': f'df={df}',
            'notes': f'4-way agreement across all models on {cat} patterns'
        })
        print(f"  {cat:30}: Q={Q:8.2f}, df={df}, p={p:.4g}, n={len(table)}")

    # Write CSV
    out_path = OUT / "phase2b_statistical_tests.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[
            'test','scope','metric_value','ci_low','ci_high','n','p_value','effect_size','notes'
        ])
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nWrote {out_path}")

    # Summary
    print("\n=== Summary ===")
    print(f"  Wilson CIs:      {sum(1 for r in out_rows if r['test']=='wilson_ci_95')}")
    print(f"  McNemar pairs:   {sum(1 for r in out_rows if r['test']=='mcnemar_pairwise')}")
    print(f"  Cochran's Q:     {sum(1 for r in out_rows if r['test']=='cochran_q')}")

if __name__ == "__main__":
    main()
