"""
demo_validation.py
==================
A small, fully self-contained demonstration of the validation core that grades
every strategy in this graveyard, run on SYNTHETIC data only. No licensed data,
no live-strategy logic — just the maths that turns a pretty backtest into an
honest verdict.

It implements:
  * Probabilistic Sharpe Ratio (PSR)        Bailey & Lopez de Prado, SSRN 1821643
  * Deflated Sharpe Ratio    (DSR)          Bailey & Lopez de Prado, SSRN 2460551
  * Probability of Backtest Overfitting (PBO) via a simplified CSCV

and then re-tells the graveyard's central lesson with a synthetic search:
pick the best of N noisy strategies, watch the raw Sharpe look great and the
DEFLATED Sharpe correctly collapse to ~0.

Run:  py -3.14 scripts/demo_validation.py
"""
import numpy as np
from math import erf, sqrt, log, pi
from scipy.stats import norm

RNG = np.random.default_rng(20260617)

# ----------------------------------------------------------------------------
# Sharpe + PSR
# ----------------------------------------------------------------------------
def sharpe(returns):
    r = np.asarray(returns, float)
    sd = r.std(ddof=1)
    return 0.0 if sd == 0 else r.mean() / sd


def psr(returns, sr_benchmark=0.0):
    """Probabilistic Sharpe Ratio: P(true SR > benchmark) given skew/kurtosis."""
    r = np.asarray(returns, float)
    n = len(r)
    sr = sharpe(r)
    sd = r.std(ddof=1)
    g3 = ((r - r.mean()) ** 3).mean() / sd ** 3          # skew
    g4 = ((r - r.mean()) ** 4).mean() / sd ** 4          # kurtosis (raw)
    denom = sqrt(1 - g3 * sr + (g4 - 1) / 4.0 * sr ** 2)
    z = (sr - sr_benchmark) * sqrt(n - 1) / denom
    return norm.cdf(z)


# ----------------------------------------------------------------------------
# Deflated Sharpe Ratio
# ----------------------------------------------------------------------------
def expected_max_sharpe(n_trials, var_sr):
    """E[max SR] of n_trials independent N(0, var_sr) Sharpes (Bailey-LdP)."""
    if n_trials < 2:
        return 0.0
    e = 0.5772156649015329  # Euler-Mascheroni
    z1 = norm.ppf(1 - 1.0 / n_trials)
    z2 = norm.ppf(1 - 1.0 / (n_trials * np.e))
    return sqrt(var_sr) * ((1 - e) * z1 + e * z2)


def dsr(returns, n_trials, var_sr_across_trials):
    """Deflated Sharpe: PSR benchmarked against the expected max of the search."""
    sr_star = expected_max_sharpe(n_trials, var_sr_across_trials)
    return psr(returns, sr_benchmark=sr_star)


# ----------------------------------------------------------------------------
# PBO via a simplified CSCV
# ----------------------------------------------------------------------------
def pbo_cscv(matrix, n_splits=10):
    """
    matrix: (T observations x M strategies) of returns.
    Returns the Probability of Backtest Overfitting: how often the IS-best
    strategy lands below the median OOS.
    """
    T, M = matrix.shape
    block = T // n_splits
    losses = 0
    trials = 0
    for k in range(n_splits):
        oos_idx = np.zeros(T, bool)
        oos_idx[k * block:(k + 1) * block] = True
        is_idx = ~oos_idx
        is_sr = np.array([sharpe(matrix[is_idx, m]) for m in range(M)])
        oos_sr = np.array([sharpe(matrix[oos_idx, m]) for m in range(M)])
        best = int(np.argmax(is_sr))
        rank = (oos_sr < oos_sr[best]).sum() / M  # fraction worse than best
        losses += 1 if rank < 0.5 else 0          # best is below OOS median
        trials += 1
    return losses / trials


# ----------------------------------------------------------------------------
# The graveyard lesson, reproduced on synthetic data
# ----------------------------------------------------------------------------
def main():
    T = 1000

    # 1) A genuinely good strategy: small positive edge.
    good = RNG.normal(0.05, 1.0, T)
    print("=== A genuinely (mildly) good single strategy ===")
    print(f"  Sharpe         : {sharpe(good):+.3f}")
    print(f"  PSR (vs 0)     : {psr(good):.3f}")
    print(f"  DSR (1 trial)  : {dsr(good, 1, 0.0):.3f}")
    print()

    # 2) The mirage: search N pure-noise strategies, keep the best.
    for N in (100, 7060, 88632):
        bank = RNG.normal(0.0, 1.0, size=(T, N))     # all zero-edge noise
        sr_each = np.array([sharpe(bank[:, m]) for m in range(N)])
        var_sr = sr_each.var(ddof=1)
        best_m = int(np.argmax(sr_each))
        best = bank[:, best_m]
        d = dsr(best, N, var_sr)
        # PBO uses a manageable slice of the search for the CSCV grid
        sub = bank[:, np.argsort(sr_each)[-min(N, 50):]]
        pbo = pbo_cscv(sub, n_splits=10)
        print(f"=== Best of N={N:,} PURE-NOISE strategies (no real edge) ===")
        print(f"  Best raw Sharpe : {sharpe(best):+.3f}   <- looks deployable")
        print(f"  Deflated Sharpe : {d:.3f}   <- the search penalty bites")
        print(f"  PBO (CSCV)      : {pbo:.3f}")
        print(f"  GATE (DSR>=0.50, PBO<=0.20): "
              f"{'PASS' if (d >= 0.5 and pbo <= 0.2) else 'FAIL'}")
        print()

    print("Lesson: a high in-sample Sharpe from a large search is evidence of "
          "the\nsearch, not the signal. The deflated Sharpe undoes it. This is "
          "exactly\nwhy every one of the 34 graveyard strategies fails the gate.")


if __name__ == "__main__":
    main()
