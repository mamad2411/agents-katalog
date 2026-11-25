---
name: work-implement
description: "Executes documentation, configuration, infrastructure, and other work without testable application behavior, including the bare \"go\" reply after a work plan. Planning-only requests use work-plan; testable application changes use implement. Excludes trivial single steps."
---

# Work Implement (non-TDD plan executor)

Execute a work plan under the verification discipline below. The parent (this skill) owns the **plan file**, the **execution decision** for each batch (direct or delegated), the **milestone global checks**, **every `Task (apply):` execution**, and the **final report**. Workers — the parent itself or a sub-agent — make the changes for their assigned items, run validation-tier commands only, and report evidence: each Verify command as run, a summary of its output against the plan's expectation, and the result.

The counterpart of TDD's Red-Green gate here is the plan's Verify steps (see the work-plan skill): each item names a command or observable state and its expected outcome. This skill's job is to make those gates actually gate — before-check, change, verify, evidence read by the parent — instead of trusting that an edit "should work".

## Verification discipline (per item)

1. **Before-check (Red analog)**: run the item's Verify step before changing anything and confirm the expected outcome does **not** hold yet. If it already holds, inspect whether the task's intended state is actually present: if so, report the work as already done, mark the item `[x]`, and move on; otherwise the Verify step is inadequate — leave the item unchecked, stop and escalate, and never "fix" the Verify step to force a pass. When a before-check is meaningless for the item's nature (e.g., a change-previewing command that errors before the config exists), record it as not checkable and proceed.
2. **Change**: make the item's change, and nothing beyond it.
3. **Verify (Green analog)**: run the Verify step and compare the output against the expected outcome stated in the plan — not merely the exit code. A pass with unexpected extra output (an unplanned resource in a `terraform plan` diff, an extra warning) is a fail until explained.

## Principles

- **Evidence, not claims**: Every item's before-check and Verify run are reported with the exact command, an output summary, and the result. The parent reads that evidence; it re-runs the plan's global check itself at milestones (phase completion, plan completion, before a commit suggestion). For a completed batch, it re-runs an item's Verify step only when the reported summary does not match the plan's expected outcome verbatim, when evidence is missing, or when fields contradict each other. A blocked batch follows step 6's stop path; an expected `not_run` is not missing evidence of success.
- **Apply stays in the parent**: `Task (apply):` items — live-state mutations — are never dispatched to sub-agents and never run without explicit user confirmation. Sub-agents are constrained to validation-tier commands (validate, dry-run, plan, lint, build).
- **Centralized plan writes**: Only the parent edits the plan file — marking items `[x]`, appending discovered tasks. Sub-agents never write under `.plans/`.
- **Work-driven delegation**: Decide per batch (step 4). Direct execution is the normal mode for one or a few small items with short command output; delegation is the normal mode for batches that load knowledge skills, produce long output (a `terraform plan` diff, a build log), or start a long plan. Whether dispatch tooling exists does not decide by itself.
- **File ownership, sequential dependence**: A batch owns the files it edits until its result is in. Items build on the verified state before them, so editing batches run one after another; only read-only work fans out.
- **Context economy**: Knowledge skills load only when a batch makes a decision they cover (selection table in `references/worker-dispatch.md`) — in the sub-agent for a delegated batch, in the parent for a direct one. Sub-agents return the structured result, never diffs or full logs.
- **No git writes**: Neither the parent nor any sub-agent commits, pushes, stashes, or changes branches. Build artifacts from mandated verification runs and the plan file under `.plans/` are expected side effects, not violations. When all items are done, suggest a commit (the git-commit skill) and leave the decision to the user.

## Skill locations

Sibling skills live next to this one. Resolve them relative to the directory this `SKILL.md` was read from: `<skills root>/<name>/SKILL.md`, where `<skills root>` is the parent of this skill's directory. Both runtimes link the same checkout, so whichever root this file was loaded from is correct — do not probe for a runtime-specific directory. Pass the resolved absolute paths into every dispatch; a sub-agent never guesses locations.

## When to use

