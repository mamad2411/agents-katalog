---
name: supermeta
description: Turn a READY coding-loop project folder into the next round's meta-plan and drive supergoal (auto-confirmed) to scaffold the goal folder the inner loop will build. Writes meta-plans/<STAMP>-r<N>.md, dispatches one PLANNER subagent that runs supergoal, appends the iteration-ledger row, and commits per superauthor A7. Stage 2 of the coding loop; runs unattended.
argument-hint: "<project-dir> [--resume-draft <draft-index.md>] [--operation <path>] [--supervisor-state <path>]"
license: MIT
related skills: superauthor, supergoal, superprd, supereval
---

# Supermeta

The **meta-planner** of the coding loop. Given a READY project folder (`prd.md`,
`knowledge-base.md`, `evaluation.md`, written by `superprd`), supermeta writes the round's
**meta-plan** — a self-contained goal description a planner can turn into a root master plan without
any other context — and drives `superagent:supergoal` (auto-confirmed) to scaffold the goal folder
the inner `superagent` loop will build. It then records the round in the project's iteration ledger.

supermeta **never plans the work itself and never touches source code** (superauthor A1): it produces
structural docs (a meta-plan and a ledger row) and dispatches exactly **one** PLANNER-role subagent
that invokes `superagent:supergoal`.

**Input:** `<project-dir>` — an existing coding-loop project folder. **Required.**
`--resume-draft <draft-index.md>` is the explicit recovery form for an incomplete supergoal draft.
Optional: `--operation <path>` uses a supervisor-persisted operation identity. Supercode dispatches
also pass `--supervisor-state <path>`: the real registered project state, required for
author-approved META entry. That flag requires `--operation`. With no operation, all manual defaults
remain unchanged.

## Incomplete-draft recovery

Before deriving a new round, recognize `--resume-draft` and read the index through supergoal's recovery
contract. It must name this project, its original meta-plan/source snapshot and digest, intended goal
destination, stable draft identity, and original round. Reuse those values exactly; do not allocate a
new round or write another meta-plan. First reconcile a lost response against the intended destination:
a complete tracked root, all indexed artifacts, and matching review is publication evidence and can flow
to the normal labelled-report parse only when its A7 PR/commit is verified in authoritative internal
main or the external vault branch. Reconstruct the result from those actual artifacts and history, not
from a success-looking child message. Absent publication resumes the same index; partial, conflicting, or
multiple publication is `BLOCKED`. The saved draft itself is never approval: the resumed child still
receives the current two-factor confirmation invocation.

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Vault root

Resolve `SUPER_GOAL_ROOT` (above). If it starts with `/` or `~`, the vault is **external**:
`<vault_root>` is that path (`~` expanded to `$HOME`, one trailing `/` stripped), resolved physically
(`cd "<path>" && pwd -P`) so it matches the paths `launch.sh` stores, and the vault is its own git
repository outside the checkout. Otherwise `<vault_root>` is `<primary_root>/<SUPER_GOAL_ROOT>`
(`primary_root` = the physical `REPO` exported by `superagent_load_context`). Every goal
folder, project folder, loop-status file and lock derives from `<vault_root>`; **never join
`SUPER_GOAL_ROOT` onto the checkout root by hand.** The same rule is `vault_root` /
`vault_is_external` in `scripts/_common.sh`.

## What supermeta is not

| Thought | Reality |
|---|---|
| "The meta-plan is basically the root plan, I'll write the master plan here" | NO. supermeta writes a *goal description* (the meta-plan). `supergoal` scaffolds the goal folder; `superplan` writes the plans; `superrun` executes. supermeta plans nothing (A1). |
| "I'll invoke `supergoal` directly, it's simpler than dispatching a subagent" | NO. supermeta dispatches exactly one PLANNER-role subagent that runs `supergoal`, so the PLANNER model pin applies and the invoking context stays lean. |
| "`--autoconfirm` alone skips the pause" | NO. It is honoured only when `SUPER_GOAL_AUTOCONFIRM` resolves to `true` (two-factor). If the key is not true, supergoal reports `--autoconfirm ignored: SUPER_GOAL_AUTOCONFIRM is not true` and pauses — treat that as a refusal (see step 6). |
| "A defect in `evaluation.md` / `prd.md` — I'll just fix it" | NO. Report it as a finding; supermeta reads the inputs, it does not edit them. |

