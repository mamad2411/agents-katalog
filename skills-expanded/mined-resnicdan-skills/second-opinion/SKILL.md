---
name: second-opinion
description: Before you push, have a second agent review your branch — ideally a different model than the one that built it — then reconcile its findings against your own review. Run it as a deliberate pre-push gate on nontrivial changes (multi-file, public surface, correctness- or security-sensitive), not on every small diff.
disable-model-invocation: true
argument-hint: "[optional: a repo path or worktree to review; defaults to the current one]"
---

# Second Opinion

Run this on a branch that is **finished and about to be pushed**. It gets a second
agent to review the diff, then reconciles that review against your own — so the
code that ships was checked by someone other than whoever wrote it.

The reason this works is **independence, not a smarter model**. An agent reviewing
its own work reads what it *meant*, not what it *wrote*, and goes easy on output it
recognizes as its own. A reviewer with a fresh context — and, better still, a
different model family — doesn't share those blind spots. So the benefit comes in
two tiers:

- **Floor:** any reviewer running in a *fresh context*, even the same tool you
  built with, already removes most of the self-review bias.
- **Upgrade:** a *different model family* removes more, because its mistakes
  aren't correlated with the ones that produced the code. If you have a second
  tool, use it; if you don't, the floor is still worth running.

Engineering policy — what counts as a blocker, test expectations, DRY, git
hygiene — is governed by your project's conventions (e.g. your `CLAUDE.md` /
`AGENTS.md`). Apply them; don't restate them here.

## Steps

Do them in order. Steps 3 and 4 are deliberately independent: dispatch the
reviewer, then review the diff yourself **without reading its output first**, so
the two passes don't contaminate each other.

1. **Scope the diff.** Resolve the target repo (the argument if given, else the
   current directory) and confirm it's a git repo. Resolve the base branch (the
   repo's default branch) and compute the current branch's diff against it. State
   in one line: repo, branch, base, and how many commits / files are ahead.
   **Stop if there is nothing to review** (zero commits ahead) or the target is
   the wrong repo — don't review air, and never return a false "looks good."

2. **Pick the reviewer.** Choose which agent runs the review. Default smart:
   prefer a **different model family** than the one running this skill (the
   upgrade); if none is available, fall back to a **fresh run of your own tool**
   (the floor). Honor an explicit choice — either named for this run, or a
   **standing default** pinned in your agent's conventions file (`CLAUDE.md` /
   `AGENTS.md` / `.cursor/rules`). Say in one line which reviewer you picked and
   whether it's the upgrade or the floor. For the exact command per tool, and how
   to set a standing default, read `reviewer-cli-reference.md`.

3. **Dispatch the review — isolated.** Run the reviewer on the diff in a context
   separate from your working one (a subagent if your harness supports it, else a
   separate process), so its raw transcript doesn't flood your session. Hand it
   the diff and the rubric below. Bring back a **compact findings list**, not the
   raw output.

4. **Review it yourself.** Before looking at the reviewer's findings, review the
   same diff against the same rubric. This is your independent pass — it catches
   what you know from context that a cold reviewer can't (project conventions,
   why a change is shaped the way it is), and it is what turns Step 5 into a
   cross-check instead of blind trust.

5. **Reconcile and tag.** Merge the two lists, de-duplicated, and tag each
   finding:
   - **`agreed`** — both passes flagged it. Highest confidence; treat as real.
   - **`reviewer-only`** — only the second agent flagged it. This is the payoff of
     a fresh / different reviewer; scrutinize it, don't wave it through *or* off.
   - **`mine-only`** — only your pass flagged it, usually the context-dependent
     ones.

   On a severity disagreement, take the **higher** of the two. A `reviewer-only`
   finding you can't reproduce or justify is a candidate to drop — say so, with
   the reason, rather than importing it blindly.

6. **Verdict.** Present the findings by severity, then give one call: **ship /
   review-needed / do-not-ship**. **Stop for approval before changing any code** —
   the skill ends at the verdict unless the user asks you to action the fixes.

## Rubric

Give the reviewer, and your own pass, this bar:

- **Severity:** `P0` blocker (correctness, security, data loss) · `P1` should-fix
  · `P2` nit. Lead with the highest.
- **Material findings only.** Every finding must answer: *what breaks, why, what's
  the impact, and the concrete fix.* "It could be cleaner" is not a finding.
- **No findings is a valid, good result.** Don't manufacture issues to look
  thorough. One real blocker beats ten nits.
- **Stack-specific checks** — framework footguns, migration safety, query
  patterns — come from your project's conventions, not this file.
