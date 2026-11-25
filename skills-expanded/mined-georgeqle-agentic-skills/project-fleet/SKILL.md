---
name: project-fleet
description: Orchestrate a central control repository that plans, provisions, tracks, and advances many related downstream repositories or work items with guarded batches, blocker handling, and productive fallback work.
type: orchestration
version: v0.1
required_conventions: [alignment-page]
argument-hint: "[--status] [--plan] [--execute]"
---

# Project Fleet

Invoke as `$project-fleet`.

Use this skill when a project is no longer a single repo or task list, but a fleet: one control repository coordinates many downstream repositories, implementation targets, specs, clients, migrations, content items, experiments, or generated artifacts.

Examples: seeding many private repos from a spec store, migrating many packages, generating plans for many apps, rolling out the same change across customer repos, or advancing a queue while rate limits or external windows control provisioning.

## Core Model

A fleet has:

- **Control repo:** canonical state, conventions, queue, scripts, logs, and status.
- **Fleet items:** downstream repos or work units, each with an ID, target, source, state, and blocker field.
- **Provisioning lane:** creates or updates external targets under strict guards.
- **Work lane:** advances already-provisioned targets while provisioning is blocked or waiting.
- **Blocker ledger:** records stop conditions and retry rules.
- **Status dashboard:** summarizes next action without re-reading the whole project.

## State Machine

Use project-specific names when needed, but preserve these semantics:

```text
candidate
ready-to-provision
provisioning-blocked
provisioned
planning-needed
plan-ready
work-in-progress
verification-needed
done
blocked
```

Never collapse "provisioned" into "done." A created repo, generated scaffold, or reserved artifact is only an available target until planning, work, and verification finish.

For broad solution-space exploration, spec-clone stores, generated app fleets, or other candidate-heavy projects, prefer this portfolio funnel:

```text
candidate -> shortlisted -> spec-ready -> seeded -> active-build -> shipped | archived | blocked
```

Preserve these meanings:

- **candidate:** cheap broad idea or rough spec; not approved for repo creation or implementation.
- **shortlisted:** scored and intentionally kept for deeper work.
- **spec-ready:** implementation-ready source/spec exists with required evidence, constraints, and blockers.
- **seeded:** downstream repo, scaffold, or external target exists; still not implementation-complete.
- **active-build:** selected for runnable milestone work under the active fleet cap.
- **shipped:** verified output reached the project's done definition.
- **archived:** intentionally removed from active consideration.
- **blocked:** cannot advance until the recorded blocker clears.

Use `scaffold-only` as an explicit item tag, not a state, when a project intentionally creates downstream scaffolds before `spec-ready`. A `scaffold-only` item may be seeded for inventory purposes, but it cannot enter `active-build` until it becomes `spec-ready`.

## Portfolio Policy

When a fleet contains many candidate apps, specs, repos, experiments, content items, or implementation targets, optimize for return on effort instead of breadth alone:

- Track portfolio fields per item: ID, name, target, source/reference, state, score, score rationale, readiness state, downstream repo or artifact, active-build eligibility, last verified state, blocker, and next milestone.
- Score candidates before deep specification or provisioning. Use project-specific criteria when present; otherwise score implementation leverage, demo value, legal/provider risk, reusable components, data/API availability, user or market signal, and build cost.
- Default active-build cap is 5 when the project has no explicit cap. Do not add more `active-build` items until an active item ships, blocks, or is archived.
- Default downstream provisioning gate is `spec-ready`. Only seed earlier when the item is explicitly marked `scaffold-only` and project rules allow scaffold inventory.
- Prefer runnable milestone progress over more broad expansion once any `active-build` item exists.
- Do not let candidate count, scaffold count, or repo count stand in for shipped or runnable progress.

## Process

1. **Read conventions first.** Load `AGENTS.md`, `CLAUDE.md`, or equivalent control-repo instructions. Treat project-specific safety rules as higher priority than this generic skill.
2. **Find fleet state.** Look for `tasks/`, `docs/`, `scripts/`, manifest tables, status files, queue files, or project-local conventions. If no state exists, propose a minimal one before executing.
3. **Normalize the queue.** Ensure each item has: ID, name, target, source/reference, state, last action, blocker, and next action. For candidate-heavy fleets, also normalize score, score rationale, readiness state, downstream repo/artifact, active-build eligibility, last verified state, and next milestone.
4. **Run preflight guards.** Check auth, rate limits, dirty worktrees, target visibility/safety, required scripts, and project-specific stop conditions before external writes.
5. **Choose exactly one lane:**
   - **Provisioning lane** when guards pass and the next target is eligible.
   - **Work lane** when provisioning is blocked by time, rate limits, or an external dependency but existing targets can advance.
   - **Repair lane** when a blocker is actionable and safe to fix.
   - **Planning lane** when the queue lacks enough detail for execution.
   - **Portfolio lane** when candidate scoring, culling, active-cap enforcement, or `scaffold-only`/`spec-ready` classification is needed before safe provisioning or implementation.
