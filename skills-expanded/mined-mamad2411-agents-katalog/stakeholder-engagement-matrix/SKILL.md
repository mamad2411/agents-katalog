---
name: stakeholder-engagement-matrix
description: Map project/initiative stakeholders onto a Power/Interest 2x2 (Manage Closely, Keep Satisfied, Keep Informed, Monitor) and assign each quadrant a distinct effort level, communication style, and cadence — instead of treating every stakeholder the same. Use when planning a project's or initiative's stakeholder communications, deciding who needs regular touchpoints vs. a monthly briefing, prioritizing limited comms time/effort across a stakeholder list, or asked to build a stakeholder engagement/comms plan.
---

# Stakeholder Engagement Matrix

Source: reviewed from an uploaded infographic — "Not all stakeholders are
created equal" (Hustle Badger, "Stakeholder Engagement Plan"). No
prompt/repo — a Power/Interest 2x2, written up as a skill the way the
source presented it. Complements the existing `internal-comms` skill:
that skill formats a given communication (3P update, newsletter, FAQ);
this skill decides *who* gets *how much* of it and how often, before any
individual message gets drafted.

## The 2x2: Power × Interest

Plot every stakeholder on two axes — how much power/influence they have
over the outcome, and how much interest they have in it — then treat
each quadrant differently. Time and attention are the scarce resource;
this grid is how to spend them deliberately instead of communicating with
everyone the same way by default.

| | **Low Interest** | **High Interest** |
|---|---|---|
| **High Power** | **Keep Satisfied** — senior people who need an overview because of their influence, but won't work with the team day to day (e.g. CEO, Managing Director, Legal, Finance). Effort: moderate. Understand their needs upfront at kickoff; regular, concise written updates; proactive comms about any problems. Their framing: *"This is under control."* | **Manage Closely** — the people who matter most, actively working to deliver the outcome, so keep them fully engaged (e.g. VP Product, marketing lead, ops lead). Effort: high. Regular touchpoints and a shared Slack channel; share rough thinking, not just finished decks; pre-wire every decision before group meetings. Their framing: *"We're building this together."* |
| **Low Power** | **Monitor** — the least important people for this initiative specifically. Give them basic information and monitor for issues or pressing questions (e.g. adjacent product teams, unaffected ops teams). Effort: low. Keep comms high-level; only communicate at major milestones; batch with other ongoing project comms. Their framing: *"Here's the TL;DR."* | **Keep Informed** — they care a lot but don't get much say; often the people who deal with whatever ships and want to be informed to do their own job well (e.g. CS agents, sales reps). Effort: moderate. Batch comms into a monthly briefing; have a point person from their side; keep it focused on what changes for them. Their framing: *"This is what it means for you."* |

## Designing the actual comms, once someone's placed

For each stakeholder (or quadrant), answer three questions before drafting anything:

1. **Objective** — what do they actually want out of the interaction?
2. **Channel** — what format fits them: email, Slack, a dashboard, an all-hands?
3. **Schedule** — how often do they actually need a touchpoint, given their quadrant's effort level?

## How to use this

1. List the actual stakeholders for the project/initiative — named people or roles, not a generic "leadership" bucket.
2. Plot each on the grid using their real power and interest, not where it would be convenient for them to sit.
3. Assign the quadrant's effort level and cadence rather than inventing a bespoke plan per person — the grid's value is in *not* treating everyone identically.
4. Answer Objective/Channel/Schedule for each stakeholder (or quadrant, if several share a profile) before drafting the first message.
5. Re-plot periodically — a stakeholder's power or interest can shift mid-project (a Monitor-quadrant team gets reorganized under the initiative, a Keep-Informed exec gets promoted into it), and the plan should move with them rather than staying fixed from kickoff.

## Related skills in this repo

- **internal-comms**: Once a stakeholder's quadrant and cadence are set here, that skill's format guides (3P updates, status reports, FAQs) draft the actual message.
- **quarterly-review-cadence**: The "share the agenda" prep step there benefits from this matrix — a Manage-Closely stakeholder gets the full agenda in advance, a Monitor-quadrant one doesn't need it at all.
- **ceo-reporting-skill** / **business-intelligence-report**: A CEO or board reader is very likely a Keep-Satisfied stakeholder (high power, lower day-to-day interest) — this matrix's guidance for that quadrant (concise, proactive-on-problems, not a working session) shapes how those reports should read.
- **ai-project-management**: This matrix is the stakeholder-communication layer of a broader project plan — pairs with that skill's WBS/schedule/resource management pieces.
