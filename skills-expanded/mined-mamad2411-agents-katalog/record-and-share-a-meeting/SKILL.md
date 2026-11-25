---
name: record-and-share-a-meeting
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Record a meeting with consent and share the recording only with the intended audience.

## Preconditions

- You have host or recording permission in the meeting tool.
- You know your organization's recording policy.
- Attendees can be notified before recording starts.

## Steps

1. **Confirm recording need.** Decide whether recording is necessary or whether notes are enough. → *Expect:* the recording has a clear business purpose.
2. **Check policy and consent rules.** Review company policy and local consent requirements for participants. → *Expect:* you know whether explicit verbal consent is needed.
3. **Tell attendees before recording.** State that you intend to record and why. → *Expect:* attendees have a chance to object or leave.
4. **Start recording.** Use the meeting tool's record button after consent is handled. → *Expect:* the tool shows a recording indicator.
5. **Pause for sensitive segments.** Stop or pause recording before confidential, personal, or off-record discussion. → *Expect:* sensitive content is not captured unnecessarily.
6. **Stop and save.** End recording when the meeting ends or the recordable portion is complete. → *Expect:* the recording is processing or saved.
7. **Set sharing permissions.** Limit access to attendees or the approved group before sending the link. → *Expect:* only intended viewers can open it.
8. **Share the link with context.** Send the recording link with notes, action items, and any retention expectations. → *Expect:* recipients can find the useful part and know how long it remains available.

## Decision points

- If an attendee objects → stop recording or excuse them before continuing.
- If external guests are present → use the strictest applicable consent and sharing rule.
- If the meeting includes regulated data → follow the organization's retention and storage policy.

## Failure modes & recovery

- **F1 Recording not allowed:** detect the record button is disabled → ask the host or use written notes instead.
- **F2 Consent missing:** detect recording started before notice → stop, disclose the mistake, and restart only with consent.
- **F3 Link over-shared:** detect broad access permissions → restrict access and notify the owner.

## Verification

The recording link opens for intended viewers only, and attendees were notified before recording began.

## Variations

- Training session: share with the class or team and include chapter markers if available.
- Customer call: confirm contract or account rules before recording.
- Internal confidential meeting: store in a restricted folder and avoid automatic broad sharing.

## Safety & privacy

Low risk when handled correctly. Recording may capture voices, faces, screens, customer data, and confidential discussion, so get consent and restrict sharing.
