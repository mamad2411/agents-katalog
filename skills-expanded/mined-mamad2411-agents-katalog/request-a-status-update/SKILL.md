---
name: request-a-status-update
domain: business
locale: [generic]
interface: mixed
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Request a status update that gets a useful answer without creating unnecessary interruption or ambiguity.

## Preconditions

- You know the project, task, or ticket needing an update.
- You know the likely owner or team.
- You have checked the tracker or recent updates first.

## Steps

1. **Check existing status.** Open the tracker, ticket, document, or channel where updates are normally posted. → *Expect:* you know what information is already available.
2. **Choose the recipient.** Identify the person responsible for the next update or decision. → *Expect:* the request goes to the right owner.
3. **Write a specific ask.** State the item, what status you need, and why you need it. → *Expect:* the recipient understands the requested information.
4. **Include a response deadline.** Name when the update is needed and whether a short answer is acceptable. → *Expect:* urgency is clear.
5. **Send in the right channel.** Use the task comment, ticket note, email, or team chat where the work is tracked. → *Expect:* the request is visible in the work context.
6. **Record any reply.** Update the tracker or document if the answer arrives outside the system of record. → *Expect:* the status is captured for others.

## Decision points

- If the update is urgent → use a direct message or call and then record the result.
- If the tracker already has the answer → do not ask; link or summarize the existing status.
- If the owner is unclear → ask in the project channel and request the accountable owner.

## Failure modes & recovery

- **F1 Asked the wrong person:** detect redirect or no ownership → recover by identifying the owner from the task, ticket, or manager.
- **F2 Vague response:** detect an answer without date, blocker, or next action → recover by asking one targeted follow-up.
- **F3 Status not recorded:** detect useful information only in chat → recover by copying the summary into the tracker.

## Verification

The status request names the work item, specific information needed, deadline, recipient, and location where the answer will be recorded.

## Variations

- Project update: ask for status, blockers, next milestone, and decision needs.
- Support update: ask for current customer impact, next reply time, and escalation state.
- Executive update: ask for overall status, risk, and decision required.

## Safety & privacy

Low risk. Keep customer or personnel details in approved systems rather than broad chat threads.
