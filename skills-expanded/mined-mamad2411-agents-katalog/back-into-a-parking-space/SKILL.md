---
name: back-into-a-parking-space
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: intermediate
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

You reverse into a parking space slowly and accurately so leaving later is safer and forward-facing.

## Preconditions

- You are licensed to drive and using a legal parking space with enough room.
- Mirrors, rear camera if equipped, and windows are usable; pedestrians and vehicles are monitored continuously.

## Steps

1. **Choose a suitable space.** Prefer a space with clear lines, no pedestrians nearby, and enough room to swing the front of the car. → *Expect:* the space can be entered without rushing.
2. **Signal and position wide.** Signal toward the space, pass it slightly, and angle or swing wide enough that the rear can turn in. → *Expect:* drivers behind understand you are parking.
3. **Stop before reversing.** Check mirrors, camera, over-shoulder views, and both sides for pedestrians, carts, and moving cars. → *Expect:* the rear path is clear.
4. **Reverse slowly toward the reference point.** [BRANCH: space on right | space on left] turn the wheel toward the space when your rear bumper or mirror lines up with the near parking line or adjacent car corner. → *Expect:* the rear of the car starts entering the space.
5. **Use mirrors to track both lines.** Keep the vehicle centered between the painted lines and watch the front corners swing. → *Expect:* clearance remains on both sides.
6. **Straighten as the car aligns.** Unwind the steering wheel when the car becomes parallel with the parking lines, then continue back slowly. → *Expect:* the vehicle moves straight into the space.
7. **Stop before the curb, wall, or car behind.** Use mirrors, camera guidelines, parking sensors, and direct vision, but do not trust any one aid alone. → *Expect:* the car is fully inside the space without touching anything.
8. **Settle the car.** Shift to park, set the parking brake if appropriate, and check that doors can open within the lines. → *Expect:* the vehicle is centered and ready to pull forward later.

## Decision points

- Traffic is close behind → signal early and let them pass before backing.
- Pedestrian enters the path → stop immediately and wait until they are clear.
- Angle is wrong → pull forward to reset rather than forcing the turn.
- Space is tight or visibility poor → choose another space if available.

## Failure modes & recovery

- **F1 Started too close to the space:** detect: rear cuts sharply toward one line, recover: pull forward wider and restart.
- **F2 Front corner swings toward another car:** detect: mirror shows shrinking clearance at the front, recover: stop, pull forward, and reduce steering angle.
- **F3 Crooked in the space:** detect: car is diagonal between lines, recover: pull forward until straight, then reverse back with smaller corrections.
- **F4 Rear obstacle is hidden:** detect: sensor, camera, mirror, or direct look reveals a cart, curb, pole, or person, recover: stop and clear the path before continuing.
- **F5 Other driver approaches impatiently:** detect: vehicle queues or honks behind, recover: pause, communicate with signal, and let them pass if needed.

## Verification

The vehicle is fully within the parking lines, centered enough for doors to open, clear of obstacles, and positioned to exit forward.

## Variations

- `rear-camera`: Use guidelines as a reference, but still check mirrors and shoulders for cross traffic.
- `large-vehicle`: Start farther forward and wider because the front swings more.
- `angled-space`: Follow the painted angle and avoid reversing against the intended traffic flow if signs prohibit it.
- `driveway`: Watch for sidewalks, children, pets, bins, and low objects that cameras may distort.

## Safety & privacy

Medium driving risk comes from reversing near pedestrians and hidden obstacles. Move at walking speed, stop whenever uncertain, and prioritize direct observation over convenience.
