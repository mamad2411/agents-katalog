---
name: drive-safely-in-heavy-rain
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

You reduce crash risk in heavy rain by slowing down, increasing visibility and following distance, and responding correctly if the car hydroplanes.

## Preconditions

- You are already driving or deciding whether to drive in heavy rain.
- Headlights, wipers, tires, brakes, and defogger are functional enough for road use.

## Steps

1. **Turn on headlights and wipers.** Use low beams, not high beams, and choose a wiper speed that keeps the windshield clear. → *Expect:* other drivers can see you and you can see lane edges.
2. **Slow down below normal speed.** Reduce speed for visibility, standing water, tire condition, and traffic. → *Expect:* you have more time to react and less hydroplaning risk.
3. **Increase following distance.** Leave at least several extra seconds behind the vehicle ahead, more at highway speed. → *Expect:* spray and sudden braking are less dangerous.
4. **Use smooth inputs.** Accelerate, brake, and steer gently; avoid cruise control in heavy rain. → *Expect:* tires keep better contact with the road.
5. **Watch for pooled water.** [BRANCH: shallow spray | deep standing water] drive through shallow water slowly if unavoidable; avoid deep water because depth is hard to judge. → *Expect:* you avoid the deepest water and lane-edge puddles.
6. **Recover from hydroplaning correctly.** If steering feels light or the car floats, ease off the accelerator, keep the wheel pointed where you want to go, and do not brake hard. → *Expect:* tire grip returns gradually.
7. **Pull over when visibility is unsafe.** Use a safe parking lot or far-off-road area if possible; avoid stopping in a travel lane or under a bridge shoulder unless truly necessary. → *Expect:* the car is out of traffic with hazards on if stopped.
8. **Restart only when conditions allow.** Wait for rain, flooding, or visibility to improve before rejoining traffic. → *Expect:* you can see and be seen before moving again.

## Decision points

- Wipers cannot keep up → slow substantially and look for a safe place to stop.
- Water covers lane markings or reaches curb height → turn around if possible; flooded roads can hide depth and washouts.
- Other drivers tailgate → increase space ahead rather than speeding up.
- Thunderstorm, hail, or flash-flood warning → delay the trip or leave the roadway safely.

## Failure modes & recovery

- **F1 Hydroplaning:** detect: engine revs, steering feels light, or the car slides over water, recover: ease off accelerator, steer gently, and avoid hard braking.
- **F2 Windshield fogs:** detect: interior glass clouds while raining, recover: use AC, heat, fresh air, and defrost.
- **F3 Visibility collapses:** detect: lane lines or brake lights disappear in spray, recover: slow down and pull off at a safe location.
- **F4 Brakes feel wet after puddles:** detect: braking response feels weak, recover: drive slowly and apply light braking briefly if safe to dry them.
- **F5 Vehicle enters deep water:** detect: water is deeper than expected or engine sputters, recover: do not continue; stop safely and seek assistance.

## Verification

You are driving at a rain-appropriate speed with headlights on, extra following distance, clear glass, and no hard braking or abrupt steering.

## Variations

- `highway`: Spray from trucks can blind you briefly; increase distance and avoid lingering beside large vehicles.
- `night`: Glare and reflections worsen visibility, so reduce speed further.
- `mountain-road`: Watch for mud, rocks, and water crossing the road after storms.
- `urban`: Pedestrians, cyclists, clogged drains, and hidden potholes are bigger concerns.

## Safety & privacy

High road-safety risk comes from hydroplaning, poor visibility, flooding, and other drivers' sudden actions. Never drive through water when you cannot judge depth, and pull over only where you are not creating a new collision hazard.
