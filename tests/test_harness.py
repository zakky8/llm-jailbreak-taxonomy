"""
Smoke + property tests for the simulation harness.

Run:  pytest -q
"""
import csv
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run_harness(seed=42, trials=2):
    """Run evaluate_phase2b.py --mock and return path to results dir."""
    r = subprocess.run(
        [sys.executable, "evaluate_phase2b.py",
         "--mock", "--trials", str(trials), "--seed", str(seed)],
        cwd=ROOT, capture_output=True, text=True, encoding='utf-8'
    )
    assert r.returncode == 0, f"Harness failed: {r.stderr}"
    return ROOT / "data" / "results"

def read_csv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

# ──────────────────────────────────────────────────────────────────
def test_harness_runs_clean():
    """Smoke test: harness executes without error and writes outputs."""
    out = run_harness(seed=42, trials=2)
    assert (out / "phase2b_controlled_results.csv").exists()
    assert (out / "phase2b_summary_by_category.csv").exists()
    assert (out / "phase2b_cross_model_comparison.csv").exists()

def test_seed_reproducibility():
    """Same seed -> identical outputs."""
    run_harness(seed=42, trials=3)
    rows_a = read_csv(ROOT / "data/results/phase2b_controlled_results.csv")
    run_harness(seed=42, trials=3)
    rows_b = read_csv(ROOT / "data/results/phase2b_controlled_results.csv")
    # Compare deterministic columns (trial_id contains epoch time so skip)
    keys = ['pattern_id','category','model','temperature','trial_number',
            'severity_score','bypass_observed','response_type']
    for a, b in zip(rows_a, rows_b):
        for k in keys:
            assert a[k] == b[k], f"Mismatch on {k}: {a[k]} vs {b[k]}"

def test_different_seeds_differ():
    """Different seeds -> at least one differing trial."""
    run_harness(seed=42, trials=3)
    rows_a = [r['bypass_observed'] for r in
              read_csv(ROOT / "data/results/phase2b_controlled_results.csv")]
    run_harness(seed=999, trials=3)
    rows_b = [r['bypass_observed'] for r in
              read_csv(ROOT / "data/results/phase2b_controlled_results.csv")]
    assert rows_a != rows_b, "Different seeds produced identical results"

def test_severity_bounds():
    """Every severity score is in {0,1,2,3}."""
    run_harness(seed=42, trials=2)
    for r in read_csv(ROOT / "data/results/phase2b_controlled_results.csv"):
        s = int(r['severity_score'])
        assert 0 <= s <= 3, f"Severity out of bounds: {s}"

def test_bypass_severity_consistency():
    """severity==0 iff bypass_observed==FALSE; severity>0 iff bypass_observed==TRUE."""
    run_harness(seed=42, trials=2)
    for r in read_csv(ROOT / "data/results/phase2b_controlled_results.csv"):
        s = int(r['severity_score'])
        b = r['bypass_observed']
        if s == 0:
            assert b == 'FALSE', f"sev 0 but bypass={b}: {r}"
        else:
            assert b == 'TRUE', f"sev {s} but bypass={b}: {r}"

def test_all_four_models_present():
    """Cross-model comparison includes all 4 frontier models."""
    run_harness(seed=42, trials=2)
    rows = read_csv(ROOT / "data/results/phase2b_cross_model_comparison.csv")
    models = {r['model'] for r in rows}
    expected = {"claude-opus-4-8", "gpt-5.5", "gemini-3.5-flash", "deepseek-v4-pro"}
    assert models == expected, f"Model set mismatch: {models}"

def test_all_ten_categories_present():
    """Per-category summary includes all 10 taxonomy categories."""
    run_harness(seed=42, trials=2)
    rows = read_csv(ROOT / "data/results/phase2b_summary_by_category.csv")
    assert len(rows) == 10, f"Expected 10 categories, got {len(rows)}"

def test_critical_tier_concentration():
    """Critical-tier bypasses concentrate in Cat 7, 8, 10 (literature prediction)."""
    run_harness(seed=42, trials=5)
    rows = read_csv(ROOT / "data/results/phase2b_summary_by_category.csv")
    by_cat = {r['category']: int(r['critical']) for r in rows}
    crit_cats = {c for c, n in by_cat.items() if n > 0}
    # At least Cat 7 (LRM) and Cat 8 (Fuzzing) should have critical bypasses
    assert 'lrm_autonomous' in crit_cats, "LRM should have critical bypasses"
    assert 'fuzzing_based' in crit_cats, "Fuzzing should have critical bypasses"

def test_pattern_count():
    """Pattern database has the expected 40 patterns."""
    rows = read_csv(ROOT / "data/prompt_patterns.csv")
    assert len(rows) == 40, f"Expected 40 patterns, got {len(rows)}"

def test_pattern_categories_complete():
    """Every pattern has a valid 1-10 category number."""
    rows = read_csv(ROOT / "data/prompt_patterns.csv")
    cats = {int(r['category_number']) for r in rows if r.get('category_number','').strip()}
    assert cats == set(range(1, 11)), f"Missing categories: {set(range(1,11)) - cats}"
