"""Offline synthetic demonstration of PSR, DSR and genuine half-block CSCV.

This educational implementation is not a promotion gate. It supplies neither
trade-count evidence nor execution/market-data validation. The published CSV is
historical summary evidence and is not recomputed by this demonstration.

References: Bailey & Lopez de Prado (2014), Deflated Sharpe Ratio;
Bailey et al. (2017), Probability of Backtest Overfitting.
"""
from itertools import combinations
from math import comb, sqrt
from numbers import Integral

import numpy as np
from scipy.stats import norm, rankdata


def _returns(values):
    r = np.asarray(values, dtype=float)
    if r.ndim != 1 or r.size < 2 or not np.isfinite(r).all():
        raise ValueError("returns must be a finite one-dimensional series of length >= 2")
    return r


def sharpe(returns):
    """Nonannualized sample Sharpe; zero variance is assigned zero, not infinity."""
    r = _returns(returns)
    if np.all(r == r[0]):
        return 0.0
    sd = r.std(ddof=1)
    return 0.0 if sd == 0 else float(r.mean() / sd)


def psr(returns, sr_benchmark=0.0):
    """Normal-approximation PSR, with no favorable result for zero variance."""
    r = _returns(returns)
    if not np.isfinite(sr_benchmark):
        raise ValueError("benchmark must be finite")
    if np.all(r == r[0]):
        return 0.0
    sd = r.std(ddof=1)
    if sd == 0:
        return 0.0
    sr = float(r.mean() / sd)
    centered = (r - r.mean()) / sd
    g3, g4 = np.mean(centered ** 3), np.mean(centered ** 4)
    variance = 1 - g3 * sr + (g4 - 1) * sr ** 2 / 4
    if not np.isfinite(variance) or variance <= 0:
        raise ValueError("PSR approximation has non-positive or non-finite variance")
    return float(norm.cdf((sr - sr_benchmark) * sqrt(len(r) - 1) / sqrt(variance)))


def expected_max_sharpe(n_trials, var_sr):
    """Expected max of independent null Sharpes; input variance is per period."""
    if isinstance(n_trials, (bool, np.bool_)) or not isinstance(n_trials, Integral) or n_trials < 1:
        raise ValueError("n_trials must be a positive integer")
    if not np.isfinite(var_sr) or var_sr < 0:
        raise ValueError("trial-Sharpe variance must be finite and non-negative")
    if n_trials == 1:
        return 0.0
    euler = 0.5772156649015329
    return float(sqrt(var_sr) * ((1 - euler) * norm.isf(1 / n_trials)
        + euler * norm.isf(1 / (n_trials * np.e))))


def dsr(returns, n_trials, var_sr_across_trials):
    return psr(returns, expected_max_sharpe(n_trials, var_sr_across_trials))


def _column_sharpes(values):
    sd = values.std(axis=0, ddof=1)
    # Repeated decimal floats can have tiny nonzero computed sample variance.
    # Inspect observations themselves rather than treating rounding as evidence.
    varying = np.any(values != values[0], axis=0)
    return np.divide(values.mean(axis=0), sd, out=np.zeros(values.shape[1]),
                     where=(sd > 0) & varying)


def pbo_cscv(matrix, n_splits=10):
    """Enumerate every equal half-block IS/OOS partition.

    Rows must divide exactly into an even number of blocks. Relative OOS ranks
    are one-based midranks divided by M+1. Logit <= 0 counts as overfit, so an
    exact median tie is conservatively included. Tied IS winners contribute
    equally, avoiding arbitrary dependence on column order. No rows are dropped.
    A 20,000-partition cap bounds accidental combinatorial work.
    """
    m = np.asarray(matrix, dtype=float)
    if m.ndim != 2 or m.shape[1] < 2 or not np.isfinite(m).all():
        raise ValueError("matrix must be finite, two-dimensional and contain >= 2 strategies")
    if (isinstance(n_splits, (bool, np.bool_)) or not isinstance(n_splits, Integral)
            or n_splits < 2 or n_splits % 2 or n_splits > 16):
        raise ValueError("n_splits must be an even integer from 2 to 16")
    if len(m) % n_splits or len(m) // n_splits < 2:
        raise ValueError("equal blocks with >= 2 observations are required; no silent truncation")
    if comb(n_splits, n_splits // 2) > 20_000:
        raise ValueError("too many CSCV partitions")
    blocks = np.split(np.arange(len(m)), n_splits)
    outcomes = []
    for selected in combinations(range(n_splits), n_splits // 2):
        train = np.concatenate([blocks[i] for i in selected])
        test = np.concatenate([blocks[i] for i in range(n_splits) if i not in selected])
        train_sr = _column_sharpes(m[train])
        test_sr = _column_sharpes(m[test])
        winners = np.flatnonzero(train_sr == train_sr.max())
        relative_rank = rankdata(test_sr, method="average") / (m.shape[1] + 1)
        outcomes.append(float(np.mean(relative_rank[winners] <= 0.5)))
    return float(np.mean(outcomes))


def main():
    rng = np.random.default_rng(20260617)
    print("SYNTHETIC DEMONSTRATION - no market or promotion-gate verdict")
    print("Per-period Sharpe; DSR uses the complete simulated search dispersion.")
    for n in (100, 1000, 5000):
        bank = rng.normal(0, 1, size=(600, n))
        sr_each = _column_sharpes(bank)
        best = bank[:, int(np.argmax(sr_each))]
        # Fixed column membership chosen without looking at performance.
        subset = bank[:, :min(n, 30)]
        print(f"N={n:5d} | best SR={sharpe(best):.4f} | "
              f"DSR={dsr(best, n, sr_each.var(ddof=1)):.4f} | "
              f"CSCV PBO (first {subset.shape[1]} candidates)={pbo_cscv(subset):.4f}")
    print("Subset PBO does not validate the full search winner. Missing trade and")
    print("execution evidence means no PASS. Noise can still score well by chance;")
    print("DSR is an approximation under assumptions, not a guarantee of truth.")


if __name__ == "__main__":
    main()
