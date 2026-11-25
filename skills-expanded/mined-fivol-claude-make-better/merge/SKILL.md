---
name: merge
description: Land a finished task branch in its base branch — sync the base into the branch and resolve conflicts there, run the final review on the integrated code, wait for green CI, merge, then tear the workspace down (servers, worktree, branches, ports, proxy). Use ONLY on an explicit user go-ahead ("done", "merge it", "финиш", "мержим") — never infer it from work looking finished. Runs standalone on any branch with an open PR, and is the last phase of the `workspace` skill.
---

# Merge — integrate the task branch, then clean up

Runs **only** on an explicit user go-ahead ("done", "finish", "merge it", or the
equivalent in the user's language). Confirm once before merging. In workspace
context read `<worktrees>/<task>/.feature.json` for the repos, base branches,
ports, PIDs and PR links, and do every step for **all** involved repos;
standalone, the current repo and its branch's PR are the whole job (steps 7–9
are then no-ops).

**Strategy** — read it from the config, don't assume:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/config.py" --root "$ROOT"   # → .merge
```

| `merge.strategy` | `merge.via` | What happens |
|---|---|---|
| `merge` (default) | `local-push` | Merge the task branch into `BASE` locally and push. The task SHAs land in `BASE`, so the host marks the PR **Merged** by itself and your local base is already up to date. |
| `merge` | `gh` | Same commit shape, but the host performs it (`gh pr merge --merge`); pull `BASE` afterwards. |
| `squash` / `rebase` | `gh` (forced) | The host rewrites the SHAs (`gh pr merge --squash\|--rebase`). Required by repos with a squash-only policy. Steps 5–6 below are replaced by that single call, and the local base is refreshed with `git pull --ff-only`. |

Whatever the strategy, **step 2 is not optional**: the integration happens on the
task branch, in its worktree, so the PR shows exactly what will land and CI runs
on it. `merge.wait_ci: false` skips step 3; `merge.cleanup: false` stops after
step 6.

Per repo: `WT="$ROOT/<worktrees>/<task>/<repo>"`, `BRANCH` = the task branch,
`BASE` = `.feature.json` `.repos.<repo>.base` (the repo's `base_branch`).
`ROOT` = the workspace root — anchor it via the `.claude/feature/config.json`
marker, never `$(pwd)`. `SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"`.

## 1. Make sure the task branch is fully committed

```bash
git -C "$WT" status --porcelain   # must be empty
```

## 2. Sync the latest base into the task branch — resolve conflicts HERE (in the worktree)

This is where conflicts are handled: on the **task branch**, in its worktree, so the PR shows exactly
what will land and CI runs on it. Skip the merge if the task already contains the latest base.

```bash
git -C "$WT" fetch origin "$BASE"
if git -C "$WT" merge-base --is-ancestor "origin/$BASE" HEAD; then
  echo "task already up to date with $BASE — nothing to sync"
else
  git -C "$WT" merge --no-ff "origin/$BASE" -m "Merge $BASE into $BRANCH"
fi
git -C "$WT" push                 # updates the PR; its head SHA is what we'll merge
```

On conflict git stops with a non-zero exit. Resolve the conflicted files **in `$WT`** (the task
worktree), then `git -C "$WT" add -A && git -C "$WT" commit --no-edit` and push. If you can't resolve
confidently, **ask the user** before committing — never guess a conflict resolution.

## 2b. Final review — the whole branch, now that the base is in it

The skill skips itself when `code_review.passes.final.run` is `false` — you always invoke it. This
runs **here** and nowhere else, and the position is the whole point:

- the task branch now contains the **integrated** code — your feature plus the latest base — so this
  is the first and only moment anything can review what will actually land;
- **conflict resolutions from step 2 are hand-written code that no one has reviewed.** They are
  written under pressure, in the least familiar part of the diff, and they are a classic source of
  silently dropped changes — a resolution that keeps "ours" and quietly discards a fix the base
  branch added. Per-pass reviews never saw them, because they didn't exist yet;
- fixes still land **in the PR**, before CI runs on it (step 3). After step 6 the merge is done and
  any fix needs a new PR — which is why this is not a post-merge step.

It also closes the gap the per-pass gate structurally cannot: pass 5 breaking an assumption pass 1
relied on. Each pass reviewed only its own diff; this one reviews the sum.

**This is the deep pass.** The per-pass runs are cheap (`medium` by default) precisely because
this one re-reviews all of that code at `code_review.level` (`max`), on the integrated branch, before
anything merges. Never trade this pass away to save a run — cutting it is what makes the cheap
per-pass runs unsafe.

```
/feature:review --pass final --root "$ROOT" --repos "<all involved repos>"
```

No flag for the PR comment: on the `final` pass the skill reads `passes.final.comment` itself and
posts one summary comment per PR (through `pr_feedback.py`, so it carries the agent marker and never
comes back as feedback). Pass `--no-comment` only to suppress it for this one run.

Then:

- **Anything fixed** → commit and push it on the task branch (`git -C "$WT" add -A && git -C "$WT"
  commit -m "review: <what>" && git -C "$WT" push`), so CI in step 3 validates the fixed code.
- **`Needs you` items** → these block the merge. Ask the user as numbered questions and wait. Do not
  merge past a finding the reviewer found and couldn't decide alone.
- **P0 that was fixed** → say so explicitly when you report (step 10); the user is about to merge and
  deserves to know something real was caught at the gate.

Describe the scope in prose if you like — the skill resolves repos on its own — but pass
`--pass final`: it selects both the branch scope and the deep level, and it is the difference between
reviewing the whole branch and reviewing the handful of lines that aren't pushed yet.

## 3. Wait for the PR's CI to go green

