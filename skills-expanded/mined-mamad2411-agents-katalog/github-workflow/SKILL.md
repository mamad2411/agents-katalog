---
name: github-workflow
last_reviewed: 2026-09-06
group: Repo hygiene
description: >-
  Open and land PRs, respond to review comments, manage issues, labels, tags and releases through
  the `gh` CLI. Use when automating GitHub issues, PR templates, labels, or project boards.
---

# github-workflow

## Core Philosophy
GitHub is the operating system of modern software collaboration. Relying on clicking through the web UI for every pull request, issue label, and release creates massive context switching. Professional engineering teams drive high-velocity delivery through the official GitHub CLI (`gh`), automated CI/CD gating, semantic branch protections, automated release drafting, and clear PR review standards.

---

## 4-Step GitHub Operations & CI/CD Discipline

### Step 1: High-Velocity GitHub CLI (`gh`) Mastery
1. **Core CLI Workflow**:
   - Create issue and start work:
     ```bash
     gh issue create --title "fix(db): handle connection pool timeout" --body "Details..."
     gh issue develop 42 --checkout
     ```
   - Open Pull Request with auto-filled commits:
     ```bash
     gh pr create --fill --assignee @me --label "bug,backend"
     ```
   - Check CI test status:
     ```bash
     gh pr checks
     ```
   - Merge PR using squash strategy:
     ```bash
     gh pr merge --squash --delete-branch
     ```

### Step 2: PR Description & Review Hygiene
1. **The 4-Part PR Description**:
   - *1. Context & Problem*: Link to issue (`Fixes #42`).
   - *2. Technical Approach*: Bullet points of architectural decisions.
   - *3. Verification Evidence*: Exact test output or screenshot/terminal recording.
   - *4. Rollback Plan*: How to revert in production if an incident occurs.
2. **Code Review Etiquette**:
   - Use conventional comments prefixes: `nit:`, `suggestion:`, `question:`, `blocking:`.
   - Never leave blocking reviews without providing a concrete code snippet or alternative.

### Step 3: Branch Protections & Automated CI Gates
1. **Repository Rulesets / Branch Protection Rules**:
   - Require linear history (enforce squash or rebase merges; ban merge commits).
   - Require status checks to pass before merging:
     - Linter / Static Analysis (`eslint`, `golangci-lint`, `ruff`).
     - Unit Test Suite with code coverage threshold ($\ge 80\%$).
     - Security / Secret Scanning (`gitleaks`, CodeQL).
   - Require signed commits (`git commit -S`).

### Step 4: Semantic Releases & Changelog Automation
1. **Automated Release Drafting (`gh release`)**:
   - Tag releases with Semantic Versioning (`vMAJOR.MINOR.PATCH`).
   - Generate automated release notes categorized by PR labels:
     ```bash
     gh release create v3.1.0 --generate-notes --title "Release v3.1.0"
     ```
2. **Artifact Bundling**:
   - Attach build artifacts (compiled binaries, tarballs, checksums `SHA256SUMS`) directly to the release via CLI.

---

## Deliverable Format: Pull Request Template (`.github/pull_request_template.md`)

```markdown
## Summary
Fixes #[Issue Number]

Provide a 2-3 sentence overview of what this PR changes and why.

## Technical Changes
- [File A]: [Explain non-obvious architecture change]
- [File B]: [Refactor detail]

## Verification & Testing
- [ ] Unit tests pass: `npm test`
- [ ] Linter clean: `npm run lint`
- [ ] Manual test verification evidence:
```bash
# Paste verification command output here
```

## Rollback Strategy
If this PR causes a production regression:
- Revert via `gh pr revert [PR_NUMBER]` or roll back deployment commit.
```

---

## Worked Example: Automated Release Automation via `gh` CLI

- **Workflow**: Developer completed Sprint release.
- **Execution**:
  ```bash
  gh pr list --state merged --milestone "Sprint 14"
  gh release create v1.4.0 --generate-notes --title "v1.4.0: Distributed Queue Support"
  gh release upload v1.4.0 ./dist/engine-linux-amd64 ./dist/SHA256SUMS
  ```
- **Outcome**: Shipped signed release notes, binary assets, and checksums in 45 seconds without touching a web browser.

---

## Verification Checklist

- [ ] PR description links to tracked issue and includes reproducible test output.
- [ ] CI pipeline enforces linter, type-check, and automated test pass gates.
- [ ] Branch protection rules require passing checks and squash-merge discipline.
- [ ] Release tags follow Semantic Versioning (`vMAJOR.MINOR.PATCH`).
- [ ] All released binaries are accompanied by cryptographic checksums.

---

## Anti-Patterns

- **Monster PRs**: Submitting a 3,000-line diff touching 40 unrelated files and asking for a quick review.
- **Bypassing CI**: Merging to `main` with failing or skipped status checks.
- **Vague Commit Messages**: Opening PRs with titles like "updates" or "fix stuff".
