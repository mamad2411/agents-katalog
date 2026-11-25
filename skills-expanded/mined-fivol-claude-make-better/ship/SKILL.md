---
name: ship
description: Ship the change that is in the working tree — simplify it, run the review gate that finds and fixes its bugs, commit, push, open or update the PR, and report what landed. Use when the user asks to ship / land / commit / push the current work or open a PR for it ("ship it", "commit this", "оформи PR"), and when the `workspace` skill drives a pass. Do NOT invoke it to write code: implementing is the turn's normal work, and only delivery is this skill's job. Merging is a separate skill (`merge`); answering PR comments is `pr-feedback`.
---

# Ship — land the change as a reviewed PR

> simplify → **review** → commit → push → PR → report

Everything here is about **delivery**. Writing the code is the turn's ordinary
work and needs no skill; this contract starts once the change is on disk.

The report is produced **last**, after the change is pushed and in the PR. Never
lead with it.

## Two ways this runs

Detect the mode once, at the start:

- **Workspace context** — you're inside a task worktree from the `workspace`
  skill: there is a `<worktrees>/<task>/.feature.json` for the checkout you're
  in, and the workspace root has `.claude/feature/config.json`. Use each repo's
  configured base branch, span **all** involved repos, persist the dashboard
  artifacts, hand out pretty URLs.
- **Standalone** — anything else (a plain repo/branch, invoked directly).
  Operate on the current git repo, PR into its default base branch, give
  how-to-verify instead of URLs. No worktree, no servers, no dashboard.

```bash
# ROOT = walk up from cwd to the dir holding .claude/feature/config.json; else the repo root
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" --root "$ROOT"
```

`_override_applied: true` **and** a `.feature.json` beside your checkout ⇒
workspace context. Otherwise standalone. The loader works in both — with no
config it just returns the shipped defaults.

**Guard (standalone):** never commit straight onto a base/default branch. If
`git branch --show-current` is the default branch, create a topic branch first
(`git switch -c <kebab-topic>`), then proceed. In workspace context the worktree
is already on its task branch — use it.

## Policy comes from config, not from this file

Read it once per pass; every knob below ships with a default, so an unconfigured
project behaves exactly as this file describes:

| Key | What it decides |
|---|---|
| `simplify` | `{enabled, when}` — whether step 1 runs, and after which changes |
| `code_review` | the gate in step 2: when it fires, how deep, what it may fix |
| `considerations` | the cross-cutting dimensions checked every pass (empty ⇒ step off) |
| `commit` | `{per_pass, message_language}` |
| `pr` | `{enabled, draft, title_template, body_template}` |
| `branch` | task-branch naming (`prefix` / `template`) |
| `output_language` | the language you write in |
| `report.chat_template` | the report's blocks — see step 5 |

Never restate a policy as prose here, and never enforce one the config turned
off. If a knob and the user's explicit request for this pass conflict, follow
the user and note the deviation in one line under **Considerations**.

## The contract — in order

Let `WT` = the checkout you work in: each involved repo's worktree in workspace
context, or the current repo standalone. Run the steps per involved repo.

### 0. Inputs — who loaded them depends on how you were reached
Two things must be in hand *before the code was written*, not now: the project's
standing instructions, and the reviewer's unaddressed PR comments.

- **Workspace context** — `workspace` Phase 2 already loaded both, before the
  change. **Do not repeat either**: re-reading the instructions here changes
  nothing, and a second `pr-feedback collect` re-opens items you just handled.
- **Standalone** — you were invoked on a change someone already made, so this is
  the first chance. Do both now, and treat anything the comments require as part
  of this pass:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" --root "$ROOT" \
        --instructions --repos "<the repos you touch, comma-separated>"   # omit --repos standalone
