---
name: refactor-guardian
description: Control risky structural change by proving a refactor is necessary and that behaviour, contracts, data, security boundaries, and operational properties can be preserved through a staged migration. Use whenever the user wants to refactor, restructure, clean up, modernise, extract, migrate, rewrite, or re-architect existing code, or asks whether they should. Prefer this over starting the refactor. DO NOT REFACTOR is a first-class outcome. Part of the audit suite; inherits the shared constitution while its own job is proving necessity and behavioural preservation.
---

# Refactor Guardian

**Epistemology: prove necessity, then prove behavioural preservation.**

Agents love to refactor. This skill is deliberately hostile to unnecessary cleverness.

> **DO NOT REFACTOR is a first-class outcome.**

If the pain is theoretical, the benefit cannot be measured, the blast radius exceeds the value, or an incremental repair is sufficient, leave the code alone and explain why.

Read `references/CONSTITUTION.md` first.

## Phase 0: Classify the proposed change

Before calling something a refactor, classify it.

- **Refactor:** internal structure changes while externally observable behaviour and required operational properties remain invariant.
- **Incremental repair:** local correction that relieves the problem without structural migration.
- **Migration:** technology, schema, protocol, or platform transition that may require compatibility management.
- **Feature change:** intended product behaviour changes.
- **Rewrite:** substantial replacement with material implementation and migration risk.

Do not smuggle feature changes or rewrites under the safer word "refactor."

## Gate 1: Necessity

### 1. Examine the claimed problem

Replace vague claims with measurable pain.

Weak:
> The code is messy.

Useful:
> Adding a provider requires editing seven modules in lockstep, and three of the last five provider additions caused inconsistent validation.

### 2. Establish baseline evidence

Collect, where relevant:

- defect frequency;
- lead time/change effort;
- repeated files/surfaces touched;
- incident history;
- performance baseline;
- reliability baseline;
- security constraint;
- dependency/platform deadline;
- test fragility;
- onboarding or ownership cost.

Do not invent metrics. If evidence is qualitative, say so.

### 3. Compare options

Compare:

A. Do nothing.  
B. Local repair.  
C. Incremental refactor.  
D. Migration.  
E. Rewrite/structural replacement.

Assess:

- expected benefit;
- implementation cost;
- migration cost;
- regression risk;
- reversibility;
- operational complexity;
- opportunity cost;
- time until benefit is realised.

Allowed verdicts:

- `DO NOT REFACTOR`
- `REPAIR LOCALLY`
- `REFACTOR INCREMENTALLY`
- `MIGRATION JUSTIFIED`
- `REWRITE JUSTIFIED`
- `NEEDS MORE EVIDENCE`

If necessity fails, stop. Do not author a migration plan for an unjustified change.

## Gate 2: Preservation

For approved structural work, build an invariant ledger.

Capture what must remain true:

- functional outputs;
- side effects;
- persistence semantics;
- transaction boundaries;
- ordering;
- retry/idempotency behaviour;
- error semantics;
- public API contracts;
- event/message schemas;
- data formats;
- backwards compatibility window;
- authentication/authorization boundaries;
- tenant isolation;
- accessibility interactions;
- performance budgets;
- availability/reliability properties;
- audit/observability requirements.

Separate intended behaviour from accidental behaviour. If consumers rely on accidental behaviour, treat it as a compatibility fact until migration is planned.

## Phase 3: Blast-radius and dependency map

Trace:

- target symbols/modules;
- direct and transitive callers;
- shared state;
- database/schema dependencies;
- API consumers;
- events and queues;
- jobs and schedulers;
- auth/policy dependencies;
- external clients and scripts;
- deployment topology;
- tests and fixtures;
- monitoring and operational runbooks.

Small diffs can have large blast radii.

## Phase 4: Choose a migration strategy

Consider, where applicable:

- branch by abstraction;
- strangler path;
- adapter/compatibility layer;
- expand-and-contract schema migration;
- shadow traffic;
- dual read with comparison;
- dual write only with reconciliation strategy;
- feature flags;
- canary rollout;
- backfill with checkpoints.

Do not cargo-cult migration patterns. Explain why the chosen pattern fits the risk.

Big-bang change is allowed only when incremental coexistence is impossible or materially more dangerous, and that claim must be justified.

## Phase 5: Define checkpoints and rollback

Each checkpoint should state:

- change;
- invariant at risk;
- proof required;
- observability signal;
- rollback method;
- point of no return, if any;
- cleanup condition.

Prefer independently shippable, behaviour-preserving checkpoints.

For schema/data migration define:

- expand step;
- backfill;
- consistency validation;
- compatibility period;
- read/write transition;
- contract step;
- rollback limits.

## Phase 6: Proof before movement

Before structural change:

- strengthen tests around invariants;
- add characterization tests where behaviour is undocumented;
- establish baseline metrics where performance/reliability motivates the change;
- capture representative contracts and fixtures;
- identify known bugs that should not accidentally become invariants.

If the test strategy itself is weak or broad, hand off to Test Architect.

## Phase 7: Incremental execution

For each approved slice:

1. state the invariant protected;
2. make one coherent structural move;
3. run targeted tests;
4. compare behaviour and relevant metrics;
5. inspect logs/errors;
6. verify compatibility;
7. decide proceed, pause, or rollback.

No opportunistic cleanup outside scope.

## Phase 8: Equivalence and migration verification

Verify:

- old and new paths agree where coexistence is expected;
- data is complete and consistent;
- clients remain compatible;
- permission boundaries are preserved or intentionally changed;
- performance remains within budget;
- retries and failure recovery still hold;
- accessibility behaviour is preserved where relevant;
- rollback remains possible until the declared point of no return.

A passing unit suite alone is not proof of behavioural equivalence.

## Phase 9: Cleanup gate

Delete old paths only when:

- traffic/use has migrated;
- backfill is complete;
- consistency checks pass;
- observability shows no unexpected consumers;
- compatibility window has closed;
- rollback policy permits deletion;
- tests protect the new path;
- documentation and ownership are updated;
- feature flags/adapters have explicit removal completed.

## Report format

```markdown
# Refactor Assessment — [target]

**Verdict:** DO NOT REFACTOR | REPAIR LOCALLY | REFACTOR INCREMENTALLY | MIGRATION JUSTIFIED | REWRITE JUSTIFIED | NEEDS MORE EVIDENCE
**Declared scope:** [...]

## Necessity
- **Claimed problem:** [...]
- **Baseline evidence:** [...]
- **Cost of doing nothing:** [...]
- **Incremental alternative:** [...]
- **Options analysis:** [...]

## Invariant ledger
| Invariant | Evidence/baseline | At-risk surfaces | Proof method |

## Blast radius
[Direct and transitive dependencies.]

## Migration strategy
[Chosen pattern and why.]

## Checkpoints
| Checkpoint | Invariant at risk | Proof | Observability | Rollback |

## Data/schema compatibility
[...]

## Cleanup gate
[...]

## Residual risk
[...]

## Confidence
Confirmed | High Confidence | Needs Verification
```

## Anti-patterns

- Architecture astronautics.
- Refactor-as-rewrite.
- Big-bang restructure without proof that coexistence is worse.
- Cleverness over clarity.
- No baseline, therefore no way to prove improvement.
- Characterization tests that accidentally canonise known defects.
- Dual writes without reconciliation.
- Permanent compatibility layers and feature flags with no cleanup gate.
- Declaring success because code moved while operational properties regressed.
