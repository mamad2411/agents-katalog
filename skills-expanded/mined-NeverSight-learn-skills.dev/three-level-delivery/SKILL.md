---
name: three-level-delivery
description: Use when the user explicitly invokes Three-Level Delivery for a long-running or multi-agent project. Do not use for small projects, ordinary questions, or implicit requests.
license: CC-BY-4.0
metadata:
  author: "NGUYỄN DUY TÂM (NDT)"
  github: "nguyenduytamgithub"
  version: "0.1.4"
  repository: "https://github.com/nguyenduytamgithub/three-level-delivery"
---

# Three-Level Delivery

## Core rule

Activate only when the Owner explicitly invokes `$three-level-delivery` inside the correct Codex project or task for a large or multi-agent project. Deliver exactly one owner-approved slice through three levels: Owner, one user-visible left-sidebar Lead task, and one Writer plus one independent read-only Reviewer internal to that Lead. Keep the Lead read-only. Keep exactly one checkout writable: the saved local checkout only for an approved S000 with no valid HEAD, or one worktree when HEAD is valid. Stop after reporting the slice. Never infer or open the next slice.

## Canonical freshness gate

Upon explicit activation, run this gate once per new PO task/activation and before any target-repository write, Git initialization, visible-task creation, or internal delivery role. Do not run it for unrelated questions.

Fetch and read only `https://raw.githubusercontent.com/nguyenduytamgithub/three-level-delivery/main/three-level-delivery/SKILL.md`. Treat this as a read-only network check: send no credentials; add no tracking, telemetry, daemon, background process, hook, or write. Parse its YAML frontmatter and require all of the following:

- `name` is exactly `three-level-delivery`;
- `metadata.author` is exactly `NGUYỄN DUY TÂM (NDT)`;
- `metadata.repository` is exactly `https://github.com/nguyenduytamgithub/three-level-delivery`; and
- both installed `metadata.version` and canonical `metadata.version` are valid strict numeric three-component dotted versions.

A valid version has exactly three ASCII-decimal components separated by dots. Each component contains only `0` through `9`, has no leading zero unless it is exactly `0`, and has no whitespace, `v` prefix, prerelease, build metadata, sign, or other suffix. Parse components as integers and compare the three-integer tuples; never compare version strings lexicographically.

- **Exact version:** Continue to the startup gate.
- **Canonical version is newer:** Report `UPDATE_REQUIRED`, show a concise prompt that asks the user to authorize backup and replacement of only the installed `three-level-delivery` skill folder outside all project repositories, reinstall the canonical tree with `$skill-installer`, verify the new installed version, and restart Codex. Make zero target-repository mutations and create no visible task or internal role.
- **Canonical version is older; either version is malformed; identity is wrong; fetch is unavailable; or parsing/comparison is unknown:** Report `VERSION_CHECK_UNAVAILABLE` and `FAIL` closed. Make zero target-repository mutations and create no visible task or internal role.

Never guess, bypass, silently update, install, or replace anything. Installs older than v0.1.4 cannot be retroactively forced to perform this gate; their users must explicitly update them.

## Startup gate

After the canonical freshness gate passes, before asking about delivery, use read-only checks to verify all three conditions:

