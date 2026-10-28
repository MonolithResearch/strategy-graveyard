# Closed-end-fund discounts: beta and execution delay

**Historical outcome: the proposed implementation was closed.** These are reported
June 2026 summary measurements, not a fresh market-data replication.

The hypothesis was that discounts to fund NAV would converge. An implementation
using a long discount basket and liquid ETF hedge initially reported Sharpe 0.91,
OOS 1.10 and DSR 0.909. Subsequent checks changed the interpretation.

## Two separate sensitivity tests

The historical report found approximately +0.21 residual equity beta. Adding a
beta hedge reduced the reported full-sample Sharpe from 0.91 to about 0.45 and
the post-2022 result from 0.79 to about 0.05.

A further execution-lag comparison reported:

| Construction | Original timing | Extra week before execution |
|---|---:|---:|
| ETF-hedged, beta-adjusted | 0.45 | -0.03 |
| Individual-fund long/short, gross | 1.50 | 0.46 |
| Individual-fund long/short, net | 0.86 | -0.19 |
| Individual-fund long/short, post-2022 | 1.49 | 0.33 |

The source also records a separate cost specification producing a more negative
lagged result. Those experiments are not pooled or presented as exact replicas.

## Interpretation

The beta adjustment weakens the incremental-return claim. Sensitivity to a later
fill weakens the proposed execution case. Stale NAVs and short-lived price effects
are plausible explanations, not causal facts established by this table alone.
An extra week is a stress test; the necessary production delay would require a
verified NAV availability clock and achievable fill model.

The public archive cannot independently re-estimate the return paths, borrow
costs or survivorship treatment. The DSR 0.909 describes an earlier construction;
it is not transferable to the beta-adjusted, delayed-fill construction. Missing
gate inputs remain **INCOMPLETE** in the public numeric audit.

The lesson is to specify the information and execution clocks and keep every
change of construction visible. An attractive statistic for one portfolio does
not validate a different portfolio needed to implement the idea.
