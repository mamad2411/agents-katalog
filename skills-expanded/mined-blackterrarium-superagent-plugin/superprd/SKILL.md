---
name: superprd
description: Use at the end of an interactive planning conversation to turn it into a coding-loop project folder — grades whether the session holds enough context (objective, measurable success criteria, knowledge-base sources, runnable evaluation checks, constraints, decisions), asks for each gap one question at a time, drafts prd.md / knowledge-base.md / evaluation.md, has a zero-context reviewer confirm they are self-sufficient, then writes the folder and merges it via PR after you confirm. `--check` only prints the readiness report.
argument-hint: "[--check] [<project-dir>]"
license: MIT
related skills: superauthor, supergoal, supermeta, supercoverage
---

# Superprd

The **input-assistance** skill of the coding loop. A planning conversation ends with its
decisions, sources, and success criteria scattered through the chat; the loop's meta-planner
(`supermeta`, Stage 2) gets none of that unless it is written down in a **project folder**.
superprd is the gate between the two: it grades the conversation against a readiness rubric,
fills the gaps with you, and only then writes the folder.

**Input:** the conversation so far (always), plus:

- `--check` — grade and print the readiness report only. Writes nothing, asks nothing.
- `<project-dir>` — an existing project folder to re-check or revise instead of creating one.

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

## What superprd is not

| Thought | Reality |
|---|---|
| "Coverage advice lets me approve new requirements myself" | NO. Propose cases and verification methods with `supercoverage`; unresolved criteria, sources, and commands go to the author. Suggestions become binding only when approved. |
| "I'll write the project folder now and ask afterwards" | NO. Draft to scratch, confirm, then write. The gate is not waived by auto-accept modes. |
| "The user said run it, I'll start planning the work" | NO. superprd produces inputs only (superauthor A1). `supermeta` / `supergoal` plan; `superrun` executes. |
| "prd-lint WARNs are fine to ignore" | They are carried into the report and the confirmation gate so the user decides. FAILs are fixed before the gate. |

## Workflow

### 1. Invoke `superagent:superauthor`

Invoke it via the Skill tool and apply **A1** (no execution), **A3** (no placeholders), **A6**
(findings capture), **A7** (commit and merge via PR), **A8** (Final Report). **A2 does not
apply** — the three files are structural docs, not plans. **A5 is overridden**: superprd pauses
for confirmation before any vault write (step 8), exactly as `supergoal` does.

### 2. Derive identifiers

