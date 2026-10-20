---
name: deal-with-a-car-that-wont-start
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Diagnose the likely reason a car will not start and choose a safe next action.

## Preconditions

- The vehicle is parked or stopped in a location where you can stay safe.
- You have the key or fob and can access the dashboard.
- You have a phone or another way to call roadside assistance if needed.

## Steps

1. **Make the location safe.** Shift to park or neutral, set the parking brake, turn on hazard lights if near traffic, and stay visible. → *Expect:* the vehicle will not roll and other drivers can see it.
2. **Check the dashboard and lights.** Turn the key or press start and watch whether interior lights, headlights, and warning lights work. → *Expect:* you know if electrical power is present.
3. **Listen during start.** [BRANCH: rapid clicks | one click | silence | cranks normally but will not start] use the sound to guide the next check. → *Expect:* the symptom category is clear.
4. **Check simple lockouts.** Confirm the transmission is in park or neutral, clutch is pressed if manual, brake pedal is pressed if required, and steering wheel is not locked. → *Expect:* start interlocks are satisfied.
5. **Check the key or fob.** Hold the fob near the start button or use the backup key method from the manual. → *Expect:* the car recognizes the key if fob battery was weak.
6. **Treat dim lights or rapid clicks as a battery problem.** Jump-start only with correct polarity and a safe donor battery or jump pack. → *Expect:* the engine starts or cranks stronger after the jump.
7. **Treat one solid click as possible starter trouble.** Do not keep trying repeatedly if the battery seems strong. → *Expect:* you avoid overheating wiring or draining the battery.
8. **Treat normal cranking as fuel, ignition, or engine-management trouble.** Check fuel level and warning messages, then stop extended cranking. → *Expect:* the battery is preserved for diagnosis or towing.
9. **Call for help when the quick checks fail.** Contact roadside assistance, a mechanic, or emergency services if stopped in a dangerous location. → *Expect:* a jump, tow, or traffic protection is arranged.

## Decision points

- Vehicle is in a travel lane or unsafe shoulder → call emergency services or roadside assistance before troubleshooting.
- You smell fuel, see smoke, or hear arcing → stop attempts, leave the vehicle, and call emergency services.
- Jump-start works but warning lights remain → drive only to a safe repair location or call a mechanic.
- Hybrid or electric vehicle shows high-voltage warnings → do not jump or inspect orange cables; call qualified service.

## Failure modes & recovery

- **F1 Reversed jump leads:** detect sparks, heat, or wrong clamp placement → stop immediately, disconnect safely, and call roadside assistance.
- **F2 Battery dies during testing:** detect lights fading after repeated attempts → stop cranking and request a jump or tow.
- **F3 Security system lockout:** detect immobilizer light or key warning → try the spare key or manual procedure.
- **F4 Flooded or overheated starter:** detect fuel smell or slow cranking after many tries → wait several minutes and call a mechanic.

## Verification

The car starts and can be moved safely, or the likely failure category is identified and roadside assistance, a mechanic, tow, or emergency service has been contacted.

## Variations

- Push-button start: brake-pedal position and fob recognition are common causes.
- Manual transmission: clutch interlock and roll-start advice depend on the vehicle and location.
- Diesel: glow plug, gelled fuel, or cold-weather issues may require professional help.

## Safety & privacy

Medium risk from traffic, battery acid, sparks, and fuel vapors. Do not troubleshoot in an unsafe lane, and share location and vehicle details only with trusted assistance providers.