- The user asks to execute an existing work plan end-to-end.
- The user asks to carry out multi-step work without automatically testable application behavior (infrastructure, configuration, CI/CD, documentation, migrations, housekeeping) — create the plan first via the work-plan skill, then execute it here.
- The user says bare `go` after a work plan was created in the current session.

Do not use when:

- The work has automatically testable application behavior — the implement skill (and the tdd stack) owns that.
- The user asks only to create a plan — the work-plan skill owns that.
- The task is a single trivial step with no plan value (one file edit, one command) — do it directly.
- The goal is reviewing, not executing — the local-review skill owns review.

## Workflow

1. **Resolve the plan**: An explicitly named plan file first, then the plan created in the current session, otherwise look at `.plans/`: exactly one plan matching the request → use it without asking; two or more candidates → list them and ask; none → create one first by following the work-plan skill (planning stays in the parent — it needs the user dialog), then continue here. If work-plan concludes the request belongs to the TDD stack, this skill does not apply either; say so and stop.

2. **Resolve the environment**: Resolve the skills root (above). From the plan's Context, note the global check command (if any) and the prerequisites (CLIs, auth, environment/workspace names). Confirm the prerequisites hold with read-only commands (`terraform workspace show`, `nix --version`, `gh auth status`, …). A missing prerequisite is an early stop: report what is missing, the plan's untouched state, and how to resume — that minimum is the report contract for every early stop this skill makes.

3. **Confirm the baseline**: Run the global check command once, if defined, and snapshot `git status --porcelain`. If the check already fails, classify the failure by reading, never by editing: inside the plan's Goal or in files the plan will change → propose a leading repair item and, when the user's request already covers those files, add it to the plan and proceed; outside the plan's scope → report per the early-stop contract and ask whether to fix, ignore, or stop. Never build on a failing baseline silently.

4. **Choose the batch and its mode**: Take the first unchecked `- [ ] Task` item and form a batch per "Batching rules" in `references/worker-dispatch.md` — a coherent responsibility, never across a phase boundary. A `Task (apply):` item always stands alone and is never dispatched. Then choose the mode for a `Task:` batch:
   - **Direct** when the batch is small and clear: one or a few items, at most one knowledge skill needed (or none), commands whose output is short enough to read in the parent.
   - **Delegate** when the batch needs catalog reads, produces long output, or starts a long plan — or when the user asked for sub-agents.
     When the runtime exposes no working dispatch tooling (no dispatch tool, or an attempt fails), every batch is direct — say so in the report. Running inside a sub-agent is not by itself a reason to go direct. Apply gating never changes with the mode.

5. **Execute the batch**:
   - **`Task:` items, delegated** — dispatch one worker with the prompt from `references/worker-dispatch.md`: it names the knowledge skills selected for this batch, pastes the plan's Goal/Context and the item text (including Verify bullets), states the verification discipline, the hard constraints, and the result schema. Wait for the result; never start a dependent batch early.
   - **`Task:` items, direct** — run the verification discipline in the parent for each item in order, reading the selected knowledge skills first, and record the same fields the result schema defines (per-item before-check, Verify command/summary/result, files changed, discovered tasks, notes) in the conversation so step 6 has the same evidence to read.
   - **`Task (apply):` items** — no dispatch. Present the item to the user: what will run, the Verify expectation, and the Rollback line. Proceed only on explicit confirmation; a confirmation may cover consecutive apply items the user approves together, but silence or a prior general "run the plan" never counts. On confirmation, run the command in the parent, then its Verify step. On refusal, leave the item unchecked and either continue with independent later items or stop and report, as the user directs.

