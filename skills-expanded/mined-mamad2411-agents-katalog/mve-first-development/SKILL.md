---
name: mve-first-development
description: "Use whenever planning, implementing, testing, or reviewing early-stage product work, greenfield features, unstable contracts, spikes, prototypes, vertical slices, MVP/MVE delivery, or requests to get the minimum real path working. Route the work through Shape, Probe, Prove, Protect, and Harden; default to Prove/MVE when the user or project does not declare a stage. Prevent premature TDD, contract freezing, broad mock-based E2E suites, and production hardening before one real end-to-end path exists."
---

# MVE-First Development

Use this skill to choose the **right delivery discipline for the current level of uncertainty**. Early product work and production work should not be forced through the same process.

Default rule: **when the stage is not explicit, use `Prove` (MVE-first)** and cut scope until one real, observable end-to-end path can run. Use a narrow `Probe` only when one unresolved technical question blocks that path.

This is not an anti-testing skill. It delays expensive contract protection until there is an accepted behavior worth protecting.

## Core Rule

**Fix the appetite; vary the scope.**

Set a bounded amount of time and attention before designing the solution. Inside that appetite:

- solve the smallest meaningful problem
- prefer one integrated vertical slice over many completed horizontal layers
- keep the solution rough enough to change and bounded enough to finish
- call out rabbit holes and explicit no-gos
- cut scope before adding time, abstraction, or test matrices
- stop when the stage exit condition is met

Do not confuse a detailed plan with reduced uncertainty. In R&D work, learning often comes from building against the real boundary.

## Stage Router

| Stage | Main question | Default work | Validation | Exit condition |
|---|---|---|---|---|
| `Shape` | What problem is worth this appetite? | Baseline, outcome, rough solution, rabbit holes, no-gos | Review the framing and key risks | The work is rough, solved enough, and bounded |
| `Probe` | Can the highest-risk assumption work? | One time-boxed spike against the real unknown | Direct experiment and captured evidence | The question is answered well enough to choose or reject an approach |
| `Prove` | Can the smallest real user/system path work end to end? | One fixed scenario and the thinnest vertical slice | One real canary plus minimal checks | The real path runs, the result is observable, and no blocker invalidates it |
| `Protect` | Which observed behavior is now accepted and must survive change? | Characterization tests, focused regressions, contract convergence, refactoring | Tests derived from real runs and known failures | Accepted behavior has a useful regression safety net |
| `Harden` | Is the system ready for external users and operational commitments? | Security, reliability, recovery, performance, migrations, runbooks, release evidence | Full risk-appropriate suites and release gates | The declared production/release bar is met |

### Selection precedence

1. Follow an explicit user instruction about the stage or required method.
2. Follow a canonical project stage when one is declared.
3. Route release, regulated, destructive, security-critical, or already-consumed stable contracts to `Protect` or `Harden`.
4. Route greenfield work with unstable behavior to `Prove`; insert a `Probe` only for the blocking unknown.
5. When still ambiguous, choose `Prove`.

A project may contain mixed stages. A settled authentication boundary may be in `Harden` while a new agent workflow remains in `Probe` or `Prove`.

## Shape-Up Principles Adapted for Agent Work

### Appetite, not estimate

Declare how much time the question deserves before expanding the design. An appetite is a constraint on the solution, not a prediction of how long a preselected solution will take.

### Rough, solved, bounded

Do enough shaping to identify the core interaction and technical path, but do not freeze speculative API fields, tables, abstractions, or edge-case behavior. Detail only the risky spots that could trap the implementation.

### R&D mode accepts scrapwork

When core behavior and architecture are unsettled, disposable code is allowed. Optimize for learning and an integrated demonstration, not for preserving every early implementation.

### Get one piece done

Make one tangible slice work early. Avoid building models, adapters, UI shells, and test scaffolds separately with integration deferred until the end.

### Scope hammering

When the work is too large, question every use case and implementation detail:

