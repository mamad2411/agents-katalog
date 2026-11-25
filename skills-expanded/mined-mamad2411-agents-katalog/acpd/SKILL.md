---
name: acpd
description: Archive an implemented issue, stage remaining tracked changes, commit code+archive together, push, and deploy to dev. Use when the user says "/acpd", "acpd #", or asks to archive+commit+push+deploy an issue (typically right after /tdd2 leaves changes staged).
---

# acpd — archive, add -u, commit, push, deploy

Merges a `/tdd2`-staged issue into `main` and deploys it to dev, in one
commit. Companion skill: `/tdd2` (implements, stops at `git add`).
Combined skill that chains both, per issue, fully automatically:
`/autotdd`.

**Precondition**: code changes for the issue are already staged
(`git add`, not yet committed) — that's where `/tdd2` stops. This
skill does the rest.

## A naming note before anything else

This skill's own script is called `deploy.sh` (`.ps1`/`.bat` too), and
that script's own step 7 calls a **different** `deploy.sh` — the
*target repo's* per-environment deploy entry point, which step 3
generates if the repo doesn't already have one. They live in different
places:

| | Path | What it is |
|---|---|---|
| This skill's script | `.claude/skills/acpd/deploy.{sh,ps1,bat}` | What you invoke to run the whole archive→commit→push→deploy pipeline |
| Target repo's script | `<target-repo>/deploy.{sh,ps1,bat}` | The project's own `--env <env>` deploy hook, called by the skill's script at the very end |

Everywhere below, "this script" / "the acpd script" means the former.

## Run it

### Explicit issue number — no prompts

```bash
bash .claude/skills/acpd/deploy.sh <issue-number> <commit-summary...>
```

```bash
bash .claude/skills/acpd/deploy.sh 42 "KP115 전력 캐시 만료 버그 수정"
```

On a Windows host without bash/WSL, use `deploy.ps1` (native
PowerShell port) or `deploy.bat` (thin dispatcher to `deploy.ps1`) —
same arguments, same behavior. `deploy.sh` is the canonical,
most-exercised implementation; the other two mirror it. See Gotchas.

### No issue number — find what's pending, then ask

When the user says `/acpd` with no number:

1. Run `bash .claude/skills/acpd/deploy.sh --pending` to list issue
   numbers whose `## 구현 결과` is already filled in (i.e. `/tdd2`
   finished them) but haven't been archived/deployed yet.
2. If empty: report there's nothing pending. Stop.
3. If one or more numbers: show them, ask the user to confirm
   deploying (compose the commit summary yourself from the issue's
   title / `구현 결과` content), then run the explicit-number form
   above for each confirmed issue.

## What the script does

Run from anywhere inside the target repo — it resolves the repo root
itself.

0. **Python-project verification gate**, only if `pyproject.toml`
   exists at the repo root: runs `run-ruff`, `run-pyright`,
   `run-unit-tests`, `run-regression-tests`, `run-pyright-full`, in
   that order (see "The five checks" below). Any failure aborts here —
   before any git mutation.
