---
description: >
  Lightweight, developer-focused security scan that runs in under a minute. Checks for
  OWASP Top 10 patterns, hardcoded secrets, and known dependency vulnerabilities. Outputs
  a short actionable summary — not a full report. Use this skill when the user asks for a
  quick security check, wants to scan before committing or opening a PR, says 'quick scan',
  'fast security check', 'check my code for security issues', or wants a lightweight
  alternative to the full security suite. Also trigger on: 'is this secure enough to merge',
  'any obvious security issues', 'pre-commit security check', or 'spot check for vulnerabilities'.
---

# Quick Security Scan

A fast, developer-focused security check. Produces actionable findings, not a formal report.

## Scope

This skill checks three things and nothing more.

To keep the scan under a minute, build a scoped file list first. Default to the
files changed against the default branch; fall back to the full tracked file set
only for small repos, and always cap the number of files scanned.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
DEFAULT_BRANCH=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
DEFAULT_BRANCH=${DEFAULT_BRANCH:-main}
MAX_FILES=200

# Prefer changed files vs the default branch; fall back to all tracked files.
if git rev-parse --git-dir >/dev/null 2>&1; then
  BASE=$(git merge-base HEAD "origin/$DEFAULT_BRANCH" 2>/dev/null || git merge-base HEAD "$DEFAULT_BRANCH" 2>/dev/null)
  if [ -n "$BASE" ]; then
    FILES=$(git diff --name-only "$BASE" HEAD)
  fi
  [ -z "$FILES" ] && FILES=$(git ls-files)
else
  # Non-git fallback: walk the current directory.
  FILES=$(find . -type f)
fi

# Drop vendored/generated/test files, then cap the list.
FILES=$(printf '%s\n' "$FILES" \
  | grep -Ev '(^|/)(node_modules|vendor|dist|build|\.git|__pycache__|\.venv|venv)/' \
  | grep -Ev '(^|/)(test|tests|spec|__tests__|fixtures)/' \
  | grep -Ev '\.(min\.js|lock|map)$' \
  | head -n "$MAX_FILES")
FILE_COUNT=$(printf '%s\n' "$FILES" | grep -c .)
```

If more than `MAX_FILES` files would be scanned, note in the summary that the
scan was truncated to the first `MAX_FILES` changed/tracked files so the
sub-minute promise still holds; suggest `/cloudyrion-security:code-review` for an
exhaustive pass.

### 1. OWASP Top 10 Code Patterns

Scan the scoped file list (`$FILES`, built above) for these high-impact patterns:

- **A01 Broken Access Control** — missing auth checks on endpoints, IDOR patterns, directory traversal
- **A02 Cryptographic Failures** — hardcoded keys, weak algorithms (MD5, SHA1 for security), plaintext storage
- **A03 Injection** — SQL concatenation, unsanitized shell commands, template injection, XSS sinks
- **A04 Insecure Design** — missing rate limiting, no CSRF protection, predictable tokens
- **A05 Security Misconfiguration** — debug modes enabled, default credentials, overly permissive CORS
- **A06 Vulnerable Components** — handled by the dependency check in Section 3 below (no source-pattern scan needed here)
- **A07 Auth Failures** — weak password rules, missing MFA, session fixation
- **A08 Data Integrity** — deserialization of untrusted data, missing integrity checks
- **A09 Logging Failures** — sensitive data in logs, missing audit trails
- **A10 SSRF** — unvalidated URLs in server-side requests

Focus on the top-level application code; vendored/generated/test files are already
excluded by the scoping block above. When [semgrep](https://semgrep.dev) is
installed, prefer a fast rule pack over hand-grepping:

```bash
if command -v semgrep >/dev/null 2>&1 && [ -n "$FILES" ]; then
  # Pass the scoped files as positional args (semgrep does NOT read targets from stdin).
  printf '%s\n' "$FILES" | xargs semgrep scan --config p/owasp-top-ten --quiet --error 2>/dev/null || true
