---
name: get-a-car-safety-inspection
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 1h
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

Complete a required or voluntary vehicle safety inspection and know what to do if the car passes or fails.

## Preconditions

- You know whether your location requires safety, emissions, or combined inspection.
- You have the vehicle, keys, registration, proof of insurance if required, and payment method.
- Basic lights, horn, wipers, tires, mirrors, and seat belts are present.
- The vehicle can be driven legally or towed to the inspection site.

## Steps

1. **Check the inspection rules.** Confirm timing, approved stations, fees, and whether emissions testing is separate. → *Expect:* you know the correct inspection type and deadline.
2. **Book or choose a station.** [BRANCH: appointment | walk-in] schedule a slot if required, or pick an approved station with posted inspection service. → *Expect:* the station can inspect your vehicle class.
3. **Do a quick pre-check.** Test headlights, brake lights, turn signals, horn, wipers, tire tread, mirrors, and seat belts. → *Expect:* obvious simple failures are found before paying.
4. **Bring documents and arrive clean enough.** Take registration, insurance, ID if required, and remove clutter blocking belts or inspection points. → *Expect:* the inspector can access the vehicle and paperwork.
5. **Authorize only the inspection first.** Ask what is included and whether repairs require separate approval. → *Expect:* you understand the inspection fee and repair consent process.
6. **Review checked systems.** Expect checks of brakes, steering, suspension, lights, tires, glass, wipers, horn, emissions equipment where applicable, and safety restraints. → *Expect:* the station performs the required checklist.
7. **Handle the result.** [BRANCH: pass | fail] accept the sticker or certificate if it passes, or get a written failure report and retest rules if it fails. → *Expect:* you leave with proof of pass or a repair list.
8. **Complete retest if needed.** Repair required items, keep receipts, and return within any retest window. ⚠️ *Irreversible:* driving an unsafe or expired-inspection vehicle can create legal and crash risk, so confirm the allowed window. → *Expect:* the vehicle is reinspected or scheduled before the deadline.

## Decision points

- A light bulb is out before inspection → replace it first if you can do so safely.
- The shop proposes unrelated repairs → ask which items are required to pass.
- The car fails for tires or brakes → avoid long driving until repaired.
- Registration is expired → ask whether inspection is allowed before renewal.
- You suspect unfair failure → use the appeal or second-station process if local rules allow.

## Failure modes & recovery

- **F1 Missing document:** detect by station refusal, recover by retrieving registration, insurance, or renewal proof.
- **F2 Failed inspection:** detect by written rejection, recover by repairing listed defects and booking retest.
- **F3 Sticker not issued:** detect by pass paperwork but no sticker where one is required, recover by asking before leaving.
- **F4 Repair upsell confusion:** detect by vague repair list, recover by asking for pass-fail items separated from recommendations.

## Verification

The vehicle has a valid inspection sticker, certificate, or electronic pass record for the required inspection period.

## Variations

- Emissions-only areas: safety items may not be inspected at the same visit.
- Commercial vehicles: expect stricter documentation and inspection intervals.
- New vehicles: some places exempt new cars for the first registration period.

## Safety & privacy

Inspection involves safety-critical systems and personal vehicle records. Do not ignore brake, tire, steering, or restraint failures just to meet a deadline.

