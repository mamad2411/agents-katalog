---
name: prd-development
description: "Produces a comprehensive Product Requirements Document using Amazon's Working Backwards method: start with the press release, then FAQ, then detailed requirements. This approach forces clarity of thought by starting from the customer outcome and working backward to the requirements."
category: execution
default_depth: standard
---

# PRD Development

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Produces a comprehensive Product Requirements Document using Amazon's Working Backwards method: start with the press release, then FAQ, then detailed requirements. This approach forces clarity of thought by starting from the customer outcome and working backward to the requirements.

## When to Use

- Kicking off a new feature or product initiative
- Aligning cross-functional teams on scope and requirements
- Documenting decisions for future reference
- Before engineering estimation or design exploration

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Small feature or fast-follow with clear scope | Press Release headline + summary, Goals & Success Metrics, Scope (In/Out), Open Questions |
| **Standard** | New feature or cross-functional initiative | All sections |
| **Deep** | New product line, platform migration, or regulatory feature | All sections + competitive analysis appendix, data privacy impact assessment, rollout experiment design |

**Omit rules:** At Light depth, skip the full Press Release, FAQ, and Detailed Requirements phases. Produce a 1-page brief: problem, proposed solution, success metric, scope boundaries, and open questions.

## Framework

### Phase 1: Working Backwards (The Press Release)

Before writing requirements, write a fictional press release announcing the finished product. This forces you to think from the customer's perspective.

The launch is imagined. The quotes are not. Every quote in the press release must come from a real, named source (interview, support ticket, sales call, memo, review). If no sourced quote exists, leave the slot as `[TBD, requires: ...]`. Invented quotes get copied into decks and sales material as if they were real.

```markdown
# Internal Press Release: [Feature/Product Name]

## Headline
[One sentence that a customer would care about]

## Subheading
[Who is it for and what benefit do they get?]

## Summary Paragraph
[2-3 sentences: What is being launched? What problem does it solve? What's the key benefit?]

## Problem Statement
[Describe the problem from the customer's perspective. No jargon. A customer should recognize this as their problem.]

## Solution
[How does the product solve this problem? Focus on the experience, not the implementation.]

## Quote from Leadership
"[Real quote from the sponsor or a named leader, with source and date. If none exists yet: [TBD, requires: sponsor quote from kickoff, strategy memo, or approval note]. Do not write one on their behalf.]"

## How It Works
[3-5 bullet points describing the customer experience, step by step]

## Customer Quote
"[Real quote from a customer interview, support ticket, sales call, or review that shows the pain or the value, with source and date. If none exists: [TBD, requires: customer interview or support ticket quote]. Never invent a customer or a quote.]"

## Call to Action
[What should the reader do next?]
```

### Phase 2: FAQ

```markdown
# Frequently Asked Questions

## Customer FAQ
Q: [Question a customer would ask]
A: [Answer]

Q: [Question about how it works]
A: [Answer]

Q: [Question about pricing or availability]
A: [Answer]

## Internal FAQ
Q: Why now? What's the urgency?
A: [Answer with data]

Q: What are we NOT building?
A: [Explicit scope exclusions]

Q: How will we measure success?
A: [Metrics and targets]

Q: What are the biggest risks?
A: [Top 3 risks and mitigations]

Q: What's the estimated effort?
A: [T-shirt size and breakdown]
```

### Phase 3: Detailed Requirements

