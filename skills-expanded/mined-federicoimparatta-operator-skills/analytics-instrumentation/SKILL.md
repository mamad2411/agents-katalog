---
name: analytics-instrumentation
description: Use this skill when the user asks to design product analytics, define events, build an event taxonomy, specify instrumentation for a new feature, or clean up existing tracking. Trigger phrases include "instrument this feature", "define events for X", "event taxonomy", "tracking plan", "analytics spec", "instrumentar esta feature", "taxonomía de eventos". Produces an instrumentation plan structured around the question the data will answer, not around what is easy to fire.
---

# analytics-instrumentation

> **Anchor:** Instrument before you ship. What is not measured did not happen.

## When to use

Use this skill when the user needs to define or revise product analytics. Works for:

- A new feature that needs tracking defined before build.
- An existing feature with inconsistent or duplicated events.
- A company-wide event taxonomy that needs to be established or pruned.
- A migration from one analytics tool to another, with naming cleanup.

Do not use when:

- The user is writing a PRD. Instrumentation is a section inside the PRD; produce the section but do not rewrite the PRD.
- The user is building a dashboard. Use `dashboard-spec`.
- The user is reconciling disagreeing metrics across tools. Use `data-reconciliation`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: event, property, funnel, cohort, tracking plan, KPI, session, payload, schema.
- **EN.** Direct US business register. Avoid analytics vendor jargon without naming what it means.
- Event names themselves are always in English, lowercase with underscores, regardless of the document language.

## Method

### Step 1. Start from the question, not the event

The first line of any instrumentation plan answers: **what question will this data answer, and who will ask it.**

Write the question in plain language before any event name appears. Examples:

- "What percentage of new users finish the setup flow within 24 hours."
- "Which integrations are most commonly attempted but never completed."
- "How long does it take a user to hit the first aha moment."

If the question is vague, the events will be vague. Fix the question first.

### Step 2. Separate actions from raw events

Two layers of event:

- **Raw events.** Low-level captures. "button_clicked", "page_viewed", "form_submitted". Fire automatically or near-automatically. Many. Often noisy.
- **Actions.** High-level business events. "order_placed", "agent_handoff", "trial_converted". Fired deliberately or derived from raw events. Few. Stable. Named after user outcomes.

Dashboards and funnels should be built on actions. Debugging and session replay should rely on raw events. Mixing the two is the single most common cause of tracking chaos.

### Step 3. Name events with a consistent grammar

One grammar, stated once in the taxonomy doc and applied everywhere.

Recommended default:

```
object_action[_qualifier]
```

Examples:

- `order_placed`
- `order_refunded`
- `agent_conversation_started`
- `agent_conversation_ended`
- `subscription_upgraded_annual`

Rules:

- All lowercase.
- Underscores, no hyphens, no camelCase, no spaces.
- Object first, action in past tense, optional qualifier last.
- No product prefixes unless the company runs multiple products in the same workspace.
- No client names, no geo prefixes, no environment prefixes.

### Step 4. Attach properties that answer the follow-up questions

For each event, list the properties that will be needed to answer the obvious follow-up questions.

Four categories:

1. **Who.** User ID, account ID, role, segment.
2. **Where.** Surface, page, feature flag cohort.
3. **What.** Specific values that describe this instance of the event.
4. **Context.** Session ID, device, client version, timestamp offset.

Rules:

- Every property is typed.
- Enum properties have a closed list. No free-form strings for categorical data.
- PII only when necessary and only in systems that can process it.
- Null is a valid value. Missing is not.

### Step 5. Define funnels and cohorts on top of actions

A funnel is an ordered sequence of actions. A cohort is a set of users who performed a named action within a window.

For each funnel:

- **Steps.** The ordered list of actions.
- **Window.** Maximum time between first and last step.
- **Primary conversion.** The step used as the headline number.
- **Breakdown dimensions.** Properties used to slice the funnel.

For each cohort:

- **Entry condition.** The action and window that qualifies a user.
- **Exit condition.** When the user leaves the cohort, if ever.

### Step 6. Point every event at a dashboard

If an event does not feed a dashboard, an alert, or a report, it should not be fired. Noise is expensive.

For each event, name:

- Dashboard or report that uses it.
- Owner of that dashboard.
- What decision it supports.

An event with no owner for its downstream use is a candidate for removal.

### Step 7. Specify the QA plan before release

Before the feature ships:

- Run the flow in a test environment.
- Verify every event fires once, with correct properties.
- Verify no event fires twice.
- Verify no event fires for a path where it should not.
- Check the event in the analytics tool, not only in the client code.

### Step 8. Handle PII with policy, not vibes

Write the PII policy for this feature, even if it is one line.

- Which properties are PII.
- Which systems are allowed to receive them.
- Whether user IDs are pseudonymous.
- Retention window.

If the company has a central policy, link to it and name the exceptions specific to this feature.

### Step 9. Write the change policy

Instrumentation drifts. Write how it gets changed.

- Who can add a new event.
- Who can deprecate an event.
- How existing dashboards are migrated when an event changes.
- Where the canonical taxonomy lives.

## Templates

- `templates/en/feature-instrumentation-plan.md`: instrumentation plan for a single feature.
- `templates/en/event-taxonomy-entry.md`: one entry in the company-wide event catalog.
- `templates/es/feature-instrumentation-plan.md`: plan de instrumentación para una feature.
- `templates/es/event-taxonomy-entry.md`: entrada en el catálogo de eventos.

## Related skills

- `dashboard-spec`: reach for it when the events feed an internal tool or admin view and you need to spec the views, not the tracking.
- `data-reconciliation`: use it when two tools already disagree on a metric, before redefining events.
- `prd-authoring`: instrumentation is a section inside the PRD; produce the section there, do not rewrite the PRD here.
- `ux-audit`: pairs with this when usage metrics look wrong and you need to find the UX cause before reinstrumenting.

## Anti-patterns

This skill must never produce:

- A tracking plan that starts with event names instead of questions.
- Events named after UI elements ("blue_button_clicked", "modal_closed") without business meaning.
- Two events that are actually the same event named differently.
- Properties with free-form strings where an enum is correct.
- A plan with no owner for any downstream dashboard.
- A plan that mixes environments or tenants in the event name.
- A plan that fires events only client-side when server-side truth is available.
- A plan that ships without a QA step.
- A plan that leaves PII policy undefined.

## Checklist before delivery

- [ ] Each event has a stated question it answers.
- [ ] Actions and raw events are clearly separated.
- [ ] Naming grammar is stated once and applied consistently.
- [ ] Every event has typed properties, with enums closed.
- [ ] Every event points to a dashboard or an explicit reason to exist.
- [ ] Funnels and cohorts are defined on actions, not raw events.
- [ ] QA plan is written.
- [ ] PII policy is stated.
- [ ] Change policy is stated.
- [ ] No buzzwords from the voice rules appear.
