---
name: assess-improvement
description: Assess an existing repository for a small, evidence-backed improvement opportunity and produce a scoped findings report and handoff briefs. Use for read-only improvement planning, including multi-harness Polytropos assessments; do not use to implement, enable providers, or promote policy changes.
---

# Assess improvement opportunities

Produce a reviewable, evidence-first assessment of whether a bounded improvement is worth testing. The result is planning input, not a diagnosis engine, evaluation record, policy change, or authorization to modify the repository.

## Boundaries

- Treat target source and configuration as read-only by default. Writing the requested findings report or task briefs to the designated output location is allowed. Do not install packages, mine private telemetry, invoke paid/private providers, make network calls, mutate target repositories, or change policy or release state solely because this skill is in use.
- Preserve existing user authorization. A bounded network, private-data, paid-provider, or test action already authorized for this assessment may be used as evidence; record its scope and provenance. The skill itself grants no new live-action authority.
- Use tools and tests only when they can answer an assessment question and are authorized. Prefer deterministic inspection; when a test needs mutation, run it against a temporary copy and report that limitation.
- Do not infer a defect from absence, a plan, a stale document, a schema, or a single anecdote. Label the state `unknown`, `unverified`, or `insufficient-evidence` as appropriate.
- Keep facts, constraints, judgments, and proposed actions separate. A proposed finding is not an authoritative engine record.
- Preserve existing ownership boundaries. Describe the authority already responsible for admission, execution, verification, evidence, pricing/budgets, and release; do not create a competing global authority through a report.
- Do not turn one repository's observation into a global rule. Recommendations are scoped to a named repository, component, harness, task cohort, and evaluation context.

## When to use

Use this skill when asked to find or prioritize improvement opportunities in an existing codebase, prepare an evidence-driven improvement plan, assess a harness/runtime ecosystem, or create a handoff for later implementation.

Do not use it to implement, activate, or promote a change. It can assess the suitability of a broad redesign, incident remedy, or provider proposal when the requested outcome is a scoped evidence-based conclusion, including `no-fit` or `insufficient-evidence`.

## Read only what can answer the question

1. Restate the assessment scope: repository/revision, requested outcome, components and harnesses in scope, time window if any, and the evidence that is allowed. State exclusions and unknown access up front.
2. Establish the baseline before suggesting change. Read repository instructions, current architecture and lifecycle documents, relevant contracts, recent tests/fixtures, release/evaluation material, and targeted source paths. Use revision-aware citations (file path, symbol or line, and revision when available).
3. Map authorities and interfaces. Identify what currently owns the behavior, what is merely documentation or an adapter claim, and which boundaries must remain fixed. Treat advertised capability and demonstrated runtime enforcement as different evidence classes.
4. Look for a *small recurring pain signal*: repeated failure category, reproducible divergence, persistent manual recovery, a documented limitation corroborated by code/tests, or a clear evaluation gap. One failure can create a hypothesis; it cannot establish recurrence or expected benefit.
5. Test applicability and no-fit. For each candidate, identify affected and unaffected scopes, prerequisites, privacy/authorization constraints, incompatible environments, and counterexamples. If the candidate requires missing evidence, say so rather than extrapolating.
6. Choose the smallest intervention that could falsify the hypothesis while preserving existing acceptance, permission, budget, and verification rules. Prefer deterministic/manual mechanisms first. Do not require an inference provider, external model, or optional dependency for a useful first experiment.
7. Define evaluation before recommending promotion. Compare a named baseline with an ordinary control and a candidate under comparable task cohort, budget/resource ceilings, acceptance criteria, and partitioning. Specify the label source, exclusion rules, counterevidence, rollback target, and the condition for `insufficient-evidence`.
8. Deliver the report and self-contained task briefs using the template in [references/assessment-template.md](references/assessment-template.md). Do not implement tasks or create global rules from this assessment.

## Evidence standard

Use an evidence ledger with one row per material claim:

| Claim | Evidence and provenance | Scope | Categorical status | Counterevidence or gap |
| --- | --- | --- | --- | --- |

Distinguish these statuses:

- `observed`: directly supported by current source, fixture, record, or authorized measurement.
- `documented`: stated in maintained material but not independently verified here.
- `inferred`: a bounded interpretation; give the reasoning and alternatives.
- `unknown` / `unverified`: evidence is absent or could not be checked.
- `insufficient-evidence`: evidence cannot support an expected-benefit or promotion claim.

