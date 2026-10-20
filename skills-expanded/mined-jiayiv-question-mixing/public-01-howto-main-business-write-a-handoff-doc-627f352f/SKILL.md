---
name: write-a-handoff-doc
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Write a handoff document that lets another person continue project or support work without losing context.

## Preconditions

- The receiving person, team, or shift is known.
- Current status, open decisions, blockers, and important links are available.
- You know where the handoff should be stored or sent.

## Steps

1. **Open the handoff destination.** Create or open the document, ticket note, project update, or shared template. → *Expect:* the handoff can be edited.
2. **State the scope.** Name the project, ticket, customer, or workstream being handed off. → *Expect:* the reader knows what the document covers.
3. **Summarize current status.** Describe what is done, what is in progress, and what is unresolved. → *Expect:* the work state is clear.
4. **List next actions.** Add each next action with owner, due date, and required input. → *Expect:* the receiver knows what to do first.
5. **Capture blockers and decisions.** Note open questions, risks, dependencies, and escalation paths. → *Expect:* unresolved items are not hidden.
6. **Add links and evidence.** Include tracker items, tickets, docs, files, dashboards, and relevant messages. → *Expect:* the receiver can verify context.
7. **Share with the receiver.** Send the handoff and ask for confirmation or questions. → *Expect:* the receiver acknowledges access or raises gaps.

## Decision points

- If the handoff is urgent → lead with immediate action and escalation contacts.
- If the receiver is unfamiliar with the work → include more background and definitions.
- If sensitive details are involved → store the handoff in an access-controlled location.

## Failure modes & recovery

- **F1 Missing next action:** detect the receiver asks what to do first → recover by adding ordered next steps.
- **F2 Broken links:** detect the receiver cannot access files or tickets → recover by fixing permissions or replacing links.
- **F3 Hidden blocker:** detect later delay caused by an unstated issue → recover by updating the doc and notifying the receiver.

## Verification

The handoff document names the scope, current status, next actions, owners, blockers, links, and receiver confirmation path.

## Variations

- Shift handoff: emphasize urgent items, queues, and unresolved customer promises.
- Project handoff: emphasize timeline, scope, decisions, and stakeholder map.
- Incident handoff: include timeline, current mitigation, severity, and escalation contacts.

## Safety & privacy

Low risk. Handoffs can concentrate sensitive links and context, so share only with people who need access.
