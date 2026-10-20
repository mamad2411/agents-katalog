---
name: check-tire-pressure
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

Set each tire to the vehicle maker's recommended cold pressure so the car handles predictably and tires wear evenly.

## Preconditions

- Tires are cold, meaning the car has been parked for 3 hours or driven less than about 1 mile.
- You have a working tire pressure gauge.
- You can access an air pump if any tire is low.
- Valve caps are present or replacements are available.

## Steps

1. **Find the correct PSI.** Open the driver's door and read the tire placard on the door jamb, not the maximum pressure molded into the tire sidewall. → *Expect:* front and rear PSI targets are known.
2. **Remove the first valve cap.** Put the cap in a pocket or cup holder so it cannot roll away. → *Expect:* the valve stem is exposed and the cap is not on the ground.
3. **Press the gauge on squarely.** Push firmly until the hiss stops and the gauge locks a reading. → *Expect:* one clear PSI number appears without continued air leakage.
4. **Compare to the placard.** [BRANCH: low | high | correct] low needs air, high needs a brief bleed, correct moves to the next tire. → *Expect:* you know the needed adjustment for that tire.
5. **Top up low tires in short bursts.** Add air for a few seconds, then recheck with the gauge instead of guessing by tire shape. → *Expect:* the reading rises toward the placard PSI.
6. **Bleed high tires carefully.** Press the valve pin briefly with the gauge nub or a small tool, then recheck. → *Expect:* the reading drops slowly and stays near target.
7. **Replace the valve cap.** Screw it on finger tight only. → *Expect:* the valve is covered and the cap threads are not crossed.
8. **Repeat for all tires, including the spare if accessible.** Note any tire that was much lower than the rest. → *Expect:* all checked tires match the placard within about 1 PSI.

## Decision points

- Tires are warm from highway driving → use the cold placard as the target, but recheck cold later before making fine adjustments.
- The pump gauge disagrees with your handheld gauge → trust the same handheld gauge consistently.
- One tire is 5 PSI or more lower than the others → inspect for a nail, rim leak, or bad valve.
- The placard lists different front and rear values → use the axle-specific value, not one average.

## Failure modes & recovery

- **F1 Gauge leaks while reading:** detect by loud hiss and falling number, recover by reseating the gauge squarely on the valve.
- **F2 Sidewall pressure used:** detect by a value much higher than the door placard, recover by deflating to the vehicle placard value.
- **F3 Lost valve cap:** detect by missing cap after inflation, recover by installing a replacement to keep dirt out.
- **F4 Repeated low tire:** detect by the same tire dropping again within days, recover by getting the tire repaired before a longer drive.

## Verification

Each tire's cold pressure matches the door-jamb placard within about 1 PSI, valve caps are installed, and no valve is hissing.

## Variations

- Bicycle-style pencil gauge: read the number at the edge of the sliding stick.
- Digital gauge: wait for the beep or stable display before removing it.
- Full-size spare: check it monthly because it may not trigger the dashboard warning.

## Safety & privacy

Low risk, but underinflated tires can overheat and overinflated tires reduce traction. Keep fingers clear of dirty valve stems and wash hands after handling tires.
