# Σ Case study — Genetic-programming US equity XS alpha (killed by a pre-registered holdout)

**The discipline showcase.** A signal that was good in two independent samples,
placebo-clean, with a real Fama-French-6 alpha — and I killed it anyway, because
a holdout I had committed to *before looking* said no.

---

## The pitch

A vectorised symbolic genetic-programming engine evolves cross-sectional alpha
expressions on a **survivorship-correct, point-in-time** US equity panel. The
best evolved signal looked like the real thing:

- In-sample Sharpe **0.50** → out-of-sample Sharpe **0.71** (it got *better* OOS).
- **Fama-French-6 alpha 7.2%/yr** — not just beta, residual alpha after the six
  standard factors.
- **Placebo-clean**: random-label permutations produced nothing.

Two samples agreeing, a positive factor alpha, and a clean placebo. By most
retail and a lot of professional standards, this is a deploy.

## Why I killed it anyway

### 1. Deflation

The genetic program searched **6,769 genomes**. Charge the deflated Sharpe for
that, and the DSR collapses from **0.959 at one trial** to **0.234 at 6,769
genomes**. Below the 0.50 gate. A signal evolved out of thousands of candidates
must clear a much higher bar than a single pre-specified idea.

### 2. The pre-registered blind holdout (the real kill)

Before I ran the genetic program, I had **walled off 2020-2025** and written down,
in advance, the single test the winner would face. One shot, no peeking, no
re-runs. When the winning signal met that holdout:

> **Gross Sharpe on the blind 2020-25 holdout: 0.03.**
> Net negative. Factor alpha t-statistic 0.09.

The edge **vanished**. Even framed at N_trials = 1 — i.e. giving it the maximum
possible benefit of the doubt, with no deflation penalty at all — the
pre-registered holdout did not rescue it. The 2-sample agreement was a
**sample-period artifact**, not a robust alpha. The discipline caught a signal
that was *lucky in two correlated samples* and would have lost money live.

## Why this is the most important case in the graveyard

Everything else here failed a metric. This one **passed several** and still got
killed, because I had **pre-committed** to a blind test and **honoured it when it
hurt**. The holdout is now spent — it can never be used again, which is the whole
point of pre-registration.

| Metric                         | Value | Gate    | Verdict |
|--------------------------------|-------|---------|---------|
| OOS Sharpe (in-sample split)   | 0.71  | —       | looked real |
| FF6 alpha                      | 7.2%/yr | —     | looked real |
| DSR after 6,769 genomes        | 0.234 | ≥ 0.50  | FAIL    |
| Pre-registered holdout Sharpe  | 0.03  | > 0     | FAIL    |
| Holdout alpha t-stat           | 0.09  | —       | FAIL    |

## Data and reproducibility

Built on a **licensed academic point-in-time panel** (CRSP/Compustat via WRDS),
which is **not** included in this repo (academic terms of use). The reusable
asset is the **engine**: a numpy/numba vectorised cross-sectional symbolic-GP
core and the survivorship-correct panel-construction methodology. Published here
as method and summary statistics only.

## Lesson

A signal that is good in two samples is a signal that is good in two **correlated**
samples until a truly out-of-sample, **pre-registered** test says otherwise.
Deflation handles the search; pre-registration handles you. Write the holdout
test down before you look, and **honour it when it hurts** — that is the entire
difference between research and storytelling.
