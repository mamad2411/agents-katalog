---
name: tip-a-delivery-driver
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Leave a fair delivery tip using cash or the app, with adjustments for effort and conditions.

## Preconditions

- An active or recent delivery order.
- A payment method in the app or small bills for cash.
- Awareness of distance, weather, stairs, and order size.

## Steps

1. **Check whether a service fee is not a tip.** Look at the checkout or receipt line items before assuming the driver receives the fee. → *Expect:* tip amount is a separate line or still unset.
2. **Start from a normal percentage.** Use about 15% to 20% for standard food delivery, with a practical floor for small orders. → *Expect:* the calculated amount is not tiny just because the order was cheap.
3. **Bump for extra effort.** Add more for bad weather, long distance, heavy bags, many drinks, stairs, parking difficulty, or late-night delivery. → *Expect:* the tip reflects driver effort, not only food price.
4. **Choose cash or app.** [BRANCH: cash | app] cash works well at the door if you have bills. app works when contactless or pre-tipping is required. → *Expect:* you have a clear way to hand off or submit the tip.
5. **Set the app tip before delivery when needed.** Some drivers see expected payout before accepting. → *Expect:* the order is less likely to sit unaccepted.
6. **Keep cash visible and ready.** If tipping cash, separate it before the driver arrives. → *Expect:* the handoff does not make the driver wait.
7. **Adjust after delivery only for real service issues.** Missing restaurant items are often not the driver's fault; unsafe behavior or ignored instructions may be. → *Expect:* any change is tied to driver-controlled behavior.
8. **Confirm the final amount.** ⚠️ *Irreversible:* once submitted or handed over, a tip may not be recoverable; check decimal placement and currency first. → *Expect:* the receipt or cash handoff matches your intended amount.
9. **Save the receipt.** Keep the app receipt or note the cash amount if you track spending. → *Expect:* the total cost is visible later.

## Decision points

- Delivery is no-contact → use the app unless you can leave labeled cash safely.
- Order is very small → use a minimum cash amount rather than a strict percentage.
- Weather or distance is unusually bad → increase the tip before the driver accepts if the app allows it.
- Food is wrong but sealed bag was delivered correctly → contact the restaurant or platform, not the driver's tip.

## Failure modes & recovery

- **F1 Service fee confusion:** total seems high but tip is zero, recover by finding the separate tip field.
- **F2 No cash at door:** you planned cash but have none, recover by adding an in-app tip immediately if supported.
- **F3 Decimal mistake:** app shows ten times the intended amount, recover by correcting before final submit.
- **F4 Delayed no-tip order:** order sits unaccepted, recover by adding a visible tip or choosing pickup.

## Verification

The driver receives a separate tip amount you intentionally chose, and the receipt or cash handoff confirms it.

## Variations

- Grocery delivery: tip more for heavy items, stairs, substitutions, and long shopping time.
- Courier package delivery: local norms vary, and some companies discourage cash tips.
- Promo or refunded order: calculate from the pre-discount effort, not only the discounted total.

## Safety & privacy

Medium risk because money is transferred and app ratings can affect workers. Do not expose cash unnecessarily at the door, and avoid using tips to punish problems outside the driver's control.
