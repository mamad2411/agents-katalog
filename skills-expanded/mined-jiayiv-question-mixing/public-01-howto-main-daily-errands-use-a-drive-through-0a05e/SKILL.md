---
name: use-a-drive-through
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Food or drink is ordered, paid for, received, and checked without holding up the line or leaving with the wrong items.

## Preconditions

- You are in a vehicle that can safely move through the lane.
- You know the general restaurant or menu category you want.
- You have payment ready.
- Passengers are seated and distractions are controlled.

## Steps

1. **Enter the correct lane slowly.** Follow arrows, clearance signs, and lane markings. → *Expect:* your vehicle is aligned with the menu board and not blocking cross traffic.
2. **Review the menu before the speaker.** Decide main items, sizes, drinks, sauces, and substitutions while waiting. → *Expect:* you can order in a clear sequence.
3. **Pull to the speaker.** Stop with your window near the microphone and turn down music or fans. → *Expect:* you can hear the greeting and be heard.
4. **Order clearly.** Say each item with size, quantity, modifications, and drink, pausing for confirmation. → *Expect:* the screen or employee repeats the order accurately.
5. **Fix errors before moving.** [BRANCH: screen correct | screen wrong] proceed, or politely correct the item, size, sauce, or quantity. → *Expect:* the final total matches the intended order.
6. **Have payment ready.** Put card, cash, phone wallet, coupon, or app code within reach before the window. ⚠️ *Irreversible:* submitting payment finalizes the order in many systems, so confirm the total before paying. → *Expect:* payment can be handed over without searching.
7. **Collect drinks and food securely.** Place drinks in cup holders and hot bags on a flat surface or passenger's hands. → *Expect:* nothing spills when the vehicle moves.
8. **Check the bag before leaving the lot.** Pull into a safe spot if needed and verify main items, drinks, sauces, utensils, and receipts. → *Expect:* mistakes are found while the restaurant can still fix them.

## Decision points

- You need time to decide → say "One moment, please" before ordering.
- The line splits into two speakers → follow staff instructions and merge politely by turn.
- A passenger is ordering → have one person speak or repeat the whole order cleanly.
- Something is missing after pickup → park and go inside or return to the window if directed.

## Failure modes & recovery

- **F1 Speaker misunderstanding:** detect wrong screen or repeated confusion → slow down, give item numbers if shown, and confirm again.
- **F2 Payment not ready:** detect searching at the window → move cards or cash to a safe reachable spot before joining next time.
- **F3 Spill risk:** detect loose cups or overfilled carrier → ask for a carrier, napkins, or lid adjustment before driving.
- **F4 Missing item:** detect wrong or absent food in the bag → keep the receipt and ask staff to correct it before leaving.

## Verification

Before driving away from the restaurant area, the bag and drinks match the receipt and requested sauces, utensils, or substitutions are present.

## Variations

- `mobile-order-pickup`: give the pickup name or code and confirm the bag label before leaving.
- `cash-payment`: count change before pulling away from the payment window.
- `large-order`: park and go inside if the order is complicated or likely to block the lane.

## Safety & privacy

Low risk. Keep the vehicle in park at windows, watch pedestrians and curbs, and do not read an app or unwrap food while driving. Payment cards and phone screens are briefly visible to staff.