fi
```

If semgrep is not installed, fall back to targeted `grep -nEi` searches over `$FILES`
for the patterns above (e.g. `md5(`, `sha1(`, string-concatenated SQL, `eval(`,
`pickle.loads`, wildcard CORS).

### 2. Hardcoded Secrets Detection

Scan for:
- API keys, tokens, passwords in source files (regex below)
- Private keys (RSA, EC, OpenSSH, PGP headers)
- Connection strings with embedded credentials
- `.env` files committed to the repository
- Common secret variable names with literal values (e.g., `password = "..."`, `api_key = "..."`)

Reuse the same secret regex shipped by the plugin's secret-detection hook
(`hooks/hooks.json`) so the quick scan and the hook stay in sync. Run it over the
scoped file list:

```bash
SECRET_RE='(api[_-]?key|api[_-]?secret|password|passwd|secret[_-]?access[_-]?key|secret[_-]?key|access[_-]?token|private[_-]?key|auth[_-]?token)[[:space:]]*[=:][[:space:]]*["'"'"']?[^[:space:]"'"'"']{6,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36,}|sk_(live|test)_[A-Za-z0-9]+|xox[baprs]-|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+'
printf '%s\n' "$FILES" | while IFS= read -r f; do
  [ -f "$f" ] && grep -nEi "$SECRET_RE" "$f" | sed "s#^#$f:#"
done
```

When semgrep is installed, the `p/secrets` rule pack catches additional formats:

```bash
if command -v semgrep >/dev/null 2>&1 && [ -n "$FILES" ]; then
  # Pass the scoped files as positional args (semgrep does NOT read targets from stdin).
  printf '%s\n' "$FILES" | xargs semgrep scan --config p/secrets --quiet --error 2>/dev/null || true
fi
```

### 3. Dependency Vulnerability Check

For each detected package manager:
- **npm/yarn**: Run `npm audit --json` if available (needs a lockfile); for yarn use `yarn audit --json` (note its output schema differs from npm's). Otherwise inspect `package-lock.json` / `yarn.lock`.
- **pip/poetry**: Run `pip-audit` if available, or check against OSV.dev
- **Go**: Run `govulncheck` if available
- **Cargo**: Run `cargo audit` if available
- **Other**: List dependencies and, if an advisory tool is available, flag any with known advisories from recent sources (OSV.dev, GitHub Advisory Database)

If audit tools are not installed, note this and check the lock file manually against known advisory databases (OSV.dev, GHSA).

## Output Format

Print findings directly to the conversation. Do NOT write a report file.

Derive the header fields from the scoping block (works outside a git repo too):

```bash
REPO_NAME=$(basename "$REPO_ROOT")
SCANNED_AT=$(date '+%Y-%m-%d %H:%M:%S %Z')
# FILE_COUNT was computed in the scoping block above.
```

Use this format:

```
## Quick Scan Results

**Repository:** <repo-name>
**Scanned:** <timestamp>
**Files checked:** <count>

### Findings

| # | Severity | Category | File:Line | Issue | Fix |
|---|----------|----------|-----------|-------|-----|
| 1 | HIGH | Injection | src/app.py:42 | SQL string concatenation | Use parameterized query |
| 2 | MEDIUM | Secrets | config.py:15 | Hardcoded API key | Move to environment variable |
| ... | | | | | |

### Dependency Issues

| Package | Version | Advisory (CVE/GHSA) | Severity | Fixed In |
|---------|---------|---------------------|----------|----------|
| lodash | 4.17.19 | CVE-2021-23337 | HIGH | 4.17.21 |
| ... | | | | |

### Summary

- **X** findings across code and dependencies
- **Critical/High:** N items need immediate attention
- **Recommendation:** [one-line next step]
```

For the Advisory column, use whichever identifier the tooling reports — `npm audit`
and OSV.dev often return a GHSA ID with no CVE. Do not invent a CVE when only a
GHSA exists.

If no findings: "No security issues found. Consider running `/cloudyrion-security:suite` for a comprehensive assessment."

## What This Skill Does NOT Do

- No formal report generation (use `/cloudyrion-security:code-review` for that)
- No threat modeling or architecture analysis
- No compliance mapping
- No attack scenario design
- No remediation patches (use `/cloudyrion-security:vibe-patch` for that)
