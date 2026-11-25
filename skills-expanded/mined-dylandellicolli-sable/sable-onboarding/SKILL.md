---
name: sable-onboarding
description: |
  Take an arbitrary target repo from unknown to a fully-wired SABLE install: a
  read-only scan (bin/sable-onboard), then a gated, individually-consented apply
  of each missing prerequisite — the install, the beads workspace, the .sable
  contract, CI — and a final proof run that SABLE actually executes end to end.
  Every apply is a named delegation and is re-verified before moving on;
  onboarding itself authors only the .sable lines and the generated CI workflow.
  Use when asked to "/sable-onboarding", "onboard this repo", "set up SABLE
  here", or "scan this repo for SABLE prerequisites".
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - AskUserQuestion
  - Skill
---

# /sable-onboarding — scan a repo, gate-apply setup, prove SABLE runs

You are onboarding an **arbitrary target repo** onto SABLE. The read-only
scanner (`bin/sable-onboard`) already tells the truth about the current state
for every prerequisite; your job is the *conversation* and the *gated apply* it
never performs. You walk the operator through a fixed, binding sequence, closing
one gap at a time — each with explicit consent, an abort path, and a re-verify —
until `sable-doctor --project` is green and a proof run confirms SABLE actually
executes here.

> **Read this repo's scanner as the source of truth.** Run
> `bin/sable-onboard --json` (or `--check <id>` for one check) and let its
> findings, tiers, and named remedies drive the report. Do not re-derive the
> checks yourself — the scanner's `CHECKS` registry is the single enumeration.

## Two invariants — do not violate them

> **1. Onboarding authors ONLY two artifacts.** The only files this skill is
> allowed to write itself are the **`.sable` contract lines** (via the
> `bin/sable_stack_detect.py` writer) and the **generated ci-verify workflow**
> (via `bin/sable_ci_template.py`). Every other mutation is a **named
> delegation** — `install.sh --project`, `bd init`, `sable-doctor --project`.
> If you are about to hand-edit `CLAUDE.md`, `.claude/settings.json`, hook
> files, or the beads workspace, STOP: that is a delegate's job, not yours.

> **2. Each apply is consented, abortable, and re-verified.** No step runs
> without the operator's explicit go-ahead for *that* step; the operator may
> abort at any gate and the repo is left exactly as the last completed step
> left it; and after every apply you re-run `sable-onboard --check <id>` for the
> check that step was meant to close and confirm it flipped to `ok` before
> advancing. A step whose re-verify does not go green is reported, not papered
> over.

The binding order is below. **Do not reorder it** — step 0 (git state + the S6
branch confirmation) runs FIRST, before any binary report and before any apply.

---

## 0. Git state FIRST, then the S6 launch-branch confirmation

Run the scanner's git-state probes before anything else:

```bash
bin/sable-onboard --json   # read git_state{} + the checks[] findings
```

**0a — Hard git-state stops (before ANY apply).** If `git_state` reports any of
the three blocking states, surface its named remedy verbatim and **stop** — do
not report binaries, do not apply anything:

- **Detached HEAD** →
  `Detached HEAD — check out a branch (e.g. `git switch -c work`) before onboarding; 'HEAD' is not a branch name.`
- **Unborn branch** →
  `Unborn branch (no commits yet) — make an initial commit before onboarding.`
- **No git remote** →
  `No git remote — add one (git remote add origin <url>) before onboarding; workers self-push and the merge gate need a push target.`

If `git_state.asks` is true (more than one remote), ask which remote is
canonical before proceeding — the default-branch and CI decisions key off it.

**0b — S6 launch-branch confirmation.** Only once git state is clean, settle the
branch of record. Use the scanner's default-branch verdict (`git_state`
`on_default_branch`, resolved from `origin/HEAD`, never `init.defaultBranch`):

- **On the default branch** — do NOT silently onboard here. **RECOMMEND creating
  a working branch**, propose a concrete name (e.g. `sable-onboarding`), and
  **offer to create it** with `AskUserQuestion`. Proceed on the default branch
  ONLY after explicit, informed confirmation that the operator wants to onboard
  directly on it.
- **On a non-default branch** — a single confirm line: "Onboard on `<branch>`?
  (y/n)".

Record the **confirmed branch of record**. It is later written as the `.sable`
`integrationBranch=` line (step 4, via the `sable_stack_detect.py` writer) and
seeds the CI template's `{{INTEGRATION_BRANCH}}` substitution (step 5). Every
exit report ends by naming this branch.

## 1. Binaries — report only

