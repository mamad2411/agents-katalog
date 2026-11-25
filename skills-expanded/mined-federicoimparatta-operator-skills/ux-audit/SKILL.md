---
name: ux-audit
description: Use this skill when the user asks to audit a product's user experience, run a heuristic review, list UX issues, or produce a prioritized backlog of UX tickets. Trigger phrases include "UX audit", "heuristic review", "audit this flow", "review this product", "find UX issues", "auditoría de UX", "revisión heurística". Produces a structured audit ranked by severity and surface area, with each finding translatable into a ticket.
---

# ux-audit

> **Anchor:** Audit what users do, not what the product claims to offer.

## When to use

Use this skill when the user needs a structured review of an existing product, surface, or flow. Works for:

- A product in use that has accumulated UX debt.
- A recent release that needs an independent second pass.
- A competitor or reference product being reviewed for inspiration or diligence.
- A flow that metrics say is underperforming, to generate hypotheses before redesign.

Do not use when:

- The user wants to decide which UX issues to fix now vs later. Use `ticket-triage` after the audit.
- The user wants to instrument the flow to measure it. Use `analytics-instrumentation`.
- The user wants a competitor teardown as a sales asset. That is a different genre. Say so.

## Philosophy

A UX audit is anthropology, not judgment. The job is to observe what users do and where the product gets in the way, not to prove the PM correct or the designer wrong. Two handbook concepts apply. **PM as anthropologist:** every finding starts from a user moment, not from a heuristic checklist dropped on a screen. **Discovery is a practice:** the audit is discovery in disguise, and it succeeds when it kills at least one assumption the team held before it started. An audit that only confirms what the team already thought was wasted time.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: UX, onboarding, empty state, loading state, tooltip, hover, affordance, dark pattern, funnel.
- **EN.** Direct US business register. Do not soften bluntness. An audit is not a compliment.
- Screenshots or flow references use the in-product language, not the document language. If the product is English-only, the document can still be Spanish with English references.

## Method

### Step 1. Name the surface and the user

Before opening the product, write:

- **Surface.** The screens, flows, or features being audited. Bounded.
- **User.** The specific persona, role, or segment performing the tasks. If unknown, pick one and name the assumption.
- **Task.** The goal the user is trying to accomplish. Short verb phrase.

An audit without a user and a task is an aesthetic review.

### Step 2. Walk the task as the user

Run the task start to finish. Take notes as you go, not after.

Record:

- **What you see.** Screens, elements, state.
- **What you try.** Actions attempted, whether intended or exploratory.
- **What you feel.** Friction, confusion, confidence, satisfaction.
- **Where the product breaks expectation.** Gaps between what you expected and what happened.

Do this at least twice: once as a first-time user, once as a returning user. Record the differences.

### Step 3. Classify findings by heuristic

Apply a product-focused heuristic set. The default set:

| Heuristic | What it checks |
|---|---|
| Discoverability | Can the user find the relevant control without searching. |
| Feedback and affordance | Does the system signal state, progress, and outcome clearly. |
| Error prevention | Does the design prevent mistakes before they happen. |
| Recovery | When a mistake is made, can the user recover without restart. |
| Consistency | Same concept, same pattern across the product. |
| Information density | Enough to decide, not enough to drown. |
| Default behavior | Does the default save the user time, or create noise. |
| Empty state | Does empty state teach, or is it a blank canvas of confusion. |
| Loading and latency | Is latency hidden, signaled, or experienced as failure. |
| Accessibility | Can users with disabilities complete the task. |
| Dark patterns | Is any decision pushed on the user against their interest. |

Each finding is tagged with one primary heuristic. A second tag is allowed.

See `references/heuristics.md` for the full set.

### Step 4. Rank by severity and surface area

Two axes. Every finding carries both.

**Severity**

| Level | Definition |
|---|---|
| Critical | Blocks the user from completing the task. |
| High | Causes measurable drop-off or data loss. |
| Medium | Creates confusion or friction that slows the task. |
| Low | Minor irritation, no measurable effect. |
| Cosmetic | Visual inconsistency without user impact. |

**Surface area**

| Level | Definition |
|---|---|
| Systemic | Affects many features or the whole product. |
| Flow | Affects one flow end to end. |
| Screen | Affects one screen. |
| Component | Affects one component in isolation. |

Systemic-critical issues are where resources go first, regardless of how many other findings exist.

### Step 5. Write each finding as user-observable evidence

A finding is not an opinion. It has five parts:

- **What was observed.** One sentence, in user terms.
- **Expected.** What the user expected.
- **Actual.** What happened.
- **Evidence.** Screenshot, recording timestamp, or exact reproduction steps.
- **Why it matters.** One line connecting the finding to a user outcome.

### Step 6. Translate findings into tickets

Each finding becomes a ticket candidate. Write the ticket alongside the finding, not at the end.

Ticket minimum:

- Title in user-terms.
- Severity and surface area.
- Reproduction steps or screen reference.
- Acceptance criterion for the fix.
- Related finding IDs.

### Step 7. Summary with pattern view

At the end of the audit, step back.

- **Top three patterns.** Cross-cutting issues, not individual bugs.
- **Top three quick wins.** Low-effort fixes with visible user impact.
- **Top three structural bets.** Larger fixes that change the shape of the product.

This is the section leadership will read. The rest is for the team that will fix it.

### Step 8. Kill one assumption

Before declaring the audit done, name one assumption the team held that the audit disproved. If you cannot name one, run the walk again with different users or tasks. An audit that confirms everything has failed.

## Templates

- `templates/en/audit-report.md`: full audit report.
- `templates/en/ticket-from-finding.md`: single ticket derived from a finding.
- `templates/es/audit-report.md`: reporte completo de auditoría.
- `templates/es/ticket-from-finding.md`: ticket derivado de un hallazgo.

## Related skills

- `ticket-triage`: run it after the audit to decide which findings get fixed now versus later.
- `analytics-instrumentation`: use it when the flow needs measuring, not heuristic review.
- `prd-authoring`: move to it when a finding turns into a redesign that needs a spec.
- `red-team-review`: use it instead when the target is a plan or system, not a live user flow.

## Anti-patterns

This skill must never produce:

- An audit without a named user and a named task.
- Findings phrased as opinions ("this looks bad") instead of observations.
- A flat list of findings with no severity or surface area.
- A summary that only praises the product.
- Findings that require designer judgment to reproduce.
- Tickets that skip the acceptance criterion.
- An audit that uses "modernize" or "refresh" as a recommendation.
- A rating for elements the user does not interact with.

## Checklist before delivery

- [ ] Surface, user, and task are named on the first page.
- [ ] Every finding has observed, expected, actual, evidence, and why-it-matters.
- [ ] Every finding has a severity and a surface area.
- [ ] Every finding links to at least one ticket candidate.
- [ ] Summary has top three patterns, top three quick wins, top three structural bets.
- [ ] At least one assumption the team held is explicitly disproved.
- [ ] No buzzwords from the voice rules appear.