## Workflow

### 1. Invoke `superagent:superauthor`

Invoke it via the Skill tool and apply **A1** (no execution), **A3** (no placeholders), **A5** (no
confirmation pause — supermeta runs unattended by design), **A6** (findings capture), **A7** (commit
and merge), **A8** (Final Report). **A2 does not apply** — the meta-plan is a structural goal
description, not an implementation plan.

### 2. Inputs

Resolve `<primary_root>` (the code checkout: the physical `REPO` exported by `superagent_load_context`) and `<vault_root>` (see **Vault root**).

1. `<project-dir>` must exist and contain `prd.md`, `knowledge-base.md`, `evaluation.md`, each with
   `**Status:** READY` in its header block. Otherwise print
   `supermeta: <project-dir> is not a READY project folder (<what is missing>)` and **exit** without
   writing.
2. Run `PRD_LINT_REPO_ROOT="<primary_root>" "${CLAUDE_PLUGIN_ROOT}/scripts/prd-lint.sh" "<project-dir>"`.
   A non-zero exit is the same refusal, quoting the FAIL lines, then **exit** without writing.

When `--operation <path>` is present, load duplicate-key-rejecting JSON containing exactly `id`,
`phase`, `round`, `agreement_revision`, `code_commit`, `meta_plan`, `goal_folder`, `report`, and
`source_vault_commit`. Apply the types and locator rules from `_coding_loop_state.py` and
`_coding_loop_evidence.py`. Require `phase` = `META-PLANNING`, empty `code_commit` and `report`, a
32-character lowercase hexadecimal `id`, and nonempty remaining identity fields. The recorded
`meta_plan` must resolve inside `<project-dir>/meta-plans`; `goal_folder` must resolve inside
`<vault_root>`. Keep the file unchanged for the child.

Operation mode has a machine-readable completion contract. Its last output line is one compact JSON
object with keys `outcome`, `phase`, `operation_id`, `round`, `meta_plan`, `goal_folder`,
`root_plan`, `goal_complete`, `goal_recoverable`, `goal_completion_reason`, `worker_complete`, `completion_reason`,
`artifacts`, and `reason`. `outcome` uses the reconciler's
`INTEGRATED`, `ABSENT`, or `CONFLICT` artifact classification; an integrated reusable goal can still
have `worker_complete: false`. That flag becomes true only after the goal, meta-plan and ledger are
verified on `main`. Paths are absolute and each verified artifact has `path` and `commit`. The caller
uses this result for recovery; the human Final Report is not phase-completion evidence.

### 3. Derive identifiers

- `<STAMP>` — `date -u +%Y-%m-%d-%H_%M`, taken once per new round. A resume takes the saved stamp.
- `<project-slug>` — the project folder's basename with its leading `YYYY-MM-DD-hh_mm-` stamp
  stripped (e.g. `csv-summariser`).
- `N` (round) — for a new run, `1 +` the number of data rows in `prd.md`'s `## Iteration ledger`
  table (so the first round is `1`); for `--resume-draft`, the index's original round. Never append a
  ledger row merely because a scratch draft exists.
- **Repair guidance** — if `<project-dir>/diagnoses/<…>-r<N-1>.md` exists (never in Stage 2; the
  file layout is fixed so Stage 3 needs no change here), read it and quote its per-problem guidance;
  otherwise repair guidance is `none — first round`.

In operation mode, do not derive identities from the clock or ledger. Use the recorded `round`, exact
`meta_plan`, and only permitted `goal_folder`; derive `<STAMP>` from the frozen basenames and reject
inconsistent round, stamp, slug, ledger, or project identities. Require `source_vault_commit` on
vault `main` and the current agreement fingerprint equal to `agreement_revision` before dispatch.
For a supercode dispatch, independently validate worker entry before drafting, dispatching a planner,
or reusing an existing artifact. Run the installed helper against the actual registered state:

