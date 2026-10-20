---
name: return-deposit-bottles
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-20
---

## Goal

Accumulated deposit bottles and cans go back through a return machine (or counter), and the deposit comes back to you as cash or store credit.

## Preconditions

- You're in a deposit-return region (`de` Pfand, nordics, `nl`, many `us`/`ca`/`au` states — the bottle's label/mark says if it carries a deposit).
- A bag of *eligible* containers: deposit-marked, empty, uncrushed (machines read the barcode and shape — a crushed can is a rejected can).
- A store with a return machine, usually one that sells the containers' type.

## Steps

1. **Sort eligible from ineligible at home.** Deposit logo/mark present, barcode intact, container empty and roughly rinsed (machines and their rooms smell of everyone who skips this). → *Expect:* a bag of machine-ready containers; juice cartons and unmarked glass left out.
2. **Find the return machine.** Usually near the store entrance or a dedicated room. → *Expect:* a machine with a round feed hole, a display, and a receipt button; note any posted limits (some cap counts or accept only what the store sells).
3. **Feed containers one at a time, barcode roughly along the roller.** The machine rotates and scans each; rhythm beats speed. → *Expect:* per-container beep + count/value ticking up on the display; rejected ones come back — set them aside, keep feeding (F1 handles the rejects after).
4. **Retry rejects once, correctly oriented and un-dented.** Gently reshape a dented can's barcode zone; a second rejection means the machine doesn't take it (foreign barcode, non-deposit, unreadable) — into your recycling stream instead (`daily/home/sort-recycling`). → *Expect:* every container either counted or consciously reclassified.
5. **Press the receipt/finish button.** ⚠️ *Irreversible-ish:* walking away without pressing it donates your total to the next person. → *Expect:* a printed voucher showing the total.
6. **Redeem the voucher at the checkout.** Cash out, or apply it against your groceries (`daily/errands/buy-groceries` synergy: bring bottles, leave with dinner partially paid). Vouchers often expire and are store-specific — redeem today. → *Expect:* deposit value in hand or off your bill.

## Decision points

- Machine out of order / full → the customer-service counter usually takes returns manually, or another branch; don't abandon the bag in front of the machine.
- Large hauls (post-party crates) → off-peak hours, and check the machine's crate slot — whole crates feed through a lower door in many systems.
- Not worth your time? → in many cities, leaving sorted deposit containers *visibly beside* (not in) a public bin is a recognized courtesy to collectors — better than binning value.

## Failure modes & recovery

- **F1 High rejection rate:** usually crushed barcodes or a foreign purchase (deposits are national systems) — reshape and retry once each; the rest is recycling, not a machine argument.
- **F2 Machine jammed mid-bag:** press the call/help button or tell staff; don't reach into the feed roller — your count so far is preserved on the display/receipt.
- **F3 Voucher lost before checkout:** small loss, honest lesson: redeem immediately after printing next time; staff can sometimes reprint if the machine log matches your story, but don't count on it.

## Verification

Every container is counted, redeemed, or reclassified to recycling; the voucher's total made it into cash or your grocery bill; and no crushed rejects went back home with you.

## Variations

- `de` Pfand: 0.25 €/single-use plastic — totals add up fast; `nordics`: similar machine culture; `us` bottle-bill states (MI, OR, CA…): counts and redemption venues vary, some via counters not machines.
- Reverse-vending with app payout (newer machines): scan your app's QR instead of printing a voucher — the redeem-today problem disappears.

## Safety & privacy

Low risk. Rinse the bag's contents (hygiene for you and the room), never reach into a jammed feed, and mind glass — a broken bottle in a carry bag is `embodied/carry-and-deliver-an-item` F2 waiting to happen.
