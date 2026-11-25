---
name: use-a-coin-or-air-pump
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

Inflate car tires at a coin or station air pump to the correct cold tire pressure without overinflating.

## Preconditions

- You know the recommended PSI from the driver's door jamb sticker or owner's manual.
- You have coins, card, or app payment if the pump charges.
- Tires are not visibly shredded, flat from sidewall damage, or unsafe to inflate.
- You can park close enough for the hose to reach all tires.

## Steps

1. **Find the correct PSI.** Read the door jamb sticker, not the maximum PSI molded on the tire sidewall. → *Expect:* you know the front and rear target pressures.
2. **Park near the pump.** Pull close enough for the hose to reach all tires and set the parking brake. → *Expect:* the car is stable and the hose reaches at least the nearest tire.
3. **Set the pump if digital.** [BRANCH: preset pump | manual gauge] enter the target PSI on a preset pump, or keep your own gauge ready for manual filling. → *Expect:* the pump is ready to inflate to the chosen pressure.
4. **Remove the valve cap.** Unscrew the cap and place it in a pocket or safe spot. → *Expect:* the valve stem is exposed and the cap is not lost.
5. **Attach the chuck firmly.** Press the air chuck straight onto the valve stem until leaking air stops. → *Expect:* the hose connection seals with little or no hiss.
6. **Inflate in bursts.** Add air for short bursts, then pause for the gauge or pump reading. → *Expect:* pressure rises gradually toward the target.
7. **Check and adjust.** Remove the chuck, check PSI, add more air or press the valve pin briefly to release excess. ⚠️ *Irreversible:* driving on badly overinflated or underinflated tires can reduce control, so correct pressure before leaving. → *Expect:* the tire reads at the recommended PSI.
8. **Replace the cap and repeat.** Screw the cap back on and repeat for each tire, including the spare if accessible. → *Expect:* every checked tire has a cap and target pressure.

## Decision points

- The pump gauge disagrees with your handheld gauge → trust a known good handheld gauge.
- Air leaks around the chuck → reposition it straight on the valve stem.
- The tire will not hold air → stop driving far and seek tire repair.
- The tire is hot from highway driving → use the placard as a guide, then recheck cold later.
- The hose will not reach all tires → move the car carefully before time expires.

## Failure modes & recovery

- **F1 Lost valve cap:** detect by missing cap after inflation, recover by replacing it soon to keep dirt out of the valve.
- **F2 Overinflation:** detect by PSI above target, recover by pressing the valve pin briefly and rechecking.
- **F3 Pump timeout:** detect by compressor stopping before all tires are done, recover by paying again or moving to another pump.
- **F4 Damaged valve stem:** detect by hissing at the stem after removing the chuck, recover by installing the cap and going to a tire shop promptly.

## Verification

Each tire you intended to inflate reads the door-jamb PSI and has its valve cap installed.

## Variations

- Nitrogen tire fill: ordinary air can still be used when pressure is low.
- Bicycle-style small pump: inflate longer and verify with a separate gauge.
- Tire-pressure monitoring system: the dashboard warning may take a short drive to clear.

## Safety & privacy

Do not inflate a visibly damaged tire, stand in traffic, or use sidewall maximum pressure as the target. Payment kiosks may expose card data, so prefer tap or coins when available.

