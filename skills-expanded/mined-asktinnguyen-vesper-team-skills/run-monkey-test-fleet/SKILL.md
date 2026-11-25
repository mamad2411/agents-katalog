---
name: run-monkey-test-fleet
description: Orchestrate a fleet of implementation, specification-review, engineering-review, integration, and final-audit agents to turn monkey-test dossiers, adversarial QA reports, audit findings, bug backlogs, or release blockers into integrated, evidence-backed fixes. Use when Codex must coordinate many findings across a repository, parallelize non-overlapping work safely, preserve concurrent user changes and live systems, independently verify every issue, resolve cross-track regressions, and report exact completed, partial, blocked, residual, and operationally unmeasured results.
---

# Run Monkey-Test Fleet

Convert a findings dossier into a controlled remediation program. Remain the root orchestrator: own scope, state, integration, verification, safety, and reporting; delegate bounded implementation and independent review work.

## Load the operating references

Read these files before spawning agents:

- [references/orchestration-contract.md](references/orchestration-contract.md) for roles, prompt contracts, fleet sizing, and review independence.
- [references/ledger-schema.md](references/ledger-schema.md) for the issue/run state machines and evidence requirements.
- [references/acceptance-gates.md](references/acceptance-gates.md) for per-lane, integration, release, runtime, and reporting gates.
- [references/failure-playbook.md](references/failure-playbook.md) when the worktree is dirty, models fail, agents under-deliver, branches collide, specifications appear late, live processes exist, or `main` moves during the run.

Initialize and validate the run ledger with `scripts/fleet_ledger.py`. Keep it in the target repository under `.codex/fleet-runs/<run-id>/` unless repository instructions require another location.

## Non-negotiable invariants

1. Treat tests as evidence, not proof of issue closure.
2. Never let an implementation owner approve its own work.
3. Require both specification and engineering review for every implementation lane.
4. Integrate semantically; never choose a branch wholesale when that would discard valid concurrent work.
5. Preserve user changes, untracked files, dirty worktrees, committed concurrent work, and live data.
6. Do not restart, deploy, migrate, publish, or mutate a live system unless the user authorized that action and a read-only safety check proves the target.
7. Report model/tool substitutions exactly. Never imply an unavailable named model or reviewer ran.
8. Keep one authoritative ledger. Do not infer status from chat history alone.
9. Mark an issue `cleared` only when its acceptance criteria, tests, independent reviews, integration evidence, and documentation are complete.
10. Keep roadmap items, production measurements, deployment, and residual risks explicit. Do not convert them into success by wording.

## Phase 0: Establish authority and repository truth

Before delegation:

1. Read the complete findings dossier, every applicable `AGENTS.md`, repository specification, approved brief, release checklist, and linked document needed to interpret acceptance.
2. Follow repository discovery instructions. Prefer code-graph tools when required; fall back to text search only for unsupported or non-code discovery.
3. Inspect branch, worktree status, untracked files, running processes, active jobs, configured runtimes, package manager, and test commands using read-only operations.
4. Identify what the user authorized: diagnosis, code changes, live verification, deployment, or monitoring. Do not broaden authority.
5. Record the exact starting revision, baseline commands, relevant live processes, dirty paths, protected paths, and known concurrent owners.
6. Run the smallest credible baseline quality matrix. If it fails, classify failures as pre-existing, environmental, or dossier-related; do not silently inherit them.

Initialize the ledger:

```bash
python3 <skill-dir>/scripts/fleet_ledger.py init \
  --run-dir .codex/fleet-runs/<run-id> \
  --repo-root "$PWD" \
  --dossier <path-to-dossier> \
  --base-revision <exact-revision>
```

Populate every finding before spawning implementation agents. Split compound findings when their acceptance or ownership differs. Add discovered requirements rather than hiding them under an existing ID.

## Phase 1: Normalize findings into contracts

For every issue, record:

- Stable ID and concise title.
- Exact source location and verbatim intent as a short paraphrase.
- Severity and release impact.
- Observable reproduction or proof gap.
- Acceptance criteria that can return `pass`, `fail`, or `unmeasured`.
- Likely code ownership and shared integration surfaces.
- Required unit, integration, security, accessibility, browser, concurrency, crash-recovery, packaging, and live proofs.
- Dependencies, conflicts, and explicit non-goals.
- Whether the issue is code-closable, operational, roadmap, or production-measurement work.

Reject vague criteria such as “works,” “secure,” or “tested.” Require observable outcomes and forbidden outcomes.

## Phase 2: Design the fleet

Partition by ownership and integration surface, not by equal issue counts. A lane may own several related issues when that reduces collisions. Keep these roles separate:

- **Implementation owners:** reproduce, test, implement, document, and commit bounded issue groups.
- **Specification reviewers:** verify the exact dossier/spec acceptance contract and identify missing product behavior.
- **Engineering reviewers:** inspect correctness, security, privacy, durability, concurrency, maintainability, type safety, and regression risk.
- **Integration owners:** reconcile known overlapping branches in an isolated integration worktree without dropping either contract.
- **Final whole-branch auditors:** review the exact integrated revision, including cross-lane behavior no isolated branch could expose.
- **Runtime verifier:** perform authorized browser/API/MCP/process probes only after code clearance and safe deployment.

Use isolated worktrees and branches for concurrent code owners when Git is available. Give every agent explicit ownership, exact paths/revisions, commands, acceptance IDs, and the instruction that other agents share the repository and their edits must not be reverted.

Use the collaboration tools to spawn agents because invoking this skill explicitly authorizes the fleet topology. Do not exhaust every slot immediately. Reserve capacity for rework, semantic merges, and independent final reviewers. Prefer one agent per cohesive ownership lane; add advisers only for genuinely independent surfaces.

Do not force requested model names without verifying support. If a requested model is unavailable, report the failure once, select the strongest callable suitable model, and keep reviewer independence through separate agents and prompts.

## Phase 3: Dispatch implementation waves

Before each spawn:

1. Create or identify the agent’s isolated worktree and branch.
2. Record its issue IDs, owned files/modules, base revision, and required gates.
3. Include exact dossier/spec paths rather than a summary alone.
4. Require the agent to inspect repository instructions and baseline its lane.
5. Require regression tests that fail before the fix when practical.
6. Require a commit, changed-file list, commands/results, residuals, and integration notes.
7. Forbid live-data mutation and unrelated cleanup.

Dispatch independent lanes concurrently. Keep cross-cutting shared surfaces—central routers, CLI entry points, canonical models, schemas, migration code, global styles, and release configuration—under explicit integration control.

While agents run:

- Send the user concise progress updates at meaningful milestones and at least once per minute during long work.
- Poll agent state without busy-waiting.
- Inspect actual branches/diffs, not only agent prose.
- Correct wrong worktrees, wrong interpreters, unsupported models, scope drift, or memo-only “implementations” immediately.
- Record new findings and cross-lane dependencies in the ledger.

## Phase 4: Review every lane twice

Start reviews only from an exact commit. Give reviewers the raw dossier/spec, branch/revision, diff, and test surface; do not leak the intended verdict or prior reviewer conclusions.

Run two independent axes:

1. **Specification review:** determine whether every assigned issue is fully, partially, or not satisfied; reproduce important claims; identify missing UX/API/state-machine behavior and undocumented scope.
2. **Engineering review:** search for correctness, security, privacy, atomicity, race, crash-consistency, stale-worker, path, lease, type, migration, accessibility, and maintainability failures.

A reviewer must return structured findings with severity, issue ID, file/function, reproduction or reasoning, required correction, and verdict. “Looks good” without inspected evidence is not clearance.

On any hard finding:

1. Move the lane to `rework`.
2. Return concrete reproduction and acceptance criteria to the implementation owner.
3. Re-review the delta with both axes when the change can affect both.
4. Never self-certify a fix because the suite is green.

## Phase 5: Integrate in dependency order

Create one isolated integration branch from the protected base. Integrate cleared lanes in dependency order:

