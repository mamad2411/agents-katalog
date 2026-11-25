---
name: claude-automation-recommender
description: "Audits .claude/hooks, agents, skills and .github/workflows for guards that never fire, fire wrongly, or are missing; proposes, never writes silently. Use when a failure keeps recurring, after adding a hook or agent, or from the monthly mbe-monthly-meta-audit routine."
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, AskUserQuestion, TodoWrite
---

# Claude Automation Recommender

The repo's automation layer has three failure modes, and only the third is obvious:

1. **A guard that never fires.** The script is present, complete, and executable — but nothing invokes it. It reads as active protection while protecting nothing.
2. **A guard that fires wrongly.** It runs on everything, or on the wrong thing, so its signal stops carrying information and reviewers learn to ignore it.
3. **A failure with no guard.** Something keeps breaking and nothing watches for it.

Audit in that order. A dead guard is worse than a missing one, because everyone believes it is working.

**Output is a proposal, never a silent write.** Show findings, get a decision, then edit.

## Arguments

- (none) — full audit of all four surfaces.
- `--surface hooks|agents|skills|workflows` — audit one surface.
- `--apply` — after review, apply the accepted recommendations.
- `--dry-run` — report only.

## Process

### Step 0: Track the run

Use TodoWrite: reachability → correctness → coverage gaps → rank → propose → apply.

### Step 1: Reachability — guards that never fire

Every hook must be reachable from something. Check all invocation sites, not just `settings.json`:

```bash
for f in .claude/hooks/*; do
  b=$(basename "$f"); found=""
  grep -qF "$b" .claude/settings.json 2>/dev/null && found="settings.json"
  [ -z "$found" ] && found=$(grep -rlF "$b" .github/workflows/ .claude/hooks/ 2>/dev/null | grep -v "/$b$" | head -1)
  [ -n "$found" ] && echo "REACHABLE ($found)  $b" || echo "ORPHAN            $b"
done
```

A hook invoked from a workflow rather than `settings.json` is legitimate — do not report it as orphaned. Confirm each invocation site before judging.

Two traps to check on any hook that _looks_ wired:

- **The script's own comments may lie.** A header claiming "Wired via settings.json" is documentation, not evidence. Only `settings.json` (or a workflow) is evidence.
- **`git log -S` settles it.** If the string never appeared in the config's history, the hook has never run once:

  ```bash
  git log -S"<hook-name>" --oneline -- .claude/settings.json
  ```

> Real finding (2026-08): `.claude/hooks/verify-push-sha.sh` had existed complete and executable, with a header reading _"Wired via .claude/settings.json PostToolUse Bash matcher"_ — but `git log -S` on that config returned nothing. It had never been referenced, so it had never fired. It guards silent push failure (push fails, the tool call still "succeeds", the remote stays at the old SHA, auto-merge arms on stale code) — the exact class that had repeatedly wedged the merge train. Wired in #3605.

Apply the same reachability question to the other surfaces: a subagent no instruction file mentions will not be invoked, and a skill absent from `CLAUDE.md`'s tables will not be discovered.

### Step 2: Correctness — guards that fire wrongly

For each _reachable_ guard, ask what fraction of its firings are true positives. A guard that flags everything has the same information content as one that flags nothing.

Read the actual matching logic — especially anything regex-matching free text (PR titles, bodies, commit messages), which is where false positives concentrate:

```bash
grep -rnE '\.test\(|=~|match\(|grep -[a-zA-Z]*E' .github/workflows/*.yml | head -30
```

For each such rule, find the cheapest input that trips it accidentally — then check whether the repo's _own_ templates or conventions contain that input. Boilerplate the repo mandates is the most common accidental trigger, because it appears in every single instance.

> Real finding (2026-08): `.github/workflows/tier-classifier.yml` escalated a PR to `tier:critical` when `/secret|credential|rotate|leak|incident/i` matched the title or body. `.github/PULL_REQUEST_TEMPLATE.md` contains the checklist line _"No hardcoded secrets or credentials"_ — matching twice. So every PR that filled in the repo's own template was auto-classified critical; the classifier was measuring template usage, not risk. Filed as #3606.

