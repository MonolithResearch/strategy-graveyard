# Σ Case study — Order-flow imbalance + DeepLOB (real foresight, below the cost bar)

**Tier 3 — Overfit / sign-flips at cost.** In-sample Sharpe **10.81** → net Sharpe
**-14.63** at 3× cost over **2,264** trades. DSR **≈ 0** vs selection-max 0.78.

---

## The pitch

A deep convolutional network (DeepLOB-style) trained on a real exchange
limit-order book (a major EUR FX future) plus an order-flow-imbalance (OFI) feature.
The model genuinely **predicts the next mid-price move** — in-sample Sharpe is an
absurd **10.81**, and even the raw OOS classification accuracy is real.

This is the most seductive failure in the graveyard, because **the foresight is
real.** The signal is not noise. The model has learned something true about
short-horizon order-book dynamics.

## Why it still dies

The edge per trade is about **+1.3 basis points gross**. That is genuine
predictive content. But:

1. **The strategy trades 2,264 times.** Microstructure signals decay in
   milliseconds, so you must trade constantly to harvest them.
2. **The realistic round-trip cost (spread + fees, charged at 3× to stress it)
   exceeds 1.3bp.** Every trade pays more to cross the book than the foresight is
   worth.

Net of cost, the +1.3bp gross becomes a catastrophic **-14.63 Sharpe**. The
deflated Sharpe is **~0** against a selection-max of 0.78 — the model is real, the
*tradeable* edge is not.

There is a second, subtler error I had to admit: I initially framed OFI as a
**contrarian** signal. On this book it is a **trend** signal (flow predicts
continuation, not reversal). Getting the sign right improved the gross number —
and changed nothing about the verdict, because the cost wall is the binding
constraint, not the direction.

## What the gate caught

| Metric            | Value   | Gate   | Verdict |
|-------------------|---------|--------|---------|
| In-sample Sharpe  | 10.81   | —      | bait    |
| OOS Sharpe (gross)| 12.69   | —      | real foresight |
| Net 3× cost SR    | -14.63  | > 0    | FAIL    |
| Deflated Sharpe   | ~0      | ≥ 0.50 | FAIL    |

## Data and reproducibility

The model was trained on **licensed exchange LOB data**, which is **not** included
in this repo (commercial terms of use). Only methodology and summary statistics
are published here. The companion repo ships a PyTorch DeepLOB implementation
that runs on small **synthetic** order-book samples so the architecture is
inspectable without the proprietary feed.

## Lesson

"Does the model predict?" and "Can I trade it?" are different questions. A
microstructure signal can be **genuinely predictive and still uninvestable** when
the per-trade edge is smaller than the per-trade cost. Always charge a stressed
(here 3×) cost before believing a high-turnover Sharpe. The cost bar, not the
R², decides.
