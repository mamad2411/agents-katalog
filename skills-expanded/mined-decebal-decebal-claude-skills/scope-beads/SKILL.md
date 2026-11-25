---
name: scope-beads
description: Invoke when splitting a feature into multiple beads, prompts, or sub-tasks — and whenever /create-prompt emits more than one prompt. Enforces trunk-based development — one feature = one short-lived branch = one PR; each bead/prompt is a slice (commit) on that single branch; parallel agents converge on that branch; NEVER a PR per bead, prompt, or agent.
---

# scope-beads — trunk-based work organization

Invoke this whenever you fan **one feature** into multiple units of work — chronis beads, `/create-prompt` prompts, or parallel sub-agents. Its job: keep the whole feature on **ONE short-lived branch → ONE PR**. It exists because fanning a feature into per-unit PRs is a recurring, explicitly-forbidden failure (angry correction: *"features are complete in a PR… it doesn't matter how large it is"*).

## The rule (non-negotiable)

**One feature = one short-lived branch = one PR to the trunk (`main`).**

- A **feature** is the epic / the whole task. Every slice — each child bead, each generated prompt, each sub-agent's output — lands on ONE branch and merges as ONE PR **when the feature works end-to-end**.
- **Slices are commits on that branch, never their own PRs.** "Done" for a slice = committed + pushed to the feature branch — not a merged PR of its own.
- **Those slice commits are work-in-progress, and each author's commits are collapsed to ONE before the PR is marked ready.** Reset to the merge-base (or, on a PR someone else started, to the last commit that is not yours), confirm `git diff <old-head> HEAD` is empty, push with `--force-with-lease` pinned to the old head, re-run the gates on the new SHA. The feature merges by rebase as one commit per author. See `~/.claude/rules/git-discipline.md` → "One PR = one commit per author, merged by rebase".
- **Size is never a reason to split.** A feature merges when COMPLETE, however large. Do NOT slice one feature into multiple PRs for size or "reviewability."
- **Separate PRs only for genuinely independent features** (no shared end-to-end). If two slices must both land for the feature to actually work, they are ONE PR.

## Trunk-based practices

- Trunk = `main`; integrate frequently via short-lived branches; keep `main` green + releasable at all times.
- Branch off **LATEST** `main`; `git fetch origin main && git rebase origin/main` before starting **and before every push**; re-verify.
- **Short-lived:** hours-to-days, not weeks. Merge the complete feature, delete the branch.
- Incomplete-but-must-land → **feature-flag / dark-launch**; never merge a half-feature as a "done" PR.

## Parallelism / agents (the exact failure this prevents)

- Fan work to agents? They **converge on the SAME feature branch** — never one branch/PR per agent or per prompt.
- **Isolate the tree, not the branch:** each agent gets a `git worktree` with a **detached HEAD on the shared feature branch** (own build dir → no file-stomping, no lock thrash); commit; `git push origin HEAD:<feature-branch>`; on a non-fast-forward, `git fetch` + `git rebase` your commit onto the tip and retry.
- Conflicting slices → sequence them on the one branch, or one agent owns the file. Never split to separate branches to dodge a conflict.

## When you scope the work

1. **Name the ONE feature branch:** `<type>/<slug>`.
2. **Each unit (bead / prompt) is a slice** toward one end-to-end feature, sequenced by dependency; each integrates without breaking the build.
3. **Stamp every unit** with the contract (below).
4. A unit that **ships on its own** (no shared end-to-end) is a SEPARATE feature → its own branch/PR.

### Stamp — paste into every bead / prompt

> **Work organization (trunk-based):** Part of feature `<name>`, branch `<type>/<slug>`. Implement your slice as commit(s) on THAT one branch — `git fetch origin main && git rebase origin/main` first, keep the build green. Do **NOT** open a separate PR for this slice. Do **NOT** squash, amend, or force-push the branch — siblings are pushing to it and a rewrite destroys their commits; the orchestrator collapses it once, at the end. The feature merges as ONE PR to `main` when all slices are done and it works end-to-end.

## Anti-patterns

- ❌ A PR per bead / per prompt / per agent for ONE feature → one `feat/<feature>` PR.
- ❌ Splitting a feature "because it's large" / "for reviewability" → size is not a split criterion.
- ❌ Long-lived branches that drift from `main` → short-lived, rebase often.
- ❌ Merging a slice that doesn't work end-to-end as its own PR → feature-flag, or wait.

## Integrations

- **Chronis / beads:** stamp each child bead's description; the epic names the single branch + the single PR. "cn done" = slice committed + pushed to the feature branch.
- **`/create-prompt` + `/run-prompt`:** when create-prompt emits multiple prompts they share ONE feature branch; a `--parallel` run means the sub-agents **converge on that branch** (not a branch each). Stamp each generated prompt.
- **Repo rules (e.g. CLAUDE.md, `.claude/rules/git.md`):** defer to any repo-specific branch discipline; this is the general contract on top of it.
