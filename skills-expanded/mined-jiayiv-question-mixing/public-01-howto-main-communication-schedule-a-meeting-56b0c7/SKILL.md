---
name: schedule-a-meeting
domain: communication
locale: [generic]
interface: web
difficulty: basic
est_time: 15min
risk: low
prerequisites: [have-email-address]
status: draft
last_verified: 2026-07-20
---

## Goal

A meeting exists on every participant's calendar at a time they actually agreed to, with the purpose, location/link, and duration clear — and it happens.

## Preconditions

- A reason concrete enough to state in one line (if you can't, the meeting may be an email — check first).
- The participant list (as small as achieves the purpose) and their emails.
- A calendar system (Google/Outlook/etc.) or, cross-organization, a scheduling-link tool.

## Steps

1. **Define the meeting in one line + a duration.** "30 min — decide the venue for the offsite." Purpose decides the invite list; duration defaults short (25/50 min beats 30/60 — buffer is humane). → *Expect:* a title anyone can parse, a duration you can defend.
2. **Find candidate times against *their* constraints.** [BRANCH: same org → calendar's free/busy overlay, pick open slots | cross-org → offer 2–3 concrete windows by email, or send a scheduling link] Time zones: state times *in theirs* or use the tool's auto-conversion — never make a group do arithmetic. → *Expect:* 1–3 candidate slots that are genuinely open for the key people.
3. **Send the invite with everything a participant needs.** Title (from step 1), the video link *or* room, agenda/one-liner in the description, any pre-reading attached or linked. Optional attendees marked optional. → *Expect:* invite lands on calendars pending acceptance; nothing crucial lives only in a separate email.
4. **Watch the responses.** Accepts roll in → done. Key person declines/counter-proposes → take their counter-slot if it works: one renegotiation round maximum before you fall back to a scheduling poll. → *Expect:* all required participants accepted; the calendar object is the single source of truth.
5. **Adjust by *updating the event*, never by side-channel agreement.** Time changes, link changes, room changes go through the calendar edit so every copy updates. → *Expect:* everyone's calendar shows the current truth; no "wait, I thought it moved" class of failure.
6. **Day-of: honor it.** Join/arrive on time; if you must cancel, cancel the event (with a line of context) as early as known — a canceled meeting returns time, a no-show burns trust. → *Expect:* the meeting occurs at the stated time with the people it needed.

## Decision points

- Recurring vs. one-off → recur only for genuinely periodic needs, and put an end date on it; orphaned recurring meetings are a famous time tax.
- More than ~5 required people cross-org → skip negotiation entirely: scheduling poll (or link) first, invite second.
- Someone's only availability is brutal for them (their 7 a.m.) → acknowledge and rotate the pain across instances if recurring; the calendar shows times, not fairness — you provide that.

## Failure modes & recovery

- **F1 Silence from a key participant:** one nudge referencing the invite ("does Tuesday 3pm work? Grabbed it tentatively") after ~a day; then their assistant/alternate channel; don't let a pending invite silently become a no-show surprise.
- **F2 Double-booked yourself:** whichever commitment you break, break it *explicitly and early* with a re-proposal — calendar Tetris is normal; ghosting is the failure.
- **F3 The meeting occurs and wasn't needed (status that could've been async):** note it in the wrap-up and downgrade the next instance to a doc/message — the recipe's step 1 test gets sharper each time you feed it.
- **F4 Cross-tool invite mangling (Outlook↔Google artifacts, missing links):** put the video link in *both* the location field and the description body — the description survives every translation layer.

## Verification

Every required participant's calendar shows the same event — right time (their zone), working link/room, purpose readable — they accepted it, and the meeting subsequently happened (or was explicitly, promptly canceled).

## Variations

- External/professional first-contact: propose times in their zone in the email body *and* attach the invite once agreed — sending unagreed invites to strangers reads presumptuous in some cultures, efficient in others; mirror their norm.
- Interview/candidate scheduling: the scheduling link is now standard and kind — candidates pick without power-dynamics negotiation.

## Safety & privacy

Low risk. Calendar descriptions are visible to all invitees and often to org members — sensitive context goes in the meeting, not the invite body; and external invitees see the attendee list, which is itself information.
