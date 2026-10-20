---
name: use-a-coinstar
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Loose coins are converted at a Coinstar-style kiosk into a cash voucher, gift card, or donation receipt.

## Preconditions

- You have loose coins in a container you can pour steadily.
- You have removed non-coins, foreign coins, batteries, screws, wrappers, and sticky debris.
- You know whether you prefer cash with a fee or a no-fee gift card option if available.
- The store has a working kiosk and a service desk or checkout that redeems vouchers.

## Steps

1. **Pre-sort obvious junk.** Spread coins on a tray or table and remove anything that is not a valid local coin. → *Expect:* no sharp, sticky, or foreign objects are mixed in.
2. **Find a working kiosk.** Check the screen, coin tray, reject slot, and printer area before starting. → *Expect:* the kiosk is on and not showing out-of-service.
3. **Choose the payout type.** [BRANCH: cash voucher with fee | gift card with no fee if offered | charity donation] → *Expect:* the screen shows the fee or no-fee terms before counting.
4. **Accept the terms.** Read the percentage fee and redemption instructions, then continue only if acceptable. → *Expect:* the machine is ready for coins.
5. **Pour slowly.** Tip coins into the tray at a steady rate instead of dumping the whole container at once. → *Expect:* coins feed without backing up or spilling.
6. **Check rejects.** Pull rejected coins from the return slot, wipe dirty coins, and feed valid ones once more. → *Expect:* only unreadable, foreign, or damaged coins remain rejected.
7. **Finish counting.** Tap done only after the tray and return slot are empty. → *Expect:* the final total appears on screen.
8. **Print and redeem.** Take the voucher or gift-card code and redeem it at the register or keep it as instructed. ⚠️ *Irreversible:* once printed or donated, payout type usually cannot be changed; confirm the total and option first. → *Expect:* you receive cash, a gift card claim, or a donation receipt.

## Decision points

- If the fee is too high, stop before accepting and use bank coin deposit if your bank offers it.
- If the kiosk sounds jammed or stops counting, pause and ask store staff rather than shaking it.
- If you have collectible coins, sort them before using the machine because the kiosk pays only face value.
- If the voucher says same-day redemption, redeem before leaving the store.

## Failure modes & recovery

- **F1 Machine rejects many coins:** detect repeated returns, recover by removing dirty, foreign, or damaged coins and feeding slower.
- **F2 Voucher does not print:** detect no paper after finalizing, recover by noting kiosk ID and asking store staff immediately.
- **F3 Fee surprise:** detect lower cash total than coin total, recover by canceling before final confirmation next time.
- **F4 Spill on floor:** detect coins scattered, recover by stopping the feed, collecting coins, and checking under the kiosk.
- **F5 Register cannot redeem:** detect cashier rejection, recover by going to customer service with the voucher and kiosk location.

## Verification

You leave with cash, a valid gift-card claim, or a donation receipt matching the kiosk's printed final total after any stated fee.

## Variations

- Bank lobby coin machines: account holders may avoid fees but may need a debit card or teller deposit.
- Gift card payout: availability varies by kiosk and may require email or printed claim code.
- High-volume coins: use smaller containers so the pour rate stays controlled.

## Safety & privacy

Low risk. Keep the voucher private like cash, do not put batteries or sharp debris into the machine, and confirm fees before committing.
