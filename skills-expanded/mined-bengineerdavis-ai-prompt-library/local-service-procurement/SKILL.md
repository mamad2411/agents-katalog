---
name: local-service-procurement
description: Helps a buyer discover what they actually need, research and validate local providers, compare complete quotes, and book a service with clear acceptance criteria. Starts from natural language and composes with interaction-questioning.
version: 0.3.0
status: draft
kind: reusable-skill
supersedes: local-service-procurement-skill-v0.2.0
composes_with:
  - interaction-questioning@2.3.2
  - service-provider-due-diligence-advisor@0.3.0
  - deep-research
  - panel-of-judges
outputs:
  - discovery-summary
  - procurement-brief
  - candidate-ledger
  - qualification-gates
  - vendor-call-sheets
  - quote-comparison-sheet
  - booking-and-acceptance-plan
license: MIT
---

# Local Service Procurement

## Purpose

Help a buyer select and use a local professional service provider when they may know the desired result but not the relevant provider types, methods, risks, questions, or realistic tradeoffs.

Examples include home cleaning, restoration, repair, moving, inspections, trades, installation, specialty services, and other purchases where service delivery matters as much as price.

## Relationship to Questioning

This skill does **not** begin by asking the buyer to fill out a procurement form. It delegates discovery control to `interaction-questioning@2.3.2`.

The questioning skill:

- distinguishes the initial request, the session task, the underlying outcome, and the session contribution;
- surfaces unknown unknowns with research and advisors;
- asks one user-facing question only when it materially improves the next decision;
- calibrates expectations where appropriate;
- stops at a good-enough threshold; and
- provides a plain-English understanding confirmation before this skill proceeds.

This skill owns the **service-buying workflow** after the session has enough context.

## Outcome

Produce a practical buying package:

1. discovery summary and assumptions;
1. procurement brief;
1. candidate ledger with evidence labels;
1. mandatory qualification gates;
1. shortlist of two to four providers;
1. short vendor-specific call sheets;
1. quote-comparison sheet with rows mapped to call questions;
1. booking, completion, and follow-up plan; and
1. reusable learning handoffs where a pattern could improve future artifacts.

## Workflow

### 1. Discover and frame

Use the Questioning skill first. Once it supplies its understanding confirmation, record:

```text
This session is helping the buyer [session contribution] so they can [underlying outcome].
```

Separate:

- hard requirements;
- preferences;
- known facts;
- safe defaults;
- research-resolvable gaps;
- decision-changing open questions; and
- acceptance criteria.

### 2. Add specialists only when needed

Use the Service Provider Due-Diligence Advisor by default.

Add a domain specialist when material, safety, health, code, asset, or method questions require expertise the buyer should not be expected to have. Add Pragmatist, Systems Thinker, Minimalist, or Negotiator only when their contribution changes the decision.

### 3. Research candidates

Use multiple evidence classes where possible:

| Evidence label | Meaning                                                             | Use                                                  |
| -------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| Verified       | Primary/regulatory/credential source or direct written confirmation | Gate or recommendation support                       |
| Corroborated   | Consistent independent sources                                      | Recommendation support with caveat                   |
| Vendor-stated  | Provider website or representative claim                            | Discovery/current claim; verify if decision-critical |
| Plausible      | Partial-evidence inference                                          | Turn into a task/question                            |
| Unsupported    | No usable evidence                                                  | Exclude from reasoning                               |

Build a candidate ledger with service fit, positive evidence, gaps, confidence, and next validation task.

### 4. Gates before scoring

Create five to eight pass/fail gates appropriate to the service. Typical gates:

- required logistics/service area;
- appropriate method or specialty competence;
- clear written estimate or statement of work;
- timing feasibility;
- sufficient evidence/communication fit;
- handling of material change before extra work; and
- practical completion/follow-up path.

Do not numerically rank a provider that fails a hard gate. Mark it `not a fit unless clarified`.

### 5. Short vendor calls

Create a 3–10 minute call sheet per viable provider:

1. friendly opening;
1. one open “walk me through how you would handle this” question;
1. targeted follow-ups only for important gaps;
1. a polite close if the workflow is not a fit;
1. short estimate request; and
1. a direct mapping from each question to one comparison-sheet field.

Use good-faith language. Documentation exists so both sides avoid surprises, not because the buyer is assuming bad intent.

### 6. Normalize quotes and select

Compare complete all-in value, not headline pricing.

```text
all-in authorized maximum =
base service
+ travel / pickup / return
+ taxes / mandatory fees / minimums
+ approved optional work
```

Identify what is included, what is optional, what is uncertain, and which provider offers the lowest **complete, comparable, clearly explained** value.

### 7. Book, accept, and learn

Create a practical job record and acceptance plan:

- agreed scope and estimate;
- appointment/access details;
- pre-service photos/notes if useful;
- what the provider will confirm at handoff/completion;
- what “done” looks like; and
- how to raise a reasonable follow-up concern.

Pass recurring discoveries, useful questions, and unsafe defaults to the Note-Taker as Questioning learning handoffs.

## Output Contract

```yaml
local_service_procurement_output:
  discovery_summary: ""
  procurement_brief: {}
  assumptions_and_defaults: []
  category_watchouts: []
  candidate_ledger: []
  qualification_gates: []
  shortlist: []
  vendor_call_sheets: []
  quote_comparison_fields: []
  booking_and_acceptance_plan: []
  reusable_learning_handoffs: []
```

## Quality Bar

The output passes only if:

- it begins from the buyer’s natural-language need rather than requiring expertise;
- questioning reaches a good-enough threshold before procurement workflow begins;
- it separates fact, evidence, vendor claim, assumption, and unknown;
- gates precede ranking;
- calls are short, friendly, and vendor-specific;
- comparison-sheet rows map directly to call questions;
- it compares all-in value rather than teaser pricing; and
- it leaves the buyer with a concrete next step.

## Version History

### v0.3.0 — 2026-09-07

- Refactored to compose explicitly with Interaction Questioning v2.3.2.
- Added goal/session-contribution handoff, understanding-confirmation dependency, and Questioning learning-handoff integration.
- Reduced duplicate discovery logic; this skill now owns procurement after Questioning finishes good-enough discovery.

### v0.2.0 — 2026-09-07

- Added adaptive discovery and unknown-unknown mapping.

### v0.1.0 — 2026-09-07

- Initial extraction from a local service-purchase workflow.