```

Then invoke the **`pr-feedback` skill** in `collect` mode (real Skill
invocation — it owns the mechanics and the traps). `pr_feedback.enabled: false`,
no PR yet, or nothing unaddressed ⇒ one line and carry on.

Either way the instructions are **constraints on the code**, never a checklist:
you obey them while simplifying, fixing review findings and committing, and you
never report them per item. Rules about how the *report* looks don't belong to
them at all — that's the report template (step 5).

### 1. Simplify — the cleanup gate
Governed by `simplify` in config. `enabled: false` / `when: never` ⇒ skip
silently and print nothing.

When it runs, invoke the `/simplify` skill (a **real** Skill invocation, not a
mention) scoped to the files changed this pass. It cleans
reuse/duplication/dead code/readability, must **not** change behavior, and its
edits are part of this commit. (Not installed ⇒ do the equivalent manual pass and
say so.)

`when: significant` — the default — skips only genuinely minor work:

| Skip (minor) | Run (significant) |
|---|---|
| one-/few-line diff in 1 file, **no new or restructured logic** | adds or changes logic / control flow |
| a constant, copy/string, type, import, config value, comment, version bump | a new function/component/hook/endpoint |
| a pure revert | a refactor, or a change spanning multiple files |

When in doubt → run it. Then declare the outcome (`simplify: ✓` /
`simplify: skipped (minor)`) — a silent skip of an enabled gate is a contract
violation.

### 1b. Considerations — validate every applicable dimension
Read `considerations` from the config; empty ⇒ **skip silently**. Each entry is a
recurring blind spot — something features get specified *without* (desktop-only,
LTR-only, Chrome-only) and that then ships broken. For each entry:

1. **Decide applicability** from its `when` and optional `repos` (only applies
   when one of those repos is touched). A backend-only diff usually makes UI
   dimensions `n/a`.
2. For every **applicable** entry, *actually verify* the change satisfies its
   `check` — inspect the diff/layout, don't hand-wave. Full mode: open the pretty
   URL (mobile viewport, switch locale/RTL) to confirm; lite/standalone: reason
   from the diff.

Declare a per-entry outcome, one token each: `✓` verified · `n/a` not applicable
(one-word reason if non-obvious) · `⚠` applicable but unverified (carry it into
**Considerations**). Writing `✓` without checking is a contract violation.

### 2. Review — MANDATORY, and the last thing before the commit
`/simplify` improves code you wrote and whose intent you know. This is the
opposite on purpose: an adversarial pass over the same diff whose finders
**never saw this conversation** and therefore cannot excuse anything. It hunts
correctness bugs first, then reuse/simplification/efficiency/altitude/
conventions, verifies each candidate before believing it, and **fixes what it
finds**.

Invoke the `review` skill (a **real** Skill invocation), after simplify and after
every code change of this pass is on disk:

```
/feature:review --pass <first|later> --root "$ROOT" --repos "<the repos you touched>"
```

**`--pass first` when this pass is opening the PR, `--pass later` on every one
after it.** The `.feature.json` entry tells you which: no `pr` recorded yet ⇒
`first`. The two are separately configurable, so getting the flag wrong silently
applies the wrong policy — read the state rather than guessing.

**Wait for it.** It is a gate and runs inline for exactly that reason: you do not
commit, push, answer the user or end your turn while it is still running. If your
turn is about to end and the review has not reported, the review has not run.

It covers everything not yet in the PR — uncommitted work, commits made this pass
but not pushed, new untracked files — across **all** repos you touched, so run it
**once** for the whole pass, not once per repo. It never commits; its edits join
this pass's commit.

**Do not pass `--level`, and do not decide for yourself whether to run it.** The
skill reads `code_review.passes.<pass>` and applies that project's policy,
including switching itself off and saying so. Not installed ⇒ say so in one line
and carry on; never fake it.

**This covers the whole pass's work, not just the chat prompt** — including code
written to satisfy a PR comment picked up in step 0.5. Those changes are written
under argument pressure and are exactly the ones that skip a step.

Take three things from its report (never paste the report into chat):

1. the status line — `review: ✓ max — fixed 4 (P0 1) · skipped 1`;
2. the **Needs you** items — the one part the user must see, as numbered
   questions in the report;
3. whether any fix touched a surface a `considerations` entry covers — if so,
   re-verify that entry before writing its `✓`.

### 3. Commit + push — explicit git, per repo
`commit.per_pass: false` ⇒ leave the work uncommitted and say so; otherwise every
pass commits, minor edits included. Stage only the files you changed; spell git
out rather than delegating to a commit utility. Message: short, imperative,
why-focused, in `commit.message_language`.

```bash
git -C "$WT" add <file> [<file> ...]
git -C "$WT" commit -m "<short imperative, why-focused>"
git -C "$WT" push -u origin "<branch>"    # first push of the branch
git -C "$WT" push                          # later passes
```

### 4. Ensure the PR exists
`pr.enabled: false` ⇒ stop after the push and report the branch. Otherwise the
branch must be pushed first; on the **first** pass create one PR per involved
repo (`gh` infers the repo from the remote) against its base branch — configured
`base_branch` in workspace context, the repo's default base standalone.

```bash
( cd "$WT" && gh pr create --base <base> --title "<title>" --body "<what + why + how to test>" )
( cd "$WT" && gh pr view --json url -q .url )
```

Add `--draft` when `pr.draft` is true. `pr.title_template` / `pr.body_template`
override the wording (placeholders: `{task}`, `{repo}`, `{base}`, `{branch}`).
Later passes need nothing — the push already updated the open PR.

### 4b. Answer on the PR
Only **after** the push, so a reply can cite the commit that settles it. Invoke
the **`pr-feedback` skill** in `answer` mode, with the verdict and the fixing sha
per item. Nothing was picked up for this pass (here or in `workspace` Phase 2) ⇒
skip.

### 5. Report — now, and only now
Load the template at the moment you write the report, not earlier:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" --root "$ROOT" --report            # chat
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" --root "$ROOT" --report --kind summary
```