1. [CodeGraph](https://github.com/colbymchenry/codegraph) is available; for an existing Git repository, it also works for that repository.
2. [Superpowers](https://github.com/obra/superpowers) is installed and enabled.
3. The current Codex project/task and folder or repository binding match the project the Owner intends to deliver.

If a dependency is absent or unusable, or the project binding is missing or wrong, make no target-repository edits, create no delivery roles, and report `FAIL`. Include both dependency links when either dependency fails. Do not install, rebind, repair, disable, delete, or replace anything automatically. Never disable or delete the global CodeGraph or Superpowers installation.

After the gate passes, ask the Owner in ordinary language to describe:

- the project idea; and
- the first visible result they want to see.

Ask the Owner to confirm the intended folder, then classify its foundation read-only:

- **Established project foundation:** Use CodeGraph first. A repository is established only when durable vision and state equivalents can be mapped safely. Read only the existing README, instruction, vision, state, and decision documents that are present. Reuse their equivalents; never duplicate or overwrite them. Preview any instruction change only as the owned marker merge below.
- **Unestablished project:** This includes an empty folder, a new non-Git project, an empty or newly initialized Git repository, or a repository without durable vision and state equivalents. Propose exactly `S000 — Create the project foundation` before any product slice. The S000 allowlist may contain only Git initialization if needed and the minimal missing `README.md`, `AGENTS.md` owned block/rules, `docs/PROJECT_VISION.md`, `docs/PROJECT_STATE.md`, and a stack-appropriate `.gitignore`. Create no app, demo, product, package, or framework code and no Superpowers-owned specification, plan, test, or review document. If the foundation status, target, or safe mapping is ambiguous, stop and ask the Owner. If Git is unavailable or declined, report `FAIL`. Initialize CodeGraph only after Git exists.

Keep foundation classification separate from the HEAD/topology gate. Immediately before visible Lead creation, run `git rev-parse --verify HEAD` read-only:

- **Success:** HEAD is a valid established commit. Create the visible Lead through the platform's user-visible task creation path with exactly one worktree. This applies to every approved slice, including a foundation-correction slice.
- **Failure for approved S000 in an unestablished target:** If the approved slice is S000 and the target is an unborn/new Git repository or a new non-Git project, create the visible Lead through the platform's user-visible LOCAL/no-worktree path bound to the saved project/local checkout. Explicitly do not request or create a worktree.
- **Any other failure or ambiguity:** Report `FAIL` and create no delivery role.

Use read-only discovery only as needed to turn the Owner’s answer into exactly one proposed slice. Show its plain-language name, one observable goal, exact writable allowlist, fresh checks, stop gate, durable-memory mapping, and any repository-recovery merge preview. The approval request must explicitly ask the Owner to approve both the slice and creation of its separate visible Lead task, for example: `Duyệt S000 và tạo Lead task riêng.` A generic `Duyệt S000`, `ok`, or `làm đi` is insufficient. Ask once for an exact, unambiguous confirmation authorizing both. Before that confirmation, do not initialize Git, code, write repository-recovery or project-memory documents, or create any visible task or internal delivery role.

## Slice contract

Require the Owner to lock these fields before work starts:

| Field | Required value |
|---|---|
| Slice | Stable code and plain-language name |
| Goal | One observable outcome |
| Size | Small enough for one Writer and one independent review cycle; otherwise the Owner must split it |
| Allowlist | Exact writable files or paths |
| Checks | Fresh commands or observations that prove the slice |
| Project memory | Existing vision/state equivalents, or the minimal approved files that will hold them |
| Stop | Owner acceptance; no automatic next slice |

If a field is missing, contradictory, or would require a new path, report `UNKNOWN` and wait for the Owner. “Directly related,” “while here,” and “needed for the demo” do not expand the allowlist.

## CodeGraph writable-checkout gate

For a valid-HEAD slice, wait until the exact Lead and its worktree are `READY`. Then, before creating the Writer role, invoke the user-scope `codegraph-context` skill in that actual writable worktree. Require its ensure/synchronize step to pass and run exactly one focused `codegraph_explore` query with `maxFiles: 2`. If the repository is genuinely no-code or documentation-only and the focused query returns no relevant code, record that exact no-code/doc-only result; it satisfies the exploration evidence but does not waive ensure/synchronize.

The per-worktree `.codegraph/` cache is required ignored tooling state. Never track, copy, commit, or treat it as a project artifact. “Do not duplicate CodeGraph” means do not create tracked indexes, MCP configuration, or call-path documentation; it does not forbid the ignored cache required in the actual writable checkout.

If CodeGraph is missing or unusable, initialization or synchronization fails, or the focused exploration cannot run or produce the documented no-code/doc-only result, report `FAIL` and `SAFE_HOLD` before Writer creation. Do not substitute Git, `rg`, manual file reading, another checkout's index, or another discovery tool. Never disable or delete global CodeGraph or Superpowers.

Approved no-HEAD S000 has one necessary sequencing exception because CodeGraph cannot initialize before Git exists. After the LOCAL/no-worktree Lead is `READY`, create the sole Writer with authority to perform Git initialization only. Immediately after Git exists, and before any foundation-file edit, that Writer must invoke `codegraph-context` in the saved local checkout and pass the same ensure/synchronize plus one focused `maxFiles: 2` exploration or documented no-code/doc-only result. Failure produces `FAIL` and `SAFE_HOLD` before foundation work; no fallback is allowed.

## Roles

- **Owner / original PO:** Own the goal and checklist, approve the slice and any repository-rule merge, and accept or reject product value. Do not code or review code.
- **Lead:** Work in exactly one separate user-visible left-sidebar task named `[Project] — Tổ trưởng — <slice code/name>`, created by the PO task only after the exact approval-and-creation confirmation and through the HEAD-selected creation path. Coordinate and report. Check only boundaries, status, and evidence. Do not edit or re-review code, widen scope, or claim acceptance.
- **Writer:** Be the only writer in the only writable checkout and an internal subagent of the Lead. For local/no-HEAD S000, work in the shared saved local checkout with no second writable checkout or worktree; before its CodeGraph gate passes, the Writer may initialize Git and do nothing else. Otherwise create the Writer only after the actual worktree passes the CodeGraph writable-checkout gate. Edit only the allowlist for the current slice. Never create a sidebar task.
- **Reviewer:** Be the only independent reviewer, remain read-only, and run as an internal subagent of the Lead. Use the applicable Superpowers review workflow to check scope/spec, risk, diff, and fresh evidence; return findings or `PASS`. Do not fix findings or create a sidebar task.

Before creating the Lead for a later accepted slice, archive the previously accepted Lead through the platform capability and verify that exact previous Lead is archived. Preserve its history; do not delete or reuse it. If archival or verification fails, report `FAIL` and create nothing.

After the exact approval-and-creation confirmation, the PO must run the HEAD/topology gate and make exactly one creation attempt through the Codex/platform user-visible task/thread creation capability (`create_thread` where available), using its worktree path for valid HEAD or its LOCAL/no-worktree path for approved no-HEAD S000. Create exactly one new Lead task named `[Project] — Tổ trưởng — <slice code/name>`. Together with the current `[Project] — PO Gốc`, exactly two unarchived user-visible tasks must appear in the left sidebar. Only the Writer and sole independent read-only Reviewer are internal subagents of the Lead and create no sidebar tasks.

A returned real `threadId` is not `READY` until a compact platform task-list observation verifies that the same real task belongs to the exact project, has the exact required Lead title, and is visibly present in the sidebar. A returned `clientThreadId` means `QUEUED_NOT_READY`: it is never `FAIL`, never a real `threadId`, and must never be passed to tools that require `threadId`. Do not create again, substitute an internal Lead, or let the PO or Lead make a manual bootstrap commit.

For `QUEUED_NOT_READY`, declare a bounded deadline or bounded observation count and use only compact platform task-list observations for the exact project/title. Do not busy-loop, poll the creation request, or read full task/thread contents. If the exact real task and canonical `threadId` appear within the bound, reconcile them to the same creation attempt, repeat the exact project/title/sidebar verification, and mark the Lead `READY`. If the bound expires, report `UNKNOWN/QUEUED`, preserve the repository, and hard-stop. On a later Owner turn, make one fresh compact reconciliation observation before any creation attempt; if the original exact Lead exists, reconcile it and never duplicate it. If it remains queued or unproved, remain `UNKNOWN/QUEUED` and do not create again.

If creation is unavailable or returns a confirmed error, exact project/title/sidebar verification fails or conflicts, an unexpected duplicate appears, or a required archival gate fails, report `FAIL`. No queued state alone is a failure. After exact confirmation, contact the Owner only for final acceptance, a true boundary expansion, or the defined queued status; the Owner remains in the PO task.

Do not merge roles because of urgency, availability, harness limits, or task size. A blocked role blocks the slice.

## No overlapping methods or reviews

Three-Level Delivery is the top-level controller for Owner intent, slice scope, roles, durable state, approval, evidence, and stop gates. It does not replace CodeGraph or invent design, implementation-plan, TDD, debugging, verification, or review methods.

Use this fixed order:

1. Three-Level Delivery confirms the project binding and Owner authority.
2. CodeGraph performs repository discovery first.
3. The applicable Superpowers method runs inside the approved slice.
4. Three-Level Delivery records evidence and durable state, then stops at the Owner gate.

Keep one plan hierarchy. The three-level work card is the owner-facing plan. Put the Superpowers implementation plan inside that slice or link it from the work card; it is subordinate and cannot create another scope, role tree, or checklist item.

`PROJECT_VISION` and `PROJECT_STATE` equivalents are Owner-level memory only. S000 must not create implementation design, plan, test, or review documents owned by Superpowers. When those artifacts are needed in a later approved slice, link them from project state; do not copy them. Do not create tracked CodeGraph indexes, MCP configuration, or call-path documentation. The ignored `.codegraph/` cache required by `codegraph-context` in the actual writable checkout is tooling state, not a duplicated project artifact.

Writer RED/GREEN and verification are self-check evidence, never independent review. The Lead checks boundaries/status/evidence without reviewing code. The Owner accepts product value and controls the next slice without reviewing code. Exactly one independent Reviewer performs the review workflow. Never add a second Reviewer. Add a re-review round only when that same Reviewer has a concrete finding or risk to re-check.

If a Superpowers workflow suggests multiple coding agents, writable checkouts, worktrees, or review hierarchies, the Three-Level Delivery one-Writer/one-writable-checkout/one-Reviewer hierarchy wins. The approved no-HEAD S000 local path uses the saved checkout without a worktree; every valid-HEAD slice uses exactly one worktree. The CodeGraph writable-checkout gate changes neither role count nor review ownership. Preserve the applicable Superpowers technical checks within that same independent Reviewer. Keep the Reviewer read-only and return every fix to the same Writer.

Include a truthful update to the mapped `PROJECT_STATE` equivalent in every slice allowlist and review it through the same Writer/Reviewer flow. Record only current facts and evidence. A stable change to the mapped project vision requires separate Owner approval; never bury it in a state update.

## Repository recovery rules

Before adding persistent rules, read the existing repository instructions. Prepare a preview using only this owned block:

```markdown
<!-- THREE_LEVEL_DELIVERY_START -->
## Three-Level Delivery
- Current slice: <code> — <plain-language name>
- Owner-approved goal: <outcome>
- Writable allowlist: <exact paths>
- Roles: Owner; read-only Lead; one Writer; independent read-only Reviewer
- Required dependencies: CodeGraph and Superpowers
- Stop rule: report this slice and wait for owner acceptance
<!-- THREE_LEVEL_DELIVERY_END -->
```

Show the exact merge preview and wait for Owner approval before writing it. Merge only inside these markers. Never replace an existing instruction file. If markers conflict, are duplicated, or overlap existing policy, make no instruction-file edit and report `FAIL` with the conflict.

## One-slice workflow

1. Confirm explicit invocation in the correct large-project Codex project/task. Run and pass the once-per-new-PO-task/activation canonical freshness gate, then pass the read-only startup gate.
2. Ask for the project idea and first visible result, confirm the intended folder, and classify its foundation as established or unestablished; stop if the classification is ambiguous.
3. For an established foundation, use CodeGraph and map the existing project-memory documents. For an unestablished project, propose only `S000 — Create the project foundation`; do not initialize Git or CodeGraph yet.
4. Propose exactly one slice, including its project-state update and any repository-recovery merge preview, and ask once for exact confirmation approving both the slice and creation of its separate visible Lead task. Until that confirmation, create no visible task, internal delivery role, or target-repository write.
5. After exact confirmation, archive and verify the previously accepted Lead when one exists, then run `git rev-parse --verify HEAD` and make one visible-task creation attempt through the selected path. Valid HEAD requires one worktree. Approved S000 with an unborn/new Git repository or new non-Git project requires the LOCAL/no-worktree path bound to the saved checkout. Verify any returned real `threadId` against the exact project, title, and sidebar. Treat `clientThreadId` as `QUEUED_NOT_READY` and reconcile only through the declared bounded compact task-list observation. A deadline is `UNKNOWN/QUEUED` and a hard stop, never permission to retry or create again; on a later Owner turn, observe once afresh before any create and reconcile the same Lead if it exists.
6. For valid HEAD, after Lead/worktree `READY` and before Writer creation, run the CodeGraph writable-checkout gate in the actual worktree. For local/no-HEAD S000, the Lead creates the sole Writer with Git-initialization-only authority; after Git exists, that Writer passes the same CodeGraph gate in the saved checkout before any foundation edit. Any CodeGraph gate failure is `FAIL/SAFE_HOLD` before writing work.
7. The Lead gives its one internal Writer exactly the slice code, plain-language name, goal, allowlist, and checks. For local/no-HEAD S000, that Writer alone creates only the approved missing foundation files after CodeGraph passes and creates the first Git commit. The root commit may contain only the approved S000 allowlist: the minimal missing `README.md`, owned `AGENTS.md` block/rules, `docs/PROJECT_VISION.md`, `docs/PROJECT_STATE.md`, and stack-appropriate `.gitignore`. It must contain no app, demo, product, package, framework, or Superpowers-owned specification, plan, test, review, or tracked CodeGraph artifact. The PO and Lead never create the bootstrap commit.
8. Have the Writer implement only that slice with the applicable Superpowers workflow, update project state truthfully, and provide fresh self-check evidence. Give the one independent read-only Reviewer the locked contract, diff, project-state update, checks, and, for S000, root-commit evidence. A finding returns to the same Writer for correction and then to that Reviewer for re-check; it does not add a Reviewer or create a new slice.
9. Return the result to the PO task, report the S000 foundation and root-commit evidence when applicable, and ask the Owner for final acceptance, then hard stop. Do not prepare or open product work. From S001 onward a valid HEAD must exist and exactly one worktree is mandatory. After S000 acceptance, do not combine, prepare, propose, or open a product slice in the same interaction. A product slice may be proposed separately only in a later Owner-gated interaction.

## Owner report

Use ordinary language and this exact shape:

```text
Slice: <code> — <plain-language name>
Status: PASS | FAIL | UNKNOWN
Changed: <exact files, or none>
Evidence: <fresh checks and results>
Reviewer: PASS | findings
Blocked/unknown: <facts, or none>
Owner gate: accept this slice or request a correction
```

`PASS` requires fresh checks and an independent reviewer with no open findings. Use `FAIL` for a violated gate or confirmed failure. Use `UNKNOWN` when evidence is missing or current runtime behavior was not proved; a queue deadline is `UNKNOWN` with `QUEUED_NOT_READY` in `Blocked/unknown`. Source inspection, fixtures, and old test output are not live proof.

## Red flags

- Lead starts coding or reviewing its own work.
- More than one writer or writable worktree exists.
- Self-check, Lead boundary checks, or Owner acceptance is counted as independent review.
- A second Reviewer or parallel plan hierarchy appears.
- A re-review happens without a concrete finding or risk from the same Reviewer.
- A new checklist item, cleanup, framework, hook, daemon, or background process appears.
- CodeGraph or Superpowers is skipped, disabled, or auto-installed.
- The canonical freshness gate is skipped on a new PO task/activation; runs for an unrelated question; uses any URL other than the exact canonical raw `SKILL.md`; sends credentials or writes; accepts malformed/wrong-identity/older/unknown canonical data; compares versions lexicographically; guesses; bypasses; or silently updates.
- A visible task or internal delivery role is created before exact approval of both the slice and separate Lead-task creation.
- The HEAD/topology gate is skipped; a valid-HEAD slice does not use one worktree; or an approved unborn/no-HEAD S000 requests or creates a worktree instead of using the saved local checkout.
- A previous accepted Lead is deleted, reused, left unarchived, or not verified archived before the next Lead creation.
- Lead creation is attempted more than once; the creation request is polled or retried; observation is unbounded or busy-loops; full task contents are read for reconciliation; a `clientThreadId` is treated as failure, readiness, or a real `threadId`; a queued deadline is treated as `FAIL`; a later Owner turn creates before fresh reconciliation; an exact returned real Lead is not verified by project/title/sidebar; an internal Lead is substituted; or more than two unarchived user-visible tasks exist.
- A valid-HEAD Writer is created before the actual worktree passes CodeGraph ensure/synchronize plus one focused `maxFiles: 2` exploration or documented no-code/doc-only result; S000 edits foundation files before that same post-Git gate; another checkout/index, Git, `rg`, or manual reading is substituted; or `.codegraph/` is tracked or copied.
- The PO or Lead creates a manual bootstrap commit, local/no-HEAD S000 has more than one writable checkout, or S000 completes without the Writer's first Git commit and root-commit evidence.
- Foundation status is ambiguous, or app, demo, product, package, or framework code appears in S000.
- The S000 root commit contains anything outside its approved foundation allowlist, creates Superpowers-owned technical artifacts, or duplicates CodeGraph artifacts.
- S000 acceptance combines with or automatically opens a product slice instead of hard-stopping.
- Existing project-memory documents are duplicated or overwritten, project state is stale, or stable vision changes without separate Owner approval.
- Existing repository instructions are overwritten.
- “Done” is reported without fresh evidence and independent review.

On any red flag, stop, preserve the repository, and report the exact gate that failed.