1. Canonical data contracts and migrations.
2. Durability, transaction, policy, and security primitives.
3. Domain services and workers.
4. Search/projection and derived indexes.
5. HTTP/MCP/CLI surfaces.
6. UI/accessibility.
7. QA tooling, packaging, and documentation.

After each meaningful wave:

- Resolve conflicts semantically, preserving both reviewed contracts.
- Run focused combined tests for the merged surfaces.
- Run the growing full suite when practical.
- Check that concurrent `main` or protected-branch work has not advanced.
- Update the ledger with the integration commit and evidence.

If `main` advances, merge only committed work into the integration branch and re-run gates. Preserve unrelated uncommitted work untouched. Never fast-forward a dirty root checkout merely to make the integration branch current.

## Phase 6: Attack cross-track boundaries

After all lanes integrate, deliberately test interactions isolated reviewers could not see:

- New UI against hardened backend validation.
- Search freshness after every newly introduced canonical mutation.
- Audit/event atomicity around all state transitions.
- Lease ownership immediately before canonical writes and terminal transitions.
- Crash recovery at every publish/outbox/journal seam.
- Old schema/legacy data against new readers and writers.
- Sanitized/public views against private internal state.
- Idempotent retry after ambiguous network or process failure.
- Symlink, path replacement, hardlink, descriptor, and DNS-rebinding edges where relevant.
- Small-viewport, keyboard, focus, reduced-motion, and screen-reader contracts.
- Packaging/entry points versus commands used by release evidence.

Spawn focused hardening lanes for real findings. Treat them as release blockers and repeat dual review and integration; do not bury them as “follow-ups.”

## Phase 7: Run the exact final gate

Freeze an exact integration revision. Run the repository’s complete applicable matrix from [references/acceptance-gates.md](references/acceptance-gates.md). Record command, revision, environment, exit code, result counts, and artifact paths.

Then spawn at least two fresh whole-branch reviewers against that exact revision:

- One reviews the complete dossier and approved specifications issue by issue.
- One reviews engineering, security, privacy, durability, and maintainability across the merged architecture.

Add a runtime/browser reviewer when the user authorized deployment or live verification. Any code change after final review invalidates clearance: freeze a new revision, rerun affected gates, and re-review the delta or whole branch according to risk.

Validate the ledger before reporting completion:

```bash
python3 <skill-dir>/scripts/fleet_ledger.py validate \
  --ledger .codex/fleet-runs/<run-id>/ledger.json \
  --strict
```

## Phase 8: Deploy or hand off safely

Deployment is a separate state from code clearance.

- If the protected/root checkout is clean and deployment is authorized, move the reviewed revision into place non-destructively, run smoke checks, and record the deployed revision.
- If it is dirty or owned by another process/person, leave the integration branch intact and report the safe handoff path and exact revision.
- Before restarting a process, prove the old process and target, check active jobs, preserve unrelated services, and verify restart safety.
- Never claim live closure from fixture-only evidence.

## Phase 9: Report with calibrated truth

Lead with the exact outcome and revision. Report:

- Issues cleared, partial, blocked, residual, roadmap, and operationally unmeasured.
- Integrated branch/worktree and whether the root/protected branch was updated.
- Exact quality matrix and counts.
- Major implementation results grouped by capability.
- Important adversarial findings discovered and fixed during review.
- Live-system actions taken or deliberately not taken.
- Concurrent work preserved.
- Actual agent/model usage and substitutions.
- Remaining deployment, production-scale, performance, or model-level risks.

Distinguish these terms rigorously:

- **Implemented:** code exists.
- **Fixture-verified:** automated evidence passes.
- **Independently cleared:** both review axes pass.
- **Integrated:** present in the combined branch.
- **Certified:** exact integrated revision passed the final matrix and whole-branch reviews.
- **Deployed:** that exact certified revision is running.
- **Production-validated:** representative live measurements meet declared thresholds.

Never collapse them into “done.”

## Completion condition

Stop only when every ledger issue is in a terminal truth state, the integration branch is clean, all required gates for the claimed state pass, final reviewers evaluated the exact revision, deployment status is explicit, and the final report can be regenerated from recorded evidence.
