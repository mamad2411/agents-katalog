---
name: check-secrets-secrets-leak
description: Detect secrets leaked in git history and files using automated scanners
argument-hint: "[path]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - deep-review-codebase
  - check-reference
  - run-audit

---
## Goal
Detect secrets, API keys, tokens, or credentials that may have leaked into the repository or files

## Scope

- Supports git history scan and filesystem scan
- Uses gitleaks, trufflehog, or regex patterns
- Reports with severity and location

## Execute
### 1. Prepare

> Goal: Prepare

1. Identify the target path or repo
2. Check which tools are available, e.g. gitleaks, trufflehog
3. Check whether the repo has git history

### 2. Scan Git History

> Goal: Scan Git History

1. Run `gitleaks detect --source <path> -v`
2. Or `trufflehog git file://<path>`
3. Save the results as JSON or CSV

### 3. Scan Filesystem

> Goal: Scan Filesystem

1. Run `gitleaks detect --no-git --source <path>` when you need to scan current files
2. Add regex scans for specific patterns
3. Filter out false positives such as examples and test fixtures

### 4. Report

> Goal: Report

1. Summarize the secrets found with commit hash, file, line
2. Set severity: Critical/High/Medium/Low
3. Recommend next actions: revoke, rotate, or `git filter-repo`
4. After that, use `/follow-secret-manager` to rotate and manage the new secrets, or `/open-web-for-config-secret` to create new API keys

## Rules
### 1. No Expose

- Never show real secret values in the report
- Never save results into the repo without review
- Use environment variables for scanner credentials

### 2. False Positives

- Verify patterns before reporting
- Note the allowlist if there is one
- Separate test data from real secrets

- Use /deep-review-codebase if needed
- Use /check-reference if needed
- Use /run-audit if needed

## Expected Outcome
- List of secrets found with location and severity
- No real secrets leaked in the report
- Clear remediation guidance
