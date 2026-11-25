---
name: fabrico-code-reviewing
description: "Performs extremely strict code and maintainability reviews against requirements, implementation plans, project conventions, and executable quality gates. Use for code reviews, thermo-nuclear or thermonuclear reviews, deep code-quality audits, and harsh maintainability reviews that must uncover structural regressions, spaghetti branching, weak abstractions, oversized files, boundary or type problems, security risks, and missing tests."
---

# Reviewing Code

Review changes for correctness and acceptance-criteria coverage, then apply an unusually strict maintainability bar. Seek high-confidence structural simplifications that preserve behavior while making the implementation smaller, clearer, and easier to extend.

<principles>

<evidence-before-findings>
Inspect the diff, surrounding implementation, project instructions, existing canonical helpers, and relevant tests before raising a finding. Distinguish verified defects and regressions from questions or preferences. Do not invent requirements or report a theoretical concern without a concrete failure mode.
</evidence-before-findings>

<structural-ambition>
Look beyond local cleanup. Search for a "code-judo" restructuring that removes branches, modes, helpers, layers, or state instead of merely redistributing them. Prefer direct, boring code and fewer concepts over cleverness, generic machinery, or extra indirection.
</structural-ambition>

<behavior-preservation>
Recommend structural changes only when the intended behavior and migration path are clear. Never trade correctness, security, atomicity, or required compatibility for aesthetic simplicity.
</behavior-preservation>

<high-signal-review>
Prioritize a small number of consequential, actionable findings. Do not bury structural problems under formatting, naming, or other low-value nits.
</high-signal-review>

</principles>

## Code Review Process

Use the checklist below and track progress:

```text
Review progress:
- [ ] Step 1: Establish requirements, scope, and project conventions
- [ ] Step 2: Verify behavior and acceptance criteria
- [ ] Step 3: Audit structural quality and maintainability
- [ ] Step 4: Audit tests, security, performance, and scalability
- [ ] Step 5: Run applicable quality gates
- [ ] Step 6: Report prioritized findings and a verdict
```

### Step 1: Establish requirements, scope, and project conventions

1. Read applicable root and nested project instructions.
2. Read the task context, acceptance criteria, and matching `*.research.md` and `*.plan.md` files when present. Use the referenced task-management source when an issue ID is available.
3. Identify the review baseline and inspect the complete diff. For branch reviews, include committed and uncommitted changes unless the request narrows the scope.
4. Inspect enough unchanged surrounding code to understand ownership, invariants, established abstractions, and existing helpers. Do not review the patch in isolation.
5. Record unavailable context or quality gates; do not silently assume they passed.

### Step 2: Verify behavior and acceptance criteria

For every meaningful change:

- Trace inputs, outputs, state transitions, error paths, and externally visible behavior.
- Compare the implementation with each requirement and plan item.
- Check edge cases, failure handling, backward compatibility, data migrations, and concurrency where relevant.
- Verify that tests exercise the behavior rather than merely mirror the implementation.
- Treat code claimed as pre-existing or reusable as in scope when the change depends on it.

Raise correctness findings before maintainability findings.

### Step 3: Audit structural quality and maintainability

Apply every lens below to the changed code and its immediate architectural context.

#### Structural simplification

- Ask whether reframing the state model, ownership boundary, or control flow can make entire conditionals, modes, wrappers, or layers disappear.
- Prefer deleting incidental complexity to extracting, renaming, or moving the same complexity.
- Reject refactors that only spread the same number of concepts across more files.
- Do not propose an abstraction unless it reduces cognitive load, centralizes a real invariant, or creates a canonical extension point.

#### Spaghetti and branching growth

- Flag ad-hoc conditionals, scattered feature checks, nullable modes, one-off booleans, and special cases inserted into unrelated flows.
- Treat repeated conditionals as evidence of a missing model, policy, dispatcher, state machine, or ownership boundary when that remedy is materially simpler.
- Flag narrow edge-case handling embedded in already busy functions.
- Reject temporary branches likely to become permanent debt unless their removal is explicit and enforceable.

#### File size and decomposition

- Measure changed files before and after the patch when size is material.
- Treat a change that pushes a file from below 1000 lines to above 1000 lines as a presumptive blocker.
- Waive the threshold only when the file has a compelling cohesive reason to remain whole and is still clearly organized.
- Recommend extraction by responsibility or ownership, not arbitrary line-count slicing.

#### Abstraction and directness

- Flag thin wrappers, identity adapters, pass-through helpers, and generic mechanisms that hide a simple data shape without buying clarity.
- Prefer a direct flow over magic, indirection, framework invention, or speculative extensibility.
- Reuse an existing canonical helper instead of adding a near-duplicate.
- Check that an extracted helper is cohesive and named after the concept it owns, not merely the code it contains.

#### Types, contracts, and boundaries

