---
name: pick-up-a-package-from-the-post-office
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Collect a held package from a post office or postal pickup point using the delivery notice, ID, and any required authorization.

## Preconditions

- Missed-delivery slip, tracking number, or pickup notification.
- Government or acceptable photo ID matching the recipient or address.
- Knowledge of post office hours and pickup location.
- Permission note if picking up for someone else.

## Steps

1. **Read the notice.** Check pickup address, available date, carrier, and any barcode or item number. → *Expect:* you know where the package is held and when it is ready.
2. **Check the hold window.** Look for the last pickup date before return to sender. → *Expect:* the deadline is clear and still in the future.
3. **Gather ID.** Bring photo ID and proof of address if the ID address may not match. → *Expect:* your name or address can be matched to the package.
4. **Bring authorization if needed.** If collecting for another person, have their signed slip or carrier-approved authorization. → *Expect:* staff can release the item without guessing.
5. **Choose counter or locker.** [BRANCH: staffed counter | parcel locker] follow the notice for counter pickup or use the locker code or QR code. → *Expect:* you are in the correct pickup line or at the correct locker bank.
6. **Present the slip or tracking.** Hand over the notice or show the barcode on your phone. → *Expect:* staff can scan or type the item number.
7. **Show ID when asked.** Keep the ID visible until staff finish matching it. → *Expect:* staff accept the identity check or explain what is missing.
8. **Inspect the package label.** Confirm recipient name and address before accepting. → *Expect:* the package is yours or clearly authorized.
9. **Sign if required.** Sign the handheld device or paper form only after confirming the item. ⚠️ *Irreversible:* signature may mark delivery complete, so verify the package first. → *Expect:* the carrier record shows pickup completed.
10. **Carry it out securely.** Use both hands for heavy packages and keep small parcels zipped in a bag. → *Expect:* package leaves with you undamaged.

## Decision points

- If the notice says redelivery is available → schedule redelivery instead of traveling.
- If the pickup location changed → follow the latest tracking update, not an old slip.
- If the package is in a locker → enter the code exactly and remove the package before closing the door.
- If the hold window expired → contact the carrier to see whether return shipment has already begun.

## Failure modes & recovery

- **F1 Package not ready:** detect tracking says at facility but staff cannot find it → ask when the next sort completes and keep the slip.
- **F2 ID mismatch:** detect staff refuse release → bring proof of address, authorization, or the named recipient.
- **F3 Wrong package:** detect label does not match → do not sign; hand it back and ask staff to search again.
- **F4 Locker code fails:** detect expired or rejected code → use the service counter or request a new code from the carrier.

## Verification

You leave the pickup location with the correct package, and tracking or the receipt shows the item was picked up or delivered.

## Variations

- `usps`: a PS Form 3849 slip may allow redelivery or authorized pickup.
- Apartment package room: ID may be replaced by an app code, but still confirm the label before removing the parcel.
- High-value item: expect signature and stricter ID matching.

## Safety & privacy

Low risk. The slip and label expose your address and tracking number, so do not post photos of them. Use care carrying heavy packages and refuse any parcel that is visibly leaking or unsafe.
