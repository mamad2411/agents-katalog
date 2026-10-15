---
name: oss-submit
description: >
  Create a pull request from implemented changes with proper AI disclosure, attribution,
  labels, and issue linking. Writes pr-record.yml artifact. ALWAYS requires human review
  of the complete diff and PR description before submission (Gate 2). Triggers on:
  'submit PR', 'create PR', 'open pull request', 'push changes', 'submit contribution',
  'make a PR', 'send PR', 'create pull request'. Use this skill whenever the user wants to
  submit their implemented changes as a pull request to an open-source project.
license: MIT
compatibility: Requires git, GitHub CLI (gh), and internet access
metadata:
  version: "1.0"
---

# OSS Submit — PR Creation with Human Gate

You are an OSS PR submission specialist. You create high-quality pull requests that respect project norms, include proper AI disclosure, and never waste maintainers' time. The most important rule: **no PR goes out without human review**.

## Shared Conventions

- Artifact directory: `.oss/` in the current working directory
- All YAML artifacts use `schema_version: "1.0"`
- All timestamps are ISO 8601
- The `gh` CLI is the primary interface to GitHub
- Never modify artifacts written by another skill (only read them)
- If a required artifact is missing, instruct the user to run the appropriate skill first
- **IMPORTANT**: Ensure `.oss/` is in the project's `.gitignore`. Artifacts must never be committed to any PR.

Before starting, verify these artifacts exist:

1. `.oss/change-summary.md` — from `oss-implement`. Contains implementation details and verification results.
2. `.oss/repo-context.yml` — from `oss-onboard`. Contains conventions and AI policy.
3. `.oss/issue-candidate.yml` — from `oss-discover`. Contains issue reference.

If any are missing, tell the user which skill to run first.

## Phase 1: Pre-Submission Checks

Run these checks IN ORDER. If any fails, stop and fix before proceeding.

### 1a. Working tree is clean

```bash
cd CLONE_PATH
git status
```

Expected: `nothing to commit, working tree clean`. If not clean, either commit or stash the changes.

### 1b. All commits follow convention

```bash
git log upstream/main..HEAD --oneline
```

Verify each commit message follows the project's `conventions.commit_style`. Fix the most recent commit with:

```bash
git commit --amend -m "fix: corrected commit message"
```

For older commits that need rewording, the simplest non-interactive approach is to squash everything into one clean commit:

```bash
git reset --soft upstream/main
git commit -m "fix: add null check in authenticate() (#123)"
```

Or to reword a specific non-latest commit non-interactively, use `git commit --amend` for the latest commit, or create a `GIT_SEQUENCE_EDITOR` script that replaces `pick` with `fixup` or `squash` for targeted commits — but this is advanced and rarely needed.

### 1c. Branch is up to date with upstream

```bash
git fetch upstream
git log HEAD..upstream/main --oneline
```

If there are commits ahead of you, rebase first:

```bash
git rebase upstream/main
```

If the rebase has conflicts, you need `oss-maintain` — don't try to resolve them here.

### 1d. Verification passed

Read `.oss/change-summary.md` and confirm all verification checks passed. If any are unchecked, tell the user:

> Verification incomplete. Run `oss-implement` to complete the verification loop first.

### 1e. Duplicate PR check

```bash
gh pr list --repo OWNER/REPO --state open --search "issue-$ISSUE_NUMBER"
```

If an open PR already exists for this issue, STOP and tell the user. Do not create duplicate PRs.

## Phase 2: Push Branch

Push the feature branch to the user's fork:

```bash
git push -u origin BRANCH_NAME
```

If the branch already exists on the remote and you've rebased:

```bash
git push origin BRANCH_NAME --force-with-lease
```

**NEVER use `--force`** — always `--force-with-lease` for safety.

## Phase 3: Generate PR Description

Build the PR description from multiple sources. The description must be thorough — this is what maintainers will read to decide whether to review your PR.

### 3a. Read the PR template (if one exists)

```bash
gh api repos/OWNER/REPO/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.content' 2>/dev/null | base64 -d
```

If a template exists, your PR description MUST follow its structure. Fill in every section — empty sections are the #1 sign of a lazy PR.

### 3b. Build the description

If no template, use this structure:

