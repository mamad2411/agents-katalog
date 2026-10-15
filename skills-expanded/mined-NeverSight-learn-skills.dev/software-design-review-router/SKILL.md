---
name: software-design-review-router
description: Use this skill when the user wants a software design review, architecture critique, domain model review, boundary review, ADR critique, naming review, dependency impact analysis, change-resilience review, scalability or performance-governance review, security/authorization/auditability review, or a review of an AI-generated plan or code change from a design perspective. Also use it when the user describes design symptoms without naming design review directly, such as unclear service boundaries, conflicting responsibilities, risky schema changes, brittle coupling, weak tenant isolation, overloaded terms, uncertainty about aggregates and ownership, workaround-heavy plans, or concern that a change is too ad hoc to survive future modification. Do not use it for straightforward implementation, syntax help, framework tutorials, or isolated bug fixes.
---

# Software Design Review Router

Review software design by routing to the smallest useful set of reference lenses, then synthesize one system-level judgment.

Match the user's language when asking questions, explaining tradeoffs, and delivering the final review.

This skill is especially useful for:

- reviewing AI-generated implementation plans before execution
- reviewing AI-generated code changes for structural risk
- collaborating on feature-change plans where long-term evolvability matters
- critiquing proposals that feel locally convenient but globally fragile

Default behavior:

1. Pick exactly one primary review lens.
2. Add up to two secondary lenses only when they materially change the judgment.
3. Read only the references you selected.
4. Return one integrated review, not a stack of disconnected mini-reviews.

## When Not To Use This Skill

Do not use this skill when the task is primarily:

- implementing a feature
- fixing a syntax or type error
- answering framework or library how-to questions
- debugging a single defect with no design tradeoff to evaluate
- reviewing code only for style, lint, or local correctness

If the task is mostly code maintainability with no meaningful design question, do not trigger this router just because maintainability is mentioned.

## Workflow

Follow this sequence:

1. Frame the review.
2. Select references.
3. Review through the selected lenses.
4. Synthesize a system-level judgment.
5. Self-check before responding.

Reference reading rule:

- start with the shared front sections of each selected reference
- go into `Deep checks` only when the initial review reveals meaningful ambiguity, structural weakness, or high-impact risk
- do not expand into deep checks for every lens by default

## 1. Frame The Review

Before opening references, identify:

- the design decision or design tension being evaluated
- the dominant concern that should drive the judgment
- the likely system scope: component, service, bounded context, API, schema, workflow, or platform capability
- whether the user wants critique of an existing design, comparison of options, or validation of a proposed direction
- whether the artifact under review is a plan, a code change, an ADR, or a broader design proposal

Choose one dominant concern. Good defaults:

- architectural decision quality for ambiguous tradeoffs
- dependency impact for risky change propagation
- coupling for boundary and responsibility leakage
- change resilience for ad hoc fixes, workaround hardening, or future modification pressure
- domain language or modeling for semantic ambiguity
- non-functional governance for scale, latency, throughput, or cost constraints
- security governance for authorization, trust boundaries, auditability, or tenant isolation

Good artifact-to-lens defaults:

- AI-generated plan with plausible structure but weak reasoning: start with `decision-quality-review`
- change plan with rollout, migration, or blast-radius uncertainty: start with `dependency-change-impact-analysis`
- code or plan that feels ad hoc, workaround-heavy, or over-abstracted: start with `change-resilience-review`
- service split, shared schema, or cross-team friction debate: start with `software-coupling-review`
- domain confusion, naming drift, or aggregate tension: start with `domain-description-language`, `ubiquitous-language-naming-review`, or `relationship-modeling-review`

## 2. Select References

Pick one primary reference first. Add secondary references only if they change the recommendation, not merely because they are related.

### Primary Lens Selection