- Can one tenant, user, provider, workspace, or message type prove the idea?
- Can a fixed configuration replace a registry for now?
- Can plain text replace cards, rich UI, or generalized schemas?
- Can a manual step remain until the core path is proven?
- Can a feature move to the deferred ledger without invalidating the result?

### Hill status

Report uncertainty, not percentage complete:

- `thought-about`: an approach exists only in theory
- `validated`: the approach touched the real boundary
- `known`: meaningful unknowns are resolved; execution remains
- `done`: the stage exit condition is met

Do not call a scope downhill merely because a design document is detailed.

### Circuit breaker

If the appetite expires without meeting the exit condition, stop by default. Record what was learned, cut or reshape the approach, and make a new bet. Do not automatically extend the task because work has already been invested.

## Minimal Planning Contract

For early work, prefer this compact contract over a large speculative task breakdown:

```yaml
stage: prove
appetite: <time or effort budget>
baseline: <what happens without this change>
outcome: <the one result this stage must prove>
real_path: <real entry -> application/core -> real boundary -> observable result>
highest_unknown: <the assumption most likely to invalidate the path>
scope_now: []
no_gos: []
rabbit_holes: []
canonical_smoke: <command or exact runbook>
exit_condition: <minimum evidence that ends the stage>
hill_status: <thought-about|validated|known|done>
deferred:
  feature: []
  hardening: []
  questions: []
```

Do not create an exhaustive backlog before touching the real work. Prefer discovered tasks over imagined tasks.

## Stage Workflows

### Shape

Produce only what is needed to make a sensible bet:

1. State the problem and current baseline.
2. Set the appetite.
3. Sketch the core elements and connections at low fidelity.
4. Identify rabbit holes that could consume the appetite.
5. Declare no-gos and unsupported use cases.
6. Stop before implementation details become speculative contracts.

### Probe

Use a probe to answer one question, not to build a disguised subsystem:

1. Write the question and pass/fail observation.
2. Touch the real dependency, runtime, provider, database, device, or protocol.
3. Use the shortest reversible implementation.
4. Capture command, input, output, logs, IDs, and limitations.
5. Decide: adopt, adapt, reject, or probe again with a narrower question.
6. Delete or clearly label disposable code when it should not become a foundation.

A probe does not need a regression suite unless it protects an irreversible safety boundary or reproduces a real defect.

### Prove — default MVE mode

Build the smallest meaningful vertical slice:

1. Fix one representative user/system scenario.
2. Use one real entry point and at least one real critical boundary.
3. Implement only the state and interfaces needed for that path.
4. Produce one observable final result or artifact.
5. Leave one canonical smoke command or exact runbook.
6. Capture minimal evidence and a deferred ledger.
7. Stop as soon as the exit condition is met.

Hard-coded test identities, one provider, one workspace, one message type, or a manual setup step are acceptable when they are explicit, reversible, and do not falsify the result.

### Protect

Protect behavior after it has been observed and accepted:

1. Start from real transcripts, traces, artifacts, bug reports, and stable examples.
2. Add characterization tests for behavior the team intends to preserve.
3. Add focused regressions for defects that actually occurred or risks now made concrete.
4. Converge contracts only where a real consumer depends on them.
5. Refactor behind the safety net.
6. Remove experimental shortcuts that now obstruct maintainability.

Do not invent a broad idealized contract suite disconnected from the behavior the product actually chose.

### Harden

Apply the production bar appropriate to the risk:

- deterministic unit and state-machine tests
- real database/service integration tests
- public API, event, tool, and provider contract tests
- critical user-journey E2E tests
- idempotency, retry, crash-window, and recovery tests
- security, authorization, secret, and tenant-isolation tests
- migration, compatibility, performance, capacity, and operability checks
- alerts, runbooks, rollback, audit, and release evidence

Hardening can cut product scope too. Production readiness is not an excuse to preserve every experimental feature.