6. **Verify and record**: Read the batch's status and evidence. For `blocked`, stop and relay the reason per the early-stop contract; a Verify that was not run before the block remains `not_run`, and does not trigger a re-run merely because it lacks the expected success output. For `done`, evidence is complete when every item reports its before-check, its Verify command as run, an output summary, and a result, and every summary matches the plan's expected outcome verbatim. When a summary does not match verbatim, evidence is missing, or fields contradict each other in a `done` result, re-run that item's Verify step in the parent before deciding.
   - **Pass**: mark the batch's items `[x]`. An item whose before-check found the outcome already satisfied still counts as completed; mark it and surface the note in the final report. Then append `discovered_tasks` from the result as new unchecked `Task:` items (with their Verify bullets) right after the current position — in a phased plan, inside the current phase. Two gates: skip any entry whose outcome an existing item already covers (compare outcomes, not wording), and never append an entry carrying an open design question or a live-state mutation — an apply-tier discovery is always escalated to the user, never self-appended. Growth guard: if appended items would outnumber the plan's original unchecked items, route further discoveries to a follow-up list for the user instead.
   - **Fail** (the worker reports a failing Verify, or the parent's re-run fails): one fix pass per the recovery policy in `references/worker-dispatch.md`, then stop if it fails again. Never revert files or roll back applied state on your own — for a failed apply item, present the item's Rollback line and let the user decide.
   - **Milestone**: when the batch completes a phase or the plan, run the global check command in the parent (if defined). A failure is handled by the recovery policy; a pass is recorded with the phase's `After this phase:` outcome. The global check also runs before the final commit suggestion — the plan-completion run is that run unless files changed after it.

7. **Repeat** steps 4–6 until no unchecked item remains. Phase completion is reported, not paused on: state the phase outcome and the global-check result, then continue. Pause only when the user asked for a checkpoint (e.g. "stop after each phase"), when an apply item needs its confirmation (always), or when a decision the next batch depends on is still open — and say which instruction or question causes the pause. Then **report**: items completed, files changed (`git status --porcelain`), Verify and global-check results, apply items executed (with confirmations) or refused, items appended or routed to the follow-up list, before-checks that found work already done, and which batches ran directly versus delegated (and whether dispatch tooling was unavailable). User-facing reports are written in the conversation language; repository artifacts (plan items, code, comments) stay in English. Suggest committing via the git-commit skill. Never commit automatically.

## Red flags (watch for rationalizations)

| Rationalization | Reality |
| --- | --- |
| "The apply is small — run it without asking." | Live-state mutations always get explicit confirmation. Small applies have large blast radii. |
| "The sub-agent can run the apply; it has the context." | Apply items never leave the parent. A sub-agent cannot be interrupted by the user mid-mutation. |
| "The command exited 0 — the item is verified." | The gate is the expected outcome, not the exit code. Compare the output against what the plan says it must show. |
| "Skip the before-check; the change obviously isn't applied yet." | An already-satisfied expectation is exactly the signal the before-check exists to catch. Run it. |
| "The result says verified — no need to read the evidence." | Read each item's command, summary, and result. A summary that does not match the plan verbatim means a parent re-run, not trust. |
| "Re-run every Verify step in the parent to be safe." | The parent re-runs the global check at milestones and spot-checks mismatched or missing evidence. Duplicate re-runs add no information. |
| "Dispatch tooling exists, so every item goes to a sub-agent." | Delegation is chosen per batch by what it buys. One small item with short output runs directly in the parent. |
| "The Verify step is too strict; loosen it so the item passes." | Weakening a gate to pass it defeats the plan. Stop and escalate the mismatch instead. |
| "Verification failed; keep patching until it passes." | One fix pass, then stop and report. The user decides between reverting and debugging. |
| "Roll back the failed apply so the report looks clean." | Rollback is a state mutation like any other: present the Rollback line and let the user decide. |
| "A phase just finished — wait for the user before continuing." | Report the phase and continue. Pause only for a requested checkpoint, an apply confirmation, or a decision that blocks the next batch. |
| "Commit after each phase to be safe." | Committing is the user's call. Suggest the git-commit skill at the end; never commit inside this skill. |

## Additional Resources

### Reference Files

- **`references/worker-dispatch.md`** — The knowledge-skill selection table (used for direct execution too), batching rules, the dispatch prompt template, the result schema, the recovery policy, and the direct-execution contract.
- **`agents/openai.yaml`** — UI metadata for this skill only.
