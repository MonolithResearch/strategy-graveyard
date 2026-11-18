# Portfolio publication work log — 2026-10-28

## Scope and custody

User requested an internship-oriented GitHub expansion using orchestration.
Work started from public main `a883c442b6e8b6b169f7a0cba95936bab7bf750d`
in a separate clone. Original research and showcase checkouts were preserved.
The unpublished local expansion ending at `4c921dd` supplied five new summary
rows and two initial case-study drafts. No private research ancestry was merged.
Every existing file rewrite was preceded by a verified, dated sibling backup;
backups are ignored and excluded from publication.

## Changes

- Expanded 34 historical summary records to 39 and six case studies to eight.
- Corrected unquoted narrative commas in four inherited CSV rows, preserving
  their numeric fields; added a schema and numeric-domain audit.
- Distinguished 2 complete numeric failures from 37 incomplete gate records.
  Removed unsupported current-live claims and certainty about DSR/causality.
- Replaced the demo's mislabeled leave-one-block routine with actual symmetric
  half-block CSCV, equal contribution for tied training winners, OOS midranks,
  and explicit input and workload limits. PBO uses fixed candidate membership
  selected without full-sample performance; its subset scope is explicit.
- Added reproducible checks, a Linux CI workflow, provenance notes, two corrected
  case studies, an explanatory essay and a regenerated, visually inspected chart.
- Removed embedded account-identifier fragments from an inherited test.

## Observed local verification

Python 3.14.3 on Windows; no dependency installation during this work.

1. Public-base baseline: 9 tests passed.
2. Imported expansion reproduced the stale-count defect: 1 failed, 8 passed.
3. New CSCV/invalid-input regressions before implementation: 15 failed, 3 passed.
   Corrected implementation: all 18 passed.
4. Dataset audit rejected the malformed inherited rows. After quoting repair,
   the combined suite passed 41 tests.
5. Independent T3 reviewer reproduced a nonzero-constant floating-point defect:
   roundoff variance could produce an enormous Sharpe and favorable CSCV result.
   Permanent regressions first gave 4 failures and 1 pass; explicit observation
   constancy checks fixed it. Final local suite: **46 passed in 1.88s**.
6. The reviewer's two independent constant-return regressions also passed.

Commands actually run:

```text
py -3.14 -B -m pytest -q -p no:cacheprovider
py -3.14 scripts/audit_dataset.py
py -3.14 scripts/demo_validation.py
py -3.14 scripts/make_graveyard_chart.py
git diff --check
```

Dataset audit: 39 records; 34 DSR values; 2 FAIL, 37 INCOMPLETE, 0 PASS.
Dataset SHA-256:
`6288801680108567d6acc90993b0e6ab19f9d9e4ebd41f94f5066fe059c84eb6`.
All three script commands exited 0. The chart was inspected for labels and clipping.

## Review and limitations

A separate T3 agent independently reviewed the public changes and ran the original
41-test suite, demo, audit and chart. Its public-project finding was the constant
case above, now covered by permanent and independent passing regressions. Local
tests do not certify Linux CI before it executes, and publication review does not
validate the original empirical studies.

The dataset remains historical summary evidence. No licensed market-data replay,
new trading signal, live-system check, capital claim or deployment occurred.
The synthetic demo is educational and deliberately issues no promotion verdict.
See [PROVENANCE.md](PROVENANCE.md) for source boundaries and corrections.

## 2026-11-18 · Timing and accounting corrections

Added the July funding-carry reconstruction and the E4 passive-fill audit.
Each study identifies the dated evidence, the broken assumption and the
scope of the corrected result. Linked both from the index and added the
withdrawal notice above the historical DeepLOB account. The source records
do not supply complete numeric gate inputs for new ranking rows.

Verification used `python -m pytest -q` and `python scripts/audit_dataset.py`.
The audit still reports 39 rows, with 2 complete numeric failures and 37
incomplete records.
