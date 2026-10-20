---
name: check-security-review
description: Audit code for security vulnerabilities, injection risks, hardcoded secrets, and proper input validation.
---

> **[Orchestrator Instructions]** Do NOT execute this skill yourself. You MUST use the invoke_subagent tool to spawn an independent subagent with the Role: **Security Auditor**.


## Step 1: Automated Tool Scanning
Before performing a manual review, you MUST run standard security auditing tools based on the tech stack. If a tool is not installed globally, attempt to use `npx` or the native package manager to run it ephemerally.
1. **Dependency Audit**: Run `npm audit`, `yarn audit`, `cargo audit`, or `pip-audit`.
2. **SAST / Secret Scanning**: If available, run tools like `trufflehog`, `semgrep`, or `gosec`.
Save the raw output of these tools for your analysis.

## Step 2: Information Gathering
Gather the code and commit history to audit:

```bash
git diff main..HEAD 2>/dev/null || git diff master..HEAD
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git status
```

If $ARGUMENTS is provided, also read that specific file or directory.

## Step 3: Dual-Review Audit
Perform a comprehensive security audit combining the tool results and your contextual code review.

### A. Evaluate Tool Output
Review the raw output from Step 1. Filter out false positives and summarize the legitimate CVE risks.

### B. Contextual Code Review
Read the `git diff` to identify logic vulnerabilities that automated tools cannot catch. Cover the following areas:

## Injection
- SQL injection, command injection, LDAP injection
- Template injection, path traversal

## Authentication & Authorization
- Missing auth checks, broken access control
- Insecure session handling, JWT misuse

## Secrets & Data Exposure
- Hardcoded credentials, API keys, tokens in code
- Sensitive data logged or exposed in error messages
- PII without encryption at rest or in transit

## Input Validation
- Missing or bypassable validation on user input
- Unsafe deserialization, type confusion

## Dependencies
- Outdated packages with known CVEs (check package.json / requirements.txt / go.mod if present)

## Format each finding as:
`🔴 [OWASP category] file:line — risk — remediation`

End with a risk summary: Critical / High / Medium / Low findings count and top recommendation.

**CRITICAL**: Write your entire security report to `.harness/reports/security-review.md`. Your chat response must ONLY be the path to this file. Do NOT output the report text in the chat.
