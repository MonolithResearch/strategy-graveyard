# Option-implied vol-spread: liquidity changes the experiment

**Historical outcome: rejected for the intended liquid-universe implementation.**
The figures below are retained summary measurements from June 2026 research,
not a fresh replication. See [provenance](../PROVENANCE.md).

## Hypothesis and reported comparison

The study used a call-minus-put implied-volatility spread as a candidate predictor
of subsequent stock returns. The historical full-universe report recorded net
Sharpe 1.55, OOS Sharpe 0.98 and DSR rounded to 1.000. The next question was whether
the result survived progressively more liquid equity universes.

| Universe | Reported net Sharpe | Reported OOS Sharpe |
|---|---:|---:|
| Full, approximately 3,000 names | 1.55 | 0.98 |
| Top 2,000 | 0.46 | 0.03 |
| Top 1,000 | 0.36 | -0.07 |
| Top 500 | 0.20 | -0.23 |
| Top 250 | -0.19 | -0.20 |

The last OOS figure is as recorded in the unpublished case-study source; another
historical summary rounds/describes the top-250 result as -0.19. The original
returns have not been recomputed here, so the small discrepancy is not silently
resolved. It does not change the negative liquid-universe conclusion.

## What follows, and what does not

The deterioration is evidence against deploying the full-universe headline in the
intended liquid subset. Thin option quotes, small-cap effects and implementation
frictions are possible explanations; this universe comparison alone does not
identify their causal contributions.

A rounded DSR of 1.000 is not a perfect certificate. It is conditional on the
search record, data quality, units and statistical assumptions. It does not validate
fills, borrow, capacity or generalization to another universe. The public dataset
does not supply every gate input for this row, so it is marked numerically
**INCOMPLETE**, while retaining the historical implementation rejection.

The engineering lesson is to preserve the liquidity ladder alongside the attractive
aggregate statistic and compare the version that could actually be implemented.