```text
python3 SCRIPTS/_coding_loop_state.py meta-entry STATE --repo PRIMARY --vault VAULT
  --conf XDG_CONFIG_HOME/superagent --operation OPERATION_JSON
```

Resolve the config directory from the process environment (`$XDG_CONFIG_HOME`, default
`$HOME/.config`), not an assertion in the worker prompt. The helper reloads state, requires exactly
one matching supercode registration, recomputes binding context, and matches the exact reserved
project/round/operation/agreement. Read its JSON `entry` result yourself. A parent-supplied result,
free-form assertion of author approval, or an authorization file elsewhere is not evidence.

- `FIRST_ROUND`: requires round 1; guidance is `none — first round`.
- `AUTHOR_APPROVED`: permits this new planning round after actual author adoption or replan even
  when the previous result was PASS, had different criteria, was a legacy round with no diagnosis,
  or had AUTHOR INPUT. The validator requires the exact consumed-answer Decisions receipt and a
  matching durable authorization bound to this operation id, project, from/to rounds and current
  agreement. Preserve its decision id and answer as meta-plan provenance. Guidance is
  `author-approved planning under the current agreement`; read prior artifacts as history and
  incorporate only still-applicable obligations. Do not require an old FAIL/current-agreement
  REPAIR in this branch, reuse old PASS, weaken criteria, or call this a first round.
- `AUTONOMOUS_REPAIR`: the helper verifies the exact prior integrated FAIL and current-agreement
  REPAIR receipt. Read that selected diagnosis and apply the strict guidance contract below.

A missing/mismatched receipt is CONFLICT, not permission to invent authorization. Repeat this
validation before integration; retries use the same state, operation id and decision receipt.
Without --supervisor-state there is no author-approved entry path: retain the strict manual /
operation-mode repair requirements below for later rounds.

For round 1, repair guidance is `none — first round`. For a later round **other than the validated
AUTHOR_APPROVED entry**, locate the unique FINAL
diagnosis linked to the previous ledger row's failed report and validate it with
the existing Python API and its complete authoritative inputs:

```python
validate_diagnosis(
    diagnosis_path,
    {
        "round": N - 1,
        "eval_report": previous_eval_report,
        "code_commit": previous_evaluated_commit,
        "agreement_revision": agreement_revision,
        "source_vault_commit": diagnosis_source_vault_commit,
        "failing_ids": validated_previous_eval["failing_ids"],
        "missing_ids": validated_previous_eval["missing_ids"],
    },
)
```

First run `validate_evaluation` on the previous report to obtain those failed/missing IDs and exact
evaluated commit; take the report path from the previous ledger row and require the diagnosis's
recorded source-vault revision on `main`. `validate_diagnosis` itself requires a unique operation ID
in the report. The result must match the previous round/report, evaluated commit, agreement and
source revision, return disposition `REPAIR`, and set `may_start_next_round: true`. Missing,
ambiguous, AUTHOR INPUT, or mismatched context is `CONFLICT` for autonomous repair; only the
validated AUTHOR_APPROVED entry above supplies a different planning authority. Never label a later
round as a first round.

### 4. Read the knowledge base

Read every row of `knowledge-base.md` by its `Kind`/`Locator`:

- `instructions` / `repo-file` / `sample-code` / `entry-point` (`<path>:<symbol>`) → read the file
  under `<primary_root>`.
- `repo-glob` → expand with `find` under `<primary_root>`.
- `doc-url` → fetch **only if** a fetch tool is available; else pass the URL through as a pointer.
- `context7` (`/<org>/<project>`) → resolve with `mcp__context7__query-docs` **when that tool is
  available**; else pass through.

For supervised operation mode every binding source must resolve: use the persisted verified
captures for doc-url/context7 sources when needed. A pointer alone is not acceptance context;
missing captures or an unresolved source is CONFLICT. This strict supervised gate does not change
the existing manual pointer behavior above.

