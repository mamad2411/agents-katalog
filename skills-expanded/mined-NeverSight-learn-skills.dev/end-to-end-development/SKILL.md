---
name: end-to-end-development
description: Run deterministic, resumable end-to-end development across one or more repositories through a durable LangGraph control plane, risk-proportional approval and challenge gates, reusable validation evidence, single-pass review and remediation limits, isolated worktrees, auto-detected headless workers, and validated artifact handoffs.
disable-model-invocation: true
compatibility: Requires uv, Python 3.11+, Git worktrees, Pi or Codex, a repository forge CLI, and the installed codebase-design skill. Paseo, Herdr, and tmux are detected automatically when the coordinator runs inside them; otherwise workers run headlessly. LangGraph dependencies are installed from the locked skill project.
---

# End-to-End Development

Use the bundled **LangGraph workflow as the sole orchestration engine**. The current Pi/Codex agent performs only request/repository discovery, dedicated-worktree creation, bootstrap-spec construction, presentation of a high-risk plan-review interrupt when requested by policy, and concise presentation of terminal status. Do not manually choose phases, construct assignments, supervise workers, manage retries, mutate `run.json`, or bypass graph routing.

Resolve `SKILL_DIR` to this directory. Before a new run or resume, read:

1. [ORCHESTRATION.md](ORCHESTRATION.md) completely;
2. [ARTIFACTS.md](ARTIFACTS.md) completely;
3. [SIMPLICITY-CHALLENGE.md](SIMPLICITY-CHALLENGE.md) only when explaining or diagnosing a challenged plan.

Workers read only their assigned `schemas/<kind>.md`, never the coordinator documents.

## Non-negotiable invariants

1. **One executable state machine.** LangGraph owns phase selection, conditional routing, retries, interrupts, fan-out/fan-in, writer leases, and completion. Never reimplement those decisions in the coordinator conversation.
2. **Evidence is hash-pinned.** A result, validation, finding, blocker, approval, delivery, or next action is known only after it exists in validated durable state or an immutable artifact.
3. **Reconcile before action.** Every graph path starts by reconciling run artifacts with output files and external state. Resume from artifacts, never conversation memory.
4. **Follow the selected policy.** Ordinary single- and multi-repository work may use the standard no-pause path. High-risk discovery escalates to full before project-file work.
5. **One active project-file writer per repository.** The lease protects a role, not an agent identity. Work packets and fix batches preserve it.
6. **Workers do not mutate coordinator state.** They write only their exact output, allowed project files, and log directory. The graph updates run, agent, event, lease, and checkpoint state.
7. **Every loop is bounded.** New runs get one review, one review-fix batch, one validation-fix cycle, and one pipeline-fix cycle. Worker replacement and planning revision limits are also enforced by the graph. Never “continue until green.”
8. **Preserve evidence, not transcripts.** Full output stays in logs. Artifacts contain commands, hashes, exit codes, concise conclusions, and evidence paths.
9. **No silent degradation.** Missing, invalid, oversized, stale-tree, or contradictory evidence leaves the gate incomplete.
10. **Migration safety is mandatory.** The graph must have isolated local/test database-target evidence before migration-capable validation. Never use production, staging, shared, or ambiguous databases; never copy `.env` into a new worktree.
11. **No undeclared high-cost mechanism.** Stop rather than invent a trigger, database function/procedure, backfill, background/event flow, cache, seam/adapter, storage system, or comparable mechanism absent from the approved plan.
12. **Independent review remains mandatory.** Every profile gets at least one fresh baseline-to-worktree review before delivery.
13. **High-risk plan approval is a hard gate.** Full-profile implementation cannot begin until a later user message explicitly approves every plan in the exact current hash-pinned review bundle. Fast/standard policy records an automatic hash-pinned decision without pausing; discovery of a high-risk surface invalidates it and escalates before implementation.
14. **External side effects are idempotently reconciled.** LangGraph checkpointing does not make workers, commits, pushes, or PR creation exactly-once. Valid existing evidence is recovered instead of repeated.
15. **Completed worker handles are short-lived.** The supervisor records an opaque backend handle, cleans it as soon as its worker settles and its output is captured, and records the result. Crash recovery uses the pinned backend to apply the same cleanup even when the output artifact already exists. Never report completion while a settled workflow worker remains open.

