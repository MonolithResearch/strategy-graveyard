# Σ Case study — Intraday mean-reversion pairs (the textbook mirage)

**Tier 4 — Structurally dead.** In-sample Sharpe **5.47** → out-of-sample **-0.54**.
Blind-OOS rank-DSR **0.015**, PBO **0.53**, 304 OOS trades.

---

## The pitch

An Ornstein-Uhlenbeck stat-arb on intraday (M5) pairs. Find cointegrated legs,
trade the spread back to its mean. The in-sample equity curve is gorgeous:
Sharpe **5.47**. If you stop there, you deploy it.

## Why it is a mirage

I did not run one backtest. I ran **7,060** (parameter sweeps over lookback,
entry/exit z-thresholds, pair-selection rules). When you keep the best of 7,060
noisy curves, the *maximum order statistic* of pure noise is large by
construction. That is what a Sharpe of 5.47 actually measured here.

Two facts make this unambiguous:

1. **The honest single, pre-chosen config is itself negative in-sample.** The
   5.47 only exists after selection. Strip the search and there is no edge to
   begin with.
2. **Out of sample the spread sign-flips to -0.54** and the deflated Sharpe,
   which charges you for the 7,060 trials, is **0.015** — three percent of the
   way to the gate.

PBO via CSCV is **0.53**: a coin-flip that the in-sample-best config is below
the median out of sample. That is the signature of selection, not signal.

## The deeper structural problem

M5 is the worst possible timeframe for this. The mean-reversion amplitude is a
few basis points; the round-trip cost (spread + commission, two legs) eats it
whole. Even if the statistical edge were real, the **cost bar sits above the
gross signal**. This OU family has now been independently rebuilt and killed
**seven times** across timeframes. It is retired permanently.

## What the gate caught

| Metric            | Value  | Gate     | Verdict |
|-------------------|--------|----------|---------|
| In-sample Sharpe  | 5.47   | —        | bait    |
| OOS Sharpe        | -0.54  | > 0      | FAIL    |
| Deflated Sharpe   | 0.015  | ≥ 0.50   | FAIL    |
| PBO (CSCV)        | 0.53   | ≤ 0.20   | FAIL    |
| Net 3× cost SR    | -0.98  | > 0      | FAIL    |

## Lesson

A high in-sample Sharpe from a large search is **evidence of the search, not the
signal**. The deflated Sharpe (Bailey & López de Prado, SSRN 2460551) exists
precisely to undo this. If your honest single-config in-sample number is
negative, no amount of selection has produced an edge — it has only produced a
story.
