---
name: proposal-scoping
description: Use this skill when the user asks to scope a custom development engagement, structure a commercial proposal, break work into phases, or decide between time-and-materials and fixed-price. Trigger phrases include "scope this proposal", "price this project", "break this into phases", "T&M vs fixed", "propuesta de alcance", "cotizar este proyecto", "statement of work", "SOW". Produces a scope document structured around phases, deliverables, exclusions, and commercial model.
---

# proposal-scoping

> **Anchor:** What is explicitly out of scope is worth more words than what is in.

## When to use

Use this skill when the user needs to convert a sales conversation, a brief, or an RFP into a scoped engagement. Works for:

- A custom development project that has a clear client and loose requirements.
- A discovery engagement that precedes a larger build.
- A retainer or fractional engagement that needs cadence, scope boundaries, and escalation rules.
- A phase-by-phase rewrite of a scope that got fuzzy mid-engagement.

Do not use when:

- The user is writing a product spec. Use `prd-authoring`.
- The user is responding to a government or enterprise RFP with a compliance matrix. Use `rfp-response`.
- The user is writing a migration plan. Use `migration-spec`.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard industry terms in English: scope, SOW, milestone, deliverable, T&M, fixed-price, retainer, kickoff, handover.
- **EN.** Direct US business register. Avoid vendor cliches: "strategic partner", "trusted advisor", "world-class".
- Write in the language of the document signatory. If the deal is bilingual, produce both.

## Method

### Step 1. Choose the commercial model before writing the scope

The model shapes the scope. Pick one:

| Model | When it fits | Risk holder | Scope shape |
|---|---|---|---|
| Time and materials | Unknown volume, changing priorities, deep unknowns. | Client. | Outcomes loose, cadence tight. |
| Fixed price | Known shape, bounded unknowns, finite output. | Vendor. | Outcomes tight, change control formal. |
| Retainer | Ongoing capacity, rolling priorities. | Shared. | Hours or seats guaranteed, list of allowed work types. |
| Outcome-based | Measurable target, shared incentive. | Shared. | Outcome defined, methods free. |

If the client pushes for fixed price on a scope with unresolved unknowns, state the risk in writing and either move to T&M for a discovery phase first or convert the unknowns to explicit assumptions with change triggers.

### Step 2. Decompose by phase

A phase is a unit of work with its own start condition, end condition, and deliverable. Common phases:

- **Discovery.** Interviews, audit, prototypes, spec.
- **Design and architecture.** Flows, data model, tech choices, risk list.
- **Build.** Implementation against a frozen spec.
- **Integration and hardening.** Third-party glue, security, performance.
- **Launch.** Release, monitoring, handover.
- **Operate.** Post-launch support or retainer.

Do not collapse phases to save words. The phase boundary is where commercial and technical risk live.

### Step 3. Write deliverables as artifacts, not activities

A deliverable is a thing the client can review and accept. "We will work on design" is not a deliverable. "Figma file with 12 screens covering flows A, B, C, reviewed with the client, revisions closed" is.

Each deliverable has:

- **Artifact.** The thing produced.
- **Format.** Where it lives and how it is accessed.
- **Review.** Who reviews and within how long.
- **Acceptance.** What it means to accept it.

### Step 4. Name dependencies and assumptions

Every engagement depends on the client doing things on time. Write them down.

- Access to staging, test data, single sign-on, secrets, design files, brand assets.
- Named decision maker available on a stated cadence.
- Stakeholder availability for interviews and reviews.
- Third-party credentials and rate limits.

An unfulfilled dependency after a stated deadline triggers the change management clause in step 7.

### Step 5. Write the exclusions list

The exclusions list is the most important section in the document. Write it before the price.

For each exclusion, one line: what it is and why it is out. Common items:

- Production infrastructure ownership.
- On-call or SLA coverage.
- Content migration beyond stated volume.
- Integrations not named in the scope.
- Accessibility audits beyond the stated level.
- Translation or localization.
- User research beyond stated number of interviews.
- Training or enablement beyond stated sessions.

If a client pushes back on an exclusion, either add it to scope with a price, or leave it out. Do not quietly absorb it.

### Step 6. Price only after scope is settled

Pricing a fuzzy scope is how vendors lose money and clients lose trust. If you are asked to price before scope is settled, quote the discovery phase only.

For each phase:

- **Model.** T&M, fixed, or milestone.
- **Effort.** Hours or rate card, with a band if T&M.
- **Timeline.** Business days from start condition to end condition.

### Step 7. Write the change management clause

A single paragraph, not a contract appendix. Cover:

- What counts as a change.
- Who requests and who approves.
- How long the change is evaluated before it is accepted or rejected.
- How the price or timeline is recalculated.

### Step 8. Define the kill clause

Either party can exit. Spell out how.

- Notice period.
- What happens to work in progress.
- What happens to intellectual property.
- What happens to already-paid fees.

### Step 9. Review the scope as the client's CFO

Before handing off, read the scope assuming you are the client's CFO. Can you tell what you are buying, what you are not buying, what triggers more money, and how you stop.

## Templates

- `templates/en/proposal-tm.md`: time-and-materials engagement.
- `templates/en/proposal-fixed.md`: fixed-price engagement.
- `templates/es/proposal-tm.md`: engagement por tiempo y materiales.
- `templates/es/proposal-fixed.md`: engagement de precio fijo.

## Related skills

- `prd-authoring`: use it when the work is a product spec, not a commercial scope.
- `rfp-response`: use it instead when responding to a government or enterprise RFP with a compliance matrix.
- `migration-spec`: use it when the engagement is a migration that needs parity, cutover, and rollback.
- `vendor-evaluation`: the buyer-side counterpart, for choosing the vendor before scoping the work.

## Anti-patterns

This skill must never produce:

- A scope with no exclusions section.
- A price before the scope is settled.
- Deliverables phrased as activities ("we will work on X").
- A fixed-price proposal with open-ended assumptions.
- A vague cadence ("regular syncs", "as needed").
- A kill clause buried in a footer.
- A scope that mentions "best practices" as a commitment.
- A phase that starts before its dependencies are named.
- A document that uses the word "partnership" more than once.

## Checklist before delivery

- [ ] Commercial model is stated in the first page.
- [ ] Every phase has a start condition, an end condition, and a deliverable.
- [ ] Every deliverable has an artifact, a format, a review path, and an acceptance rule.
- [ ] Dependencies have owners and deadlines.
- [ ] Exclusions list has at least five items.
- [ ] Price is tied to the scope, not to an anchor from the sales call.
- [ ] Change management clause fits in one paragraph.
- [ ] Kill clause is visible and readable.
- [ ] No buzzwords from the voice rules appear.
