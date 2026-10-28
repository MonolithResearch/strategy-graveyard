# Evidence, provenance and reproduction

## What is public

The CSV is a manually curated historical summary. It includes metrics from
different experiment designs and dates, plus descriptions and retrospective
verdicts. It is not a uniform panel of independently reproduced results.

The public base is commit `a883c442b6e8b6b169f7a0cba95936bab7bf750d`.
The five-row expansion and initial drafts of case studies 07/08 came from the
previously unpublished local branch ending at
`4c921ddc7f425ca0722957fc76d0a09f21a63ba9`. The 2026-10-28 publication rewrites
the presentation and tests instead of importing that branch's Git ancestry.

## Underlying research record

The private Monolith research snapshot examined was
`4ee675385b3db8efa499009150107f6f8d56b963`. Relevant logical source paths include:

- `57_alpha_factory_2026_06_19/RESULTS_LOG.md`: the resolved 2026-06-20 CEF
  execution-lag discussion and separate cost-specification corrections.
- `57_alpha_factory_2026_06_19/STRATEGY_GRAVEYARD.md`: historical vol-spread,
  earnings-announcement, institutional-crowding and short-interest summaries.

These references identify the source record; they do not provide public access to
licensed return panels. No raw CRSP/Compustat, OptionMetrics, order-book or account
records are included. A public reader can check the summary consistency and
demonstration, but cannot independently reconstruct the underlying market studies
from this repository alone. Numerical uncertainty and later superseding research
must not be hidden by describing these summaries as fresh validated outcomes.

Case 07 records a small historical top-250 OOS reporting discrepancy explicitly.
The CEF note keeps distinct cost/lag experiments distinct. Its mechanism language
is an interpretation, not a causal identification result.

## Corrections in this publication

- Added the five historical rows and two case studies. Preserved the original
  numeric CSV fields while quoting four previously malformed narrative fields.
- Replaced assertions of a current private live winner with the actual scope:
  historical research and synthetic demonstrations. Other historical articles
  remain dated records, not present operational attestations.
- Separated the three-input numeric screen into **2 complete failures**,
  **37 incomplete records**, and **0 passes**. A documented case-study rejection
  and a complete numeric gate failure are different statements.
- Replaced the demo's leave-one-block calculation with actual combinatorially
  symmetric half-block enumeration. Midranks handle OOS ties; tied IS winners
  contribute equally; an exact median tie is included in the overfit count.
  Even block counts, finite data and exact divisibility are required. No partial
  rows are silently discarded and no full-sample performance shortlist is used.
- The demo's PBO concerns a small fixed subset of simulated candidates. It is not
  the PBO of the larger search used for the illustrative DSR calculation. The CLI
  therefore emits no promotion verdict.
- Removed embedded account-identifier fragments from a legacy test. Generic
  credential-marker checks do not constitute a comprehensive secret audit.

## Decisive checks

`python scripts/audit_dataset.py` reports row coverage and a SHA-256 of the exact
CSV bytes. `python -m pytest -q` includes an independently written CSCV reference,
malformed-input cases, complete/missing evidence cases, and command execution from
an unrelated directory. `python scripts/demo_validation.py` runs only generated
Gaussian examples. `python scripts/make_graveyard_chart.py` redraws the summary.

The CSCV definition is based on Bailey et al.,
[The Probability of Backtest Overfitting](https://escholarship.org/uc/item/4w1110bb).
The DSR approximation follows Bailey and Lopez de Prado,
[The Deflated Sharpe Ratio](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).
The small demonstration is educational, not a replacement for a complete research
protocol or independently audited performance.

Fresh command results, review responses and publication details are in
[WORK_LOG.md](WORK_LOG.md). Local recovery backups are intentionally ignored.
