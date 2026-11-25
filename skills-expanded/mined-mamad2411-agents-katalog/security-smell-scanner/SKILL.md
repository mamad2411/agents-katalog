---
name: security-smell-scanner
description: "Security smell scanner: statically detects 10 families of security anti-patterns across a codebase (SQL injection, XSS, command injection, path traversal, hardcoded credentials, insecure defaults, IDOR, open redirect, TOCTOU, missing input validation). Produces an evidence-backed report with severity, location, and contextual analysis. Read-only. Audience: Senior > Vibe. Cross-link from quality/ cluster. Trigger: /security-scan"
trigger: /security-scan
---
## What this is for

Security vulnerabilities don't always come from one bad line - they come from
**recurring patterns**: unsanitized input in SQL strings, innerHTML without
escaping, user-controlled file paths, exec() calls with string interpolation,
hardcoded credentials, or security features explicitly disabled.

This skill finds those patterns statically. It combines a deterministic collector
(regex-based heuristics for 10 pattern families) with LLM context analysis that
validates each finding, filters false positives, and produces an actionable
security-smell report.

**Audience:** Senior > Vibe
- Seniors use it as a systematic pre-PR review and a way to prove absence of
  common patterns before an audit.
- Vibe-coders get an "idiot-proofing" pass: the LLM explains what's wrong and
  what to do about it, so every finding is a learning opportunity.

### Trigger: `/security-scan`

Intervention-free static analysis. The collector reads only - never writes,
never executes the target code, never connects to a network.

## PROTECTION RULE - never `~/.claude/`

This skill analyzes foreign projects. It is read-only. The protection guard
is still active: if the skill ever gets a write mode, the guard from
The protection guard (target path validation) must be implemented.

## What You Must Do When Invoked

### Step 1 - `-help`/`-h` check
If invoked with `-help` or `-h`, print the usage block below and stop.

### Step 2 - Confirm `-ProjectDir`
If not provided, prompt the user. Confirm the path exists. Print:
`Security smell scan on <path> ...`

### Step 3 - Run Collector
```powershell
& .\scripts\security-scan.ps1 -ProjectDir "<path>"
```

Parse the JSON output. If exit code ? 0, report error and stop.

### Step 4 - LLM Context Analysis
For each finding in the JSON:
1. Read the `context` snippet (3 lines before + 3 lines after the evidence line).
2. Determine if this is a **true positive**, **false positive**, or **uncertain**.
3. Assign confidence: `proven`, `likely`, `suspected`.
4. For `hardcoded-creds` findings: redact the value in your output.
   Show only `[REDACTED]` - never the actual credential.
5. For SQL/command injection: check if the code path is reachable from a
   public entry point (HTTP handler, CLI command, message consumer).

### Step 5 - Produce Report
Write `security-smell-report.md` to the working directory:

```
# Security Smell Report - <project-name>

## Executive Summary
- <count> findings: <n> high, <m> medium, <p> low
- Risk level: critical / elevated / moderate / low

## Critical Findings (high confidence + high severity)
| # | File | Line | Pattern | Evidence (truncated) | Suggested Fix |
|--|---|---|-----|-----------|--------|
...

## Medium Findings
Grouped by pattern family. Each entry: file, line, confidence, evidence.

## Low / Informational
Stuff worth knowing but not blocking.

## False Positives (matched by heuristics, dismissed by LLM)
| File | Line | Pattern | Dismissal Reason |
|---|---|-----|---------|

## Open Questions (uncertain - needs manual review)
| File | Line | Pattern | Why Uncertain |
|---|---|-----|-------|

## Pattern Coverage
Applied: sql-injection, xss, command-injection, path-traversal, hardcoded-creds,
insecure-defaults, idor, open-redirect, toctou, missing-input-validation.
```

### Step 6 - Console Summary
After writing the file, print a short summary:
```
=== Security Smell Scan Complete ===
  Findings: <n> (high: <x>, medium: <y>, low: <z>)
  False positives dismissed: <m>
  Report: security-smell-report.md
```

## Usage

```
/security-scan                   # interactive, prompts for directory
/security-scan /path/to/project  # scan project directory
/security-scan -help            # show this usage info
```
