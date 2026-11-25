---
name: objective-code-review
description: Review commits, pull requests, and merge requests for requirement correctness, disciplined scope, design integrity, project fit, non-functional obligations, and regression protection without confusing pragmatism with permissiveness.
---

# Objective Code Review

Review for the product, not for personal taste. A change must satisfy its requirements, fit the system, and leave the touched design coherent without expanding beyond its scope.

Core rule:

> Surface unmet requirements, material product risk, and structural defects in priority order. Explain the consequence and smallest corrective direction; leave the merge decision to the human owners.

## Establish the contract

Before judging implementation, determine what the change is required to do.

Triangulate from:

- the ticket, commit, PR, or MR description;
- acceptance criteria and author explanation;
- existing behavior, tests, documentation, and nearby code;
- repository policies, configuration, and established conventions;
- obligations implied by the changed surface.

Do not invent a requirement from preference. If available evidence cannot establish intent, ask one precise question that names the ambiguity and risk. Do not present an unproven concern as a defect.

## Review order

1. **Correctness** — Does every affected path produce the required behavior, including relevant failures and boundaries?
2. **Design integrity** — Does new code model the current domain honestly, or does it introduce copied history, impossible states, ambiguous names, or repeated defensive reasoning?
3. **Scope** — Is each change necessary for the requirement or a small, low-risk cleanup directly adjacent to it?
4. **Material risk** — Does the change introduce security, data integrity, reliability, compatibility, or serious maintainability risk?
5. **Project fit** — Does it use the project's deliberate design, libraries, patterns, and abstractions rather than blindly reproducing nearby accidents?
6. **Non-functional requirements** — Does the changed surface preserve its operational and product obligations?
7. **Regression protection** — Do tests protect the observable behavior that changed?

A passing test suite is evidence, not proof that the requirement is satisfied. Trace the requirement through the changed behavior.

## Review the structural delta

Treat behavior changes as changes to system structure, not isolated lines.

For a **bug fix**, trace:

1. the observable symptom;
2. the representation, boundary, ownership gap, dependency, or control flow that allowed it;
3. the path by which it escaped existing types, tests, validation, or signals;
4. the new home of the invariant;
5. the compensating guards or duplicate policy the fix makes removable.

Treat a patch that only suppresses the reported input as incomplete when the same allowing structure remains. A local correction is sufficient when the invariant already exists, the system normally enforces it, and the defect is genuinely isolated—for example, incorrect static text.

For a **feature**, identify the structure it creates or modifies:

- public and internal contracts;
- shared domain vocabulary used by product owners, project or product managers, designers, documentation, support, and engineers;
- domain states and transitions;
- responsibility and ownership;
- dependencies and component boundaries;
- data relationships, ordering, identity, and expected size;
- resource, failure, observability, compatibility, and test obligations.

A feature is incomplete when its happy path works but its new states, boundaries, ownership, or failure behavior remain implicit.

### Structural probes, not a checklist

Use only probes relevant to the changed surface. Convert every concern into an observable mismatch, violated invariant, or concrete change cost.

- **Architecture and semantics** — Does the implementation follow the deliberate architecture? Are APIs, names, versions, types, and product vocabulary consistent and truthful?
- **Local comprehension and total flow** — Can the behavior, component interactions, conditional outcomes, failures, and transitions be understood from declared inputs without hunting through hidden state?
- **Cohesion and boundaries** — Does each component own one cohesive policy? Are dependencies minimal, explicit, testable, and directed toward the invariant's owner?
- **Representation fitness** — Do types and data structures naturally express required states, relationships, ordering, identity, cardinality, and dominant operations without sentinels, parallel collections, awkward key mutation, or caller compensation?
- **Evolution cost** — At evidenced data size and caller growth, does the design remain bounded and changeable without speculative abstraction or premature optimization?

Code length, modularity, reuse, loose coupling, composition, and inheritance are not goals by themselves. Use them only as evidence for or remedies to a concrete comprehension, ownership, representation, testability, or change-cost problem. A stack models LIFO; a queue models FIFO; judge either by required ordering rather than a generic preference.

## Tiger Style lens