- Read [references/decision-quality-review.md](references/decision-quality-review.md) when the main question is whether the decision framing, criteria, alternatives, or reasoning are sound. This is the default primary lens for ADR critique and architecture tradeoff review.
- Read [references/dependency-change-impact-analysis.md](references/dependency-change-impact-analysis.md) when the main risk is blast radius, migration safety, hidden consumers, or compatibility fallout from a change.
- Read [references/software-coupling-review.md](references/software-coupling-review.md) when the main issue is service boundaries, schema or API coupling, responsibility placement, or change propagation across layers.
- Read [references/change-resilience-review.md](references/change-resilience-review.md) when the main issue is ad hoc structure, workaround hardening, speculative extensibility, or whether the change makes the next likely change easier without overbuilding for unknown futures.
- Read [references/domain-description-language.md](references/domain-description-language.md) when the main issue is ambiguous business meaning, fuzzy rules, overloaded states, or unclear domain operations.
- Read [references/ubiquitous-language-naming-review.md](references/ubiquitous-language-naming-review.md) when the main issue is naming, term consistency, vocabulary drift, or context-specific semantics.
- Read [references/relationship-modeling-review.md](references/relationship-modeling-review.md) when the main issue is aggregates, ownership, lifecycle relationships, conceptual boundaries, or entity coordination.
- Read [references/non-functional-budget-governance.md](references/non-functional-budget-governance.md) when the main issue is scale, latency, throughput, reliability, performance-cost tradeoffs, or operational budget governance.
- Read [references/security-authorization-auditability-governance.md](references/security-authorization-auditability-governance.md) when the main issue is authorization, trust boundaries, privileged flows, auditability, or tenant isolation.

### Secondary Lens Selection

- Add [references/maintainability-review.md](references/maintainability-review.md) only as a secondary lens when long-term changeability, readability, or testability would materially alter the design recommendation.
- Add [references/decision-quality-review.md](references/decision-quality-review.md) as a secondary lens when another primary lens finds a structural issue but the deeper problem may be bad framing or a distorted evaluation axis.
- Add [references/software-coupling-review.md](references/software-coupling-review.md) as a secondary lens when another primary lens exposes boundary leakage or cascading ownership problems.
- Add [references/change-resilience-review.md](references/change-resilience-review.md) as a secondary lens when the main proposal looks locally convenient but may harden a workaround, increase future change friction, or introduce speculative abstraction.
- Add [references/non-functional-budget-governance.md](references/non-functional-budget-governance.md) as a secondary lens when the design may be locally elegant but operationally expensive or unstable.
- Add [references/security-authorization-auditability-governance.md](references/security-authorization-auditability-governance.md) as a secondary lens when a design change crosses trust boundaries or weakens accountability.
- Add [references/domain-description-language.md](references/domain-description-language.md), [references/ubiquitous-language-naming-review.md](references/ubiquitous-language-naming-review.md), or [references/relationship-modeling-review.md](references/relationship-modeling-review.md) when the primary issue is really semantic drift or broken conceptual boundaries.

## 3. Review Through The Selected Lenses

For each selected reference:

- apply its method faithfully
- keep findings in the language of that reference
- extract only the findings that matter to the current design tension

Do not turn every review into a full checklist run. Prefer the smallest set of decisive findings.

If the initial pass reveals hidden risk, contradictory signals, or unclear structural tradeoffs, read the `Deep checks` section of the selected reference before finalizing the judgment.

## 4. Synthesize One Judgment

Integrate the findings in this order:

1. conflicting optimization goals
2. local optimizations that displace cost elsewhere
3. short-term versus long-term tradeoffs
4. final system-level recommendation

If lenses disagree, explain which dominant concern wins and why.

## Output Contract

Structure the final review with these sections:

- `framing`: what problem is actually being solved and what decision is under review
- `dominant concern`: the primary evaluation axis and why it should dominate
- `findings`: the most important design findings, ordered by severity or decision impact
- `tradeoffs`: the real tradeoffs, including what gets worse if the recommendation is adopted
- `recommended direction`: the best current direction, with any preconditions or sequencing advice
- `open questions`: missing information that could change the judgment

When the user asked for a review of existing material, keep the output in a review voice. When they asked for guidance, keep the same structure but phrase the recommendation as design advice.

## Gotchas

- Do not blur multiple references into generic architecture advice.
- Do not include a secondary lens unless it changes the recommendation.
- Do not let maintainability replace the primary design judgment; it is a supporting axis here.
- Do not confuse naming symptoms with domain-model problems without checking both possibilities.
- Do not stop at isolated critiques; always conclude with a system-level judgment.
- Do not optimize for short-term implementation convenience if it shifts complexity into future change, operations, or governance.
- Do not skip `Deep checks` when the proposal feels polished but under-evidenced, or when an AI-generated plan or code change looks coherent yet structurally suspicious.

## Self-Check

Before responding, verify:

- one primary lens is explicit
- no more than two secondary lenses were used
- each selected reference was necessary
- the review explains the dominant concern
- the conclusion is integrated rather than a list of unrelated observations
- the response stays at design-review level rather than drifting into implementation details