1. Stages `issues/issue-<#>.md` (its own edits, e.g. the `## 구현 결과` section).
2. Archives it: `git mv` to `issues/archive/YYYY/MM/DD/issue-<#>.md`.
3. For each of the **target repo's** `deploy.sh`, `deploy.bat`,
   `deploy.ps1`: if missing, generates a placeholder/dispatcher (see
   Gotchas) and stages it. Only the same-platform one is actually
   invoked by this script at step 7 (`deploy.sh` invokes the target's
   `deploy.sh`, `deploy.ps1` invokes the target's `deploy.ps1`) — the
   others are scaffolded for other hosts (several of these projects
   deploy to a Windows box over ssh) but aren't run automatically.
4. `git add -u` — stages the rest of the already-tracked changes. Never touches untracked files.
5. Commits code + archiving as **one commit**, message `issue-<#>: <summary>` with the `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` trailer appended automatically — don't add it yourself.
6. `git push`.
7. Runs the target repo's own same-platform `deploy.{sh,ps1} --env dev`
   — **dev only, always**. This skill never touches qa/prod.

Fails fast (`set -e`, exit 1) with no git side effects if
`issues/issue-<#>.md` doesn't exist, or if any step-0 check fails —
check the issue number first, and don't call `acpd` on code that
hasn't already passed `/tdd2`'s own verification.

## The five checks (Python projects only)

For each of `run-ruff`, `run-pyright`, `run-unit-tests`,
`run-regression-tests`, `run-pyright-full`: if the target repo has its
own executable `./run-<name>.sh`, that runs. Otherwise this skill's
bundled default in `defaults/run-<name>.sh` runs instead — **not**
copied into the project, just invoked from the skill directory with
CWD already set to the repo root. `.bat`/`.ps1` siblings exist in
`defaults/` for a human on Windows running the equivalent by hand, and
`deploy.ps1` resolves `.ps1` project-or-default the same way — but
each of `acpd`'s own three entry scripts only ever calls its own
platform's flavor.

This is a final gate, not a substitute for `/tdd2`'s own step 5–9
verification — by the time `acpd` runs, these should already be green.
It exists so nothing broken reaches `main`/dev even if the working
tree changed after `/tdd2` finished.

`run-pyright` is scoped to `src/` (fast); `run-pyright-full` has no
path restriction (slower, whole project) — same fast/thorough split as
`run-unit-tests` vs a project's own coverage script.

Verified end-to-end (via `deploy.sh`) against a real `uv`-managed
Python project: all five defaults ran for real (ruff, pyright, and
pytest actually executed, not mocked) and the gate correctly aborted
with zero git side effects on a real pytest failure; a project with
its own `run-*.sh` overrides had every check dispatch to the project's
version instead of the default; a non-Python repo (no `pyproject.toml`)
skips step 0 entirely.

## How "pending" is detected

No separate state file. An issue counts as pending-deploy once its
`## 구현 결과` section's `**구현 완료 일시**:` line is no longer the
`(미정)` placeholder — that's the existing issue-template completion
marker, already written by `/tdd2` when it finishes. `--pending` greps
every `issues/issue-*.md` (archived ones are excluded — they live
under `issues/archive/`, a different path) for that signal.

## Gotchas

- **`deploy.ps1` and `deploy.bat` were not run in this environment —
  no PowerShell available here.** `deploy.ps1` is a careful,
  line-by-line manual port of the exercised `deploy.sh` (same steps,
  same guarantees) but hasn't been executed for real; verify it on an
  actual Windows/PowerShell host before relying on it for anything
  important. `deploy.bat` is intentionally thin — it just locates
  `pwsh` (preferred) or `powershell` on `PATH` and forwards to
  `deploy.ps1`, rather than reimplementing ~200 lines of archive/
  commit/push/gate logic a third time in raw batch. It does **not**
  pass `-ExecutionPolicy Bypass`; if your system's execution policy
  blocks local scripts, set it yourself
  (`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`) or use
  `deploy.sh` under WSL/git-bash instead.
- **The target repo's `deploy.sh`/`deploy.bat`/`deploy.ps1` are a
  per-project convention, not guaranteed to exist.** Older projects
  have `deploy-to-dev.sh` / `deploy-to-qa.sh` instead (or Windows
  equivalents). Each of the three is checked and generated
  **independently** — a repo can end up with only the ones it was
  missing; existing files (any content) are never touched. Each
  placeholder dispatches to a legacy `deploy-to-<env>.{sh,bat,ps1}`
  when one exists, or prints a `TODO` and exits 0 otherwise (so a
  project with no deploy automation yet doesn't fail the whole merge —
  it just doesn't deploy). Verified via `deploy.sh`: a repo with only
  `deploy-to-dev.sh` deploys correctly through the generated
  `deploy.sh` dispatcher; a repo with a pre-existing custom
  `deploy.bat` keeps it untouched while still generating the missing
  `deploy.sh`/`deploy.ps1`; a repo with none of the three gets stubs
  with clear TODO messages in all of them.
- **Commit message trailer is baked into the script.** Don't pass a
  message that already includes `Co-Authored-By` — you'll get it
  twice.
- **`git add -u` is deliberate, not `git add -A`.** Untracked files
  (scratch files, new files the issue didn't ask for) are never staged
  by this skill.