```markdown
# Product Requirements Document: [Feature Name]

## Metadata
- Author: [PM name]
- Last updated: [date]
- Status: [Draft / In Review / Approved]
- Stakeholders: [list]

## 1. Context & Motivation
[Why are we doing this? What evidence supports the need?]
- Customer evidence: [interviews, support tickets, usage data]
- Business case: [revenue impact, retention impact, strategic alignment]
- Opportunity cost: [what we're NOT doing to do this]

## 2. Goals & Success Metrics
| Goal | Metric | Segment | Current | Target | Unit | Timeframe | Source |
|---|---|---|---|---|---|---|---|
| [Goal 1] | [metric] | [customer group] | [baseline value] | [target value] | [%, days, $, or count] | [when] | [where the baseline came from] |
| [Goal 2] | [metric] | [customer group] | [baseline value] | [target value] | [%, days, $, or count] | [when] | [where the baseline came from] |

Current and Target hold only the value: a number, comparator, range, or an explicit placeholder such as TBD. Label the customer group in Segment, put the measurement label in Unit, and put every citation, link and "(source: ...)" note in the Source column. The validator rejects source text inside a value cell and requires Segment, Unit, and Source columns for structured metrics.

**Guardrail metrics** (must NOT get worse):
- [metric] must stay above [threshold]

## 3. User Stories
### Persona: [Name]
- As a [persona], I want to [action] so that [outcome]
  - Acceptance criteria:
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
  - Edge cases:
    - [Edge case 1: expected behavior]

### Persona: [Name]
[Repeat for each relevant persona]

## 4. Scope
### In Scope
- [Requirement 1]
- [Requirement 2]

### Out of Scope
- [Item 1], Rationale: [why]
- [Item 2], Rationale: [why]

### Future Considerations
- [Item that may come later]

## 5. Design & UX Requirements

### Key Flows
For each primary user flow (usually 2-4):
- **[Flow name]:** [Entry point] > [step] > [step] > [success outcome]
  - Screens touched: [list]
  - Decision points: [where the user chooses, branches, or can go wrong]

### Screen States
For every new or changed screen:
| Screen | Empty | Loading | Error | No permission | Success |
|---|---|---|---|---|---|
| [Screen] | [what shows before any data exists] | [skeleton, spinner, or progressive load] | [message and recovery action] | [what a user without access sees] | [confirmation and next action] |

### Interaction & Accessibility
- [Key interaction patterns, and which existing design-system components they reuse]
- [Accessibility requirements: keyboard, screen reader, contrast, focus order]
- Designs: [link to mockups if they exist; otherwise [TBD, requires: design mockups]. Until mockups exist, the flows and states above are the design brief.]

## 6. Technical Considerations
- [API changes needed]
- [Data model implications]
- [Performance requirements]
- [Security considerations]

## 7. Dependencies
| Dependency | Team/System | Status | Risk |
|---|---|---|---|
| [Dep 1] | [team] | [status] | [risk level] |

## 8. Rollout Plan
- [ ] Phase 1: [Internal dogfood, date]
- [ ] Phase 2: [Beta with N%, date]
- [ ] Phase 3: [GA, date]

## 9. Open Questions
| Question | Owner | Due Date | Resolution |
|---|---|---|---|
| [Question 1] | [name] | [date] | [TBD / resolved] |
```

### Cross-Section Consistency Check

Before finalizing a Standard or Deep PRD, reconcile every material customer promise across the Press Release, FAQ, Detailed Requirements, Scope, Dependencies, and Rollout Plan. Check especially:

- supported audiences, applications, integrations, and availability stages;
- access, security, data-retention, or other state-change behavior;
- timing guarantees, including what happens to work already in progress or sessions already active;
- metrics, populations, units, targets, and timeframes; and
- exclusions, fast-follows, dependencies, and GA gates.

For each promise, either specify the same behavior and boundary in every relevant section or state the difference plainly. Do not let a customer-facing statement imply an outcome that the requirements, scope, or rollout cannot deliver. For example, if a release promises cancellation, say whether work already queued or in progress completes, stops, or needs a support action. If immediate cancellation is required, make it an explicit requirement, dependency, rollout gate, and measurable acceptance criterion.

Work backward from the operative acceptance criteria as well as forward from the promise. Keep an internal mapping of promise, requirement and acceptance measure, mismatch, and correction. Compare the trigger, affected population, time bound, exceptions, and required dependencies. A percentile target is not an absolute guarantee, an optional safeguard cannot support an unconditional promise, and a schedule is not continuous behavior. Narrow the customer claim to the specified behavior or make the stronger design an explicit unresolved requirement that blocks approval. Recheck the corrected announcement, FAQ and decision summary against that mapping.