6. **Execute in bounded batches.** Follow project batch size, serial/parallel limits, and external-service rules. If no policy exists, default to one item.
7. **Verify before state changes.** Do not mark an item advanced until evidence exists: target exists, expected files or outputs exist, tests/checks pass, visibility is correct, or the planned artifact is committed.
8. **Update central state.** Record completed work, blocker evidence, next eligible time, next target, and any skipped items.
9. **Ship changes.** If tracked files changed, follow the repository shipping convention: validate, commit, and push unless the project explicitly says not to.
10. **Report the next action.** End with the next concrete fleet item and the recommended command or lane.

## Control-Repo Files

Prefer existing files. If the project lacks a structure, create or recommend:

```text
tasks/fleet-status.md       # generated or hand-maintained dashboard
tasks/fleet-queue.md        # manifest of items and states
tasks/fleet-blockers.md     # blocker ledger if not embedded in queue
tasks/history.md            # shipped work log
scripts/fleet-status.*      # optional deterministic status generator
scripts/fleet-next.*        # optional next-item selector
scripts/fleet-provision.*   # optional guarded provisioning script
```

For domain-specific projects, use clearer names like `tasks/repo-seeding.md`, `tasks/migration-queue.md`, or `tasks/customer-rollout.md`. Generic file names are a fallback, not a requirement.

## Guarded Provisioning

Provisioning means any operation that creates, publishes, mutates, or schedules many external targets. Examples: `gh repo create`, remote pushes, deployments, package publishing, account/API provisioning, bulk imports, or paid-service operations.

Before provisioning:

- Confirm explicit user/project approval exists for the operation class.
- Confirm target visibility and privacy defaults.
- Confirm the target satisfies the project's readiness gate. For candidate-heavy fleets, the default gate is `spec-ready`; earlier provisioning requires an explicit `scaffold-only` tag.
- Check service limits and local rolling caps.
- Use project scripts when they exist.
- Keep operations serial unless the project explicitly permits parallelism.
- Stop on auth failures, rate limits, permission errors, target conflicts, visibility mismatches, partial propagation, template validation failures, or unexpected paid/irreversible actions.

On a rate limit, obey `retry-after` or reset headers when available. Otherwise record a conservative next eligible time and switch to work lane if safe.

## Productive Fallback Work

When provisioning is waiting or blocked, advance existing fleet items without violating the provisioning guard:

- Generate or refine per-item roadmaps.
- Expand implementation plans from source specs.
- Score and cull candidates, promote promising candidates to `shortlisted`, or archive low-return candidates.
- Run local validation or hygiene checks.
- Fix documented blockers that do not require the blocked external operation.
- Prepare templates, scripts, or status reports.
- Verify already-created targets.

Do not use fallback work to bypass a guard. If the blocked operation is required for an item, pick a different eligible item.

## Blocker Ledger

Each blocker entry should include:

```text
timestamp
item ID / target
lane
blocker type
evidence
attempted fix
retry rule or owner
next eligible action
```

Common blocker types:

```text
auth-permission
rate-limit
target-conflict
propagation-delay
visibility-safety
template-validation
dirty-worktree
missing-source
verification-failure
legal-or-policy-risk
manual-human-action
```

## Output

Report:

- Current fleet count by state.
- Portfolio summary when relevant: active-build count/cap, top scored candidates, `scaffold-only` count, `spec-ready` count, and archived/blocked count.
- Lane selected and why.
- Items advanced.
- Guards checked.
- Blockers created or cleared.
- Validation evidence.
- Files changed and shipped status.
- **Next work:** the next concrete item or blocker.
- **Recommended next command:** `$project-fleet --execute`, `$project-fleet --status`, another project-specific skill, or the exact project script.

## Constraints

- Do not invent permission to create, publish, deploy, spend money, or make public resources.
- Do not continue provisioning after a stop-condition failure.
- Do not parallelize externally fragile operations unless the project explicitly allows it.
- Do not mark planning/scaffold targets as implementation-complete.
- Do not move `candidate`, `shortlisted`, or `scaffold-only` items into `active-build` without `spec-ready` evidence.
- Do not exceed the active-build cap unless the project explicitly changes the cap.
- Do not let downstream repos become the source of truth for fleet-wide state unless the project explicitly chooses a distributed model.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/project-fleet-{topic}.html`.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next caller has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, production deploy confirmation, paid actions, or public visibility changes.
