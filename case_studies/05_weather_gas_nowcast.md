# Σ Case study — Weather → gas-storage nowcast (genuine skill, below the cost bar)

**Tier 2 — Real signal, undeployable (funding-grade).** Walk-forward OOS
**R² 0.946** — and still a no-go. Blind-OOS DSR **0.112**, PBO **0.621**, all 10
variants net-negative, placebo p **0.45**.

---

## The pitch

Population-weighted heating- and cooling-degree-days (HDD/CDD) from public
weather data, mapped to weekly US natural-gas storage changes. Predict the
storage print before it is released, trade the gas curve around it.

The nowcast **works**. Walk-forward out of sample, it explains **94.6%** of the
variance in storage changes (R² 0.946). This is real, defensible, genuine
modelling skill — there is no overfitting story to tell here. The model predicts
the fundamental.

## Why it is still not a trade

A great nowcast of a fundamental is worthless if the fundamental is already in
the price. Three walls:

1. **Public weather is already priced.** The correlation between my
   public-weather-driven nowcast surprise and the subsequent gas move is
   **-0.03** — essentially zero. The market has the same free weather data I do
   and has already traded it. The information is real; the **edge** is gone.

2. **The genuine edge is licensed.** The institutional desks that *do* extract
   weather alpha use **licensed numerical-weather-prediction ensembles** that beat
   the free models. That data is behind a commercial paywall. My free-data
   nowcast is structurally a step behind.

3. **Carry buries the rest.** Gas futures sit in roughly **18%/yr contango**.
   Holding the position to harvest a small storage-surprise edge means paying a
   large roll cost that swamps the signal.

Net result: **all 10 strategy variants are net-negative**, the placebo test is
**p = 0.45** (indistinguishable from noise), PBO is **0.621**, and the deflated
Sharpe is **0.112** — well below the gate.

| Metric                  | Value  | Gate    | Verdict |
|-------------------------|--------|---------|---------|
| Walk-forward OOS R²     | 0.946  | —       | genuine skill |
| Nowcast-vs-move corr    | -0.03  | —       | already priced |
| Blind-OOS DSR           | 0.112  | ≥ 0.50  | FAIL    |
| PBO                     | 0.621  | ≤ 0.20  | FAIL    |
| Placebo p-value         | 0.45   | small   | FAIL    |

## Why it is "funding-grade", not "dead"

This is not a noise strategy — it is a **real modelling result killed by market
structure**, built entirely on free, legal public data. It mirrors the exact
process institutional weather desks run. As a research artifact for a prop-firm
or quant-internship portfolio it is a *strength*: it demonstrates I can build a
genuinely predictive model **and** correctly diagnose why it is not a tradeable
edge — instead of deploying a 0.946-R² mirage.

## Lesson

**R² is not edge.** You can model a fundamental almost perfectly and have zero
tradeable alpha because (a) everyone has the same free inputs, (b) the real edge
sits behind licensed data, and (c) carry/cost eats whatever is left. Predictive
skill is necessary, never sufficient. Always test the *surprise* against the
*subsequent move*, not the level against the level.
