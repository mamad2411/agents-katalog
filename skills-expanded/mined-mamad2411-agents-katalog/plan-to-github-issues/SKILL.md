---
name: plan-to-github-issues
description: Convert a phased implementation plan (Markdown file with phases and acceptance criteria) into GitHub issues, a CI workflow that runs tests on PRs, and a PR template that maps each PR to its acceptance criteria. Use when user wants to create GitHub issues from a plan, push phases to GitHub, set up acceptance-criteria CI, or track plan phases as issues.
---

# Plan to GitHub Issues

Turn a local `plans/*.md` file into GitHub issues (one per phase), a CI workflow, and a PR template — so every PR proves its acceptance criteria through tests.

## Process

### 1. Locate the plan file

If the user hasn't specified a file, look for plan files matching `**/plans/plan-*.md` or ask the user to point you to it.

Read the plan file and identify:
- The GitHub repo (run `gh repo view --json nameWithOwner`)
- All phases — each `## Phase N: Title` section
- The acceptance criteria checklist under each phase (`- [ ] ...` lines)

### 2. Create labels

Create two labels if they don't exist:

```bash
gh label create "phase" --color "#0052CC" --description "Implementation phase" --repo OWNER/REPO
gh label create "acceptance-criteria" --color "#5319E7" --description "Has acceptance criteria" --repo OWNER/REPO
```

### 3. Create one issue per phase

For each phase, create a GitHub issue with:
- **Title**: `Phase N: <Title>` (matching the plan heading exactly)
- **Labels**: `phase`, `enhancement`, `acceptance-criteria`
- **Body**: use the template below

Run all `gh issue create` calls in parallel for speed.

<issue-body-template>
## Overview

<"What to build" content from the plan phase>

**Related user stories**: <user stories list from the plan>

## Acceptance Criteria

<acceptance criteria checklist copied verbatim from the plan, as - [ ] items>

## Test Coverage Requirements

All acceptance criteria above must have corresponding automated tests. A PR for this phase will not be merged unless:
- All tests pass in CI
- Each acceptance criteria checkbox has a test that directly validates it
- Test file names or descriptions reference the criterion they cover
</issue-body-template>

### 4. Create the CI workflow

Create `.github/workflows/ci.yml` in the repo via the GitHub API. The workflow must:

- Trigger on `pull_request` (opened, synchronize, reopened) and `push` to `main`
- Spin up real service containers (Postgres + Redis) — no mocks
- Run: install deps → type check → db migrations → tests with coverage → upload coverage artifact
- Include an `acceptance-criteria-check` job (PR only) that reads the linked issue via `Closes #N` in the PR body, counts checked vs unchecked `- [ ]` / `- [x]` lines, and posts a warning for any still-unchecked criteria
- Include a lint job

Adapt the stack/commands to the project (Bun/Node, test runner, lint command). Inspect `package.json` or `bunfig.toml` to infer the right commands.

Use the GitHub Contents API to create the file (base64-encode content):

```bash
gh api --method PUT /repos/OWNER/REPO/contents/.github/workflows/ci.yml \
  -f message="chore: add CI workflow with acceptance criteria tracking" \
  -f content="<base64>"
```

### 5. Create the PR template

Create `.github/PULL_REQUEST_TEMPLATE.md` with:
- Linked issue field (`Closes #N`)
- Acceptance criteria checklist (to be filled by the author)
- A table mapping each criterion to the test file + test name that proves it
- A merge checklist (tests pass, type check passes, criteria proven, issue checkboxes updated)

Create via the GitHub Contents API same as above.

### 6. Report back

List all created issue URLs, confirm the workflow and PR template paths, and explain the workflow:

> When you open a PR for a phase, add `Closes #N` in the body. Check off each acceptance criterion in the issue as you prove it with a test. CI will report how many remain unchecked.

## Notes

- Create issues in parallel — don't wait for each one sequentially
- If the repo has no local checkout, use the GitHub Contents API for all file creation
- If the plan has no "What to build" section, use the phase title + acceptance criteria as the overview
- Don't hardcode env vars (JWT secrets, encryption keys) — use obviously-fake test values in the workflow
- The `acceptance-criteria-check` job should warn, not fail — unchecked criteria are a signal to the author, not a hard gate
