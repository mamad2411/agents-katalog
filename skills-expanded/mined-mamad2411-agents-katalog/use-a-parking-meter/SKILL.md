---
name: use-a-parking-meter
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

Parking time is paid for the correct space or license plate, within the posted rules, so the vehicle is less likely to receive a ticket or tow.

## Preconditions

- The vehicle is legally parked inside a marked space or zone.
- You have coins, a card, or the required parking app.
- You can read the nearby sign and the meter display.
- You know the vehicle license plate if the meter or app asks for it.

## Steps

1. **Read the curb signs first.** Check days, hours, time limits, permits, loading zones, street cleaning, tow-away rules, and accessible-space restrictions. → *Expect:* you know parking is allowed right now.
2. **Find the correct meter or zone.** Match the space number, stall marker, curb zone, or app zone code to your vehicle. → *Expect:* the meter or app identifier matches where the car is parked.
3. **Check payment options.** [BRANCH: meter | mobile app] use coins or card at the meter, or open the app and enter the zone and plate. → *Expect:* the payment screen or meter display is ready for time selection.
4. **Choose enough time.** Add time for the errand plus walking and checkout delays, staying within the posted maximum. → *Expect:* the display shows an expiration later than your expected return.
5. **Confirm before paying.** Review plate, space, zone, duration, fee, and any convenience charge. ⚠️ *Irreversible:* once submitted, parking payments often cannot be moved to another plate or zone, so check identifiers before paying. → *Expect:* the details match the actual car and curb.
6. **Complete payment.** Insert coins, tap or swipe card, or submit in the app. → *Expect:* the meter shows paid time, or the app shows an active session.
7. **Display proof if required.** Put the receipt on the dashboard only if the machine or sign says pay-and-display. → *Expect:* the receipt is visible from outside, or no display is required.
8. **Set a return reminder.** Set an alarm 5 to 10 minutes before expiration and note whether extensions are allowed. → *Expect:* you have time to return, extend, or move the car.

## Decision points

- Sign says no parking during the current time → move the vehicle before paying.
- Meter is broken → follow posted instructions, try the app, or move if the rules require payment.
- App zone conflicts with the sign or meter → trust the physical posted rule and move if unsure.
- Maximum time is shorter than your errand → choose another space or plan to move the car.

## Failure modes & recovery

- **F1 Wrong zone or plate:** detect mismatch on receipt or app session → start a correct session if needed and save proof for appeal.
- **F2 Card declined:** detect failed payment or no active time → try another payment method before leaving.
- **F3 Meter accepts money but shows no time:** detect unchanged display → photograph the meter, note the number, and move or report as local rules require.
- **F4 Reminder missed:** detect expired time while away → return immediately, extend if allowed, or move the vehicle.

## Verification

The meter or app shows an active paid session for the correct plate, space, or zone, and the expiration time is later than your planned return.

## Variations

- `pay-by-plate`: no dashboard receipt is needed, but the plate must be exact.
- `pay-and-display`: receipt must be visible on the dashboard with the time readable.
- `event-parking`: flat rates and no in-and-out privileges may replace normal meter timing.

## Safety & privacy

Medium risk because mistakes can cost money or lead to towing. Do not stand in traffic while reading signs, and avoid saving payment cards in unfamiliar apps unless you trust the provider.
