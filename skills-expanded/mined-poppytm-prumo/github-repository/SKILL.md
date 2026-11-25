# GitHub Repository Management

## Purpose
Configure repositories securely and consistently: branch protection, required checks, secrets/environment scoping, CODEOWNERS routing, and labels — applied as reviewable changes with verification, never click-ops without evidence.

## Use when
- Setting up branch protection (required reviews, required status checks, force-push and deletion blocks) for `main` or release branches.
- Scoping secrets and environments (per-environment reviewers, secret rotation, fork-PR secret isolation).
- Standardizing labels, CODEOWNERS, and repository defaults across an organization.
- Operating in mode(s): `implementation`.

## Do not use when
- Debugging a failing workflow run (use `github-ci-debug`).
- Authoring issues or PRs (use `github-issue-create` / `github-pr-create`).
- Changing organization-level policies beyond one repository (escalate to org owner).

## Required context
- Repository URL, default branch, and current settings snapshot (`gh api repos/{owner}/{repo}/branches/main/protection`).
- Governance baseline: required reviewers count, required check names, secret inventory and rotation dates.
- CODEOWNERS paths and environment list (staging, production) with approver rosters.

## Procedure
1. **Snapshot current state**: export branch protection, required checks, environments, and secret names (never values) before changing anything.
2. **Apply least-privilege protection**: require PR reviews (≥1, more for high-risk paths), require up-to-date branches, list required status checks by exact name, block force pushes and branch deletion on protected branches.
3. **Scope secrets and environments**: store secrets at the lowest scope that works (environment > repository > organization); require reviewers on production environments; confirm fork PRs cannot read secrets.
4. **Wire CODEOWNERS and labels**: ensure every protected path has an owner team and that area labels match triage routing; remove stale owners.
5. **Verify via API, not UI memory**: re-fetch protection and environment payloads after applying; run a negative proof (e.g. direct push to `main` rejected, fork PR secrets empty) where safe.
6. **Record the change**: log before/after settings diff with timestamps in the task report; rotate any secret that was exposed during the operation.

## Decision rules
- **Settings as reviewable change**: repository mutations are scripted or documented diffs, never undocumented clicks.
- **Default deny on secrets**: a secret readable from a broader scope than necessary is a finding.
- **Protection parity**: release branches carry equal-or-stronger protection than `main`.
- **No secret values in evidence**: logs and reports contain names and scopes only.

## Evidence required
- Before/after settings payloads and negative-proof results.
- Secret scope map (names + scopes, no values).
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Structured GitHub artifact (applied settings with diff record).
- Validation confirmation (API re-fetch + negative proof).

## Stop conditions
- Branch protection, checks, secrets, environments, and CODEOWNERS verified against the governance baseline.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to organization owner for SSO enforcement, org-wide policy, or billing/visibility changes.
- Escalate immediately on suspected secret exposure or unauthorized settings changes.
