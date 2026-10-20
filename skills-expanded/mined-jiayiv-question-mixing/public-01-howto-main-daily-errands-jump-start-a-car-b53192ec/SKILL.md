---
name: jump-start-a-car
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: intermediate
est_time: 15min
risk: high
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Start a car with a weak battery using another car or jump pack without reversing polarity, sparking at the battery, or touching moving parts.

## Preconditions

- Both vehicles are in park or neutral with parking brakes set.
- Both ignitions and all accessories are off before cables touch metal.
- Jumper cables are undamaged and clamps are color coded.
- The dead battery is not cracked, frozen, leaking, or visibly swollen.

## Steps

1. **Position the power source.** Park the good car close enough for cables to reach, but keep the vehicles from touching. → *Expect:* both batteries are reachable and the cable path avoids belts, fans, and hot exhaust.
2. **Turn everything off.** Switch off ignitions, lights, climate controls, radios, and chargers in both cars. → *Expect:* dashboards are dark except any unavoidable security indicators.
3. **Identify terminals and bare metal.** Find dead positive, good positive, good negative, and an unpainted metal ground on the dead car away from the battery. → *Expect:* plus and minus marks are visible and the ground point is solid engine or chassis metal.
4. **Connect red to dead positive.** Clamp the red cable to the dead battery positive terminal. → *Expect:* the clamp grips clean metal and does not touch any other part.
5. **Connect red to good positive.** Clamp the other red end to the good battery positive terminal. → *Expect:* both red clamps are on positive terminals only.
6. **Connect black to good negative.** Clamp the black cable to the good battery negative terminal. → *Expect:* the black clamp is secure on the good car negative post.
7. **Connect black to dead-car metal ground.** ⚠️ *Irreversible:* wrong cable order or polarity can damage electronics or ignite battery gas; confirm red is on positive before placing this final black clamp. → *Expect:* the final black clamp is on bare metal away from the dead battery.
8. **Start the good car, then the dead car.** Run the good car for 2 to 5 minutes, then crank the dead car for no more than 5 seconds at a time. → *Expect:* the dead car starts or the starter sound improves after each rest.
9. **Remove cables in reverse order.** Remove black from dead-car metal, black from good negative, red from good positive, then red from dead positive. → *Expect:* no clamp touches another clamp or loose metal during removal.
10. **Keep the revived car running.** Drive or idle it in a safe place for at least 20 minutes, then arrange a battery and charging-system check. → *Expect:* the engine keeps running after cables are removed.

## Decision points

- The dead battery is leaking, cracked, frozen, or smells like rotten eggs → do not jump it; call roadside assistance.
- You cannot identify positive and negative terminals → stop and use the owner's manual or a mechanic.
- The dead car clicks but will not crank after several attempts → the battery may be too discharged or the starter may have failed.
- A jump pack is used instead of another car → follow the pack's clamp order, but still connect positive first and keep black away from the dead battery if instructed.

## Failure modes & recovery

- **F1 Reversed polarity:** detect by sparks, alarms, or wrong terminal markings, recover by stopping before starting either car and removing cables carefully.
- **F2 Clamp sparks at battery:** detect by visible spark near a battery vent, recover by disconnecting and moving the final ground to bare metal away from the battery.
- **F3 Cable near moving parts:** detect by cable crossing a belt or fan path, recover by rerouting before any engine starts.
- **F4 Car dies after removal:** detect by stall or dim lights, recover by getting the battery and alternator tested before relying on the car.

## Verification

The revived car starts, cables are removed in reverse order, all clamps are clear of metal, and both vehicles show no warning smoke, smell, or exposed cable damage.

## Variations

- Remote battery posts: many cars provide under-hood jump posts even when the battery is elsewhere; use the labeled posts.
- Manual transmission: keep the car in neutral with the parking brake set during the jump.
- Hybrid or electric vehicle: consult the manual because jump points and limits vary.

## Safety & privacy

High risk from battery acid, explosive gas, electronics damage, and moving engine parts. Keep faces away from batteries and never let red and black clamps touch once connected.
