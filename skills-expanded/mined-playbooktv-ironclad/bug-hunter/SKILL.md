---
name: bug-hunter
description: Reproduce, isolate, and diagnose a specific software failure before changing production behaviour, then propose the smallest safe fix with regression protection. Use whenever the user reports a bug, crash, error, stack trace, flaky test, incorrect output, "works on my machine," intermittent failure, regression after a deploy, or any behaviour that diverges from expectation and the cause is not obvious. Prefer this over jumping straight to a fix. Part of the audit suite; inherits the shared constitution, while its own job is proving causality.
---

# Bug Hunter

**Epistemology: prove the causal chain.**

A fix applied without a proven cause is a guess, and guesses that happen to work can hide the real defect. This skill is not done when the symptom disappears. It is done when the cause is established, the mechanism from cause to symptom is explained, the correction addresses that cause, and the original failure is verified against the repaired system.

Where safe and practical, causal proof should be bidirectional: the failure exists under the causal condition and disappears when the cause is corrected. Never reintroduce destructive behaviour into production merely to prove causality. Use controlled reproduction, fixtures, simulation, replay, or equivalent evidence.

This skill inherits the suite constitution (`references/CONSTITUTION.md`). Read it once for the shared disciplines. Everything below specialises that spine for debugging.

## Prime discipline: discovery and repair are separate

**Permanent behavioural edits are forbidden during discovery.**

Steps 0–9 happen without changing the production behaviour under investigation. During discovery, you may:

- inspect code, configuration, logs, traces, metrics, history, and runtime state;
- add temporary instrumentation;
- use breakpoints or profilers;
- write a failing characterization or reproduction test;
- create isolated fixtures, scripts, simulations, or test harnesses;
- perform emergency containment when continued operation creates material harm.

You may not make speculative product-code changes to see whether the symptom moves.

A failed diagnostic attempt must update the hypothesis tree, not trigger a random edit.

### Emergency containment exception

Containment is allowed before root cause is established when delay risks ongoing data loss, security exposure, financial harm, severe availability impact, or irreversible user harm.

Examples include:

- rolling back a suspect deployment;
- disabling a feature flag;
- pausing a destructive worker;
- blocking a dangerous endpoint;
- revoking a compromised credential;
- isolating a failing dependency.

Containment must be documented separately from diagnosis. Do not misrepresent containment as root-cause repair.

### Instrumentation warning

Instrumentation can change the system being observed. Logging, breakpoints, debug builds, tracing, profilers, and test harnesses may alter timing, scheduling, memory pressure, cache behaviour, and race frequency.

For timing-sensitive or intermittent failures:

- record the instrumentation used;
- compare minimally instrumented and instrumented runs where practical;
- record whether reproduction frequency changes;
- do not treat disappearance under instrumentation as proof of resolution.

# Protocol

Move through the phases in order. Looping back is expected. Skipping from symptom to repair is not.

## 0. Intake, impact, and containment

Capture the report without accepting the reporter's causal explanation as fact.

Record:

- observed symptom;
- expected behaviour and the source of that expectation;
- affected environment, version, commit, release, region, browser, device, or runtime;
- affected users, roles, tenants, plans, or data shapes;
- first known occurrence;
- frequency or reproduction rate;
- business and user impact;
- whether data loss, security exposure, financial harm, or destructive behaviour is ongoing;
- exact error text, timestamps, correlation IDs, screenshots, logs, traces, and metrics;
- recent deploys, migrations, configuration changes, dependency updates, feature-flag changes, and infrastructure events.

Decide whether emergency containment is required before deeper investigation.

Urgency and root-cause confidence are separate. A severe incident may have an unknown cause.

## 1. Reconnaissance

Build a lightweight map of the failure surface before narrowing onto one file.

Identify, where relevant:

- user action or external trigger;
- frontend event and state path;
- API, RPC, server action, resolver, or service boundary;
- authentication and authorization context;
- database and transaction boundary;
- cache and invalidation path;
- queues, workers, schedulers, retries, and dead-letter behaviour;
- webhooks and third-party dependencies;
- feature flags and environment-specific configuration;
- deployment topology and version skew;
- observability available;
- existing tests around the path.

Trace implementation rather than relying on README claims or remembered intent.

## 2. Reproduction contract

Establish the most reliable trigger available.

Record:

- preconditions;
- environment;
- exact data/setup;
- exact action or request sequence;
- expected result;
- actual result;
- frequency;
- timing sensitivity;
- cleanup/reset requirements.

If the failure is intermittent, report a reproduction rate rather than false determinism.

If reproduction fails after reasonable attempts, report `CANNOT REPRODUCE` with:

