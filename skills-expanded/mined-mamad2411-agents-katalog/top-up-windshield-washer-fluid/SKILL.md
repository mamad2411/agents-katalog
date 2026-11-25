---
name: top-up-windshield-washer-fluid
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

You fill the windshield washer reservoir with the correct washer fluid and confirm the sprayers work.

## Preconditions

- The car is parked safely with the engine off, parking brake set, and hood release accessible.
- You have windshield washer fluid suitable for the season, especially freeze-rated fluid in winter.

## Steps

1. **Park and open the hood safely.** Stop on level ground, turn the engine off, set the parking brake, and use the hood prop if needed. → *Expect:* the hood stays open securely.
2. **Find the washer reservoir.** Look for the cap with a windshield spray symbol, often blue. Do not use the coolant reservoir, brake fluid reservoir, or oil fill. → *Expect:* the washer-fluid fill neck is identified.
3. **Confirm it is not coolant.** Coolant reservoirs often have warning labels, pressure caps, colored coolant, and hot-system warnings. Washer fluid is usually a simple flip cap. → *Expect:* you are certain the blue-cap reservoir is for windshield washer fluid.
4. **Open the cap and pour slowly.** Use a funnel if the neck is narrow, and keep dirt out of the reservoir. → *Expect:* fluid enters the washer reservoir without spilling into the engine bay.
5. **Fill to the line or near full.** Stop at the marked fill line if present; otherwise stop before overflowing. → *Expect:* the reservoir is filled without liquid running out.
6. **Close the cap and hood.** Snap the cap shut, remove the bottle and funnel, and close the hood securely. → *Expect:* nothing is left loose under the hood.
7. **Test the washer spray.** [BRANCH: front windshield | rear window] activate the sprayer briefly and check that fluid reaches the glass. → *Expect:* spray hits the windshield or rear window and wipers clear it.

## Decision points

- Weather can freeze → use winter-rated washer fluid, not plain water, because frozen water can crack parts and block lines.
- Reservoir is empty and does not spray immediately → hold the sprayer briefly in short bursts to prime, but do not run the pump continuously.
- Fluid leaks underneath → stop filling and inspect for a cracked reservoir or disconnected hose.
- You cannot identify the reservoir → check the owner's manual before pouring anything.

## Failure modes & recovery

- **F1 Wrong reservoir risk:** detect: cap says coolant, brake, oil, or power steering, recover: do not pour and reidentify the washer symbol.
- **F2 Fluid overflows:** detect: liquid backs up or spills, recover: stop pouring, wipe spills, and close the cap.
- **F3 Sprayer still does not work:** detect: pump sound without spray or no sound at all, recover: check fluid level, nozzle blockage, fuse, pump, or frozen lines.
- **F4 Fluid freezes:** detect: no spray in freezing weather after using water or summer fluid, recover: move the car somewhere warm and refill with freeze-rated fluid once thawed.
- **F5 Nozzle sprays wrong direction:** detect: stream misses the glass, recover: clean or adjust the nozzle gently or have it serviced.

## Verification

The washer reservoir is filled with season-appropriate washer fluid, the cap is closed, and the washer spray reaches the windshield when tested.

## Variations

- `winter`: Use fluid rated below the lowest expected temperature, and do not dilute it unless the label allows it.
- `rear-wiper`: Some vehicles use the same reservoir for front and rear washers, while others route longer lines to the rear.
- `ev`: Washer fluid service is similar, but under-hood layout may be unfamiliar; use the manual.
- `fleet-or-rental`: Use only approved fluid if the vehicle owner specifies supplies.

## Safety & privacy

Medium risk comes from pouring into the wrong reservoir and from poor visibility if washers fail. Washer fluid is poisonous, so keep it away from children and pets, and wipe spills from paint and hands.
