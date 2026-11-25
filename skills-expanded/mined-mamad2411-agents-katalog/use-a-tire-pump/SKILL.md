---
name: use-a-tire-pump
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

Use an air pump to bring a vehicle tire to the manufacturer's recommended pressure without overinflating it.

## Preconditions

- The vehicle is parked safely away from traffic with the parking brake set.
- Tires are cold if possible, parked for 3 hours or driven less than about 1 mile.
- You have access to a tire pump, the valve caps, and ideally a separate pressure gauge.
- The tire is not visibly flat, shredded, or separated from the rim.

## Steps

1. **Find the PSI target.** Open the driver's door and read the tire placard on the door jamb, not the tire sidewall maximum. → *Expect:* the correct front and rear PSI values are known.
2. **Park close enough to the pump.** Position the car so the hose reaches the tire without stretching across a walkway or traffic lane. → *Expect:* the hose reaches the valve comfortably.
3. **Remove the valve cap.** Put it in a pocket or cup holder so it does not roll away. → *Expect:* the valve stem is uncovered and the cap is secure.
4. **Attach the chuck squarely.** Press or clamp the pump chuck straight onto the valve until the loud hiss stops. → *Expect:* the chuck stays seated and air is not leaking around it.
5. **Read the current pressure.** [BRANCH: built-in gauge | handheld gauge] use the pump gauge or briefly remove the chuck and check with your own gauge. → *Expect:* you know how far the tire is from target.
6. **Inflate in short bursts.** Add air for 3 to 5 seconds at a time, then pause. → *Expect:* the pressure rises gradually instead of jumping past the target.
7. **Check after each burst.** Re-seat the gauge if the reading seems unstable or the hose hissed during inflation. → *Expect:* the reading approaches the door-jamb PSI.
8. **Stop at the target.** Do not keep adding air for a cushion above the placard value. → *Expect:* the tire is at the listed PSI or within about 1 PSI.
9. **Bleed if needed.** If the tire is high, press the valve pin briefly and recheck. → *Expect:* pressure drops slowly back to target.
10. **Replace the cap and repeat.** Screw the cap on finger tight, then move to the next tire. → *Expect:* all adjusted valves are capped.

## Decision points

- The pump has a preset PSI mode → set the door-jamb value for that axle and still verify afterward.
- The tire is more than 10 PSI low → inflate enough to drive slowly, then inspect for a puncture before normal driving.
- The valve keeps hissing with the chuck attached → remove and reattach squarely instead of holding it at an angle.
- The tire is warm from driving → use the placard as a temporary target and recheck cold later.

## Failure modes & recovery

- **F1 Overinflated tire:** detect by a reading above the placard PSI → recover by bleeding air in short taps and rechecking.
- **F2 Leaking chuck connection:** detect by constant hiss and no pressure increase → recover by reseating the chuck straight on the valve.
- **F3 Missing valve cap:** detect after the hose is removed → recover by installing a spare cap to keep dirt out.
- **F4 Tire will not hold air:** detect by pressure falling during or soon after inflation → recover by avoiding highway driving and getting the tire repaired.

## Verification

Every serviced tire matches its door-jamb PSI target within about 1 PSI, has a valve cap installed, and is not audibly leaking.

## Variations

- Gas-station coin pump: check the time limit before starting so you can reach all tires.
- Portable 12-volt inflator: keep the engine running outdoors if the manual requires it to protect the battery.
- Dual rear wheels: use a long chuck or extension designed for inner valve stems.

## Safety & privacy

Low risk when the tire is intact. Do not exceed the door-jamb pressure, keep hands and hose clear of moving traffic, and do not try to inflate a tire with sidewall damage or a bead separated from the rim.
