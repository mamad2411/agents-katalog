---
name: use-a-parcel-locker
domain: daily
subdomain: errands
locale: [generic]
interface: mixed
difficulty: basic
est_time: 10min
risk: low
prerequisites: [have-phone]
status: draft
last_verified: 2026-07-20
---

## Goal

Your parcel is out of the locker and in your hands, the compartment is closed behind you, and the pickup is registered as complete before any storage deadline expires.

## Preconditions

- A delivery notification (SMS, email, or carrier app push) saying the parcel is in a named locker location.
- The access credential from that notification: a one-time PIN, a QR/barcode in the app, or an app "open door" button. Some systems additionally require the phone number or ID the parcel was addressed to.
- You can reach the locker before the storage deadline (commonly 2 to 3 days; some grocery and same-day lockers give only 24 hours).

## Steps

1. **Check the deadline the moment the notification arrives.** Find the "pick up by" date in the message; if none is stated, assume 48 hours. → *Expect:* a pickup slot planned before expiry, with a margin.
2. **Retrieve the code before you travel.** Open the notification and confirm the PIN or QR loads; screenshot it. Locker banks are often in garages and lobbies with poor signal, and a code you cannot load is the classic stranding. → *Expect:* code or QR visible offline on your phone.
3. **Locate the correct terminal.** Sites often host lockers from several carriers side by side; match the brand and the location name in your notification exactly. → *Expect:* terminal brand matches the notification.
4. **Authenticate at the screen.** [BRANCH: PIN → type it at the touchscreen | QR/barcode → hold it to the scanner window, adjusting brightness up | app-driven → stand at the locker, press the in-app open button with Bluetooth on] → *Expect:* screen confirms your parcel and a compartment door pops ajar somewhere in the bank; watch and listen for it, the open door can be at ankle height or above your head.
5. **Empty the compartment completely.** Reach in and sweep the full depth; multi-parcel orders can mean two boxes in one compartment, and small padded envelopes hide at the back. → *Expect:* compartment visibly empty on a final look.
6. **Inspect before the door closes.** Check the label is yours and the box is not crushed or leaking. ⚠️ *Irreversible:* once the door shuts, most systems mark the pickup complete and the code dies; you cannot reopen it to put a wrong or damaged parcel back. Wrong parcel or serious damage → photograph it in the open compartment and use the terminal's help/support option before touching the door. → *Expect:* your name on the label, box intact.
7. **Close the door firmly until it latches.** An unlatched door keeps the transaction open and can flag the compartment as faulted. → *Expect:* door flush with the bank, a click, and the screen (or app) showing pickup complete.

## Decision points

- Parcel exceeded the largest compartment size → carriers divert oversized items to a counter or depot; the notification will name a different pickup point, so read it fully before traveling to the locker.
- Deadline is about to lapse and you cannot get there → many apps allow a one-time extension or redirect to a depot; request it before expiry, not after. After expiry the parcel returns to the depot (held some days) or to the sender.
- Code limited-attempts warning on screen → stop after two failed tries and re-check you are at the right terminal and using the newest notification; a third failure can lock the transaction and force a support call.
- Sending (not receiving) via locker → reverse flow: you need a compartment size class at drop-off; if the label's declared size class is smaller than the box, the door will not be offered and you must rebook the size.

## Failure modes & recovery

- **F1 Code rejected:** most often it is yesterday's code after a redelivery, or a sibling terminal two meters away → use the newest message, verify the terminal ID printed on the bank against the notification.
- **F2 Door pops but appears empty:** parcel slid to the back or the wrong door was watched → sweep the compartment by hand, scan neighboring doors for one ajar, then use terminal support with the transaction still open.
- **F3 Door will not open (mechanical jam):** do not pry; press the door inward once and re-trigger from the app → still stuck: report via the terminal's support flow so the parcel is redirected, since jammed compartments are reassigned to depot pickup.
- **F4 No signal at the locker:** use the screenshot from step 2; app-only systems without offline mode → step outside the dead zone, load the open command, and some apps then give a grace window to press open at the door.

## Verification

The parcel with your name on it is in your possession, the compartment door is latched flush, and the carrier app or a follow-up message shows the delivery status as picked up or complete.

## Variations

- Carrier ecosystems differ in credential: some are PIN-first (SMS code at a keypad), some app-only with Bluetooth unlock, some send the QR only to the addressee's registered app account, which matters when someone picks up for you.
- Proxy pickup: forward the PIN and you have effectively handed over the parcel; some systems instead support formal delegation in the app, which keeps an audit trail.
- Refrigerated grocery lockers: deadlines are hours, not days, and expiry means disposal rather than return.

## Safety & privacy

The PIN or QR is the parcel: anyone holding it can collect, so share it only deliberately. At the terminal, shield the keypad as you would at an ATM. Low physical risk; mind low compartment doors left ajar at shin height.