It resolves, in order: `report.chat_template` from the config ▸
`<root>/.claude/feature/report.md` ▸ the template shipped with this skill.
**Follow the resolved template** — its blocks, its order, its status lines. It is
the project's, not yours, so don't add or drop blocks to taste.

In workspace context also write the dashboard artifacts (`--kind summary`):
overwrite `<worktrees>/<task>/summary.md` with the task's current cumulative
state, then stamp the session so the dashboard's "continue chat" is exact:

```bash
python3 - "$ROOT/<worktrees>/<task>/.feature.json" "$CLAUDE_CODE_SESSION_ID" <<'PY'
import json, sys
p, sid = sys.argv[1], sys.argv[2]
d = json.load(open(p))
if sid:
    d["session_id"] = sid
json.dump(d, open(p, "w"), indent=2)
open(p, "a").write("\n")
PY
```

Also store each repo's PR url into `.feature.json` `.repos.<repo>.pr` on first
creation. Standalone ⇒ skip this step entirely.

The next user prompt starts a new pass.

## Red flags — STOP, you're about to break the contract
- Invoking this skill to *write* code → no. It starts once the change is on disk;
  the constraints and the reviewer's comments that shape that code are loaded
  before it, by whoever owns the writing phase.
- Re-loading the instructions or re-running `pr-feedback collect` in workspace
  context → no. Phase 2 did it before the code was written, which is the only
  moment either is worth anything.
- Committing without the review gate (step 2) → no. Impartial review before the
  commit is the whole point; after the push it reviews an empty diff.
- Ending the turn while the review is still running → no. Then it didn't run.
- Excluding PR-comment work from the review because "it was only a comment" → no.
  Same pass, same diff, same gate.
- Dropping a **Needs you** item → no. It's a found defect nobody decided on.
- Pasting the whole review report into chat → no. Status line + `Needs you` only.
- Reviewing your own change inline instead of invoking the skill → no. The gate's
  value is that the reviewer never saw this conversation.
- Writing `mobile ✓` without actually checking → no.
- Answering a PR thread before the push → no. The reply cites the commit.
- Writing the report before pushing → no. Push first, report last.
- Committing onto a base/default branch → no. Branch off first.
- Improvising the report's blocks instead of loading the template → no. That's
  the project's format, and it's a file.
- Enforcing a gate the config turned off, or "helpfully" skipping one it turned
  on → no. Policy is config; this file only sequences it.
