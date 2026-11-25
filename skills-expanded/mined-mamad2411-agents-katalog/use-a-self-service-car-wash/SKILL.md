---
name: use-a-self-service-car-wash
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Wash a car in a coin or card-operated self-service bay without scratching paint, wasting paid time, or leaving soap residue.

## Preconditions

- The bay is open and the floor drains are not blocked.
- Windows, sunroof, fuel door, and trunk are closed.
- You have payment, microfiber towels, and optional wheel cleaner.
- The car paint is cool enough to touch comfortably.

## Steps

1. **Read the control panel before paying.** Note the order of modes, timer behavior, and any minimum charge. → *Expect:* you know how to switch between rinse, soap, brush, wax, and stop.
2. **Prepare the car quickly.** Remove loose trash, fold mirrors only if needed, and place towels where they will stay dry. → *Expect:* nothing loose will blow away or block the wash hose.
3. **Start with pre-rinse.** Spray from top down, keeping the nozzle 1 to 2 feet from paint and farther from loose trim. → *Expect:* grit, mud, and loose debris run off before anything touches the paint.
4. **Apply soap.** Switch to soap and cover roof, glass, panels, wheels, and bumpers in that order. → *Expect:* the car is wet with visible foam before it starts drying.
5. **Use the brush only after rinsing it.** Spray the brush head first, then brush top down with light pressure; skip it if the bristles hold grit. → *Expect:* dirt lifts without dragging visible grit across paint.
6. **Watch the timer.** [BRANCH: enough time | time nearly out] continue the wash if enough; if nearly out, switch to rinse immediately. → *Expect:* soap will not dry on the car.
7. **Rinse thoroughly.** Work top down, including mirrors, grille, wheel wells, door handles, and lower panels. → *Expect:* water sheets off with no foam hiding in seams or trim.
8. **Dry outside the bay if allowed.** Move to the drying area and use clean towels on glass first, then paint, then dirty lower panels. → *Expect:* the bay is clear for the next user and the car has fewer water spots.

## Decision points

- The brush looks sandy or oily → skip contact washing and use rinse plus soap only.
- The car has fresh paint, vinyl wrap, or loose trim → keep the nozzle farther away and avoid high-pressure edges.
- Soap starts drying in sun or wind → stop brushing and rinse immediately.
- The timer cannot be paused → plan the route before inserting more money.

## Failure modes & recovery

- **F1 Soap dries on paint:** detect by chalky streaks, recover by re-wetting and rinsing that panel before continuing.
- **F2 Brush scratches risk:** detect by grit in bristles or on paint, recover by rinsing brush and panel or skipping the brush.
- **F3 Missed wheel grime:** detect by brown runoff after final rinse, recover by rinsing wheels again before drying towels touch them.
- **F4 Water spots after drying:** detect by mineral dots on glass or dark paint, recover by re-wetting small areas and drying with a clean towel.

## Verification

The car has no visible soap foam, grit, or heavy water spots, and the bay floor is clear of your towels, trash, and equipment.

## Variations

- Touchless preference: use pre-rinse, soap, dwell time, and rinse, but skip the brush.
- Winter salt: spend extra rinse time on lower panels and wheel wells.
- Pickup or roof rack: step back and change spray angle rather than stretching under the hose.

## Safety & privacy

Low risk from slippery floors, high-pressure spray, and moving vehicles in nearby bays. Keep the nozzle away from skin and never spray another person, camera, or open window.