Report the scanner's binary checks. `required-hard` misses (`bin:bd`,
`bin:git`, `bin:python3`, `bin:claude`) block onboarding — name the remedy and
stop. `ci-required` (`bin:gh`) gates step 5 only. `fleet-optional` (`bin:tmux`,
`bin:dolt`) are advisory: the solo onboarding loop needs neither, so a miss is
reported with its remedy and never fails the run. This step writes nothing.

## 2. Install — delegate to `install.sh --project`

Close the `install-scope`, `claude-md-prime-block`, and `settings-wiring`
checks by delegating to the installer at **project scope**:

```bash
install.sh --project
```

This is a named delegation (invariant 1) — onboarding does not hand-place hooks,
the CLAUDE.md Prime Directive block, or the committed `.claude/settings.json`.
Consent first, then run it, then **re-verify**:

```bash
sable-onboard --check install-scope
sable-onboard --check settings-wiring
sable-onboard --check claude-md-prime-block
```

Advance only when all three read `ok`.

## 3. Beads workspace — delegate to `bd init`

Close the `beads-workspace` check by delegating to beads:

```bash
bd init
```

Consent, run, then re-verify:

```bash
sable-onboard --check beads-workspace
```

## 4. `.sable` testCommand — propose → confirm → execute-once → write

This is the first artifact onboarding authors itself. **Never write a
`testCommand=` line on faith** — the `sable_stack_detect.py` writer refuses
(`WriteRefused`) any test command whose execute-once run did not pass.

1. **Surface candidates.** `sable_stack_detect.detect_stack(repo)` returns every
   lockfile/`packageManager`-keyed candidate (e.g. `pnpm test`, `pytest`,
   `go test ./...`). Present them; an empty detection is the explicit `none`
   signal — ask the operator for the command outright.
2. **Confirm/edit.** The adopter confirms one candidate or edits it. This is
   their decision, never a silent default.
3. **Execute once.** Run it exactly once via `sable_stack_detect.execute_once`
   (mirrors the pre-push TEST phase — `timeout … sh -c "$CMD" 2>&1`) and **show
   the exit code**.
4. **Only then write.** On a passing run, call the `sable_stack_detect.py`
   `write()` with the confirmed `testCommand` AND the step-0 confirmed
   `integrationBranch`. On a non-zero exit, report it and loop back to step 2 —
   do not write.

Re-verify the contract shape:

```bash
sable-onboard --check sable-contract
```

## 5. CI — generate via `sable_ci_template` (GitHub-or-none)

The second artifact onboarding authors. Use the scanner's `ci-verify` verdict
(`sable_ci_template.detect_provider`), which has exactly four outcomes:

- **`existing-ci-verify`** — a workflow is already present. **Never overwrite
  it.** Report present and skip.
- **`github-remote`** — apply: render with `sable_ci_template.render_workflow`
  (feeding the step-0 `integrationBranch` into `{{INTEGRATION_BRANCH}}` and the
  step-4 confirmed command into `{{TEST_COMMAND}}`) and write it to
  `.github/workflows/ci-verify.yml`.
- **`non-github-ci`** — **report-only**: name the detected system and point at
  `templates/ci-verify-project.yml` for a manual equivalent. Do not apply.
- **`no-ci`** — **report-only**: no GitHub remote, nothing to apply.

Apply only for `github-remote`. Consent, generate, then re-verify:

```bash
sable-onboard --check ci-verify
```

## 6. Doctor green — delegate to `sable-doctor --project`

Confirm the whole install is coherent by delegating the verdict to the doctor
(the same delegate the scanner's `install-scope` check runs):

```bash
sable-doctor --project
```

A clean exit means the project's own `.claude` install matches repo HEAD with no
drift. Any problem is reported with the doctor's own tail line — do not attempt
to fix it by hand (invariant 1); re-run the relevant apply step instead.

## 7. Proof run — offered, default **yes**, operator-locked

Prove SABLE actually executes here. This step is **offered-default-yes**: you
propose it and the default answer is **yes**, but it is **skippable** and is
**never run unconsented**. It is operator-locked — only the human confirms it.

Propose a **quick-tier `/sable-plan`** sample run: create ONE throwaway sample
bead, then close it, exercising the beads + hooks path end to end. On consent,
run it and report the created/closed bead id. If the operator declines, skip it
and say so in the exit report.

```bash
# offered-default-yes; skippable; operator-locked — proof that the loop closes
# a quick-tier /sable-plan run: create one sample bead, then bd close it.
```

## Exit report

Close with a plain-language summary stating:

- **Exactly what changed** — each applied step and the artifact it produced.
- **What remains manual** — every `report-only`/`optional-missing` outcome the
  operator must handle themselves (non-GitHub CI, absent fleet tools, a declined
  proof run).
- **The confirmed branch of record** — the step-0/S6 branch, named explicitly.