Never convert a model output, valid typed response, benchmark replay, or self-reported cost into proof of semantic correctness or causal improvement. Cache/replay evidence only applies when its project/provider eligibility, task and acceptance version, complete input state, policy version, and relevant calibration/version context match.

Use the categorical status above; do not introduce a numeric probability by default. If a proposal uses a numeric confidence or probability, state its prediction target, provenance, and validation status separately. An uncalibrated number is not an expected-benefit estimate.

## Candidate selection

Prefer candidates that are narrow, reversible, and testable. Suitable first candidates often include a deterministic guard, stronger evidence join, bounded context-repair trigger, clearer unsupported-state handling, or a manual proposal/reporting seam.

Record a candidate's gated prerequisites before recommending evaluation or promotion. A candidate may still be worth assessing when it needs:

- a new permission or authority boundary, including an experiment-isolation gap;
- access to private data, telemetry, credentials, or a paid provider;
- clean evaluation partitions and a controller-owned hidden-label boundary;
- defined labels and held-out validation before any calibration claim;
- a simpler experiment that separates simultaneous changes and permits attribution.

Broad executable policy languages and autonomous self-modification are `no-fit` or deferred by default. Assess them only as separately requested research with external acceptance and permission boundaries. Reject a proposal that requires candidate access to hidden answers or treats contaminated audit data as independent evidence.

Future provider integrations may be recorded as conditional work: name the required authorization, privacy review, technical conformance, no-spend/manual fallback, and local comparative evaluation. Do not assume credentials, network access, a model identity, prices, or provider behavior beyond what the user has already authorized.

## Polytropos whole-system mode

When the scope is Polytropos as a whole, assess the shared runtime and each supported harness independently before synthesizing. Cover, where present:

| Surface | Ask |
| --- | --- |
| Shared runtime/contracts | Which component is authoritative for task lifecycle, admission, budgets, policy identity, evidence, readiness, and acceptance? |
| Four harnesses | Which behavior is native, adapted, documented-only, runtime-verified, or unsupported for each harness? Do not transfer pricing, capability, or enforcement claims across harnesses. |
| Skills and context/planning | Is applicability explicit? Can a skill be withheld for contradiction, staleness, or no-fit? Are graph/context outputs advisory evidence rather than permission? |
| Evaluation and release | Are baseline, control, candidate, partitions, labels, release claims, rollback, and supported-environment matrix separately evidenced? |

Do not require an arbitrary repository to adopt these modules. For another repository, use the same questions only where their existing architecture has an analogous responsibility; otherwise record `not-applicable` with the reason.

For an adaptive-decision opportunity, preserve this chain: bounded state -> advisory typed judgment or deterministic rule -> deterministic policy selection -> fresh admission -> native execution -> required verification -> authoritative attempt evidence. A judgment cannot grant tools, spend, remove dependencies, weaken acceptance, or promote itself.

## Deliverables and stopping condition

Deliver a scope-specific findings report plus zero or more independent task briefs in the requested or designated output location. A good report may conclude there is no supported intervention. Stop after the assessment when evidence is insufficient, no small recurring signal exists, the required evidence is unavailable, or the next step needs authorization that is not already present.

Each task brief must state: objective; exact scope and out-of-scope; existing authorities to preserve; evidence links; proposed bounded change; non-goals; acceptance criteria; deterministic/offline verification; evaluation dependencies; required approval or private/paid access; and rollback/no-promotion condition. It must be usable by a later implementer without access to the assessment conversation.

If multiple candidates exist, rank only within the assessment scope using expected learning value, reversibility, evidence quality, and disruption. Do not rank by an invented probability, vendor claim, or presumed cost.

## Optional context travel

If the current surface separately exposes the `context-travel` skill and an explicit repository, kit, assignment, and authorized startup config are supplied, consult that skill's on-demand guide at `docs/CONTEXT-TRAVEL-SURFACES.md` for a bounded reviewer brief. This assessment card does not install or claim that skill on any surface. Treat missing, stale, partial, or refused context as advisory; retain this workflow's authoritative sources, policy, pricing, permission, and mandatory verification rules. If context travel is unavailable, continue this assessment and report that limit.
