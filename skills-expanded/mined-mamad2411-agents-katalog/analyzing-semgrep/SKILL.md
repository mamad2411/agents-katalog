---
name: analyzing-semgrep
description: |
  Use when working with Semgrep — semgrep static application security testing
  (SAST). Covers code scanning, custom rule creation, CI integration, autofix
  capabilities, multi-language support, and vulnerability triage. Use when
  scanning source code for security vulnerabilities, creating custom detection
  rules, or integrating SAST into CI pipelines.
connection_type: semgrep
preload: false
---

# Semgrep SAST Analysis Skill

Analyze source code for security vulnerabilities, bugs, and anti-patterns using Semgrep.

## MANDATORY: Discovery-First Pattern

**Always check Semgrep version and project languages before running scans.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Semgrep Version ==="
semgrep --version 2>/dev/null

echo ""
echo "=== Project Languages ==="
find . -maxdepth 3 -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" -o -name "*.rb" -o -name "*.php" \) 2>/dev/null | sed 's|.*\.||' | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Semgrep Config ==="
cat .semgrep.yml 2>/dev/null || cat .semgrep.yaml 2>/dev/null || echo "No local config found"

echo ""
echo "=== Available Rulesets ==="
echo "  p/default       - Semgrep default rules"
echo "  p/security-audit - Security-focused rules"
echo "  p/owasp-top-ten - OWASP Top 10"
echo "  p/ci            - CI-optimized rules"
```

## Core Helper Functions

```bash
#!/bin/bash

# Semgrep wrapper with JSON output
semgrep_cmd() {
    semgrep "$@" --json --quiet 2>/dev/null
}

# Scan with specific ruleset
semgrep_scan() {
    local ruleset="${1:-p/default}"
    local target="${2:-.}"
    semgrep --config "$ruleset" "$target" --json --quiet 2>/dev/null
}

# Summary extractor
semgrep_summary() {
    jq '{
        findings: (.results | length),
        by_severity: (.results | group_by(.extra.severity) | map({severity: .[0].extra.severity, count: length})),
        by_rule: (.results | group_by(.check_id) | map({rule: .[0].check_id, count: length}) | sort_by(-.count) | .[0:10])
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--json --quiet` for structured results
- Group findings by rule and severity
- Never dump full file contents -- show finding location and context

## Common Operations

### Security Scan

```bash
#!/bin/bash
TARGET="${1:-.}"
RULESET="${2:-p/security-audit}"

echo "=== Security Scan: $RULESET ==="
semgrep --config "$RULESET" "$TARGET" --json --quiet 2>/dev/null | jq '{
    total_findings: (.results | length),
    files_scanned: (.paths.scanned | length),
    by_severity: (.results | group_by(.extra.severity) | map({
        severity: .[0].extra.severity,
        count: length
    }) | sort_by(.severity)),
    top_findings: [.results | sort_by(.extra.severity) | .[:10][] | {
        rule: .check_id,
        severity: .extra.severity,
        message: .extra.message,
        file: .path,
        line: .start.line,
        fix: (.extra.fix // null)
    }]
}'
```

### OWASP Top 10 Scan

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== OWASP Top 10 Scan ==="
semgrep --config p/owasp-top-ten "$TARGET" --json --quiet 2>/dev/null | jq '{
    total: (.results | length),
    categories: (.results | group_by(.extra.metadata.owasp // "uncategorized") | map({
        owasp: .[0].extra.metadata.owasp,
        count: length,
        examples: [.[:2][] | {rule: .check_id, file: .path, line: .start.line}]
    }) | sort_by(-.count))
}'
```

### Custom Rule Scanning

```bash
#!/bin/bash
RULE_FILE="${1:?Rule file required}"
TARGET="${2:-.}"

echo "=== Custom Rule Scan ==="
semgrep --config "$RULE_FILE" "$TARGET" --json --quiet 2>/dev/null | jq '{
    findings: (.results | length),
    results: [.results[:15][] | {
        rule: .check_id,
        message: .extra.message,
        file: .path,
        line: .start.line,
        code: .extra.lines
    }]
}'

echo ""
echo "=== Rule Validation ==="
semgrep --validate --config "$RULE_FILE" 2>&1 | tail -5
```

### Autofix Preview

```bash
#!/bin/bash
TARGET="${1:-.}"
RULESET="${2:-p/default}"

echo "=== Autofix Available ==="
semgrep --config "$RULESET" "$TARGET" --json --quiet 2>/dev/null | jq '{
    fixable: [.results[] | select(.extra.fix != null) | {
        rule: .check_id,
        file: .path,
        line: .start.line,
        original: .extra.lines,
        fix: .extra.fix
    }] | .[0:10],
    total_fixable: ([.results[] | select(.extra.fix != null)] | length),
    total_findings: (.results | length)
}'

echo ""
echo "=== To apply fixes ==="
echo "semgrep --config $RULESET $TARGET --autofix --dryrun  # Preview"
echo "semgrep --config $RULESET $TARGET --autofix           # Apply"
```

### CI Integration Report

```bash
#!/bin/bash
TARGET="${1:-.}"

echo "=== CI Scan Report ==="
semgrep --config p/ci "$TARGET" --json --quiet 2>/dev/null | jq '{
    pass: ((.results | length) == 0),
    findings: (.results | length),
    errors: (.errors | length),
    files_scanned: (.paths.scanned | length),
    files_skipped: (.paths.skipped | length),
    severity_breakdown: (.results | group_by(.extra.severity) | map({
        severity: .[0].extra.severity,
        count: length
    })),
    blocking: ([.results[] | select(.extra.severity == "ERROR")] | length)
}'
```

## Safety Rules

- **Scans are read-only** unless `--autofix` is used -- autofix modifies source files
- **Use `--autofix --dryrun` first** to preview changes before applying
- **Custom rules should be tested** with known-good and known-bad samples
- **CI integration** should use `p/ci` ruleset which is optimized for low false-positive rate
- **Semgrep App** uploads findings to cloud -- ensure compliance with data policies

## Output Format

Present results as a structured report:
```
Analyzing Semgrep Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Rule performance**: Complex patterns with deep nesting can be slow -- use `--timeout` and `--max-memory`
- **Language detection**: Semgrep auto-detects languages -- incorrect detection causes missed findings
- **Metavariable matching**: Metavariables in rules may match more broadly than expected -- test thoroughly
- **Taint tracking**: Taint mode rules require specific syntax -- not all rules support data flow analysis
- **Ignore files**: Use `.semgrepignore` for test files and generated code -- reduces noise
- **Rule versioning**: Ruleset updates can add new rules that fail CI -- pin ruleset versions
- **Monorepo scanning**: Large monorepos can be slow -- use `--include` to target specific directories
- **JSON output size**: Large codebases produce huge JSON output -- use `--max-target-bytes` to limit