## Coordinator command interface

The orchestrator resolves the required `codebase-design` skill beside this skill and in common Pi/Codex global skill directories. If it is installed elsewhere, set `E2E_CODEBASE_DESIGN_DIR` to the directory containing its `SKILL.md` and `DEEPENING.md` files.

Always invoke the locked project through the wrapper, which keeps the generated virtual environment in the user cache rather than the installed skill directory:

```bash
ORCHESTRATOR="$SKILL_DIR/scripts/run-orchestrator"
```

Do not invoke `workflow_tools.py run-batch` directly during a graph-managed run. It is an internal graph primitive.

### New run

Treat skill arguments plus relevant user conversation as the complete request.

1. Discover every affected repository and every material risk before creating run state.
2. Ask the user only when repository identity or a material product choice cannot be established from the request and repository evidence. A later plan-review interrupt is mandatory only if policy selects full.
3. Create one dedicated worktree per repository, preferring Worktrunk:

   ```bash
   wt switch --create <branch> --format json --no-cd
   ```

   The dedicated worktree must be clean. Never copy `.env` or other database credentials into it.
4. Write a bootstrap specification using the exact shape in [ORCHESTRATION.md](ORCHESTRATION.md). Preserve material user wording in requirement source text and acceptance criteria.
5. Choose durable run state under:

   ```text
   ${HOME}/.local/state/pi/end-to-end-development/<UTC-timestamp>-<request-slug>/
   ```

   Never use `/tmp`.
6. Initialize, then execute:

   ```bash
   "$ORCHESTRATOR" init --spec "$BOOTSTRAP_SPEC" --run-dir "$RUN_DIR"
   "$ORCHESTRATOR" run "$RUN_DIR" --worker-runtime auto
   ```

The command runs until completion, a validated blocker, or a full-profile plan-review LangGraph interrupt.

### Resume

For an explicit run directory:

```bash
"$ORCHESTRATOR" resume <absolute-run-directory> --worker-runtime auto
```

If the user says only “continue,” search the durable root for incomplete runs whose repository roots contain the current directory. Resume only when exactly one matches; otherwise list candidates. If that full-profile run is awaiting plan review, **do not call `resume`**: re-present the current bundle and request explicit whole-bundle approval or changes.

Inspect without advancing:

```bash
"$ORCHESTRATOR" status "$RUN_DIR"
```

Never edit `run.json`, `agents.json`, `events.jsonl`, assignments, or LangGraph SQLite state to repair a run. Diagnose the rejected evidence or use a supported CLI transition. `resume` retries blockers classified as environment, authentication, permission, or infrastructure after the external condition is fixed; it never clears code, dependency, or decision blockers. If an older engine created a validation assignment without the canonical plan IDs and then emitted the exact validation-coverage blocker, update the engine and use the narrowly guarded recovery command:

```bash
"$ORCHESTRATOR" retry-validation-evidence "$RUN_DIR" --worker-runtime auto
```

This command rejects every other blocker and reruns validation with a new plan-hash-bound assignment; it does not weaken ordinary code-blocker handling.

If a dependent fix was started concurrently with an upstream contract fix and stopped on the exact hash-pinned bundle-drift blocker, update the engine and use:

```bash
"$ORCHESTRATOR" retry-dependent-fixes "$RUN_DIR" --worker-runtime auto
```

The guarded transition rejects other dependency blockers, serializes remaining fixes in shared-contract dependency order, grants read-only access to upstream worktrees, and pins accepted upstream fix artifacts into each dependent assignment.

## Full-profile plan-review interrupt

Fast and standard runs still emit a complete hash-pinned review bundle, but policy accepts it atomically without a user pause. When a full-profile graph returns `status: awaiting-user` and `phase: plan-review`:

1. Read `plan_review.path` and verify the reported SHA-256 still matches.
2. Present the bundle path, hash, and concise per-repository task/packet/risk/validation summaries.
3. Ask exactly: **“Approve all plans in this exact review bundle, or send the changes you want.”**
4. End the turn. Do not create implementation work, edit project files, or invoke a generic resume.