## Testing Policy

In `Probe` and `Prove`, do **not** default to Red-Green-Refactor for behavior whose contract is still being discovered. Use this order:

```text
cheapest check needed to keep the experiment honest
-> one targeted real integration path
-> one real end-to-end canary
-> one critical invalidation case, only when it would make the result false or unsafe
```

A test is worth adding when it protects at least one of these:

- accepted product behavior
- a known failure or reproduced bug
- a stable interface with a real consumer
- an irreversible or high-risk safety invariant
- a refactor that would otherwise be unsafe

Mocks may accelerate local diagnosis, but they do not prove a real integration or MVE. A broad mock-based E2E suite before the real path runs is usually negative progress.

In `Protect` and `Harden`, TDD and broader regression suites are appropriate. If the user explicitly requests TDD earlier, honor that instruction while keeping the appetite and test surface narrow.

## Review Policy

Classify every finding before deciding whether it blocks the current stage:

- `BLOCKER-NOW`: the real path cannot complete, the evidence is false, a critical boundary is bypassed, or the experiment creates an unacceptable safety/data risk
- `DEFERRED-FEATURE`: useful for the next product slice but not required for the current proof
- `HARDENING`: reliability, recovery, security depth, performance, operability, edge cases, or polish for production
- `QUESTION`: unresolved decision with an explicit, reversible temporary path

In `Probe` and `Prove`, only `BLOCKER-NOW` is a required change by default. Review should answer:

1. Did the stage prove what it claimed?
2. Did a real user or system path actually run?
3. Is the result observable and reproducible?
4. Is the next stage unblocked?
5. Which findings belong in the deferred ledger?

Do not require every correct review suggestion to be fixed in the same slice.

## Timebox and Stop Rules

- At the midpoint, if no real path exists, hammer scope before adding abstractions or tests.
- When the appetite expires, stop and reshape instead of automatically extending.
- When the exit condition is met, stop polishing and move to the next stage.
- When the same issue recurs, promote it from a note into a regression, lint, skill, tool contract, or architecture rule.

## Promotion Triggers

Move from `Probe` to `Prove` when the blocking unknown is resolved enough to choose a path.

Move from `Prove` to `Protect` when one or more are true:

- the owner accepts the observed behavior
- the path succeeds repeatedly
- a second consumer depends on it
- persistent data or migration semantics now matter
- a structural refactor is about to begin

Move from `Protect` to `Harden` when external users, production data, operational commitments, regulated behavior, or a release decision make failure costs material.

## Interaction with Other Skills

This skill owns **stage selection, appetite, scope, and validation intensity**.

- Use team-lead/orchestration skills for delegation after this skill defines the finish line.
- Use runtime companion skills for concrete execution commands.
- Apply TDD/test-generation skills by default only in `Protect` or `Harden`, unless the user explicitly requests them earlier.
- Apply security and release skills whenever risk demands them; MVE-first never overrides critical safety boundaries.

## Non-Goals

This skill does not:

- excuse unverifiable claims or fake integrations
- permit secrets, cross-scope data leaks, or unapproved destructive actions
- replace product judgment about whether the problem matters
- require six-week cycles or Basecamp tooling
- force every project to remain experimental
- prohibit tests; it makes them follow evidence and stage maturity

## Shape Up Source Notes

Adapted from the following Shape Up concepts:

- Set Boundaries: https://basecamp.com/shapeup/1.2-chapter-03
- R&D, Production, and Cleanup modes: https://basecamp.com/shapeup/2.3-chapter-09
- Risks, rabbit holes, and out-of-bounds scope: https://basecamp.com/shapeup/1.4-chapter-05
- Get One Piece Done: https://basecamp.com/shapeup/3.2-chapter-11
- Circuit breaker: https://basecamp.com/shapeup/2.2-chapter-08
- Hill Charts: https://basecamp.com/shapeup/3.4-chapter-13