Consider adjacent applications, user flows, and active state when they share the changed behavior. State the affected boundary and add a regression guardrail or acceptance criterion when the change can affect them. Keep a fast-follow out of customer promises until it is actually in scope.

## Minimum Evidence Bar

**Required inputs:** A problem statement with at least one form of customer evidence (interviews, support tickets, usage data, or market research). At Light depth, prior PRD, launch data, or documented stakeholder alignment satisfies the evidence requirement for fast-follows with clear scope.

**Acceptable evidence:** Customer interview transcripts, support ticket volume/trends, usage analytics, churned-customer feedback, competitive teardowns, or sales call recordings.

**Insufficient evidence:** If no customer evidence exists for the stated problem, produce a partial artifact with unanswered sections marked `[TBD, requires: customer interviews, support ticket analysis, or usage data]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Problem statement, current metric baselines, and documented customer pain must be grounded in evidence.
- **Hypotheses:** Proposed solution, success metric targets, and estimated effort are hypotheses -- label them as such until validated through design review or prototype testing.

## Output Format

When an automated handoff or benchmark explicitly requests structured output, also read `docs/structured-artifacts.md` and the matching schema from the Shipwright installation root. Append the validated envelope and keep it consistent with the visible artifact. Ordinary chat output needs no JSON duplicate.

At **Light** depth, produce the 1-page brief from the Depth table: problem, proposed solution, identified success metric with explicit baseline/target gaps, scope in/out, and open questions. Do not require the full press release, FAQ, or detailed requirements. A Light PASS means the brief is directionally usable; it does not authorize engineering handoff.

At **Standard** and **Deep** depth, produce a complete PRD with all three phases:
1. **Press Release**, customer-facing narrative
2. **FAQ**, customer and internal questions answered
3. **Detailed Requirements**, full specification

**Shipwright Signature (required closing):**
4. **Decision Frame**, build/buy/partner recommendation, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, unvalidated customer assumptions, missing technical feasibility data, untested pricing or GTM hypotheses
6. **Pass/Fail Readiness**, PASS if the problem is evidence-backed, success metrics have baselines and targets, and scope boundaries are explicit. At Light depth, a directional brief can PASS with an identified metric and explicit baseline/target gaps; it is not engineering-ready until those gaps and detailed requirements are resolved. FAIL if evidence or scope boundaries are absent. A well-formed FAIL is an honest unreadiness result, not a broken artifact.
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why. When the PRD includes UI work and section 5 still says `[TBD, requires: design mockups]`, name a design step (mockups or a UX flow review of the key flows and screen states) before `technical-spec`, so engineering does not spec against undefined screens

## Common Mistakes to Avoid

- **Starting with requirements**, Always start with the press release to ground the work in customer value
- **No success metrics**, If you can't measure success, you can't know if you succeeded
- **Missing "out of scope"**, Scope creep starts when boundaries aren't explicit
- **Writing for engineers only**, A good PRD is readable by design, marketing, and leadership too
- **Treating the PRD as final**, It's a living document; update it as you learn
- **Inventing quotes**, A made-up leadership or customer quote is not evidence and will be reused as if it were; use a sourced quote or a `[TBD, requires: ...]` placeholder
- **UX section as a link placeholder**, "[Link to designs]" gives engineering nothing to build; spell out the key flows and the empty, loading, error and permission states per screen

## Weak vs. Strong Output

**Weak:**
> **Problem:** Users have trouble with onboarding. We should make it better. **Success metric:** Improve onboarding completion.

No customer evidence, no baseline, no target -- impossible to scope, estimate, or measure.

**Strong:**
> **Problem:** 62% of trial users abandon onboarding at the integration step (Mixpanel, Jan-Feb data). Support tickets citing "can't connect my data" increased 3x since v2.1 launched. **Success metric:** Integration-step completion rate from 38% to 65% within 60 days of launch; support tickets tagged "integration-setup" decrease by 50%.

Grounded in specific data, cites sources, and sets measurable targets with timeframes.