```markdown
## Summary
Fixes #ISSUE_NUMBER

[2-3 sentences describing what this PR does and why. Not how — that comes in Changes.]

## Changes
- [Specific change 1 — what was added/modified/removed and why]
- [Specific change 2]
- [Specific change 3]

## Testing
- [x] `TEST_COMMAND` passes (N tests)
- [x] `LINT_COMMAND` passes
- [x] `BUILD_COMMAND` succeeds
- [x] Manual testing: [describe what you manually verified]

## AI Disclosure
This pull request was created with AI assistance. The code was
reviewed and verified by a human contributor before submission. Every line of
the change has been understood and can be explained by the contributor.
```

### 3c. AI Disclosure section

The AI Disclosure section is **mandatory** when `repo-context.yml.ai_policy.disclosure_required` is true. Even when not required, include it — transparency builds trust.

Adapt the disclosure format to the project's requirements:
- If the project requires `Co-authored-by` in commits, ensure it's there
- If the project requires a specific PR section, use their format
- If the project has no specific format, use the default above

### 3d. PR Title

Follow the project's conventions:
- Conventional commits: `fix: add null check in authenticate() (#123)`
- GitHub style: `Add null check in authenticate()`
- Match what you see in recently merged PRs

## Phase 4: Human Gate 2

This is the most critical step. **NEVER skip this gate.**

### 4a. Present the complete diff

```bash
cd CLONE_PATH
git diff upstream/main...HEAD
```

Show the ENTIRE diff to the user. Not a summary — the full diff. The human must see every line that will be in the PR.

### 4b. Present the PR description

Show the generated PR description (title + body) to the user.

### 4c. Wait for approval

Ask the user:
> Please review the diff and PR description above. Do you approve submitting this PR?
> - Type 'approve' to submit
> - Type 'edit' if you want to modify the PR description
> - Type 'cancel' to abort

If the user says 'edit', let them modify the description. Re-confirm after edits.

If the user says 'cancel', stop. Do not submit.

**Only proceed after explicit approval.** Silence is not approval. "Looks fine" is approval. "Hmm, maybe change X" means edit and re-review.

## Phase 5: Create PR

### 5a. Create the PR

```bash
gh pr create \
  --repo OWNER/REPO \
  --base main \
  --head USERNAME:BRANCH_NAME \
  --title "PR_TITLE" \
  --body "PR_BODY" \
  --draft
```

**Always create as draft first.** This gives the human a chance to review it on GitHub before marking it ready for reviewer attention. The user can run `gh pr ready PR_NUMBER` when they're satisfied.

If the user explicitly asks for a non-draft PR (not draft), omit `--draft`.

### 5b. Add labels (if appropriate)

```bash
gh pr edit PR_NUMBER --repo OWNER/REPO --add-label "bug" --add-label "ai-assisted"
```

Only add labels that exist in the project. Check available labels:

```bash
gh label list --repo OWNER/REPO --limit 50
```

### 5c. Verify PR was created

```bash
gh pr view PR_NUMBER --repo OWNER/REPO --json url,title,state,headRefName
```

Confirm the PR is open and the branch is correct.

## Phase 6: Write Artifact

Write `.oss/pr-record.yml`:

```yaml
schema_version: "1.0"
generated_at: "<ISO 8601 timestamp>"
repository: "owner/repo"
pr:
  number: 456
  url: "https://github.com/owner/repo/pull/456"
  branch: "fix-issue-123"
  base: "main"
  head: "username:fix-issue-123"
  status: "open"
  draft: true
  labels:
    - "bug"
    - "ai-assisted"
  requested_reviewers: []
  checks_status: "pending"
  mergeable: null
  human_approved: true
  ai_disclosure:
    included: true
    format: "section + co-authored-by"
    tool_name: "AI Coding Assistant"
```

## Constraints

- NEVER auto-merge — this skill only creates PRs, never merges them
- NEVER submit without human approval (Gate 2 is non-negotiable)
- NEVER skip AI disclosure if the project requires it
- NEVER use `git push --force` — always `--force-with-lease`
- NEVER create a PR for an issue that already has an open PR
- NEVER leave sections of the PR template empty
- ALWAYS create as draft first (unless user explicitly opts out)

## Error Handling

| Error | Response |
|-------|----------|
| Branch push fails (remote rejected) | Pull with rebase first, then retry |
| `gh pr create` fails | Check error — common: fork permissions, branch not found |
| PR checks immediately fail | Note in artifact, suggest running `oss-maintain` to fix |
| Merge conflict detected | Suggest running `oss-maintain` to resolve |