Borrow [Tiger Style](https://tigerstyle.dev/)'s safety, performance, and experience lenses, not its project-specific rulebook. Apply them proportionately to the changed surface.

### Safety

Correctness is necessary but not sufficient. For code at a meaningful boundary or failure domain, check:

- explicit limits on caller-controlled resources, concurrency, retries, queues, loops, and fan-out;
- invariants expressed through types, assertions, or validation at the point where violation becomes dangerous;
- failures that are visible and contained instead of silently swallowed or converted into false success;
- interfaces with minimal surface area, clear ownership, and a defined fault model;
- deterministic seams around physical or non-deterministic dependencies where the project already supports them.

Do not demand assertions, limits, or fault machinery without a concrete failure mode. Existing behavior on a trusted, naturally bounded path is not a material concern merely because it lacks extra defense-in-depth.

### Performance

For changes that can materially affect latency, throughput, or capacity, make a rough mechanical sketch across network, storage, memory, and compute. Consider both bandwidth and latency, including multiplicative costs such as unbounded fan-out, repeated allocation or copying, serialization, and per-item I/O.

Performance findings need repository evidence, measurements, an explicit requirement, or a plausible material scale. Do not block on speculative micro-optimization.

### Experience

Optimize for the total cost of ownership: users who run the product and engineers who read, debug, and operate it repeatedly. Prefer:

- direct control and data flow;
- small interfaces and simple representations;
- names that expose meaning, units, ordering, and limits;
- state and variables defined close to where they are used;
- designs whose failure behavior can be understood locally.

Use established project conventions as the default, but do not use them to excuse a semantically false model. Do not impose Tiger Style's static allocation, zero-dependency policy, fixed integer choices, naming syntax, recursion ban, or zero-technical-debt stance unless the project or a concrete requirement calls for them. In particular, never use “zero technical debt” to expand a scoped change.

## Design integrity

Pragmatism means choosing the simplest design that expresses the actual contract. It does not mean approving avoidable confusion because the code runs or resembles nearby code.

Apply a higher bar to greenfield code and newly introduced abstractions: there is no compatibility constraint yet. Legacy constraints can explain a compromise; copied legacy code does not create one.

Check the touched design for:

- **Honest history** — Names and versions describe real, current contracts. A new controller, API, or type must not inherit `V2`, `V3`, `legacy`, migration flags, or predecessor comments unless those predecessors or an external compatibility contract actually exist.
- **Copy residue** — Reused code must be adapted completely. Audit copied identifiers, routes, versions, comments, error messages, feature flags, authorization, types, and tests. Similar structure is acceptable; leaked source semantics are not.
- **Truthful state models** — Types represent the domain states callers may rely on. An optional boolean creates three states: `true`, `false`, and absent. If absence has no distinct meaning, remove the optionality or default once at the boundary. If the domain has more than two meaningful states, use the language's enum, union, discriminated union, or equivalent named representation.
- **Local reasoning** — Do not make every caller remember permissive expressions such as `flag !== false`, double negation, sentinel combinations, or repeated absent-value checks. Give the policy one name and one boundary.
- **Justified abstraction** — Every suffix, layer, mode, and configuration branch must correspond to a present requirement or established project contract, not anticipated history or cargo-culted structure.
- **Shared domain vocabulary** — Use the same concept name used by the people defining and operating the product, whether that group is called product, project management, a product owner, or something else. Check tickets, acceptance criteria, UI copy, product documentation, support language, APIs, events, metrics, tests, and nearby code. Two names for one concept force engineers and stakeholders to translate mentally; one name for two concepts hides a domain distinction.

Treat this as semantic correctness, not naming taste. If authoritative sources disagree, ask which term is canonical and name the affected contracts. When a legacy or external protocol requires another term, translate once at that boundary and keep the shared vocabulary inside. Do not spread aliases through the system.

These are not cosmetic findings when introduced by the change. Treat misleading history, an ambiguous state model, competing vocabulary, or copied residue as a material concern when it establishes a public contract or a pattern future code must repeat. Keep a one-off readability improvement optional only when the current representation is still semantically exact and locally obvious.

Project conventions are evidence, not immunity. Follow deliberate conventions; challenge a nearby pattern when the new change exposes that it is accidental, semantically false, or needlessly spreads invalid states.

## Classify and process structural design defects

Call this family **structural design defects**: the code may execute today, but its names, types, or duplicated policy make correct future changes unnecessarily expensive. Do not downgrade them to “code smells” or “technical debt”; those labels hide the concrete defect and imply optional cleanup.

Use one subtype:

- **Semantic integrity defect** — A name, version, comment, interface, or domain term claims history or meaning the system does not have, or introduces a second name for an existing product concept. Example: a greenfield `V3` controller with no predecessor or a feature called “Saved Views” by the product team but “Presets” throughout new code.
- **Copy-residue defect** — Reused code retains source-system identity, policy, assumptions, or dead branches that do not belong in the target.
- **State-model defect** — The representation permits unnamed, contradictory, or impossible states, so callers must infer policy. Example: an optional boolean when absence is not a real domain state.
- **Boundary/ownership defect** — A responsibility or invariant has no clear owner, dependencies point the wrong way, or correctness relies on hidden component interactions.
- **Representation mismatch** — A type or data structure does not naturally support the domain's relationships, ordering, size, or dominant operations, forcing compensating code.
- **Change-amplification defect** — One policy is encoded as repeated conditions, sentinels, or compensating checks, increasing the number of places a correct change must touch.

Process each defect with four facts:

1. **Mismatch** — Quote what the code says and the repository evidence that makes it false or ambiguous.
2. **Invariant** — State the rule the design should make obvious, such as “this controller has no version lineage” or “feature state is exactly enabled or disabled.”
3. **Amplification** — Name who must compensate now and what becomes more expensive later: callers, tests, documentation, routing, migration, or compatibility.
4. **Direction** — Recommend the smallest correction that restores truthful semantics; do not prescribe a broad redesign.

Severity follows propagation and correction cost, not whether production has failed yet:

- **Material concern** — The change introduces false semantics, competing vocabulary, or an invalid state model into new code; establishes a public/shared contract; makes callers compensate; duplicates the workaround; or would require compatibility work or migration to correct later.
- **Separate follow-up** — The defect is pre-existing, not relied on or worsened by this change, and has a named owner.
- **Worth considering** — The representation is semantically exact and local; only presentation or readability could improve.

The key review question is: **Does merging this make the next correct change touch more places or first unlearn a lie?** If yes, it is a defect with measurable change-amplification cost, not a preference.

## Scope discipline

Allow:

- code required to implement or safely verify the requested behavior;
- small, low-risk cleanup next to the changed code when it makes the requested change clearer.

Challenge:

- unrelated refactoring;
- broad renaming or formatting churn;
- opportunistic architecture changes;
- dependency or pattern replacement unrelated to the stated goal.

An architectural change is in scope when the PR explicitly exists to introduce or replace that design. Otherwise, respect deliberate project decisions even when another design would be preferable. Challenge an established pattern when using it here causes concrete correctness or material risk, carries false history into a new contract, or spreads an ambiguous state model.

## Non-functional requirements

Non-functional requirements are requirements. Infer applicable obligations from repository evidence and the type of surface being changed.

Check only relevant obligations, including:

- API or controller documentation, discoverability, and whether the surface is intentionally internal;
- authentication, authorization, privacy, and input boundaries;
- compatibility for existing callers, stored data, protocols, and configuration;
- failure visibility, observability, resource ownership, and operational behavior;
- performance or capacity constraints where the change can materially affect them;
- rollout, migration, and rollback safety where state or external consumers are involved.

Do not demand generic ceremony. Tie every finding to repository evidence, the changed surface, or a concrete material risk.

## Tests

Changed observable behavior should be protected where practical and proportionate.

For bug fixes, normally surface a missing regression test as a material concern. The escaped bug demonstrates an unprotected path, so the test must fail without the fix and pass with it. Treat coverage as optional only when the author gives a concrete reason that it is impractical or disproportionate.

For other changes, surface missing coverage as material when the new or changed observable contract has meaningful regression risk and existing tests do not protect it. Prefer contract behavior over private implementation details.

## Classify advice

### Material concerns

Use for:

- unmet functional or non-functional requirements;
- incorrect behavior or incomplete handling of an affected path;
- concrete security, data integrity, reliability, compatibility, or similarly material risk;
- newly introduced misleading history, competing vocabulary, copy residue, or an ambiguous state model that becomes a contract or repeatable pattern;
- avoidable accidental complexity in greenfield code that forces callers to reproduce non-obvious reasoning;
- an unjustified scope expansion that increases review or product risk;
- a practical but missing regression test for a bug fix;
- missing protection for another materially risky observable contract.

### Questions

Use when missing evidence prevents a conclusion. Ask for the exact fact needed to assess the risk; do not disguise a preference as a question.

### Worth considering

Use for optional improvements that do not prevent the change from satisfying its contract. A pre-existing issue that this change neither relies on nor worsens belongs in a separate follow-up only when material.

## Advisory policy

- Act as an advisor, not the merge authority. Never output `Approve`, `Disapprove`, `Request changes`, or another merge verdict.
- State material concerns plainly; advisory language must not soften evidence-backed correctness or structural defects.
- Lead with the highest-cost root cause. Consolidate repeated symptoms under it and cite only representative locations.
- Return at most five findings across all sections. Omit low-value nits and empty sections.
- Recommend the smallest corrective direction, not a mandatory implementation, unless only one implementation can satisfy the invariant.

## Output

Use:

```md
## Review assessment
[One or two sentences naming the requirement status, highest material risk or structural theme, and any evidence limit. No merge verdict.]

## Material concerns
- `path/to/file.ext:line` — `[Semantic integrity | Copy residue | State model | Boundary/ownership | Representation mismatch | Change amplification]` What is wrong, why it matters, and the smallest corrective direction.

## Questions
- `path/to/file.ext:line` — Precise question naming the missing fact and why it changes the assessment.

## Worth considering
- `path/to/file.ext:line` — Optional improvement and its concrete benefit.
```

Omit empty sections. Keep the assessment to two sentences and the complete response to the highest-value five findings. Point to the smallest useful file and line range. For repeated symptoms, report the shared structural cause once and list representative locations. Use a Tiger Style lens tag only when it sharpens a separate safety, performance, or experience reason.

When no material concerns, questions, or worthwhile observations exist, output:

```md
## Review assessment
No material concerns found in the reviewed scope.
```

## Avoid

- raising personal style, preferred libraries, or hypothetical purity as material concerns;
- restating the diff without identifying a defect, risk, or useful question;
- prescribing broad refactors for a local bug;
- treating uncertain risks as established failures;
- forcing the author to fix unrelated pre-existing debt;
- reporting no material concerns because tests pass without checking the actual requirement;
- treating copied code as an established convention without checking whether its names, versions, states, and assumptions are valid here;
- introducing implementation terminology that conflicts with the shared product vocabulary without a real domain distinction or external compatibility constraint;
- dismissing a misleading greenfield model as “just maintainability” when it creates the contract future changes must follow;
- burying a material concern among nits or optional suggestions.