- Question avoidable `any`, `unknown`, casts, optional parameters, silent fallbacks, and loosely shaped objects that obscure an invariant.
- Prefer explicit models and shared contracts at system boundaries.
- Flag feature logic leaking into general-purpose modules, implementation details leaking through APIs, and logic placed outside the package, service, or layer that owns the concept.
- Check that validation and normalization occur at the canonical boundary rather than repeatedly downstream.

#### Orchestration and state

- Flag independent work serialized without a correctness or resource constraint when parallel execution is both clearer and safe.
- Flag related updates that can leave state partially applied; prefer transactions, idempotent operations, or another atomic design appropriate to the system.
- Separate orchestration from business rules when combining them makes either difficult to reason about or test.

#### Duplication and complexity

- Check copy-pasted logic, near-duplicate helpers, high cyclomatic complexity, deep nesting, excessive state, and modules with multiple unrelated responsibilities.
- Apply DRY only to stable, meaningful duplication. Do not create a forced shared abstraction for superficially similar code with different reasons to change.

### Step 4: Audit tests, security, performance, and scalability

Verify coverage for critical paths using the appropriate mix of unit, integration, and end-to-end tests.

- Treat missing integration coverage as substantive when correctness depends on a real database, transaction boundary, SQL semantics, migration, queue, filesystem, or external service.
- Check authorization, authentication, input validation, injection paths, secret exposure, unsafe deserialization, sensitive-data handling, and other relevant OWASP risks.
- Check N+1 database or network access, work performed inside loops, unbounded reads, and pagination, filtering, sorting, or aggregation done in memory when the database or upstream service should own it.
- Check algorithmic complexity, resource lifecycle, horizontal scaling constraints, race conditions, non-idempotent retries, and stateful components where relevant.
- Review documentation only when an API, operational procedure, public contract, or non-obvious invariant changed.

### Step 5: Run applicable quality gates

Discover project-provided commands and run the relevant subset:

1. Unit tests.
2. Integration tests.
3. End-to-end tests.
4. Linters, type checks, static analysis, and formatting checks.
5. Application and container builds when applicable.

Report the exact commands and outcomes. Never claim a gate passed when it was skipped, unavailable, or only partially run.

### Step 6: Report prioritized findings and a verdict

Order findings by impact:

1. Correctness, data loss, and security defects.
2. Structural regressions and high-confidence simplifications that delete material complexity.
3. Spaghetti branching, ownership leaks, non-atomic state, and unclear contracts.
4. File-size, decomposition, duplication, performance, and test-coverage concerns.
5. Other maintainability concerns.

For every finding include:

- severity and whether it blocks approval;
- precise file and line reference;
- concrete evidence and failure or maintenance consequence;
- the smallest credible remedy, favoring a simpler model over a cosmetic cleanup;
- a verification step when the fix is not self-evident.

After findings, include assumptions or open questions, quality-gate results, and one verdict: `APPROVED` or `CHANGES REQUESTED`. If no findings exist, say so explicitly and still report residual risks and skipped gates.

## Presumptive Blockers

Treat these as approval blockers unless concrete repository evidence justifies them:

- The change preserves material incidental complexity despite a clear, behavior-preserving path that removes it.
- A file crosses from below 1000 lines to above 1000 lines without a compelling cohesive reason.
- New special-case branching tangles an existing flow or scatters feature checks across shared code.
- An unnecessary wrapper, generic mechanism, cast-heavy contract, or optionality makes the design more indirect.
- Logic lands in the wrong architectural layer or duplicates a canonical helper.
- Related writes can leave state partially applied, creating a realistic consistency failure.
- Required behavior lacks meaningful verification or an applicable quality gate fails.

Do not approve merely because the implementation works on the happy path or current tests pass. Approval requires no unresolved correctness issue, no unjustified structural regression, and no obvious missed simplification whose absence materially harms maintainability.

## Preferred Remedies

Prefer remedies in this order when applicable:

1. Delete a concept, branch, wrapper, or layer that is not needed.
2. Reframe the model or default flow so special cases disappear.
3. Move ownership to the canonical module and reuse its existing extension point.
4. Make the boundary or type contract explicit.
5. Separate orchestration from business logic or make related state changes atomic.
6. Extract a cohesive helper, component, or focused module.

Be direct and specific without being rude. State material design regressions plainly; do not soften blockers into optional polish.

## Connected Skills

- `fabrico-implementation-gap-analysing` - compares the implementation with the approved plan and required scope
- `fabrico-technical-context-discovering` - establishes project conventions, architecture, and available quality gates
- `fabrico-codebase-analysing` - expands a change review into repository-wide dependency, duplication, and dead-code analysis
- `fabrico-sql-and-database-understanding` - provides deeper persistence, migration, transaction, index, and query review criteria
- `fabrico-reviewing-frontend` - provides frontend-specific component, hook, rendering, accessibility, and performance criteria
- `fabrico-engineering-prompts` - provides prompt-specific structure, injection defense, and evaluation criteria