The whole reason we sync in the worktree is so CI validates the *integrated* code before it reaches the
base. Don't integrate on red.

```bash
PR=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['repos']['<repo>']['pr'] or '')" "$ROOT/<worktrees>/<task>/.feature.json")
[ -n "$PR" ] && gh pr checks "$PR" --watch   # wait for green; no-op/skip if the repo has no required checks
```

If checks fail, fix on the task branch (back to step 2) — do **not** proceed to integration.

## 4. Prepare the main checkout (the integration point for BASE)

`$ROOT/<repo>` is where `BASE` lives. It MUST be on `BASE` and clean — otherwise STOP and tell the
user (don't auto-stash someone else's work).

```bash
test "$(git -C "$ROOT/<repo>" rev-parse --abbrev-ref HEAD)" = "$BASE"   # else STOP
test -z "$(git -C "$ROOT/<repo>" status --porcelain)"                   # else STOP
git -C "$ROOT/<repo>" pull --ff-only origin "$BASE"                     # latest base
```

## 5. Merge the task branch into BASE — now conflict-free

Because the task branch already contains the latest `BASE` (step 2), this merge carries no conflicts.

```bash
git -C "$ROOT/<repo>" merge --no-ff "$BRANCH" -m "Merge $BRANCH into $BASE"
```

If git *does* report a conflict here, `BASE` moved again between step 2 and now — go back to **step 2**
(re-sync the task branch, push, wait for CI), then retry. Never guess a resolution on the `BASE` side.

**`via: gh` or a rewriting strategy** replaces steps 4–6 with one call, then a refresh:

```bash
( cd "$WT" && gh pr merge "$PR" --merge|--squash|--rebase )   # per merge.strategy
git -C "$ROOT/<repo>" checkout "$BASE" && git -C "$ROOT/<repo>" pull --ff-only origin "$BASE"
```

Skip to step 7 afterwards — the PR is already Merged and the local base is current.

## 6. Push — this *is* the PR merge

```bash
git -C "$ROOT/<repo>" push origin "$BASE"
```

Verify the PR flipped (the worktree/branch still exists at this point):

```bash
[ -n "$PR" ] && gh pr view "$PR" --json state -q .state   # expect: MERGED
```

If it still shows OPEN, the host didn't see the head SHA in `BASE` — confirm step 2 pushed and the
worktree HEAD == the PR head before continuing.

## 7. Stop the dev servers

**Full mode only** (`mode: lite` ⇒ no servers were started). Servers were started detached via `serve.py`, so `dev_pid` is also the
process-group id — kill the whole group to catch worker children:

```bash
kill -- -<dev_pid>                                       # from .feature.json, per repo (negative = the group)
kill -0 <dev_pid> 2>/dev/null && kill -9 -- -<dev_pid>   # SIGKILL any straggler
```

## 8. Remove the worktree and delete the branches

```bash
git -C "$ROOT/<repo>" worktree remove --force "$WT"
git -C "$ROOT/<repo>" branch -d "$BRANCH"            # -d is safe (already merged); use -D only if it refuses
git -C "$ROOT/<repo>" push origin --delete "$BRANCH" # tolerate "remote ref does not exist"
git -C "$ROOT/<repo>" worktree prune
```

## 9. Free the ports, proxy, and workspace folder

```bash
python3 "$SCRIPTS/ports.py" --root "$ROOT" free <task>            # full mode only; no-op otherwise
python3 "$SCRIPTS/caddyfile.py" --root "$ROOT" --reload           # drop the task's hosts
rm -rf "$ROOT/<worktrees>/<task>"   # leftover .feature.json / empty repo dirs
```

## 10. Report

Tell the user (in their language): that the **final review** ran on the integrated branch and what it
caught (`final review: ✓ max — fixed 3 (P0 1) · skipped 1`, plus one line per P0 — and say it was
posted to the PR when the review reported doing so); which PR(s) are now **Merged** (with links); that the
local base was updated & pushed; that worktrees/branches/ports/proxy were cleaned up; and any
follow-up (deploy, QA, related tickets).

## 11. Reflect — propose new `considerations` / `instructions` from this session

After reporting, look back over **this session's own history** (what was built, what got reworked,
what review feedback / bugs / "oh, also fix X" came up mid-task) and compare it against the current
`considerations` list in `.claude/feature/config.json`. The goal is a self-improving checklist: a
class of issue that bit *this* task — and isn't yet covered — is exactly what should be caught
automatically next time.

- If you spot a **recurring, cross-cutting** dimension that's missing (e.g. the user kept asking
  "what about mobile?", a bug turned out to be RTL-only, an empty/error state was forgotten, a
  migration was nearly missed) → propose adding it. Show the concrete entry you'd append
  (`name`, `when`, `check`, optional `repos`) and *why this session suggests it*.
- If instead the session surfaced a **standing rule** — something the user corrected you on that has
  one right answer every time ("always use the shared `Dropdown`", "never edit generated migrations")
  → propose it for `instructions` rather than `considerations`. The split: a *check* you re-verify per
  change is a consideration; a *rule* you simply follow is an instruction. Per-repo rules go to that
  repo's `repos[].instructions`.
- Be conservative: propose only genuinely **reusable** entries, not one-off task details. One or
  two strong candidates beat a long speculative list. If nothing qualifies, say so and add nothing.
- **Only on the user's approval**, append the approved entries to the matching array in
  `.claude/feature/config.json` (read it, add, write it back — don't touch anything else). From the
  next feature on, the `ship` skill picks them up automatically: considerations are validated in
  its step 1b, instructions are loaded in its step 0.

This step never blocks the merge — the merge/cleanup above is already complete. It's a quick "should we
teach the checklist something?" at the very end.
