---
name: cloud-devsecops-sast
description: "Cloud Devsecops Sast."
domain: cybersecurity
---

|
| SAST | Static Application Security Testing — analyzes source code without executing it to find security vulnerabilities |
| SARIF | Static Analysis Results Interchange Format — standardized JSON format for expressing results from static analysis tools |
| CodeQL | GitHub's semantic code analysis engine that treats code as data and queries it for vulnerability patterns |
| Semgrep | Lightweight static analysis tool using pattern matching to find bugs and security issues across many languages |
| Security Extended | CodeQL query suite that includes additional security queries beyond the default set for deeper analysis |
| Quality Gate | Automated checkpoint that blocks code from progressing through the pipeline unless security criteria are met |
| False Positive | A scan finding that incorrectly identifies secure code as vulnerable, requiring suppression or tuning |

## Tools & Systems

- **CodeQL**: GitHub's semantic code analysis engine with deep dataflow and taint tracking analysis
- **Semgrep**: Fast, lightweight pattern-matching SAST tool with 3000+ community rules and custom rule support
- **GitHub Advanced Security**: Platform providing code scanning, secret scanning, and dependency review in GitHub
- **SARIF Viewer**: VS Code extension for reviewing SARIF results locally during development
- **GitHub Security Overview**: Organization-level dashboard aggregating security alerts across all repositories

## Common Scenarios

### Scenario: Monorepo with Multiple Languages Needs Unified SAST

**Context**: A platform team manages a monorepo containing Python microservices, TypeScript frontends, and Go infrastructure tools. Security reviews happen manually every quarter, missing vulnerabilities between reviews.

**Approach**:
1. Configure CodeQL with a matrix strategy covering Python, JavaScript, and Go languages
2. Add Semgrep with `--config auto` to detect language automatically and apply relevant rulesets
3. Create path-based triggers so only changed language directories trigger their respective scans
4. Upload all SARIF results to GitHub Security tab with unique categories per tool and language
5. Set branch protection requiring all SAST jobs to pass before merge
6. Schedule weekly full-repository scans to catch issues in unchanged code from newly published CVE patterns

**Pitfalls**: Setting CodeQL to analyze all languages on every PR increases CI time significantly. Use path filters to trigger only relevant language scans. Semgrep's `--config auto` may enable rules that conflict with CodeQL findings, creating duplicate alerts.

### Scenario: Reducing Alert Fatigue from High False Positive Rate

**Context**: After enabling SAST, developers ignore findings because 40% are false positives, undermining the security program.

**Approach**:
1. Export all current alerts and categorize them as true positive, false positive, or informational
2. Create a custom CodeQL config excluding noisy query IDs that produce the most false positives
3. Write `.semgrepignore` patterns for test files, generated code, and vendored dependencies
4. Establish a weekly triage meeting where security and development leads review new rule additions
5. Track false positive rate as a metric and target below 15% for developer trust

**Pitfalls**: Over-suppressing rules to reduce noise can create blind spots. Always validate suppressions against the OWASP Top 10 and CWE Top 25 to ensure critical vulnerability classes remain covered.

## Output Format

```
SAST Pipeline Scan Report
==========================
Repository: org/web-application
Branch: feature/user-auth-refactor
Scan Date: 2026-02-23
Commit: a1b2c3d4

CodeQL Results:
  Language    Queries Run   Findings   Critical   High   Medium
  javascript  312           4          1          2      1
  python      287           2          0          1      1

Semgrep Results:
  Ruleset          Rules Matched   Findings   Errors   Warnings
  auto             1,847           3          1        2
  owasp-top-ten    186             2          1        1
  custom-rules     12              1          0        1

QUALITY GATE: FAILED
  Blocking findings: 2 Critical/High severity issues
  - [CRITICAL] CWE-89: SQL Injection in src/api/users.py:47
  - [HIGH] CWE-79: Cross-site Scripting in src/components/Search.tsx:123

Action Required: Fix blocking findings before merge is permitted.
```
