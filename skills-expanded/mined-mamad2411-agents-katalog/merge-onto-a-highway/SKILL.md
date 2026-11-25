---
name: merge-onto-a-highway
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

You use the entrance ramp to match highway speed, choose a safe gap, and merge smoothly without surprising highway traffic.

## Preconditions

- You are licensed to drive and the vehicle is fit for highway speeds.
- You know the ramp direction and can use mirrors, signals, and blind-spot checks.

## Steps

1. **Read the ramp early.** Check signs, curve, ramp length, and whether the lane becomes an exit-only or add lane. → *Expect:* you know how much space you have to accelerate.
2. **Signal before the merge area.** Turn on the signal while still on the ramp, not after drifting toward traffic. → *Expect:* highway drivers can see your intent.
3. **Accelerate to match traffic.** Use the ramp to approach the speed of the lane you will enter, within weather and legal limits. → *Expect:* your speed is close enough that only a small adjustment is needed.
4. **Find the gap, not the car.** Look for open space between vehicles, then adjust speed to arrive beside that space. → *Expect:* a specific gap is selected.
5. **Check mirrors and blind spot.** [BRANCH: clear gap | blocked gap] merge if clear; if blocked, adjust speed and choose the next gap. → *Expect:* no vehicle is hidden beside your rear quarter.
6. **Commit smoothly.** Steer gently into the lane while maintaining speed, then center the vehicle in the lane. → *Expect:* the merge is one controlled movement, not a hesitation across the line.
7. **Cancel the signal and rebuild space.** Once fully in the lane, leave a following gap and match traffic flow. → *Expect:* you are established in the highway lane with safe space ahead.
8. **Use the shoulder only as an emergency escape.** If the ramp ends and no safe gap exists, avoid stopping in the lane; use available escape space only if needed to prevent a collision. → *Expect:* the vehicle remains controlled and visible.

## Decision points

- Ramp has a short acceleration lane → build speed earlier and choose a gap sooner.
- Traffic is stop-and-go → merge zipper-style at low speed, one vehicle at a time.
- Highway traffic is much faster → do not force entry; keep scanning and use the full ramp.
- You missed the merge or entered the wrong ramp → continue safely and reroute instead of sudden braking or reversing.

## Failure modes & recovery

- **F1 Too slow at the merge point:** detect: highway traffic closes rapidly from behind, recover: accelerate if safe or choose a later gap.
- **F2 Blind spot occupied:** detect: shoulder-check shows a vehicle beside you, recover: hold lane position and adjust speed.
- **F3 Gap disappears:** detect: another vehicle speeds up or changes lanes into it, recover: abandon that gap and select the next one.
- **F4 Panic stop on ramp:** detect: you are braking hard near the lane end, recover: keep the vehicle straight, signal, and use remaining ramp or escape area safely.
- **F5 Driver will not let you in:** detect: repeated blocked gaps, recover: adjust speed rather than racing or forcing the merge.

## Verification

You are fully in the highway lane at a speed close to traffic, with your signal canceled and safe space ahead and behind.

## Variations

- `metered-ramp`: Stop at the ramp signal if required, then accelerate decisively when released.
- `left-side-entry`: Some highways merge from the left; scan the appropriate blind spot and lane.
- `truck-or-heavy-load`: Acceleration is slower, so leave more ramp distance and avoid tiny gaps.
- `rain-or-snow`: Match a safer reduced traffic speed and leave more space before and after merging.

## Safety & privacy

High driving risk comes from speed mismatch, blind-spot conflicts, and stopping at the end of a ramp. The safest merge is planned early, signaled, speed-matched, and completed without forcing another driver to brake hard.