On a later message, approval is valid only when the user's wording explicitly approves the whole current bundle. Preserve that wording exactly:

```bash
"$ORCHESTRATOR" approve "$RUN_DIR" \
  --review-sha256 "$CURRENT_BUNDLE_SHA256" \
  --text "$EXACT_USER_APPROVAL" \
  --worker-runtime auto
```

The CLI independently rejects generic continuation and a stale hash.

For requested changes:

```bash
"$ORCHESTRATOR" request-changes "$RUN_DIR" \
  --review-sha256 "$CURRENT_BUNDLE_SHA256" \
  --text "$EXACT_USER_FEEDBACK" \
  [--repository <repo-id>] \
  --worker-runtime auto
```

Omit `--repository` when feedback affects the whole bundle. The graph creates a hash-pinned revision basis, returns the affected plans through the bounded planning path, reruns required challenges, emits a new complete bundle, and interrupts again. Any canonical contract, plan, or challenge hash change invalidates prior approval.

## Database-target safety gate

If the graph blocks because a plan contains a migration-capable validation, independently confirm that the target is disposable and isolated. Never print or record the database URL or credentials. Then record only safe classification evidence:

```bash
"$ORCHESTRATOR" database-target "$RUN_DIR" \
  --repository <repo-id> \
  --classification isolated-test \
  --description "Ephemeral database dedicated to this worktree"
```

Allowed classifications are `isolated-local` and `isolated-test`. The command rejects production, staging, shared, and ambiguous targets. Resume through the graph afterward. This evidence does not authorize an unplanned destructive migration, reset, fresh migration, seed, or drop operation.

## Deterministic policy

The initializer applies:

```bash
python3 "$SKILL_DIR/scripts/workflow_tools.py" policy \
  --repository-count <N> \
  [--risk authorization] [--risk database-migration] \
  [--profile auto|fast|standard|full] [--report]
```

`fast` is opt-in. `standard` is the automatic ordinary-work default, including coordinated multi-repository changes. Authorization, security, concurrency, migration, backfill, background processing, new storage, public-interface changes, or another high-cost mechanism force `full`. Planning can escalate before implementation when it discovers risk. Repository count and the `cross-repository` flag alone do not force full.

| Gate | Fast | Standard | Full |
|---|---|---|---|
| Shared contract | embedded in plan | multi-repository only | multi-repository only |
| Design challenge | none unless discovery escalates | risk-only | risk-only |
| Complete-plan user approval | policy-accepted | policy-accepted | explicit user approval |
| Implementation packet | ≤4 tasks | ≤3 tasks | ≤3 tasks |
| Independent full review | one | one | one |
| Targeted second review | never | never | never |
| Cross-repository integration | no | multi-repository only | multi-repository only |
| Deterministic HTML report | requested only | requested only | requested only |

New runs use these hard stage limits:

```json
{
  "worker_replacements_per_stage": 1,
  "contract_revisions": 1,
  "plan_revision_cycles": 1,
  "validation_fix_cycles": 1,
  "review_rounds": 1,
  "pipeline_fix_cycles": 1
}
```

A review may produce one compatible `fix-1` batch, but that fix never starts another review. A validation or required-check failure may produce one compatible fix batch and one check afterward; another failure blocks with preserved evidence. Never modify limits during an active run. Existing durable runs retain their pinned limits when resumed.

The graph checks `coordinator_attempt_budget` after each atomic batch. When reached, it checkpoints at `reconcile`; when `auto_resume` is true the CLI starts a fresh bounded graph invocation from that checkpoint, otherwise it returns `outcome: budget-checkpoint` for a supported later resume. Neither path can cross a pending plan-review interrupt.

## Executable phase behavior

The compiled graph contains these phase nodes, with `reconcile` between every transition:

