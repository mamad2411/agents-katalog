---
name: clinic-client-comms-log
version: 1.0.0
description: Maintain a dated, factual log of every client communication in a clinic matter file — who, when, what, and follow-ups, with no unreviewed legal conclusions.
author: matrixx0070
tags: [legal-clinic, communication-log, matter-file, recordkeeping, follow-up, confidentiality]
capabilities: []
---

## When to use
Use this every time you speak with, email, meet, or receive a message from a client (or a third party about the client's matter). A contemporaneous log protects the client, the clinic, and you: it preserves what was actually said, tracks promised follow-ups, and gives the supervising attorney an accurate picture without relying on memory. Log the entry as soon as possible after the contact while details are fresh.

**Not for:** running the initial intake and relationship decision (use clinic-client-intake), writing correspondence the client will receive (use clinic-client-letter), or building a reusable process template (use clinic-build-guide). This log records facts of contact only — it is not the place to render legal advice, which students cannot give independently (Rule 5.5 / UPL).

## Method
1. Capture the contact metadata: date, time, channel (call/email/meeting/text), participants, and duration if relevant.
2. Summarize what was communicated in neutral, factual terms — what the client said, what you conveyed, what documents changed hands.
3. Record follow-up actions with owners and due dates.
   **Decision point:** if the client asked a legal question or you feel pressure to answer one, log the question and route it to the supervising attorney — do not record your own answer as advice given (Rule 5.5 / UPL); students act only under supervision.
4. Keep legal conclusions out of the log unless the supervising attorney has reviewed and approved them; otherwise note "pending attorney review."
5. Store the log inside the confidential matter file; never paste client-identifying details into external or AI tools (Rule 1.6; ABA Op. 512).
6. Append, never overwrite — each contact is a new timestamped entry so the record stays a true chronology.

## Example
> 2026-07-11, 2:15pm, phone (12 min). Participants: student J. Rivera, client "M.T." Client reported landlord shut off water 07-09; wants to know options. Provided no advice; question logged for attorney. Client emailing lease copy by 07-12. Follow-up: student to add lease to file, flag to Prof. Adams for review by 07-13.

## Pitfalls
- Writing your own legal conclusion into the log before attorney review — reads as advice given.
- Overwriting or backdating entries, destroying the chronology's reliability.
- Logging days later from memory, losing accuracy on what was actually said.
- Copying client-identifying details into external note or AI tools (Rule 1.6).

## Output format
```
[<YYYY-MM-DD> <HH:MM>] <channel> (<duration>)
Participants: <names/initials>
Summary: <neutral factual account of what was communicated>
Documents: <exchanged, if any>
Legal question raised: <verbatim or none> -> routed to <attorney> [pending review]
Follow-up: <action> | Owner: <who> | Due: <YYYY-MM-DD>
```

## Reference
- Model Rules 1.4 (communication), 1.6 (confidentiality), 5.5 (UPL — no unsupervised advice).
- ABA Formal Opinion 512 — confidentiality and competence when using GenAI on client matters.
- Clinic norm: contemporaneous, append-only logs; legal conclusions await supervising-attorney review.
