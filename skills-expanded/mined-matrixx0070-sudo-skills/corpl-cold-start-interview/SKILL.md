---
name: corpl-cold-start-interview
version: 1.0.0
description: Run a structured intake interview at the start of a corporate/M&A matter to capture the facts, parties, scope, and constraints before any work begins.
author: matrixx0070
tags: [corporate-legal, intake, interview, scoping, matter, onboarding]
capabilities: []
---

## When to use

Use this at the very start of a new matter — a contemplated acquisition, an entity clean-up, a governance question — when you know little and need the facts before choosing a workflow. A disciplined intake prevents work built on wrong assumptions and surfaces conflicts and privilege issues early.

**Not for:** a matter already scoped and underway (use the specific corpl- skill); giving legal advice during intake (intake gathers facts, it does not opine); resolving a conflict of interest — that is escalated to counsel immediately. This skill produces a fact record, not a legal conclusion.

## Method

1. **Identify who and what.** Client entity, requesting person and role, and the business objective in their words.
2. **Screen for conflicts and privilege early.** Capture all parties and adverse parties. *Decision point:* any potential conflict → stop and escalate to counsel before proceeding.
3. **Establish the transaction/matter shape.** Type, target or counterparty, structure if known, and stage.
4. **Capture the entity picture.** Jurisdiction of formation, entity type, cap table basics, subsidiaries, and where it operates.
5. **Pin down constraints.** Timeline and hard deadlines, budget, confidentiality/NDA status, and who the decision-makers are.
6. **Ask what documents exist** and where (data room, contracts, org docs) — inputs for downstream diligence.
7. **Note open questions and unknowns explicitly**, then confirm the fact record back to the requester for correction before any substantive work.

## Example

Intake: founder of a Delaware C-corp exploring sale of the company. Requester: CEO. Objective: "sell within 6 months, keep the team." Conflict screen: no adverse party yet — clear. Structure: likely stock sale, no buyer identified. Entity: DE C-corp, ~14 stockholders, one wholly-owned subsidiary. Constraints: NDA required before sharing financials, board must approve, target close Q4. Documents: cap table and key contracts in Google Drive. Open: outstanding SAFEs unquantified — flagged. Confirmed back to CEO.

## Pitfalls

- **Skipping the conflict screen.** The cheapest time to catch a conflict is before any work is done.
- **Recording assumptions as facts.** If the requester was unsure, mark it unknown.
- **Giving advice mid-intake.** Answering "should we…" during fact-gathering skips the analysis and the attorney gate.
- **Not confirming the record.** An unverified intake propagates errors into every downstream deliverable.

## Output format

```
MATTER INTAKE — <matter name>
Client entity / requester / role:
Objective (client's words):
Conflict & privilege screen: clear | ESCALATE — <issue>
Transaction/matter type / stage / counterparty:
Entity: jurisdiction / type / cap table / subs / footprint:
Constraints: timeline / deadlines / budget / NDA / decision-makers:
Existing documents & location:
Open questions / unknowns:
Confirmed by requester: <date>
Next: <workflow / attorney assignment>
```

## Reference

Intake sequence: identify client and objective, run the conflict and privilege screen first, then capture matter shape, entity picture, constraints, and document inventory. The conflict screen is a hard gate — a potential conflict stops intake and goes to counsel. The output is a fact record confirmed by the requester, feeding corpl-matter-workspace and the relevant diligence workflow. Nothing in intake constitutes legal advice.
