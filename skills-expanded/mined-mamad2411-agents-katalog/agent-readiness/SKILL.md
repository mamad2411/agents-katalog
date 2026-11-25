---
name: agent-readiness
description: "Audit and improve repository and runner infrastructure for dependable autonomous implementation, QA, and unattended task execution. Covers reproducible bootstrap, noninteractive machine identities, real-surface verification, artifacts, CI, observability, isolation, recovery, and result submission. Use when a repository cannot boot or verify reliably, agents still need manual setup, credentials or worktrees block automation, or a devbox or orchestrator must complete tasks without supervision. Do not use for reviewing an existing diff or documentation-only cleanup."
disable-model-invocation: true
---

# Agent-Readiness

Make a repository and its declared runner dependable for autonomous work. Build
toward the requested target; default to B and treat C only as a checkpoint.

## Boundaries

- In scope: readiness infrastructure and repeatable application QA.
- Out of scope: source-diff review, unrelated documentation cleanup, ship
  decisions, and unauthorized external actions.
- Do not invent an orchestrator. Grade platform tools, network access, and
  machine authentication as runner capabilities.
- Require task-relevant guidance and empirical proof; mock-only tests,
  documentation claims, and builder self-evaluation do not prove readiness.

## Readiness Model

Use [references/grading.md](references/grading.md) to grade the applicable
capabilities: **Legibility, Executability, Feedback, Safety, Durability, and Scale**.

Report three different things rather than hiding them in one letter:

- **repository grade**: what the checkout makes possible
- **runner grade**: what the declared devbox, CI worker, or automation host provides
- **evidence level**: how strongly the claim has been exercised

The lowest applicable capability sets each grade; never average away a blocker.

## Automation Path

For unattended work, inspect the entire path:

**Triage → Dispatch → Provision → Execute → Prove → Submit → Reconcile → Complete**

**Any nonterminal stage → Recover → Retry, Escalate, or Fail**

Record each stage's input, output, owner, and terminal condition. For no-diff
tasks, also name the result type, evidence, target, and allowed side effects.

## Workflow

### 1. Audit the declared execution boundary

Establish the target grade, intended task classes, and runner before grading.
Then:

1. Read the repository-owned entrypoint and follow its links to relevant contracts.
2. Run the cold-start, boot, smoke, interaction, verification, and teardown paths
   that exist; static file presence alone is weak evidence.
3. Fill the [Required Output](references/grading.md#required-output) profile; for
   every applicable capability record its grade, evidence, gap, and owner.
4. Walk the automation path and record missing transitions, inputs, outputs, and terminal states.
5. Assign an evidence level using [references/autonomy-evidence.md](references/autonomy-evidence.md).

Use [references/setup-patterns.md](references/setup-patterns.md) for machine
identity ownership and managed-worktree inputs. Interactive human login,
profile switching, copied secrets, and printed tokens are runner gaps.

For React and existing Effect repositories, apply the mechanical enforcement
and runtime guidance in [references/react-enforcement.md](references/react-enforcement.md)
and [references/effect-readiness.md](references/effect-readiness.md). For Effect
implementation task classes, require repository-local Effect guidance; a
machine-global skill is not readiness evidence. Do not introduce Effect solely
for readiness.

### 2. Build the missing contract

Prioritize work in this order:

**Legibility → Runner contract → Cold start → Real-surface feedback → Enforcement → Isolation → Recovery and result submission → Repeated trials**

Prefer three stable repository entrypoints when the capability is in scope.
Their minimum lifecycle is executable and always tears down:

```bash
set -euo pipefail
trap './scripts/agent-teardown.sh' EXIT
./scripts/agent-bootstrap.sh
./scripts/agent-verify.sh
```

Bootstrap validates prerequisites and becomes ready; verification is canonical
and reused by CI; teardown handles success, failure, timeout, and cancellation.
Automation artifacts are keyed by task and attempt.

Keep the execution boundary explicit:

| Enforce mechanically | Leave to agent judgment |
| --- | --- |
| workspace and branch setup, allowed targets, tool install, secret injection | task interpretation and implementation |
| boot, test, teardown, artifact manifests, upload and push mechanics | exploratory QA, diagnosis, evidence selection, and recovery strategy |

When readiness work includes agent entrypoints, keep `AGENTS.md` as the canonical
authored guide and place `CLAUDE.md` beside it as a symlink to `AGENTS.md`.

That reference also owns boot, verification, observability, isolation,
unattended runs, proof artifacts, and result contracts.

### 3. Prove outcomes, not recipes

- Run the stable lifecycle once on the happy path and once with a safe failure,
  such as a missing required runner input; preserve both statuses and artifacts.
- Record each trial in a machine-readable form such as:

```json
{"task_class":"qa","scenario":"missing-runner-identity","result":"expected_failure","human_interventions":0,"duration_seconds":12,"retries":0,"failure_class":"runner/missing_identity","artifacts":"artifacts/task-123/attempt-1/"}
```

- Grade final environment or repository state, not the agent's completion claim.
- Accept equivalent implementations that satisfy the contract; do not require a
  particular tool, hook, port algorithm, or retry count without an external reason.
- For B or A claims, repeat representative trials and aggregate their records
  into success, intervention, duration, retry, resource, and failure metrics.
- Test parallel isolation and crash or stall recovery when claiming unattended
  or orchestrated readiness.
- Inspect transcripts and artifacts for false success, grader defects, secret
  exposure, and ambiguous task requirements.

### 4. Finish at the requested outcome

Finish at the requested target or an evidenced blocker. Report the path to A
and relevant documentation drift without expanding into unrelated cleanup.

## Output

Keep the handoff compact:

```text
- grades: repository and runner, before → after
- evidence: level plus the strongest exercised outcomes
- automation path: first missing or newly proven transition
- files changed: readiness infrastructure only
- remaining gaps: highest-impact gaps with owner, or none
- next: next capability or none
```

Name exact commands only for failures, reproduction, or when asked. Do not
repeat capability evidence in the footer when it already appears in an audit table.

## References

- [references/grading.md](references/grading.md) — repository and runner grades, capability matrix, ceilings, and blockers
- [references/autonomy-evidence.md](references/autonomy-evidence.md) — evidence levels, representative trials, outcome graders, and reliability metrics
- [references/setup-patterns.md](references/setup-patterns.md) — bootstrap, gates, credentials, observability, isolation, artifacts, recovery, and result patterns
- [references/react-enforcement.md](references/react-enforcement.md) — React-specific lint, local-gate, and CI adoption
- [references/effect-readiness.md](references/effect-readiness.md) — Effect-specific source, runtime, test, observability, and cleanup proof
- [references/industry-examples.md](references/industry-examples.md) — current harness, eval, and orchestration patterns