1. `bootstrap`, auto-detecting and pinning the worker backend/runtime, then verifying Git worktrees, forge remotes, and forge CLI authentication
2. `contract` when policy requires it
3. `plan`, including conditional challenge and one bounded revision
4. `plan-review`, implemented with LangGraph `interrupt()` only for full; fast/standard records a policy decision and proceeds
5. `implement`, scheduling topologically eligible work packets
6. `validate`, with at most one validation-fix batch
7. `review-1`
8. `fix-1` when must-fix findings exist, with no follow-up review cycle
9. `integrate` when policy requires it
10. `deliver`, with at most one pipeline-fix batch for change-related failures
11. post-delivery content-evidence confirmation
12. `report` when required
13. `complete`, with final audit and deterministic metrics

The graph retains `review-2` and `fix-2` nodes only so older durable runs with a pinned two-round limit can resume safely. New runs never schedule them.

Repository IDs and stable IDs sort lexicographically. Independent repositories launch together through one supervisor batch. Contract dependency evidence is the only reason to serialize repositories.

### Worker routing

The graph constructs immutable assignments and invokes the supervisor internally. Users do not configure a terminal manager. Bootstrap selects the first positively detected active environment in this order: a reachable Paseo parent from `PASEO_AGENT_ID`, a compatible Herdr server from `HERDR_ENV`, the active tmux session from `TMUX`, then the always-available direct headless backend. `PASEO_HOST` alone never selects remote workers because remote paths may not match the coordinator's hash-pinned paths. The selected backend and evidence are pinned in `run.json` for recovery.

`--worker-runtime auto` inherits a Paseo parent's Pi/Codex provider when present, otherwise follows the coordinator: Codex when `CODEX_THREAD_ID` is present and Pi by default. `E2E_COORDINATOR_RUNTIME` remains an internal diagnostic override, not required user setup.

Every worker uses `gpt-5.6-luna` with assignment-proportional runtime reasoning:

- `xhigh` (runtime `max`): full planning, design challenge, review, and integration;
- `high`: standard planning/review, implementation, and complex fixes;
- `medium`: validation, mechanical fixes, and delivery.

Workers never spawn nested agents. A Paseo coordinator creates Paseo subagents, Herdr creates non-focused workspaces, tmux creates detached windows, and direct mode runs non-interactively without a terminal manager. The supervisor archives or closes each settled handle immediately after capturing its artifact result, including rejected artifacts; working, blocked, and timed-out workers are retained for diagnosis.

### Work packets and bounded deviations

The plan defines the packet, not individual task, as the implementation unit. A worker may record a bounded deviation only when it preserves accepted requirements and contract, adds no risk or mechanism, follows repository precedent, remains within the packet concern, and records evidence. A new behavior, contract/interface change, migration, dependency edge, or high-cost mechanism is material and blocks rather than silently replans.

### Validation and review

The graph computes a content fingerprint independent of commit identity. The final implementation/fix writer runs the complete planned suite, and the graph reuses that evidence only when validation ID, exact command hash, and content fingerprint match. A delivery-only commit therefore causes no duplicate validation; any source change invalidates the evidence. Compatible failures are fixed in one batch and checked once afterward.

One fresh worker independently reviews the complete baseline-to-worktree state. Critical/high actionable findings always block; medium correctness/spec findings normally block; low findings remain advisory. Compatible must-fix findings are resolved in one repository batch, affected checks run once, and the workflow proceeds without a second review. An incompatible or still-failing correction blocks instead of opening another remediation loop.

### Delivery and completion

Delivery workers may write Git and forge state but not project files. They preserve pre-existing changes, commit only task changes, push, create/update PRs, and monitor required checks. Authentication, permission, and infrastructure failures block rather than churn. Change-related failures get at most one pipeline-fix batch.

After delivery, the graph verifies that the committed content still matches passing evidence rather than invalidating it merely because `HEAD` changed. Completion then verifies the policy-selected plan decision, canonical hashes, current validation, required integration/report evidence, delivery artifacts, no unresolved must-fix finding, no unexplained writer lease, no open workflow worker handle, empty actions, and empty blockers. Metrics are generated deterministically.

## Final response

Use the orchestrator JSON output. Keep the final response concise:

- status;
- absolute run directory;
- PR URLs;
- report path/URL when present.

For WSL local HTML, convert the absolute report path to a `file://wsl.localhost/Ubuntu-Shared...` URL on its own line.
