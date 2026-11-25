---
name: use-a-self-checkout
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 10min
risk: low
prerequisites: [have-payment-method]
status: draft
last_verified: 2026-07-20
---

## Goal

Your basket of items is scanned, paid, and bagged at a self-checkout kiosk without triggering the attendant more than the system inherently demands.

## Preconditions

- A basket of items and an operational self-checkout kiosk (screen awake, no "closed" sign).
- A payment method the kiosk takes (many are card-only — check the lane sign if you're carrying cash).
- Roughly know which items lack barcodes (loose produce, bakery) — they take the lookup flow.

## Steps

1. **Start the transaction.** Tap the screen's start button; answer the opening prompts (own bags? loyalty card? — scan the loyalty code *now*, most kiosks won't add it later). → *Expect:* scanning screen active; your bag placed *in the bagging area* if prompted, and acknowledged by the kiosk.
2. **Scan items one at a time, and place each in the bagging area immediately.** Barcode toward the glass/laser; listen for the beep; then set it down in the bagging zone *before* scanning the next — the scale there is watching, and rhythm is what keeps it happy. → *Expect:* beep → item on screen with price → placed → no complaint. A red-screen "unexpected item / please place item" → F1.
3. **Handle barcode-less items via lookup.** Produce: place on the scale, tap Lookup, find the item (or type its code from the sticker/shelf—PLU), confirm the weight-price. Bakery/bulk similar. → *Expect:* item added at a plausible weight and price.
4. **Handle restricted items by design, not surprise.** Alcohol and similar flag for age verification — the light will summon the attendant; have ID ready and just wait. → *Expect:* attendant tap-in, ID glance, transaction resumes.
5. **Verify the item count and total before paying.** Screen list vs. basket-now-empty; kiosks double-beep or miss in ways cashiers don't. → *Expect:* list matches what's bagged; total plausible.
6. **Pay.** Tap/insert card or feed cash; take the receipt (some exits check it). → *Expect:* approval, receipt printed, screen resets to idle.
7. **Take everything.** Bags, receipt, card, and the phone you set down at step 3. → *Expect:* bagging area and shelf empty of your belongings.

## Decision points

- Big cart / lots of produce / a wine bottle → the staffed lane is honestly faster once lookups + verification stack up; self-checkout's advantage is small baskets of barcoded goods.
- Own heavy bag confuses the scale at start → use the kiosk's "own bag" flow, or hold bags off the scale until the end and pack after paying.
- Item won't scan after two tries → don't keyboard-guess the barcode: use lookup by name, or hold it up when you summon help — attendants clear these in seconds.

## Failure modes & recovery

- **F1 "Unexpected item in bagging area" / red light:** almost always rhythm — item placed late, leaned on the scale, or a bag shifted. Reseat the last item squarely, wait a beat; persists → the attendant clears it with a tap (this is routine for them, not an accusation).
- **F2 Double-scan (item listed twice):** most kiosks let you tap the line item → remove, or the attendant voids it; check happens at step 5 by design.
- **F3 Wrong PLU picked for produce (priced absurdly):** void the line via attendant and redo the lookup; paying and fixing at the service desk is the slow path.
- **F4 Card declined:** retry once, alternate card, or convert to cash if the kiosk takes it; else the attendant suspends the transaction so you can sort payment without rescanning everything.

## Verification

Everything from the basket is in your bags, each listed exactly once on a receipt in your hand, the payment cleared, and nothing of yours is left at the kiosk.

## Variations

- Scan-as-you-shop (handheld/app): you scan while picking; the kiosk step becomes pay-only, plus random audit checks — cooperate and it's fast.
- `uk`/`eu` kiosks weigh aggressively; `us` big-box kiosks often relax the scale — the place-immediately rhythm works everywhere regardless.

## Safety & privacy

Low risk. Scan honestly — kiosks are surveilled and "forgotten" items are treated as theft regardless of intent; the machine's job is to be annoying, the attendant's job is to help, and neither is personal.