For each row that resolved, keep the 1–10 lines most relevant to planning the work (a function
signature, a config key, a doc sentence) for the meta-plan's Excerpt column.

### 5. Draft `meta-plans/<STAMP>-r<N>.md`, self-review, and move it in

Draft in scratch (`$TMPDIR/supermeta-<project-slug>-r<N>/`) with **exactly** this section order,
then self-review it (A4 — spec coverage against the PRD/evaluation, A3 placeholder scan):

```
# <Project title> — meta-plan round <N> — <STAMP>-r<N>
**Date:** <YYYY-MM-DD> · **Status:** READY · **Related:** [[<SUPER_PROJECT_DIRNAME>/<project-folder-basename>/prd]] · **Round:** <N>
**Operation:** <operation id> · **Agreement revision:** <agreement_revision> · **Source vault commit:** <source_vault_commit>   (operation mode only; omit this line manually)

## Goal for this round
<one or two paragraphs: what the inner loop must build or repair this round, written as a goal
description supergoal can plan from without any other context. Round 1: the PRD objective in full.
Round N>1: the objective restated plus the repair scope from the diagnosis.>

## Success criteria and checks
<every SC row from prd.md verbatim, then every C/J row from evaluation.md verbatim, including the
Environment setup/cwd lines, the full Acceptance checklist with its approval record, and all
binding contract notes. Preserve source references and identify the source project revision
(`commit:<sha>` in GitHub mode or the recorded local mode/root plus file paths before evaluation).
Carry optional suggestions separately as nonbinding context.
These are the approved conditions the plan must satisfy; do not derive a new coverage inventory.>

## Knowledge base
| Id | Kind | Locator | Read for | Excerpt |
<every knowledge-base row, plus an Excerpt column: the 1–10 lines the meta-planner judged most
relevant after reading the source. Never empty for rows that resolved; `(not fetched)` for unfetched
doc-url/context7 rows.>

## Constraints and locked decisions
<prd.md's "Constraints and non-goals" and "Locked decisions" sections verbatim>

## Repair guidance
<`none — first round`, the verified diagnosis's per-problem guidance, or author-approved planning with its decision id and exact answer>

## Planner instructions
- Goal folder slug: `<project-slug>-r<N>`.
- Every implementation plan's verification steps must run the checks above by id; the loop's
  evaluator will run them unchanged afterwards.
- Carry relevant approved AC IDs, their full requirements and expected results into each leaf
  plan, together with the source revision. Keep a resolvable path to the full agreement. Report
  ambiguity or conflict for PRD revision; do not adopt extra test cases as new acceptance scope.
- Legacy projects without a checklist retain their existing explicit criteria and binding notes;
  do not fabricate an approval or retroactively require the new format. Ambiguous coverage needs
  an author decision, not a fresh unattended checklist.
- Do not modify `evaluation.md`, `prd.md`, or `knowledge-base.md`; a defect in them is reported as
  a finding, not fixed.
```

Then **move** the reviewed file from scratch into `<project-dir>/meta-plans/<STAMP>-r<N>.md`
(uncommitted until the ledger commit in step 7) so the goal folder's `**Source:**` link can point at
its vault path. In operation mode, if the exact path already exists, require its Operation line and
complete identity to match and resume it; never replace it or choose another timestamped name.

### 6. Dispatch supergoal via one PLANNER subagent

