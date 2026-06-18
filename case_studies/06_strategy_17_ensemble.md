# Σ Case study — TSMOM ensemble (the live bot that the gate sent home)

**Tier 3 — Overfit / sign-flips.** Headline Sharpe **1.72** → 17.6-year pure-OOS
Sharpe **0.108** (DSR **0.191**). This one had been **deployed with real capital**
before the gate caught it. The book was wound down to zero live risk.

---

## The pitch

A vol-parity ensemble of three time-series-momentum sleeves plus a regime
overlay. The headline backtest Sharpe was **1.72** — comfortably "deployable" by
the standards I held at the time, so it went live.

## Why it was a mirage

The 1.72 was **selection**. The ensemble had knobs — sleeve weights, lookbacks,
the regime thresholds — and the configuration that produced 1.72 was the
best-looking of many. When I went back and ran an **honest, pre-specified
configuration over a full 17.6-year pure out-of-sample window**, the Sharpe was:

> **0.108.**

Not negative — just nowhere near tradeable, and statistically indistinguishable
from zero once costs are charged. The best honest in-sample config is **~0 net of
cost**, and the OOS turns **negative**. The deflated Sharpe, charged for the
search, is **0.191**.

The deeper problem is what the surviving signal *was*: a long-biased trend book
in a **2023-26 bull market** is harvesting **beta**, not alpha. Strip the market
exposure and the standalone edge collapses.

| Metric                       | Value  | Gate    | Verdict |
|------------------------------|--------|---------|---------|
| Headline (selected) Sharpe   | 1.72   | —       | bait    |
| 17.6yr pure-OOS Sharpe       | 0.108  | —       | FAIL    |
| Deflated Sharpe              | 0.191  | ≥ 0.50  | FAIL    |
| Best honest IS, net of cost  | ~0     | > 0     | FAIL    |
| OOS Sharpe                   | negative | > 0   | FAIL    |

## The hardest part: I had to retire a live book

This is the case that proves the gate is not theatre. The strategy was **running
on a live account**. When the honest revalidation came back at 0.108, the right
action was to **wind it down** — which is what happened on 2026-06-12. The account
was flattened to roughly **£696 NAV** and **zero live risk**. No grandfathering,
no "but it's already deployed", no sunk-cost defence.

(The strategy internals stay private; what is public is the verdict and the
numbers behind it.)

## Lesson

A headline Sharpe over 1.5 is a **prompt to be suspicious**, not a green light —
especially for a tunable ensemble in a trending market, where "alpha" is usually
**beta in disguise**. The test that matters is a long, honest, pre-specified
out-of-sample window with costs charged. And when that test fails a strategy you
have **already deployed**, the discipline is to **turn it off**. Treating your own
live book as an adversary is the whole job.
