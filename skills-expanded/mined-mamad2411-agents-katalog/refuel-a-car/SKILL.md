---
name: refuel-a-car
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: medium
prerequisites: [have-payment-method]
status: draft
last_verified: 2026-07-20
---

## Goal

The car's tank is filled with the *correct* fuel, paid for, and you drive off with the cap closed and nothing on fire.

## Preconditions

- You know the car's fuel type (petrol/gasoline grade or diesel — it's inside the fuel-door flap and in the manual) and which side the filler is on (the pump icon's arrow on the dashboard fuel gauge points to it).
- A payment method; some stations are prepay/card-at-pump only.

## Steps

1. **Pull up with the filler side toward the pump; engine off.** No smoking, and leave the phone call for later — attention, not radiation, is the real reason. → *Expect:* filler flap within hose reach; engine and cabin ignition sources off.
2. **Open the fuel door and uncap.** Release lever/button inside the car if it has one; hang or rest the cap per its tether. → *Expect:* open filler neck.
3. **Authorize payment.** [BRANCH: card/phone at the pump → follow the screen | prepay inside → tell the cashier the pump number and amount | attended station → state fuel + amount and let them work] → *Expect:* pump display resets to zero and shows "ready"/lifts to live.
4. **Select the correct fuel and lift that nozzle.** Diesel nozzles are usually larger and color-coded differently — the *label*, not the hose color, is the truth. ⚠️ *Irreversible:* pumping the wrong fuel (especially petrol into diesel) means do-not-start-the-engine and a drained tank — triple-check the label against the flap sticker. → *Expect:* nozzle in hand matching the car's required fuel exactly.
5. **Insert the nozzle fully into the filler neck and squeeze; latch if fitted.** → *Expect:* fuel flowing, counter running; stay at the nozzle — this is not the moment to wander inside.
6. **Stop at the auto-click.** The first click means full — do not round up with extra squeezes ("topping off" floods the vapor system and spills). → *Expect:* flow stopped by itself; counter shows the final amount.
7. **Return the nozzle, cap the tank until it clicks, close the flap.** → *Expect:* cap clicked (a loose cap triggers the check-engine light later); flap flush.
8. **Collect the receipt and depart.** Prepay-inside stations: settle up if you pumped an open amount. → *Expect:* paid in full; receipt if wanted; pump area left as found.

## Decision points

- Grade choice (regular vs premium petrol) → use the octane the manual requires; premium in a regular-spec car buys nothing.
- Tank on the far side from the only free pump → hoses often reach across the car; otherwise wait — dragging a hose over paint is a bad trade.
- Static-prone dry days → touch bare metal (the car door) before re-gripping the nozzle after getting in and out of the car mid-fill (best: don't re-enter the car mid-fill at all).

## Failure modes & recovery

- **F1 Wrong fuel realized before starting the engine:** stop, do NOT turn the key — push the car aside with help; the tank must be drained (roadside service does this routinely). Realized *after* starting: stop the engine immediately and call it in; running spreads the damage.
- **F2 Small spill/overfill splash:** stop the nozzle upright, alert staff (they have absorbent), rinse skin, and keep ignition sources away until it's handled.
- **F3 Pump won't authorize your card:** try inside with the pump number; foreign cards often need the cashier path.
- **F4 Drove off with the filler cap on the roof:** common enough that caps are sold separately — retrace or buy a matching replacement; drive is safe, the light may nag.

## Verification

The pumped fuel type matches the flap sticker, the auto-click ended the fill with no topping-off, the cap clicked shut, payment is settled, and the gauge reads full as you pull away.

## Variations

- Full-service regions/stations: you state fuel and amount and stay in the car — verification compresses to "correct fuel stated, cap confirmed."
- EV drivers: the analogous recipe is charging — different enough (connectors, apps, sessions) to be its own file.

## Safety & privacy

Medium risk: fuel is the hazard — engine off, no flames, stay at the nozzle, ground static, and treat the wrong-fuel ⚠️ as the expensive mistake it is. Card skimmers exist at pumps: give the reader the same one-glance wiggle test as an ATM.