Dispatch **one** `PLANNER`-role subagent. Resolve `SUPER_MODEL_PLANNER` / `SUPER_EFFORT_PLANNER`.
<!-- cc-only:start -->
If the model is `inherit` or a bare tier name (`sonnet`, `opus`, `haiku`, `fable`) **and** the effort is `inherit`, dispatch with the plain subagent mechanism — `model: <tier>` when a tier, no `model:` when `inherit`. Otherwise — a full model ID such as the default `claude-opus-5`, a non-`inherit` effort, or a bridged harness prefix — dispatch with `subagent_type: super-planner` and omit `model:`; that is the definition `superagent:init` generates in `.claude/agents/`, and a missing definition is a hard error: report "re-run `superagent:init`" and stop.
<!-- cc-only:end -->
<!-- cursor-only:start
If the model is `inherit` or a bare model name **and** the effort is `inherit`, dispatch with the plain subagent mechanism — `model: <name>` when named, no `model:` when `inherit`. Otherwise dispatch with `subagent_type: super-planner` and omit `model:`; that is the definition `superagent:init` generates in `.cursor/agents/`, and a missing definition is a hard error: report "re-run `superagent:init`" and stop.
cursor-only:end -->
<!-- codex-only:start
For a native Codex role, use `spawn_agent` with `fork_turns: "none"`, `model` (the `codex:` prefix stripped), and `reasoning_effort`, omitting each pin that is `inherit`. For a foreign harness, use the generated banner's relay dispatch with `fork_turns: "none"`; pass the foreign model/effort to `role-bridge.sh`, never to the native spawn. No definition file is involved.
codex-only:end -->
<!-- pi-only:start
The planner gets no `.pi/agents/` definition; dispatch it exactly as `superagent`'s Subagent-dispatch section does the planner on Pi — a blocking `role-bridge.sh --tools planner` process with the model/effort from `SUPER_MODEL_PLANNER` / `SUPER_EFFORT_PLANNER` (a bridged prefix runs that harness's CLI). Wait on it; never poll.
pi-only:end -->
Set `SUPER_GOAL_AUTOCONFIRM=true` **only for this child dispatch**, together with
`--autoconfirm` below. Do not edit `.superenv` or change the caller's environment. For a CLI bridge,
prefix that invocation with `SUPER_GOAL_AUTOCONFIRM=true`; for a native subagent, include
`Treat SUPER_GOAL_AUTOCONFIRM=true as a dispatch-scoped override for this invocation` in its prompt.
On Pi also set `SUPERAGENT_PI_SKILLS="${CLAUDE_PLUGIN_ROOT}/skills"` on the bridge invocation,
so an attended call delivers `supergoal` to the child just as a scheduler tick does.

For a new run, the subagent's prompt instructs it to invoke the `superagent:supergoal` skill via the
Skill tool with

```
<GOAL> = <absolute path of meta-plans/<STAMP>-r<N>.md>   --autoconfirm   --slug <project-slug>-r<N>
```

and to **return supergoal's complete Final Report verbatim** as its final message.

For `--resume-draft`, pass `supergoal --resume-draft <draft-index.md> --autoconfirm` under the
same dispatch-scoped `SUPER_GOAL_AUTOCONFIRM=true`. This re-applies confirmation to the completed
current draft; it does not treat the saved index as confirmation. It remains the same one PLANNER
child, with no planner children beneath it. In operation mode append `--operation <the same absolute
operation JSON path>` to either the new-run or resume invocation. Before dispatch,
run `_coding_loop_evidence.py reconcile <primary_root> <vault_root> --operation <path>`. An
`INTEGRATED` result supplies the exact `goal_folder` and `root_plan`. If `worker_complete` is true,
return the existing completed operation. If `goal_complete` is true, reuse the scaffold and skip the
PLANNER dispatch while finishing meta/ledger work. If `goal_complete` is false and
`goal_recoverable` is true, dispatch PLANNER once with the same operation so supergoal explicitly
repairs only the missing matching scaffold. A false `goal_recoverable` is a hard conflict. For
`ABSENT`, dispatch once. For `CONFLICT`, resume only exact pending A7 work owned by this operation,
finish its normal integration, and reconcile again. An identity mismatch or
unrelated partial output is a hard conflict. Never infer success from child text, a folder
collision, working-tree bytes, or an unmerged commit.