- environments and versions tested;
- data and scenarios attempted;
- evidence inspected;
- differences from the reported environment;
- missing information or access required;
- recommended instrumentation or monitoring.

Do not fix a bug you cannot see unless direct implementation evidence independently establishes the causal mechanism.

## 3. Expected versus actual

State the behavioural delta precisely.

Avoid:
> It is broken.

Prefer:
> When an authenticated editor submits the form twice within the pending transition, two create requests are accepted and two records are persisted. Expected behaviour is one logical operation producing at most one record.

The expected behaviour must come from a product requirement, contract, invariant, established test, protocol, or clearly stated user expectation. If expectation itself is ambiguous, say so.

## 4. Minimise the reproduction

Reduce the failure to the smallest input, state, environment, and sequence that still produces it.

Vary one meaningful dimension at a time where practical:

- input shape;
- data volume;
- role or tenant;
- cache state;
- session age;
- network condition;
- concurrency;
- request ordering;
- retry count;
- dependency behaviour;
- browser/device;
- clock/timezone boundary;
- feature flag;
- deployment version.

Every removed condition that does not stop the failure is evidence about where the cause is less likely to be.

Preserve a known failing case before experimentation.

## 5. Trace the actual execution path

Follow the reproduction through the real system:

`trigger → event → state transition → request → handler → dependency/persistence → side effect → acknowledgement → cache/state reconciliation → render/observable symptom`

At each boundary record:

- input;
- output;
- state mutation;
- ordering;
- error handling;
- retry behaviour;
- ownership/authority context;
- observability gap.

Find where actual behaviour first diverges from expected behaviour.

## 6. Generate competing hypotheses

Create multiple plausible causal hypotheses when uncertainty remains.

For each hypothesis record:

- proposed cause;
- predicted mechanism;
- supporting evidence;
- contradicting evidence;
- unknowns;
- prediction that differs from alternatives;
- discriminating test.

Do not invent weak alternatives merely to satisfy ceremony. If direct evidence already establishes one mechanism, state why competing explanations are already excluded.

Maintain hypothesis states:

- ACTIVE
- WEAKENED
- REJECTED
- SUPPORTED
- CONFIRMED

A single plausible explanation is not automatically a root cause.

## 7. Design discriminating tests

For each active hypothesis, design the smallest safe experiment whose outcome would distinguish it from alternatives.

Prefer tests that can falsify the favoured hypothesis.

Examples:

- hold cache state constant while changing database state;
- coordinate two requests at a specific barrier rather than relying on random timing;
- replay the same payload with and without a stale version token;
- substitute a controlled dependency response;
- compare fresh and aged sessions;
- run against the same data on two deployment versions.

Do not change several causal dimensions at once unless reproducing a known production sequence.

## 8. Eliminate hypotheses and verify adversarially

Run discriminating tests and update the hypothesis tree after each result.

For serious or surprising conclusions, use a fresh verifier or fresh reasoning pass where possible. Give the verifier:

- the claimed cause;
- the minimal reproduction;
- the expected mechanism;
- the evidence needed to reproduce or disprove it.

The verifier's job is to break the explanation, not agree with it.

Possible outcomes:

- REPRODUCED
- PARTIALLY REPRODUCED
- NOT REPRODUCED
- DISPROVED
- BLOCKED BY ACCESS
- NEEDS SPECIALIST REVIEW

## 9. Establish root cause

A root cause is established only when it explains:

1. why the observed symptom occurs;
2. the mechanism connecting cause to symptom;
3. why the reproduction conditions trigger it;
4. why relevant non-triggering conditions do not;
5. how the proposed correction interrupts the causal chain.

Separate:

- **Trigger:** the condition that activates the failure.
- **Root cause:** the underlying defect that makes failure possible.
- **Contributing factors:** conditions that increase probability, reach, or impact.
- **Symptom:** the observable failure.

Example:

- Trigger: user double-clicks before pending state renders.
- Root cause: server mutation has no idempotency boundary.
- Contributing factor: client disables the control only after asynchronous state reconciliation.
- Symptom: duplicate order creation.

If the explanation is still "probably X," return to hypothesis testing or report `PARTIAL`.

*Discovery ends here. Permanent repair may now begin.*

## 10. Design the smallest safe correction

Propose the smallest change that addresses the established cause rather than suppressing the symptom.

Document:

- behavioural invariant being restored;
- exact correction;
- affected files and surfaces;
- blast radius;
- compatibility and migration risk;
- rollback path;
- observability needed after release;
- residual uncertainty.

If the correct fix requires broad structural change, stop scope expansion and hand off to Refactor Guardian.