Where a hook can block work, also check that it fails **open** — a guard whose own crash deadlocks editing is worse than the bug it prevents.

### Step 3: Coverage — failures with no guard

Mine committed history for recurring failures, then ask which are mechanically checkable. Use repo-committed signals; this runs in cloud checkouts with no local session files.

```bash
# recurring pain already written down
grep -cE '^- \*\*' .claude/rules/gotchas.md
grep -nE '^- \*\*' .claude/rules/gotchas.md | head -40

# what actually broke recently
gh pr list --state merged --limit 60 --json number,title \
  --jq '.[] | select(.title | test("^(fix|revert)")) | "\(.number) \(.title)"'
```

A gotcha entry is a failure a human had to write down because it kept recurring — the highest-value candidates for automation. For each, classify:

| Signal                                                          | Right tool                                                  |
| --------------------------------------------------------------- | ----------------------------------------------------------- |
| Deterministic, checkable from a file's content or the repo tree | **hook** (blocks at edit time — cheapest possible feedback) |
| Needs judgment across several files, semantic not syntactic     | **subagent** (reviews a change class)                       |
| A multi-step procedure a human repeats                          | **skill**                                                   |
| Needs the full repo, or must gate merge                         | **workflow check**                                          |

Prefer the earliest-firing option that can actually catch it: a hook beats a workflow, because a workflow costs a CI round-trip. But do not propose a hook for something requiring semantic judgment — it will produce false positives and land in step 2 next month.

Before recommending anything new, check it does not already exist in some form:

```bash
ls .claude/hooks/ .claude/agents/ .claude/skills/
```

### Step 4: Rank and propose

Order by expected value — how often it fires × cost of the failure it prevents:

1. **Dead guard** — a protection everyone believes is active. Wiring it is usually a one-line, high-value change.
2. **Miscalibrated guard** — actively degrading a signal reviewers depend on.
3. **Uncovered recurring failure** — ranked by how many times it has already recurred.
4. **Uncovered one-off failure** — usually not worth automating; say so rather than padding the list.

For each recommendation, state: the failure it prevents, evidence it has happened (commit/PR/issue reference), the surface, and roughly what it costs. A recommendation with no evidence of the failure ever occurring is speculation — drop it. Per the repo's simplicity mandate, **not** automating something is a legitimate outcome; report it plainly.

Then apply the repo's standard contract:

- Implement the single best recommendation → **one reviewable PR**.
- File the rest as `ready` + `meta-improvement` issues with self-contained acceptance criteria.
- Never merge; every change lands as a reviewable PR.

## Verifying a hook before you ship it

A hook is shell that runs on someone else's machine in a context you cannot easily reproduce. Exercise it directly, covering the skip path, the pass path, and each failure branch:

```bash
CLAUDE_BASH_COMMAND="pnpm test" bash .claude/hooks/<hook>.sh; echo "exit=$?"      # skip → 0, silent
CLAUDE_BASH_COMMAND="git push -u origin <branch>" bash .claude/hooks/<hook>.sh; echo "exit=$?"
```

Include the observed exit codes and stderr in the PR. Two things that bite:

- **Test with the flags the repo actually uses.** This repo mandates `git push -u origin <branch>`; a hook tested only against a bare `git push` misses argument-parsing bugs. Wiring `verify-push-sha.sh` surfaced exactly one — a token loop running `grep -qx "$tok"` parsed `-u` as a grep _option_, so every push emitted grep usage noise into the stderr surfaced to Claude. Use `grep -qxF --` for literal token matching.
- **Stderr is the user interface.** On a non-zero exit it is what the model reads, so noise in it directly degrades the guard.

## Anti-patterns

- **Don't** trust a script's own header comment about being wired. Verify against `settings.json` and `git log -S`.
- **Don't** recommend automation for a failure that has occurred once. Wait for a pattern.
- **Don't** propose a hook for something needing semantic judgment — that is a subagent.
- **Don't** add a guard without checking its false-positive rate against the repo's own templates and boilerplate.
- **Don't** report an orphan without checking workflows and other hooks for the invocation.