Parse labelled `**Goal folder:**` and `**Root plan:**` from a complete returned report; an upfront
complete report must also carry labelled `**Planning mode:** upfront-v1`, `**Stages:**`, and
`**Tree review:**`, plus the merged internal `**PR:**` or external-vault `**Commit:**` publication
evidence. Synchronize and verify that one A7 unit contains every reported artifact before appending the
ledger. **If** the report contains `DRAFT-INCOMPLETE` and `**Draft index:**`, supermeta writes nothing
to the ledger, preserves/reports that index and its original meta-plan/source/round, and exits so the
explicit resume form can reuse it. **If** the report is missing a required complete field, or supergoal
reports a refusal — the key is not `true`
(`--autoconfirm ignored: SUPER_GOAL_AUTOCONFIRM is not true`), the goal folder already exists (the
never-overwrite collision report), or `I need a goal description` — then supermeta writes **nothing**
to the ledger, **moves the meta-plan back** out of `meta-plans/` into scratch, and reports the
failure **verbatim** with the scratch path, then exits.

### 7. Ledger and commit (A7)

Before appending, reconcile `prd.md` and authoritative history for this project/round/meta-plan/goal
identity. A matching integrated ledger row means a prior supermeta publication succeeded after its
response was lost: reuse it and report the existing PR/commit without appending or publishing again. A
single partial A7 unit resumes with the same row and branch; conflicting rows/publications are BLOCKED.

Append this row to `prd.md`'s `## Iteration ledger` table (the goal-folder path is
`**Goal folder:**` from step 6 made relative to `<vault_root>`):

```
| <N> | [[<SUPER_PROJECT_DIRNAME>/<project-folder-basename>/meta-plans/<STAMP>-r<N>]] | [[<goal-folder-path-from-vault-root>]] | - | - | - | - |
```

This is the new `Source` ledger shape. When appending to a legacy ledger with a `Commit` identity
column, preserve that header and use `-` in the identity cell. When appending to the older six-column
shape with no identity column, omit one `-`; do not silently change existing row widths.

In operation mode, inspect `main` for round `N` first. Reuse its one row only when it exactly links
the recorded meta-plan and goal. If absent, append it once. A duplicate or different identity is a
conflict. Commit or resume the exact pending A7 work; do not create another branch, row, meta-plan,
or goal.

Then apply **A7** with:

- **Local mode:** when `SUPER_GIT_MODE=none`, reopen and verify the meta-plan, updated `prd.md`, and
  returned goal/root paths under inherited workspace ownership. Do not run git/GitHub operations.

- **branch prefix:** `project/<project-slug>-r<N>-meta`
- **commit subject:** `docs(project): <project-slug> round <N> meta-plan`
- **PR title:** `docs(project): <project-slug> r<N> meta-plan`
- **PR body:** `Meta-plan for round <N> written by supermeta; goal folder <goal-folder>.`
- **explicit `git add`:** the meta-plan file (`meta-plans/<STAMP>-r<N>.md`) and `prd.md`. Never
  `git add -A`. (supergoal has already committed the goal folder itself under its own A7; the
  explicit list keeps that commit and this one disjoint.)
- **External vault:** A7's target is the vault repo — a direct commit, no PR (see A7 **Target
  repo**); its precondition applies (STOP and report if `<vault_root>` is not its own repository).

After A7, operation mode reconciles again and separately verifies the exact meta-plan and one ledger
row on `main` alongside the reconciled goal plan. Dirty bytes, an unmerged commit, missing or
duplicate output, or an identity mismatch produces a non-integrated JSON result and no phase
completion.

### 8. Final Report (A8)

```
## Supermeta complete

**Project:** <project-dir>   **Round:** <N>
**Meta-plan:** <path>
**Goal folder:** <path>   **Root plan:** <path to master-plans/…>
**PR:** <url> (merged)
**Commit:** <short-sha> in <vault_root>   (external vault — print this line INSTEAD of the PR line)
**Persistence:** local files verified (SUPER_GIT_MODE=none)   (local mode instead)
**Repair guidance:** none — first round | <diagnosis path> | author-approved planning (<decision id>)
**Next:** superagent:superagent-external <root plan>   (then superagent:supereval <project-dir> when the loop is DONE)
```

After printing the report, take no further action and ask no follow-up question.

In operation mode only, print the compact operation-result JSON as the final line after the report.
