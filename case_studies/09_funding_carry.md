# Funding carry with a missing hedge return

**Historical outcome.** The July 2026 rebuild withdrew the original excess-over-cash Sharpe. A spot position paired with a short perpetual contract can collect funding, but its daily P&L also depends on the price changes of both legs.

## Where the apparent carry came from

The coverage check found that the price requests stopped after 1,000 daily observations, in September 2023. Funding observations continued. The backtest aligned those histories and filled the missing hedge returns with zero. On an affected day the recorded portfolio could collect a funding payment even though neither price leg supplied the return needed to value the trade.

Zero is an economic assumption here. It says that the missing hedge contributed exactly nothing, regardless of how the difference between spot and perpetual prices moved.

## What the rebuild measured

The rebuild paginated the price histories, required spot, perpetual and funding observations for each day, and used dates common to the basket. Its cost model allowed four fills per completed round trip across the two legs. The internal July 9 rebuild, frozen as of July 1, reported **net excess-over-cash Sharpe 1.06**. Both coverage and accounting changed, so the record cannot attribute the whole revision to one line of code.

The July 10 review interpreted the residual carry as a **risk premium**. The basket was fixed using surviving assets, and counterparty and liquidation risks remained unresolved. That reconstruction supplies no independent evidence of alpha.

## Lesson

Make a return conditional on observing every cash flow and price leg needed to compute it. Compare the dates of the last valid price and funding observation before aggregating daily P&L. A complete funding column can hide an incomplete portfolio.

**Dated evidence.** The funding-carry lane's `README.md`, rebuilt 2026-07-09, records the coverage diagnosis and replacement series. `STRATEGY_LOGIC_HUNT_2026-07-10.md`, dated 2026-07-10, records the withdrawal and interpretation.
