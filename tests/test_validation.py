"""
Known-answer + invariant tests for the public Strategy Graveyard.

These cover (a) the validation maths shipped in scripts/demo_validation.py and
(b) the honesty invariants of the public dataset — most importantly that the
headline claim "zero of the 34 strategies clear the gate" is true against the
committed CSV, and that no row smuggles in a deployable PASS.

Run:  py -3.14 -m pytest -q
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import demo_validation as dv  # noqa: E402

CSV_PATH = os.path.join(ROOT, "data", "gate_ranking_public.csv")


# --------------------------------------------------------------------------
# Validation maths (known answers)
# --------------------------------------------------------------------------
def test_sharpe_of_constant_is_zero():
    assert dv.sharpe(np.zeros(50)) == 0.0


def test_sharpe_sign_and_scale():
    rng = np.random.default_rng(0)
    pos = rng.normal(0.1, 1.0, 5000)
    neg = -pos
    assert dv.sharpe(pos) > 0
    assert dv.sharpe(neg) == -dv.sharpe(pos)


def test_psr_in_unit_interval_and_monotone():
    rng = np.random.default_rng(1)
    weak = rng.normal(0.01, 1.0, 2000)
    strong = rng.normal(0.20, 1.0, 2000)
    for x in (weak, strong):
        p = dv.psr(x)
        assert 0.0 <= p <= 1.0
    assert dv.psr(strong) > dv.psr(weak)


def test_expected_max_sharpe_monotonic_increasing():
    e2 = dv.expected_max_sharpe(2, 1.0)
    e100 = dv.expected_max_sharpe(100, 1.0)
    e1e4 = dv.expected_max_sharpe(10_000, 1.0)
    assert 0 < e2 < e100 < e1e4
    # single trial has no selection penalty
    assert dv.expected_max_sharpe(1, 1.0) == 0.0


def test_deflation_collapses_best_of_noise():
    """The graveyard's core lesson: best-of-N noise has a high raw Sharpe but a
    deflated Sharpe that does NOT clear the 0.50 gate."""
    rng = np.random.default_rng(20260617)
    T, N = 1000, 5000
    bank = rng.normal(0.0, 1.0, size=(T, N))
    sr_each = np.array([dv.sharpe(bank[:, m]) for m in range(N)])
    best = bank[:, int(np.argmax(sr_each))]
    raw = dv.sharpe(best)
    d = dv.dsr(best, N, sr_each.var(ddof=1))
    assert raw > 0.05          # raw looks deployable
    assert d < 0.50            # deflation correctly fails it


def test_pbo_in_unit_interval():
    rng = np.random.default_rng(2)
    mat = rng.normal(0.0, 1.0, size=(600, 30))
    p = dv.pbo_cscv(mat, n_splits=10)
    assert 0.0 <= p <= 1.0


# --------------------------------------------------------------------------
# Public-dataset honesty invariants
# --------------------------------------------------------------------------
def _rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_exactly_34_strategies():
    assert len(_rows()) == 34


def test_zero_strategies_clear_the_full_gate():
    """Headline claim: zero of the 34 clear the gate.
    Gate = DSR>=0.50 AND PBO<=0.20 AND trades>=50. No row may satisfy all three.
    """
    for r in _rows():
        dsr = r["blind_OOS_DSR"].strip()
        pbo = r["PBO"].strip()
        trades = r["OOS_trades"].strip()
        if dsr == "" or pbo == "" or trades == "":
            continue  # missing a gate input -> cannot be a PASS by definition
        clears = (
            float(dsr) >= 0.50
            and float(pbo) <= 0.20
            and int(float(trades)) >= 50
        )
        assert not clears, f"{r['name']} unexpectedly clears the gate"


def test_no_secrets_or_account_numbers_in_csv():
    blob = open(CSV_PATH, encoding="utf-8").read().lower()
    # Account-number fragments are assembled at runtime so the literal private
    # identifiers never appear verbatim in this public source file.
    acct_a = "209" + "68673"
    acct_b = "387" + "97789"
    for bad in (acct_a, acct_b, "api_key", "apikey", "bearer", "password", "-003"):
        assert bad not in blob


if __name__ == "__main__":
    raise SystemExit(__import__("pytest").main([os.path.dirname(__file__), "-q"]))
