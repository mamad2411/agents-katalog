---
name: ship
description: Ship current work through the branch → commit → push → PR → merge → cleanup flow. Picks up wherever you are in the cycle. Use when the user says "ship it", "land this", "merge this", or invokes /ship.
allowed-tools: Bash, Read, Grep, Glob
---

# Ship Workflow

Deliver current work to main. Assess the current state and pick up from wherever the user is.

## Arguments

- `/ship` — default flow, adapts review gate to repo flavor
- `/ship full-sail` — skip the review pause (solo/pair repos only; team repos still pause)

## Assess First

Run these in parallel to determine current position in the flow:

```bash
git status --short              # Uncommitted changes?
git branch --show-current       # On main or a feature branch?
git log --oneline main..HEAD    # Commits ahead of main?
git remote show origin 2>&1     # Remote tracking state?
```

Also check repo flavor for review gating:

```bash
# Active contributors in last 90 days
git log --since="90 days ago" --format='%aN' | sort -u | wc -l
```

- **≤2 active**: Solo/pair — lightweight PRs, review pause optional
- **3+ active**: Team — review pause mandatory, suggest reviewers

If the GitHub way has already injected context (look for `**Context**: Team project` or
`**Context**: Solo/pair project` in the conversation), use that instead of re-checking.

## Flow Steps (skip what's already done)

### 1. Branch (if on main with changes)

```bash
git checkout -b <branch-name>
```

Pick a name from the changes: `feature/thing`, `fix/thing`, `refactor/thing`.
If the user provides a name, use it. If changes are already committed on main,
create the branch first, then it carries the commits.

### 2. Commit (if uncommitted changes)

Stage and commit. Follow conventional commit format.
If there are multiple logical changes, make multiple atomic commits.
Ask the user for a commit message direction if the intent isn't clear.

### 3. Push

```bash
git push -u origin <branch>
```

### 4. PR

```bash
gh pr create --title "..." --body "$(cat <<'EOF'
## Summary
...

## Test plan
...
EOF
)"
```

Keep the title under 70 characters. Summary should be 1-3 bullets.
For small/obvious changes, the test plan can be brief.

### 5. Review Gate

**Team repos (3+ active contributors):**
- Always pause here. State the change scope and suggest reviewers.
- Do NOT proceed to merge without explicit user approval.
- Exception: `/ship full-sail` is rejected for team repos — tell the user why.

**Solo/pair repos (≤2 active contributors):**
- **Default**: Offer to spawn a `code-reviewer` subagent against the PR. This is the
  normal path — don't wait for the user to ask. Frame it as: "I'll run a code review
  on this PR before we merge" and proceed unless the user declines.
- **Trivial** (typos, config, single-file): mention the review is optional, still offer
- `/ship full-sail` skips both the review and the pause

State your assessment and let the user decide.

**Running the review:**

```
Agent(subagent_type="code-reviewer", prompt="Review PR #<number> in this repo.
Run gh pr diff <number> to see the changes. Post findings as a gh pr comment.")
```

After the review completes, summarize findings and ask whether to proceed to merge.

### 6. Merge

```bash
gh pr merge <number> --merge
```

Use `--merge` (not squash or rebase) unless the user prefers otherwise.

### 7. Cleanup

After merge, always run the full cleanup sequence — don't stop at `git pull`:

```bash
git checkout main && git pull && git fetch --prune
```

Then delete the local branch we just merged:

```bash
git branch -d <branch>
```

And verify the workspace is clean:

```bash
git branch  # Should show only main (and any other active work branches)
```

This keeps the repo tidy. Stale local branches and dangling remote tracking refs
accumulate fast if you skip this.

### 8. Publish (if applicable)

After merge, check if the project has publishing targets:

```bash
make help 2>/dev/null | grep -iE 'release|dist|publish|deploy'
```

If found, ask the user whether to publish:
- **`make release`** — version bump, tag, publish artifacts
- **`make dist`** — build distributable artifacts without publishing
- **`make deploy`** — deploy to staging/production

Don't auto-publish — always confirm. Publishing is a one-way door (npm publish, GitHub Release, AUR push).

If no Makefile targets exist but the changes warrant a release (new feature, breaking change), suggest:
- Tagging: `git tag -a vX.Y.Z -m "summary" && git push origin --tags`
- GitHub Release: `gh release create vX.Y.Z --generate-notes`

## Key Principles

- **Don't ask permission for each step** — assess state, propose the full remaining flow, then execute
- **Pause only at decision points**: commit message wording, PR description, review gate, publish
- **If already mid-flow**, pick up from current state — don't restart
- **One commit is fine** for most changes; only split if there are genuinely separate concerns
- **Repo flavor drives review**, not just change size — a one-line fix in a team repo still pauses
- **Merge ≠ ship** for projects with artifacts — check for `make release` after merge
