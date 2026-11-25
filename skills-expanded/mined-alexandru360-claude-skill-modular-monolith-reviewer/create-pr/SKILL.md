---
name: create-pr
description: Create a GitHub Pull Request with a structured description from the current branch's changes. Triggers on phrases like "create PR", "open PR", "make a pull request", "submit PR", "create pull request", "PR for this branch", or "open a pull request".
allowed-tools: Read, Glob, Grep, Bash
model: sonnet
version: 1.0
---

# Create Pull Request

Generate a well-structured GitHub Pull Request from the current branch using `gh pr create`.

## When this skill applies

Use when the user wants to:
- Create a new Pull Request for the current branch.
- Open a PR with a structured description derived from commits and changes.

Do **not** use when:
- The user wants to commit/push first (use `ship-changes` instead).
- The user wants to review an existing PR.
- There is nothing to open a PR for (branch is up-to-date with default branch).

## Stop conditions

| # | Condition | Check | Stop message |
|---|-----------|-------|--------------|
| 1 | Not a git repository | `git rev-parse --is-inside-work-tree` fails | "Not a git repository." |
| 2 | On default branch | Current branch equals `<default-branch>` | "You are on the default branch. Switch to a feature branch first." |
| 3 | No commits ahead | `git log <default-branch>..HEAD --oneline` is empty | "No commits ahead of `<default-branch>`. Nothing to open a PR for." |
| 4 | Branch not pushed | `git ls-remote --heads origin <current-branch>` is empty | "Branch not pushed to remote. Push first with `git push -u origin <current-branch>`." |
| 5 | PR already exists | `gh pr view --json state` returns an open PR | "A PR already exists for this branch: <url>. Use `gh pr edit` to update it." |
| 6 | `gh` CLI not available | `gh --version` fails | "GitHub CLI (`gh`) is not installed or not authenticated. Run `gh auth login`." |

## Execution steps

### Step 1 — Gather context

Run in parallel:
```
git branch --show-current
git log <default-branch>..HEAD --oneline
git diff <default-branch>...HEAD --stat
git diff <default-branch>...HEAD   # full diff for understanding changes
```

From the commit history and diff, determine:
- **Type of change** (feat, fix, refactor, docs, etc.)
- **Scope** (which features/areas are affected)
- **Key changes** (summarized from commits)
- **Trade-offs or decisions** that a reviewer might question

### Step 2 — Write PR title

Requirements:
- **Maximum 8 words** — forces clarity and scannability.
- Start with a verb in imperative mood (Add, Fix, Update, Remove, Refactor, Migrate, etc.)
- Describe what changed, not why.
- Be specific but concise.

Good examples:
- "Add user authentication with OAuth"
- "Fix race condition in payment processing"
- "Migrate components to CONNECT Design System"

Bad examples:
- "Made some changes to the authentication system and updated tests" (too long)
- "Changes" (too vague)
- "This PR fixes the bug we talked about" (unclear)

**Base branch**: Auto-detect default branch (`main` or `master`).

### Step 3 — Draft PR body

Generate the PR body using this template. **Keep Summary under 100 words** unless the PR is large (10+ files or 500+ lines) or involves complex trade-offs.

```markdown
## Summary

<2-3 sentences: what changed, why, and impact/behavior change if relevant>

## Type of Change

- [x] <detected type, mark only the relevant one(s)>

Options:
- 🐛 Bug fix (non-breaking change which fixes an issue)
- ✨ New feature (non-breaking change which adds functionality)
- 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- 📝 Documentation update
- 🎨 Style/UI change
- ♻️ Code refactoring
- ⚡ Performance improvement
- 🧪 Test update
- 🔧 Configuration change

## Testing Notes

- Tested locally: <yes/no>
- Manual testing steps:
  1. <step>
  2. <step>

## Known Issues

<Only include if there are deliberate trade-offs or decisions that might be questioned.
Explain rationale for each. Keep each item to 1-2 sentences.
Omit this entire section if everything is straightforward.>

## Checklist

- [x] My code follows the project's code style
- [x] I have performed a self-review of my code
- [x] My changes generate no new warnings
- [x] The application builds successfully
- [x] I have tested my changes thoroughly
```

### Writing guidelines

- **Don't list all files changed** — the reviewer can see the diff.
- **Don't include step-by-step implementation details** — that's what the code is for.
- **Don't apologize or be overly cautious** — state facts.
- **Summary answers**: What changed? Why? What's the impact?
- **Known Issues answers**: What trade-offs were made? Why were they acceptable?
- **Screenshots section**: Only include if `git diff` shows changes to UI-related files (`.tsx`, `.css`, `.scss`, `.svg`). Otherwise omit entirely.

### Step 4 — Present draft and confirm

**Intent detection:**
- User said "create and submit PR" / "create PR in GitHub" → Show preview, then ask to confirm submission.
- User said "create a PR" / "open PR" (no explicit submit) → Show preview, ask before submitting.

Show the full PR title and body to the user:

> **Title:** `<title>`
> **Base:** `<default-branch>` ← `<current-branch>`
>
> <body preview>
>
> Options:
> **(a)** Create PR as proposed
> **(b)** Edit — tell me what to change
> **(c)** Cancel — just show me the content to copy

**Never create the PR without explicit user approval.**

### Step 5 — Create the PR

Once approved, create the PR:

```bash
gh pr create --title "<title>" --base "<default-branch>" --body "$(cat <<'EOF'
<body content>
EOF
)"
```

If labels were suggested and accepted:
```bash
gh pr edit <number> --add-label "<label1>,<label2>"
```

### Step 6 — Summary

Output:
```
PR created:
- Title: <title>
- URL: <pr-url>
- Base: <default-branch> ← <current-branch>
- Commits: N
```

## Quick reference

| Element | Constraint | Purpose |
|---------|-----------|---------|
| Title | Max 8 words, imperative verb | Quick scan of what changed |
| Summary | 2-3 sentences (~100 words max) | Core changes and rationale |
| Known Issues | Only if needed | Preempt review questions |
| Total body | <150 words typical | Respect reviewer time |

## Constraints

- **Never create a PR without user approval** of the title and body.
- **Never force-create** if a PR already exists for the branch.
- **Checklist items**: Pre-check items that are verifiable from context (build passes, lint passes). Leave unchecked items that require manual confirmation.
- **Known Issues section**: Only include if there are genuine trade-offs. Never pad with generic text or "none" placeholders.
- **Brevity over completeness**: A PR that takes 30 seconds to read gets reviewed faster.
