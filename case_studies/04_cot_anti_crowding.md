# Σ Case study — COT anti-crowding (momentum wearing a costume)

**Tier 3 — Overfit / sign-flips.** Pooled rank-IC **-0.0106**. Best tertile OOS
**+0.50** → locked holdout **-0.40**. Blind-OOS DSR **0.005**.

---

## The pitch

Commitments-of-Traders (COT) data tells you how speculators and commercials are
positioned. The thesis: when speculative positioning gets crowded, fade it —
trade *against* the crowd ("anti-crowding"). Intuitive, has a behavioural story,
and the best-tertile out-of-sample slice printed a healthy **+0.50 Sharpe**.

## Why it dies

### 1. The pooled signal is already negative

Across the full cross-section, the pooled rank information coefficient is
**-0.0106**. There is no positive relationship between the COT signal and forward
returns at the population level. The +0.50 only existed in a **hand-picked
tertile**.

### 2. The locked-holdout sign-flip — the overfit tell

I locked away a final holdout. The best-tertile slice that scored **+0.50** in
development scored **-0.40** on the locked holdout. A clean **sign flip** of
nearly a full Sharpe point between the slice you selected and the data you had
never touched. That is the textbook overfit signature: the selection found a
pocket of noise, not a structural effect.

### 3. It is momentum in disguise

When I decomposed what the surviving COT "signal" was actually trading, it
reduced to **price momentum**. COT levels are highly autocorrelated and track
recent price moves; ranking on them is a roundabout way of ranking on trend. The
crowding overlay was not reading positioning — it was reading the tape. And
published work (Klitgaard–Weir and others) finds FX order flows from this source
are essentially **published-null**.

| Metric                  | Value    | Gate    | Verdict |
|-------------------------|----------|---------|---------|
| Pooled rank-IC          | -0.0106  | > 0     | FAIL    |
| Best-tertile OOS Sharpe | +0.50    | —       | selection |
| Locked-holdout Sharpe   | -0.40    | > 0     | FAIL (sign flip) |
| Blind-OOS DSR           | 0.005    | ≥ 0.50  | FAIL    |
| Net 3× cost SR          | -0.645   | > 0     | FAIL    |

## Bonus: it explained three earlier ghosts

The crowding decomposition did real work elsewhere: it explained three prior
"reversal" sightings in other lanes as the same momentum-in-positioning artifact.
A dead strategy that diagnoses other dead strategies still earns its place.

## Lesson

**Decompose your signal before you believe it.** A behavioural story (anti-crowding)
can be a re-labelling of a known factor (momentum). When a hand-picked slice
beats the pooled signal and then sign-flips on a locked holdout, you have found
**selection**, not edge. Always ask: "what is this actually trading?"
