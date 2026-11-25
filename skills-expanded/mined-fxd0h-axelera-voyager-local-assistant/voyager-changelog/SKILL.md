---
name: voyager-changelog
description: Generate a Keep a Changelog fragment for the current PR in the Axelera Voyager / Voyager SDK development workflow. Provide a PR number or let the skill derive it from gh pr view.
argument-hint: "[PR number]"
allowed-tools: Read, Bash, Glob, Grep, Write
---

# Changelog Fragment Generator

Generate a Keep a Changelog fragment for the current changes.

## Instructions

### Step 1: Get PR number

```bash
PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || echo "")
```

If $ARGUMENTS contains a number, use that. If no PR number is available from either source, ask the user to provide one or create the PR first.

### Step 2: Analyze changes

```bash
git diff --stat origin/main...HEAD
git log --oneline origin/main..HEAD
```

Map commit types to fragment types:

| Commit type | Fragment type |
|-------------|--------------|
| feat | added |
| fix | fixed |
| security, deps (CVE) | security |
| perf, deps (routine) | changed |
| refactor, docs, style, test, build, ci, chore | skip (recommend skip-changelog label) |

### Step 3: Write fragment

File: `changes/{PR_NUMBER}.{type}.md`
Set `FRAGMENT_TYPE` to the mapped type before writing, for example
`FRAGMENT_TYPE=added`.

Rules:
- 1-2 sentences, user-facing language
- Imperative present tense ("Add X" not "Added X")
- No file paths, commit hashes, or implementation details

Good: "Add workspace selector to the dashboard sidebar"
Good: "Fix authentication token refresh loop on expired sessions"
Good: "Upgrade requests library to address CVE-2026-25645"
Bad: "Updated auth.ts to fix bug"
Bad: "Refactored the codebase"

### Step 4: Verify

```bash
test -s "changes/${PR_NUMBER}.${FRAGMENT_TYPE}.md"
cat "changes/${PR_NUMBER}.${FRAGMENT_TYPE}.md"

# When available, run the repo's fragment verifier
bash scripts/checks/verify-commit-changelog.sh
```

If no user-facing changes, tell the user to add the `skip-changelog` label instead.
Do not read or rewrite unrelated fragments while verifying this PR.
