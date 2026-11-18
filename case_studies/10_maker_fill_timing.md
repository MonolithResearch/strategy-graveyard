# The passive quote that knew its own fill

**Historical outcome.** The July 2026 audit withdrew the positive E4 maker screen. It had measured how prices moved after trades classified as passive fills. A favourable move after a putative fill is a markout. To interpret it as a trading result, the order must first have been eligible to fill.

## Reconstructing the decision

The audit followed a single trade event through the calculation. The event determined the alleged fill side and entered the rolling signed-flow signal. The screen then used that updated flow and the same row's imbalance to select which fills to count. By the time the filter could identify a desirable fill, the incoming trade had already occurred.

A passive order must already be resting when the incoming trade reaches it. Conditioning on that trade left no evidence that the selected quote would have been there. Even treating the screen as an upper bound would grant the quoting rule information it could not have had.

## What the correction established

The internal audit corrected the interpretation. The dated record contains no replacement causal P&L for this screen. It calls for a decision from pre-event features, a declared delay before a placement or cancellation takes effect, and a replay that accounts for queue ahead and order size. Only then can each fill and exit be reconciled at an executable price.

## Lesson

For a claimed fill, write down the last event visible to the quoting decision and the first event eligible to fill the resulting order. Here the same event appeared on both sides of that boundary. Changing the post-trade measurement horizon would leave the timing error intact.

**Dated evidence.** `AUDIT_NOTE_20260709_E4_MAKER_CAUSALITY.md`, dated 2026-07-09, traces the event through the fill assignment and signal. `STRATEGY_LOGIC_HUNT_2026-07-10.md`, dated 2026-07-10, confirms the disposition.
