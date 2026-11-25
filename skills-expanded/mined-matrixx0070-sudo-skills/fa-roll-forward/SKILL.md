---
name: fa-roll-forward
version: 1.0.0
description: Build a roll-forward for a fund balance — capital, NAV, investment cost, accruals, or a partner's account — proving beginning balance plus movements equals ending balance and ties to the GL.
author: matrixx0070
tags: [fund-accounting, roll-forward, capital-account, nav, movement, close]
capabilities: []
---

# Roll-Forward

## When to use
Use this to prove the *movement* of a balance across a period — total NAV, partners'/members' capital, a single investor's capital account, investment cost, an accrual, or an allowance — by walking beginning balance through every flow to the ending balance and tying the endpoint to the GL. Roll-forwards are the backbone of the capital statement, the financial-statement movement notes, and every balance-sheet reconciliation that has to show *how* the number changed.

**Not for:** proving a point balance to a source with no movement analysis (use fa-gl-recon) or striking/pricing the NAV itself (fa-nav-tieout). This proves the *walk*, beginning to ending.

## Method
1. **Define the balance and period.** Name the account (fund-level or investor-level), beginning date/balance, and ending date. Beginning must equal the prior period's *proven* ending.
2. **Enumerate the movements** in economic order: capital in (subscriptions/contributions/drawdowns), capital out (redemptions/distributions/returns of capital), income, expenses, realized and unrealized P&L, fees/carry, FX, and reclasses.
3. **Sign each flow.** Contributions and gains increase; redemptions, distributions, expenses, and losses decrease. Decision point: a return *of* capital reduces the capital balance; a return *on* capital (income) flows through P&L — don't conflate them.
4. **Compute the ending balance.** `Beginning + increases − decreases = ending`. Recompute independently.
5. **Tie the endpoint to the GL / register.** Ending roll-forward balance must equal the GL account (fund-level) or the investor register (investor-level). Decision point: if it doesn't tie, a flow is missing or mis-signed — find it before you publish.
6. **Cross-check the pieces.** Sum of all investor accounts must equal fund-level capital; sum of class roll-forwards must equal total NAV.
7. **Present and sign off.** Show the walk, the tie, exceptions, and reviewer.

## Example
Investor A capital account, Q2. Beginning $5,000,000. Movements: subscription 5/1 +$1,000,000; management fee −$22,500; allocated income +$18,000; allocated net gain +$310,000; incentive allocation (carry) −$60,700; redemption 6/30 −$500,000. Ending = 5,000,000 + 1,000,000 + 18,000 + 310,000 − 22,500 − 60,700 − 500,000 = $5,744,800. Ties to the investor register at $5,744,800. Cross-check: sum of all investor endings = fund capital per GL. Signed.

## Pitfalls
- **Beginning balance not equal to prior ending.** Roll-forwards chain; a beginning that doesn't match last period's proven ending imports an error you'll never find inside this period.
- **Mis-signing a flow.** Distributions and redemptions reduce capital; booking a redemption as a positive flips the walk and can still coincidentally "look" plausible.
- **Return of vs return on capital.** A distribution that is a return of capital cuts the basis; treating it as income overstates capital and P&L.
- **Investor accounts not summing to fund capital.** A per-investor allocation error can leave every account slightly wrong while the total still ties — cross-check the sum.
- **Ignoring equalization / carry crystallization.** Series or equalization funds book performance fees at crystallization; omitting the incentive-allocation flow overstates every LP's ending balance.

## Output format
```
Account: <fund/class/investor> | Period: <start–end>
Beginning balance: <$>  (= prior ending: Y/N)
Movements:
  + Subscriptions / contributions     <$>
  − Redemptions / distributions       <$>
  + Investment income                 <$>
  − Expenses / fees                   <$>
  ± Realized / unrealized P&L          <$>
  − Incentive allocation / carry      <$>
  ± FX / reclass / other              <$>
Ending balance: <$>  (independently recomputed: <$>)
Tie: GL / register <$>  [match: Y/N]
Cross-check: Σ investor accounts == fund capital  [Y/N]
Sign-off: <preparer / reviewer / date>
```

## Reference

### The roll-forward identity
`Beginning balance + additions − reductions ± adjustments = ending balance`, and the ending must equal the GL (or the register, for investor-level). This is the standard movement proof for every balance-sheet account that changes over time — capital, NAV, investment cost, accruals, prepaids, allowances, fixed assets, and debt. Auditors test the *flows*, not just the endpoints, because compensating errors in additions and reductions leave the endpoint correct and the account wrong.

### Capital roll-forward (partners'/members' capital)
For a partnership/LLC vehicle, each partner's account walks:
`beginning + contributions + allocated income/gains − allocated expenses/losses − distributions − incentive allocation = ending`. Allocations follow the LPA — pro-rata to capital, or via a distribution waterfall (return of capital → preferred return/hurdle → GP catch-up → carry split). The sum of all partner accounts must equal fund net assets.

### NAV roll-forward (fund level)
`beginning NAV + subscriptions − redemptions + income − expenses ± realized ± unrealized ± FX = ending NAV`. Per-share, capital activity transacted at NAV is neutral to existing holders; the per-share walk is `market P&L + income − expenses` (see fa-nav-tieout for the price bridge).

### Contribution/distribution mechanics
- **Subscriptions/contributions:** cash in, units issued at the dealing-date NAV (open-end) or a drawdown against commitment (closed-end).
- **Redemptions:** units cancelled at NAV, cash out; may carry gates, lock-ups, redemption fees, or holdbacks pending audit.
- **Distributions:** income distributions (return *on* capital, from P&L) vs return *of* capital (reduces basis); recallable distributions in PE can be re-drawn and restore unfunded commitment.
- **Return of capital** reduces the investor's basis and, when it exceeds basis, becomes a gain — track basis separately.

### Commitment / unfunded roll-forward (closed-end funds)
For PE/credit vehicles also roll the commitment: `committed − called (paid-in) = unfunded`, adjusted for recallable distributions that restore unfunded. Paid-in capital and unfunded feed DPI/RVPI/TVPI and the capital-call schedule; a mis-tracked recallable distribution understates future drawdown capacity.

### Equalization and series
Where a performance fee applies, equalization (via equalization credits/debits or series accounting) ensures each investor bears carry only on their own gains above their own high-water mark. The incentive-allocation flow crystallizes on the fee date (period-end, redemption, or year-end) and must appear in the roll-forward; omitting it overstates capital until the next crystallization.
