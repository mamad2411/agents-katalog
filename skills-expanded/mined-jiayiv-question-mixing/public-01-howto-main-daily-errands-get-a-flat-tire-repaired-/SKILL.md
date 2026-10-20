---
name: get-a-flat-tire-repaired
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

Have a flat tire inspected and repaired safely, or replaced if the damage cannot be repaired.

## Preconditions

- The vehicle is parked safely or is using a spare, tow, or roadside assistance.
- You know which tire lost air and when the problem started.
- You can get to a tire shop without driving on a flat tire.
- You have the wheel lock key if your wheels use locking lug nuts.

## Steps

1. **Avoid driving on the flat.** Stop before the sidewall is crushed or the rim is damaged, and use a spare or tow if needed. → *Expect:* the tire is not being destroyed by continued driving.
2. **Locate the suspected puncture.** Look for a nail, screw, cut, sidewall bulge, or slow leak, but do not remove objects before the shop sees it. → *Expect:* you can tell the shop what happened.
3. **Call or visit a tire shop.** Ask whether they repair punctures, expected wait, cost, and whether appointment or walk-in is better. → *Expect:* the shop can inspect the tire.
4. **Explain temporary driving.** Tell the shop if you drove on it flat, used sealant, or installed a spare. → *Expect:* the technician knows what hidden damage to check.
5. **Ask plug versus patch.** [BRANCH: patch-plug repair | replacement] prefer an internal patch-plug for repairable tread punctures, or replace if damage is unsafe. → *Expect:* the shop explains the repair method.
6. **Confirm repairability.** Make sure the puncture is in the tread area, not the sidewall or shoulder, and not too large or near another repair. → *Expect:* the technician either approves repair or shows why it cannot be repaired.
7. **Authorize the work.** Approve repair, replacement, balancing, valve stem, or rotation only after price and tire match are clear. ⚠️ *Irreversible:* removing and discarding a tire ends any chance to reuse it, so confirm it is unrepairable first. → *Expect:* the work order matches your decision.
8. **Reinstall and check pressure.** Have the repaired or replacement tire installed, torqued, inflated, and the spare stored properly. → *Expect:* the car drives normally and the tire-pressure warning clears or is explained.

## Decision points

- Damage is on the sidewall or shoulder → replace the tire, not plug it.
- The tire was driven flat → ask for internal sidewall inspection before repair.
- Tread is low or uneven → replacement may be wiser than repairing an old tire.
- AWD vehicle has worn matching tires → ask whether one tire can be shaved or whether a set is needed.
- You used emergency sealant → tell the shop because it affects cleanup and sensors.

## Failure modes & recovery

- **F1 Unsafe repair offered:** detect by plug-only repair for sidewall or shoulder damage, recover by declining and replacing the tire.
- **F2 Slow leak continues:** detect by PSI dropping after repair, recover by returning for leak check of puncture, valve stem, and bead.
- **F3 Missing wheel lock key:** detect by shop unable to remove wheel, recover by finding the key or ordering a replacement.
- **F4 Spare left low:** detect by spare warning or low reading after swap, recover by inflating the spare before storing it.

## Verification

The repaired or replacement tire holds recommended pressure, is mounted and torqued, and the spare or damaged tire is accounted for.

## Variations

- Run-flat tire: some shops will not repair it after low-pressure driving.
- Temporary spare: observe speed and distance limits until the repaired tire is back on.
- Road-hazard warranty: check whether repair or replacement is covered before paying.

## Safety & privacy

Do not drive far on a flat, do not rely on a sidewall plug, and keep clear of shop bays unless staff directs you. Tire invoices may include plate or contact data.

