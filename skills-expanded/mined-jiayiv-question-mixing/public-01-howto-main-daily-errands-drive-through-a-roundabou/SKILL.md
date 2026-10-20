---
name: drive-through-a-roundabout
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: intermediate
est_time: 5min
risk: high
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

You enter, travel through, and exit a roundabout predictably while yielding correctly and protecting pedestrians, cyclists, and nearby drivers.

## Preconditions

- You are licensed to drive and following local traffic law.
- You can identify your intended exit before entering the roundabout.

## Steps

1. **Slow on approach.** Read lane arrows, destination signs, and crosswalks before the yield line. → *Expect:* you know which lane and exit you need.
2. **Choose the correct lane early.** [BRANCH: right or first exit | straight or later exit] use the lane markings; do not change lanes inside unless markings clearly permit it. → *Expect:* your vehicle is positioned in the proper approach lane.
3. **Yield to pedestrians and cyclists first.** Stop before the crosswalk if anyone is crossing or about to cross. → *Expect:* the crosswalk is clear before you reach the yield line.
4. **Yield to traffic already in the roundabout.** Look left in right-side-driving countries, or toward circulating traffic in your locale. Enter only when there is a safe gap. → *Expect:* you do not make circulating traffic brake for you.
5. **Enter smoothly and keep lane discipline.** Maintain a low steady speed and follow your lane around the circle. → *Expect:* your path is predictable and within lane markings.
6. **Signal before exiting.** Turn on the exit signal after passing the exit before yours, or as local rules require. → *Expect:* waiting drivers and pedestrians can read your intention.
7. **Check the exit crosswalk.** Watch for pedestrians, cyclists, and scooters at the exit, where drivers often accelerate too soon. → *Expect:* the exit path is clear.
8. **Exit without stopping inside.** Leave the roundabout in your lane and cancel the signal. → *Expect:* you are on the intended road and traffic flow remains smooth.

## Decision points

- Missed your exit → continue around again rather than cutting across lanes or stopping.
- Large truck or bus is circulating → give extra space because it may straddle lanes.
- Multi-lane roundabout → obey lane arrows before entering; last-second lane changes are the main conflict.
- Emergency vehicle approaches → follow local law, but usually clear the roundabout before pulling over safely.

## Failure modes & recovery

- **F1 Gap is too small:** detect: entering would make another driver brake, recover: wait at the yield line for a larger gap.
- **F2 Wrong lane chosen:** detect: lane arrows do not match your exit, recover: follow the lane's legal exit and reroute.
- **F3 Driver beside you drifts:** detect: adjacent vehicle crosses markings, recover: hold speed, avoid side-by-side conflict, and give space.
- **F4 Pedestrian appears at exit:** detect: person steps into or waits at the exit crosswalk, recover: yield before the crosswalk and leave room behind you.
- **F5 You miss the exit:** detect: intended exit passes, recover: keep circulating calmly and take it on the next lap if legal.

## Verification

You exited onto the intended road without forcing circulating traffic to brake, crossing lane markings improperly, or failing to yield to pedestrians.

## Variations

- `left-side-driving`: Reverse the traffic direction and mirror checks according to local road rules.
- `mini-roundabout`: Speeds are lower, but yielding and signaling expectations still apply.
- `multi-lane`: Lane markings decide exits; do not assume the outside lane can continue around.
- `bike-heavy-area`: Expect cyclists at entry and exit crossings, not just inside the roadway.

## Safety & privacy

High road-safety risk comes from failure to yield, wrong-lane exits, pedestrian conflicts, and panic stops inside the circle. When uncertain, slow early, yield, and take another lap or reroute.
