---
name: customer-ops-email
description: Draft customer and ops emails (shipment status, delay, incident, go-live, maintenance, follow-up) with subject line and next-update time. Use when the user asks to write a client mail, inform the customer, or send a delay or downtime notice.
---

# Customer & Ops Email

## Inputs
- Facts from the user: what happened, IDs (AWB, flight, ULD, ticket), times, impact
- Pasted thread, ticket, or alert to reply to or summarise
- Optional: recipient name/org, sender signature, previous notice (for updates)

## Defaults (state them in the output if used)
| Setting | Default | Options |
|---|---|---|
| Scenario | Inferred from facts | See table in Steps |
| Recipient | Client ops contact | Client ops · Client management · Partner (GHA, airline, forwarder) |
| Tone | Formal-friendly | Formal (management) · Friendly (daily ops) |
| Time zone | As given; else "TBD" | Always show zone, e.g. 14:00 IST |
| Length | ≤ 150 words body | Incident/maintenance ≤ 200 |

Ask **one** question only if the scenario is ambiguous or the impact is unknown for an incident. Otherwise use defaults and state them.

## Steps
1. Read all input; list facts, IDs, times, and what is still unknown.
2. Pick the scenario and its template from `templates/email-templates.md`:
   | Scenario | Trigger |
   |---|---|
   | Shipment status | Routine update on AWB / consignment |
   | Delay / exception | Offload, missed connection, short-ship, customs hold, damage |
   | Incident notice | System outage, message failure (FWB/FFM/FSU), integration down |
   | Go-live announcement | New module, airport, airline, or partner live |
   | Maintenance window | Planned downtime or deployment |
   | Request follow-up | Chasing data, documents, sign-off, UAT feedback |
3. Write the subject line using `references/tone-and-subject.md`.
4. Fill the template with facts only; every unknown becomes "TBD" in the draft and a line in Needs input.
5. Add the **next update time** (incident, delay, maintenance) or the **reply-by date** (follow-up), only if given; else "TBD".
6. Apply the tone rules in `references/tone-and-subject.md`.
7. Run the self-check and fix before returning.

## Format
Subject line, greeting, body per template, clear ask or next update, sign-off. For an update to an earlier notice, prefix the subject with "Update n:" and state what changed first.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never promise a date, time, ETA, root cause, or compensation that the user did not give. Write "TBD" and flag it.
- Keep AWB, flight, ULD and ticket numbers exactly as given.
- Apologise once, near the start, for customer impact only. No repeated sorry.
- No blame: never name an airline, handler, colleague or vendor as at fault. State the fact ("the flight was offloaded").
- Every incident, delay and maintenance email states when the next update comes.
- One ask per email, with a date if given.
- No internal tool names, internal ticket comments or jargon the client may not know.
- Plain language, active voice, short paragraphs; bullets for ≥ 3 facts.

## Self-check
- [ ] Right scenario template used
- [ ] Subject line follows the pattern and includes the key ID
- [ ] No invented dates, ETAs, causes or commitments
- [ ] IDs match the input character for character
- [ ] Apology appears at most once; no blame
- [ ] Next update time or reply-by date present (or TBD and flagged)
- [ ] Within length limit

## Output
Return the email (subject + body), then an **"Assumptions & Needs input"** block (scenario and defaults used, TBDs, facts to confirm before sending) outside the email.

Benchmark after edits with `evals/test-cases.md`.
