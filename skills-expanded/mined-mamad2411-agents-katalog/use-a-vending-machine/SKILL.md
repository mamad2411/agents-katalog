---
name: use-a-vending-machine
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 5min
risk: low
prerequisites: [have-payment-method]
status: draft
last_verified: 2026-07-20
---

## Goal

The item you wanted drops, you retrieve it plus any change, and you walk away — even the stuck-spiral scenario handled correctly.

## Preconditions

- A powered vending machine stocked with something you want.
- Accepted payment: coins/small notes, contactless card/phone, or the machine's app/QR system.

## Steps

1. **Survey the machine's state before paying.** Item in stock (visible product, or the slot not flagged "sold out"), price noted, payment types listed on the reader. → *Expect:* your item visibly available at a known price; a payment path you can satisfy.
2. **Pay.** [BRANCH: coins/notes → feed them flat and unwrinkled | contactless → tap when the reader wakes | QR/app → scan and authorize] → *Expect:* credit displayed on screen equal to what you provided, or reader showing approval.
3. **Select the item by its code.** Punch the letter-number (e.g., "B4") exactly as labeled *under* the item you want — not the neighbor's. Verify the display echoes it. → *Expect:* display shows your code; the spiral/pusher for that slot begins turning.
4. **Watch the drop.** → *Expect:* item falls to the retrieval bin. Wobbling-but-hanging → F1; nothing moved at all → F2.
5. **Retrieve the item and your change.** Push the flap, take the item; check the coin-return cup. → *Expect:* item in hand; change matches (paid − price).

## Decision points

- Two of you buying → separate transactions; stacked credits confuse both machines and humans.
- Machine looks sketchy (dark display, taped reader) → find another; prepaying a dead machine is the whole failure class.
- Cold/hot food machines → check the heated/chilled indicator is actually lit before trusting perishables.

## Failure modes & recovery

- **F1 Item hanging on the spiral:** buy the *same slot* again if you want two-for-the-price-of-two-attempts (often knocks both down), or gently bump the machine's flank with a palm — never rock or tilt it: vending machines that tip kill people. Then F3's refund path for the loss.
- **F2 Paid but no vend / no credit shown:** press coin return; if nothing, note the machine's ID and the operator's phone number (stickered on the front), and request the refund — small, but the mechanism exists and works.
- **F3 Wrong item dropped (miskeyed or misloaded):** miskeyed is on you — enjoy the mystery snack; misloaded slot (label ≠ contents) is the operator's — same refund path as F2.
- **F4 Change shorted:** coin return again, then the operator number; card payments auto-settle to the exact price and dodge this whole class.

## Verification

You hold the item you selected, correct change (if cash), and the machine shows an idle display ready for the next person.

## Variations

- `jp`: machines are ubiquitous, reliable, and IC-card (Suica) tap is the norm; hot and cold drinks in the same machine (red = hot, blue = cold labels).
- Office/honor machines with app unlock: your app account statement *is* the receipt — check it if a vend fails.

## Safety & privacy

Low risk with one absolute: never rock or tilt a machine that ate your money — the money has a refund path; a tipping machine doesn't.
