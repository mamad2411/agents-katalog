---
name: github-pr-create
description: Semantic PR authoring, change impact isolation, automated checklist validation, atomic commits, and gh CLI automation
---
# GitHub Pull Request Authoring & Creation

## 1. Atomic Scope & Single Responsibility
Ensure each pull request addresses exactly one logical feature, bug fix, or refactoring goal. Separate structural reformatting from behavioral logic modifications into distinct commits or PRs.

## 2. Conventional & Structured Titling
Format pull request titles using strict Conventional Commits conventions (feat:, fix:, docs:, refactor:, test:, chore:). Include scope tags (e.g. feat(auth): implement PKCE OAuth code flow).

## 3. Comprehensive Pull Request Description
Structure the PR body with explicit sections: Objective / Context, Technical Changes Made, Verification Evidence (test command and pass output), and Linked Issues (Closes #123).

## 4. Pre-Flight Readiness Checklist
Verify that all local automated checks pass before creating the PR: linters clean, formatters applied, unit tests passing with zero regressions, and race detectors clean.

## 5. Minimal Diff & Hygiene
Review the git diff prior to publication. Eliminate commented-out debug code, unintended temporary files, trailing whitespace, and unneeded dependency bumps.

## 6. Deterministic gh CLI Automation
Automate PR creation via the GitHub CLI: gh pr create --title 'feat(scope): title' --body-file .prumo/templates/pr-body.md --base main --draft (if work in progress).

## 7. Draft PR Workflow for Active Collaboration
Publish in-progress or exploratory work as Draft PRs. Transition to 'Ready for Review' only after all automated CI checks and self-review verifications pass.

## 8. Reviewer & Assignee Routing
Assign primary code owners or relevant domain experts based on modified subsystem paths. Avoid pinging broad organizational teams indiscriminately.

## 9. Breaking Change Disclosure
Explicitly highlight any breaking API, schema, or configuration modifications in the PR description with clear migration instructions and backwards compatibility notes.

## 10. Self-Review & Diff Walkthrough
Perform a meticulous self-review in the GitHub web interface or terminal diff view, adding explanatory line comments on complex or non-obvious design decisions.
