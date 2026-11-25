---
name: commit
version: 0.1.1
description: |
  Atomic commit discipline for any code change. Enforces Conventional Commits
  format, one-behavior-per-commit rule, and safe git operation sequences.
  Invoke via /commit, or when the user says "commit this", "make a commit",
  "how should I commit", "commit message", or asks about commit conventions,
  atomic commits, or git workflow after making changes.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, migration, data, cloud, release-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Commit Discipline

Every commit is one externally describable behavior change. No exceptions.
Before opening a PR, the diff must read like a story — each commit a
single sentence.

## Format

```
<type>[scope]: <description>

[optional body: why, not what]

[optional footer: BREAKING CHANGE: ..., Closes #N]
```

**Types:**

| Type | When | Version bump |
|------|------|-------------|
| `feat` | New capability | MINOR |
| `fix` | Bug fix | PATCH |
| `perf` | Performance win | PATCH |
| `refactor` | Restructure, no behavior change | none |
| `test` | Tests only | none |
| `docs` | Docs only | none |
| `chore` | Tooling, deps, config | none |
| `ci` | CI/CD pipeline | none |
| `build` | Build system | none |

Subject line: imperative mood, present tense, ≤72 chars, no period.
`feat: add retry` not `feat: Added retry.`

Breaking change: append `!` and add `BREAKING CHANGE:` footer.
`feat!: remove legacy auth endpoint`

## The One-Behavior Rule

One commit = one sentence description that makes sense to a future reader
with no context. If "and" appears in the description, split the commit.

**Stage surgically:**
```bash
git add -p          # stage hunks, not whole files
git diff --staged   # verify what you're about to commit
```

**Signs you have too much staged:**
- Description needs "and"
- Changes span unrelated files (e.g. feature code + unrelated test fix + formatting)
- Diff is >200 lines for a "simple" change

## Safe Sequences

**Normal commit:**
```bash
git add -p
git commit -m "feat(scope): description"
```

**Before pushing (rebasing):**
```bash
git add -p
git commit -m "..."         # commit FIRST
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**Never:**
- `git commit --no-verify` — bypasses hooks
- `git push --force` — use `--force-with-lease`
- `git commit -a` on files with unrelated changes — stage selectively

## When to Commit

Commit after each discrete unit of work completes — not at end of session.
Triggers:
- A function/class is added or changed and tests pass
- A refactor is complete (behavior unchanged, tests still green)
- A bug is fixed with a reproducing test
- A config or build change is isolated

Do not accumulate changes across multiple behaviors before committing.
If tests fail, stash or fix before committing — never commit red.

## Commit Before Asking

When you complete a discrete change, commit it immediately. Do not ask
"should I commit?" — commit, then continue. The user can always amend or
squash before the PR.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