Do not bundle unrelated cleanup.

## 11. Add regression protection

The preferred standard is a test that:

1. fails against the unpatched behaviour;
2. passes against the corrected behaviour;
3. protects the relevant invariant rather than implementation detail.

Verify both directions where safe and practical.

If a deterministic regression test is impractical, add the strongest available protection, such as:

- invariant test;
- controlled simulation;
- replay fixture;
- contract test;
- property-based test;
- concurrency harness;
- chaos/fault-injection scenario;
- observability assertion;
- targeted alert or monitor.

Document why direct deterministic regression coverage was not feasible.

## 12. Implement and verify

When authorised to change code:

1. preserve the original failing reproduction;
2. implement the smallest correction;
3. run targeted tests;
4. run the original reproduction unchanged;
5. test adjacent failure modes;
6. run relevant broader regression checks;
7. inspect logs, traces, metrics, and side effects for hidden failure;
8. verify rollback remains possible until confidence is sufficient.

For intermittent bugs, record:

- pre-fix run count;
- pre-fix failure count and rate;
- post-fix run count;
- post-fix failure count and rate;
- test conditions;
- instrumentation differences;
- remaining statistical uncertainty.

Do not declare an intermittent defect fixed because it passed a few times.

## 13. Monitor and close

After deployment or release, define:

- metrics or logs to watch;
- expected signal after correction;
- alert threshold;
- observation window;
- rollback trigger;
- owner for follow-up.

Closure statuses:

- `ROOT CAUSE ESTABLISHED`
- `FIXED AND VERIFIED`
- `MITIGATED`
- `CANNOT REPRODUCE`
- `PARTIAL`
- `NEEDS INVESTIGATION`
- `ACCEPTED RISK`

# Report format

```markdown
# Bug Report — [short title]

**Status:** FIXED AND VERIFIED | ROOT CAUSE ESTABLISHED | CANNOT REPRODUCE | PARTIAL | NEEDS INVESTIGATION
**Impact:** [user/business/operational consequence]
**Environment:** [relevant version, runtime, role, tenant, device, etc.]
**Reproduction:** [exact trigger; rate if intermittent]
**Expected vs actual:** [precise behavioural delta]

## System path
[trigger → relevant boundaries → symptom]

## Causal analysis
- **Trigger:** [...]
- **Root cause:** [...]
- **Contributing factors:** [...]
- **Symptom:** [...]

### Mechanism
[cause → intermediate mechanism(s) → symptom]

## Hypotheses considered and eliminated
| Hypothesis | Prediction | Discriminating test | Result | Status |
|---|---|---|---|---|

## Fix
- **Invariant restored:** [...]
- **Change:** [...]
- **Blast radius:** [...]
- **Compatibility/migration risk:** [...]
- **Rollback:** [...]

## Regression protection
[Test or strongest available protection. State whether failing-before/passing-after was verified.]

## Verification
[Original reproduction re-run, adjacent cases, intermittent run counts/rates where applicable.]

## Monitoring and residual risk
[Post-release signals, observation window, unresolved uncertainty.]

## Confidence
Confirmed | High Confidence | Needs Verification
```

# Anti-patterns this skill exists to prevent

## Shotgun debugging

Changing several things at once so the causal contribution of each change is unknowable.

## Symptom suppression

Catching the exception, clamping the value, retrying indefinitely, hiding the error, or disabling the visible trigger while the underlying defect remains.

If the proposed fix does not interrupt the mechanism named in the root-cause section, explain why it is still causal rather than suppressive.

## Single-hypothesis tunnelling

Committing to the first plausible explanation and collecting only supporting evidence.

## Fixing what cannot be reproduced or proven

A plausible patch is not a diagnosis. Use `CANNOT REPRODUCE`, `PARTIAL`, or `NEEDS INVESTIGATION` when that is the evidence.

## Confusing containment with repair

Rollback or feature disablement can be the correct emergency action without being the root-cause fix.

## Observer-effect blindness

Instrumentation can alter timing-sensitive failures. Record and test for this.

## Regression theatre

Adding a test that passes before and after the fix, mocks away the failing boundary, or asserts implementation details without protecting the failed invariant.

# Reference material

Read as needed:

- `references/CONSTITUTION.md` — shared suite disciplines.
- `references/REPRODUCTION.md` — reproduction contracts and minimisation.
- `references/HYPOTHESIS-TESTING.md` — hypothesis trees and discriminating experiments.
- `references/INTERMITTENT-BUGS.md` — timing-sensitive and probabilistic failures.
- `references/INCIDENT-CONTAINMENT.md` — separating emergency mitigation from diagnosis.