- `<slug>` — concise kebab-case summary of the objective (mirror `supergoal`'s style).
- `<STAMP>` — `date -u +%Y-%m-%d-%H_%M`. `<DATE>` — `date +%Y-%m-%d` (branch name and the header block).
- Project folder — `<vault_root>/<SUPER_PROJECT_DIRNAME>/<STAMP>-<slug>/` (see **Vault root**;
  the primary checkout's vault, or the external vault). If `<project-dir>` was given, use it
  instead and treat its files as the
  starting draft. If the derived folder already exists and no `<project-dir>` was given,
  disambiguate the slug; if it is clearly the same project, report that and exit — never
  overwrite.
- Scratch — `$TMPDIR/superprd-<slug>/` (outside the vault). All drafting happens here.

### 3. Extract from the conversation

Collect, quoting the conversation where possible:

1. the **objective** — what the finished software does;
2. candidate **success criteria** and, for each, how the conversation said it would be verified;
3. **sources** — files the discussion touched or named, libraries and their docs, sample code,
   entry points, plus every `CLAUDE.md` / `AGENTS.md` / `AGENT.md` at the repo root (auto-added as
   `instructions` rows; the user may remove them);
4. **evaluation commands** — test runners, build steps, scripts the discussion called out, and
   the setup needed before they run;
5. **constraints and non-goals**;
6. **decisions** made in the conversation, each with the alternative rejected and why.

### 3a. Advise on coverage before approval

Invoke **superagent:supercoverage** on the extracted requirements. Put its draft acceptance
checklist in `evaluation.md`, with stable AC IDs and owning C/J IDs. Keep optional suggestions
and unresolved questions separate from required rows. Resolve the latter with the author
under step 5. This is where coverage is interpreted and agreed; downstream agents receive
that agreement and verify the delivered evidence.

For `--check`, inspect existing text only: report missing or ambiguous coverage as R8 gaps,
without invoking the interactive advisory workflow or creating new obligations.

### 4. Grade readiness

| Id | Rubric item | PASS when |
|---|---|---|
| R1 | Objective | One paragraph states what the finished software does, without reference to the conversation. |
| R2 | Measurable criteria | Every success criterion can be tied to a command check (`exit <n>` / `stdout ~ /regex/`) or a judged objective with yes/no criteria. |
| R3 | Coverage | Every criterion has ≥1 check id; every check id serves ≥1 criterion. |
| R4 | Knowledge base | Every source needed to plan the work is listed and resolves. |
| R5 | Evaluation runnable | The setup command and every check command name a binary on `PATH` or a repo path, each with a timeout ≤ `SUPER_EVAL_TIMEOUT_MIN`. |
| R6 | Constraints and non-goals | Stated, or explicitly "none". |
| R7 | Locked decisions | Every decision the conversation made is captured with its rejected alternative. |
| R8 | Acceptance agreement | The draft checklist accounts for explicit cases and general rules, has observable outcomes and valid owning C/J IDs, and leaves no unresolved required coverage decisions. Suggestions are separate. |

R1, R2, R6, R7, R8 are judged by you from the extraction and draft. R8 is a semantic review;
`prd-lint.sh` checks neither checklist completeness nor approval. R3, R4, R5 are mechanical: write the
current drafts to scratch (step 6's formats) and run

```
PRD_LINT_REPO_ROOT="<primary_root>" "${CLAUDE_PLUGIN_ROOT}/scripts/prd-lint.sh" "$TMPDIR/superprd-<slug>" --json
```

Always pass `PRD_LINT_REPO_ROOT` — the scratch folder (and, in external mode, the project folder) is
outside the code repo, so the linter cannot derive the repo root itself; `repo-file` / `entry-point`
locators must resolve against the code checkout.

A `FAIL` maps to a rubric item by its `<file>:<loc>` and message:

- `prd.md:SC*` (an unknown check id, or a criterion with no check ids) and any `evaluation.md:<id>` whose message says `serves no success criterion` → **R3**;
- `knowledge-base.md:*` (a row id, `header`, `table`, or `file`) → **R4**;
- every other `evaluation.md:*` (an empty command, a malformed `Pass when`, a non-numeric or excessive timeout, a judged row with empty criteria or evidence, duplicate or missing ids, `Environment`, `setup`, `config`, `file`) → **R5**;
- every other `prd.md:*` (`file`, `header`, a missing or out-of-order section, the ledger header, no success-criteria rows) → **R2** (the criteria table is not in the shape the loop reads).

Never report R1–R8 all PASS while `prd-lint.sh` exits non-zero: a FAIL matching none of the rules above is an R2 gap naming its `<file>:<loc>`. WARNs are not gaps; keep them for the report.

When the `mcp__context7__resolve-library-id` tool is available, also resolve every `context7` row live and turn a non-resolving id into an R4 gap.

Each item is `PASS` or `GAP <what is missing>`.

### 5. `--check` exit, or fill the gaps

**`--check`:** print the Readiness report (below) and **stop**. Write nothing, ask nothing.

**Otherwise:** for each `GAP`, in rubric order, ask the user **one question at a time**
(AskUserQuestion where the harness has it, plain chat otherwise), re-grade after each answer,
and continue until R1–R8 all PASS. A question names the gap and offers the concrete options the
conversation supports (e.g. "SC2 'fast enough' needs a threshold: p95 < 200 ms on the fixture,
or a judged objective?"). Never fill a gap with your own guess.

### 6. Draft the three files to scratch

All three open with the header block:

```
# <Title> — <STAMP>-<slug>
**Date:** <DATE> · **Status:** DRAFT · **Related:** [[<SUPER_PROJECT_DIRNAME>/<STAMP>-<slug>/<other-file>]]
```

**`prd.md`** — sections in this exact order:

```
## Objective
<one or more paragraphs>

## Success criteria
| Id | Criterion | Verified by (check ids) |
|---|---|---|
| SC1 | … | C1, C2 |

## Constraints and non-goals
- …

## Locked decisions
- <decision> — rejected: <alternative>, because <why>

## Iteration ledger
| Round | Meta-plan | Goal folder | Inner loop | Source | Eval report | Verdict |
|---|---|---|---|---|---|---|
```

**`knowledge-base.md`** — one table, kinds `instructions`, `repo-file`, `repo-glob`,
`sample-code`, `entry-point` (`<path>:<symbol>`), `doc-url`, `context7` (`/<org>/<project>`):

```
| Id | Kind | Locator | Read for |
|---|---|---|---|
| K1 | `instructions` | `CLAUDE.md` | repo conventions |
| K2 | `repo-file` | `src/ingest/pipeline.py` | the current entry point |
```

**`evaluation.md`**:

```
## Environment
- setup: `<command run once in the frozen evaluation workspace; may be empty>`
- cwd: `<repo-relative dir every check runs in unless its row overrides>`

## Command checks
| Id | Command | Cwd | Pass when | Timeout |
|---|---|---|---|---|
| C1 | `npm test` | `.` | `exit 0` | 20 |

## Judged objectives
| Id | Objective | Criteria | Evidence to inspect |
|---|---|---|---|
| J1 | Errors are user-readable | Every failure path returns a message naming the offending field | `src/cli/*.py` |

## Acceptance checklist
**Approval:** DRAFT — awaiting author approval of this revision.
| Id | Source | Required case or rule | Expected result | Verification and check ids |
|---|---|---|---|---|
| AC1 | prd.md SC1 | … | … | …; C1, J1 |

## Coverage suggestions and decisions
<Optional suggestions, explicitly unapproved; accepted/rejected author decisions and rationale.>
```

`Pass when` is exactly `exit <n>` or `stdout ~ /<regex>/`; `Timeout` is whole minutes. Check ids
are unique across both tables. AC IDs identify agreement rows; they are not runnable check IDs
and do not replace the PRD's C/J links. Every AC row names existing C/J checks. When acceptance
requires assertions to exist and be meaningful, include an explicit judged objective to inspect
those assertions and list its evidence paths; a suite-exit check alone cannot establish that.
Keep checklist and suggestions under separate level-two headings so command/J table parsing
is unchanged. Preserve binding contract notes and resolve conflicts before approval. A literal `|` inside a cell must be written `\|`.

Run `prd-lint.sh` on the scratch folder (with `PRD_LINT_REPO_ROOT="<primary_root>"`, as in step 4).
Fix every FAIL (returning to step 5 when the fix needs the user). Keep the WARNs.

### 7. Zero-context review

Dispatch **one** read-only `PRD_REVIEWER` subagent. Resolve `SUPER_MODEL_PRD_REVIEWER` / `SUPER_EFFORT_PRD_REVIEWER`.
<!-- cc-only:start -->
If the model is `inherit` or a bare tier name (`sonnet`, `opus`, `haiku`, `fable`) **and** the effort is `inherit`, dispatch with the plain subagent mechanism — `model: <tier>` when a tier, no `model:` when `inherit`. Otherwise — a full model ID such as the default `claude-opus-5`, a non-`inherit` effort, or a bridged harness prefix — dispatch with `subagent_type: super-prd-reviewer` and omit `model:`; that is the definition `superagent:init` generates in `.claude/agents/`, and a missing definition is a hard error: report "re-run `superagent:init`" and stop (the same rule superloop L7 applies to the panel).
<!-- cc-only:end -->
<!-- cursor-only:start
If the model is `inherit` or a bare model name **and** the effort is `inherit`, dispatch with the plain subagent mechanism — `model: <name>` when named, no `model:` when `inherit`. Otherwise dispatch with `subagent_type: super-prd-reviewer` and omit `model:`; that is the definition `superagent:init` generates in `.cursor/agents/`, and a missing definition is a hard error: report "re-run `superagent:init`" and stop.
cursor-only:end -->
<!-- codex-only:start
For a native Codex role, use `spawn_agent` with `fork_turns: "none"`, `model` (the `codex:` prefix stripped), and `reasoning_effort`, omitting each pin that is `inherit`. For a foreign harness, use the generated banner's relay dispatch with `fork_turns: "none"`; pass the foreign model/effort to `role-bridge.sh`, never to the native spawn. No definition file is involved.
codex-only:end -->
<!-- pi-only:start
The PRD reviewer gets no `.pi/agents/` definition. Run one blocking
`role-bridge.sh --tools evaluator --role prd-reviewer` process with the resolved harness/model/effort
from `SUPER_MODEL_PRD_REVIEWER` / `SUPER_EFFORT_PRD_REVIEWER`; a native role uses `--harness pi`
(and `inherit` resolves to Pi). This fresh CLI receives only the review prompt below, without
conversation history. Wait for completion and report a failed dispatch; never grade it yourself.
The required `pi-subagents` extension is used by the inner loop's task-loop roles.
pi-only:end -->
The prompt contains **only** the three scratch files
verbatim and these three questions:

1. Could a fresh planner, given these files and the sources they name and nothing else, write
   a root master plan for this objective? List every piece of missing context.
2. Could a fresh agent run `evaluation.md` unaided and reach a PASS/FAIL verdict? List every
   ambiguity in a check or a judged criterion.
3. Does the acceptance checklist retain each explicitly required case and general rule, with
   distinguishing expected results and valid owning check IDs? Identify omissions, conflicts,
   and suggestions accidentally promoted to requirements. Do not add acceptance conditions.

The reviewer returns a findings list. Fix what the conversation already answers; ask the user
about the rest (step 5 rules); re-dispatch at most **twice**. Findings still open after that
go into the report as WARNs. A finding that leaves R8 (or another readiness item) unmet remains
a GAP and must be resolved before READY; the retry limit cannot waive required decisions.

### 8. Confirmation gate (REQUIRED — overrides A5)

Nothing has been written to the vault. Present:

- the project folder path that **will** be created;
- the objective in one line;
- the success-criteria table and complete draft acceptance checklist;
- optional coverage suggestions and the author's decisions, clearly distinguished;
- the check ids (command and judged) and the knowledge-base ids with kinds;
- every WARN from `prd-lint.sh` and every open reviewer finding.

Ask: *"Write this project folder to the vault and open the PR?"* and **wait**.
Approved → step 9. Changes requested → revise the scratch drafts, re-run steps 6–7 as needed,
re-present. Declined → write nothing, report the scratch path, exit. This pause is mandatory
and is **not** waived by auto-accept / `bypassPermissions` mode.

### 9. Write-out and PR (superauthor A7)

Record `**Approval:** Approved by the author on <date>; applies to this checklist and its
source requirements at this project revision.` Replace the date with the actual approval date,
and retain the approval reference in Locked decisions. Do not infer approval from lint/reviewer
success. For an already approved identical revision, carry its existing approval forward.

Create the project folder; write the three files with `**Status:** READY`; create
`meta-plans/`, `eval-reports/`, `diagnoses/` each with a `.gitkeep`. Then A7 with:

- **Local mode:** when `SUPER_GIT_MODE=none`, reopen and verify these six explicit artifacts under
  inherited workspace ownership, report their physical paths, and skip every branch/commit/PR step.

- **branch prefix:** `project/<slug>` → branch `project/<slug>-<DATE>`
- **commit subject:** `docs(project): <slug> — superprd output`
- **PR title:** `docs(project): <slug>`
- **PR body:** `Coding-loop project folder (prd, knowledge base, evaluation) generated by superprd.`
- **explicit `git add` list:** the three files and the three `.gitkeep`s. **Never `git add -A`.**
- **External vault:** A7's target is the vault repo — the six paths relative to `<vault_root>`,
  committed directly there; no branch, no PR (see A7 **Target repo**). A7's **precondition**
  applies: if `<vault_root>` is not its own repository, STOP and report — never improvise a
  `git init`.

### 10. Final Report (superauthor A8)

```
## Superprd complete

**Project folder:** <full path>
**PRD:** <path>   **Knowledge base:** <path>   **Evaluation:** <path>
**PR:** <url> (merged)
**Commit:** <short-sha> in <vault_root>   (external vault — print this line INSTEAD of the PR line, verbatim form)
**Persistence:** local files verified (SUPER_GIT_MODE=none)   (local mode instead)
**Readiness:** R1–R8 all PASS
**Warnings:** <prd-lint WARNs and open reviewer findings, or none>
**Next:** superagent:supermeta <project-dir>   (Stage 2 of the coding loop)
```

After printing the report, take no further action and ask no follow-up question.

## Readiness report (`--check`; also embedded in the gate)

```
## PRD readiness — <slug>
| Item | Result | Gap |
|---|---|---|
| R1 Objective | PASS | |
| R2 Measurable criteria | GAP | "fast enough" has no threshold |
| R3 Coverage | PASS | |
| R4 Knowledge base | GAP | context7 id /acme/sdk does not resolve |
| R5 Evaluation runnable | PASS | |
| R6 Constraints and non-goals | PASS | |
| R7 Locked decisions | GAP | the ORM choice was discussed but not settled |
| R8 Acceptance agreement | PASS | |
**Verdict:** NOT READY (3 gaps)
**Warnings:** <prd-lint WARNs, or none>
```
