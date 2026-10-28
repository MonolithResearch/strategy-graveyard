# What the rejected experiments taught us

The 39 records in this repository are a historical research notebook in summary
form. They are useful because they preserve why a promising number was not enough.
Their underlying licensed-data experiments are not rerun by the public demo.

## Questions that changed the conclusion

**What was searched?** A high Sharpe after many attempts has a different evidential
meaning from a prespecified test. Deflation depends on an honest trial family,
the dispersion and dependence of trials, and assumptions about returns. It is not
a certificate that a strategy is genuine. The synthetic demo exposes the search
effect without claiming that every noise experiment must be rejected.

**What information was actually available?** Publication lags, revisions and a
mark observed after the decision can invalidate an apparently clean split.
Chronological train/test separation alone does not establish point-in-time validity.

**What caused the return?** A high score may describe ordinary beta, carry or a
tail-risk premium. Exposure analysis and matched baselines are necessary before
calling it incremental predictive value. Retrospective attribution also has
estimation error and should not be treated as an oracle.

**Could the intended portfolio be traded?** Costs must be measured on the traded
universe, with turnover, liquidity, borrow and plausible fills. A liquidity ladder
can reveal concentration in names outside the intended implementation. It does
not, by itself, prove which microstructure mechanism caused that concentration.

**Does the result survive a later fill?** The closed-end-fund case weakened under
beta adjustment and an extra execution lag. That supports rejecting the proposed
implementation. It is consistent with stale marks or short-lived price effects,
but a lag sensitivity test alone cannot identify the mechanism conclusively.

## Several checks, several limitations

A useful sequence is to specify the economic mechanism, audit availability,
declare the search, compare with competent alternatives, model costs and exposures,
and reserve an appropriate confirmation procedure. These tests are complementary;
they are not statistically independent merely because they have different names.

No available field should silently stand in for a missing one. The public dataset
contains two complete three-input numeric screens and 37 incomplete records.
Its case-study verdicts draw on additional historical reasoning. Calling every
row a newly verified failure would overstate the evidence.

## Further reading

- Bailey and Lopez de Prado, [The Deflated Sharpe Ratio](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).
- Bailey, Borwein, Lopez de Prado and Zhu,
  [The Probability of Backtest Overfitting](https://escholarship.org/uc/item/4w1110bb).

The transferable work is the experiment design, implementation and correction
record. The repository does not claim a surviving live strategy.
