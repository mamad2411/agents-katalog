---
name: semgrep-scanning
description: Run Semgrep scans with curated rulesets, filter by severity, produce SARIF, and wire scans into CI. Use when the user wants to find vulnerabilities or policy violations in their own code.
---

# Semgrep scanning

Semgrep is a fast, local SAST engine. Nothing leaves the machine unless you opt
into the platform (`semgrep ci` or `semgrep login`).

## Core commands

```bash
semgrep scan                             # current dir, default rules
semgrep scan --config auto               # rules picked per detected languages
semgrep scan --config p/security-audit   # curated security ruleset
semgrep scan --config p/owasp-top-ten
semgrep scan --config p/secrets          # hardcoded credentials
semgrep scan --config p/default src/     # limit to a path
semgrep scan --config rules/my-rules.yaml  # local rule file or dir
```

Stack configs: repeat `--config` to merge rulesets. Registry rulesets use the
`p/<name>` shorthand; browse them at https://semgrep.dev/r.

Note: `--config auto` sends package/project metadata to the registry to select
rules. For fully offline scans, pin explicit rulesets or local rule files.

## Filtering and output

```bash
semgrep scan --severity ERROR                 # ERROR | WARNING | INFO
semgrep scan --json --output findings.json
semgrep scan --sarif --output findings.sarif  # loads in SARIF viewers / code hosts
semgrep scan --error                          # exit 1 when findings exist
```

Exit codes: `0` clean, `1` findings (with `--error`), other nonzero values are
scan failures. This makes gating trivial in any CI.

## Suppressions

- Inline: append `# nosemgrep: <rule-id>` on the offending line (language
  appropriate comment). Always include the rule id, never bare `nosemgrep`.
- Path-level: `.semgrepignore` at repo root (gitignore syntax). Semgrep skips
  `.git` and common vendored dirs by default.
- Review suppressions in PRs like any other security decision.

## CI usage

Plain CLI (no account needed):

```yaml
- run: pip install semgrep
- run: semgrep scan --config p/security-audit --sarif --output semgrep.sarif --error
```

Platform-connected (diff-aware scans, PR comments, findings dashboard):

```bash
export SEMGREP_APP_TOKEN=<token>   # from the Semgrep AppSec Platform
semgrep ci
```

`semgrep ci` scans only changed files on PR branches (diff-aware), full scans
on the default branch, and reports findings to the platform. Upload the SARIF
to your code host's code scanning UI so findings annotate PRs.

## Triage order

1. `ERROR` severity findings on injection, deserialization, authz checks.
2. Secrets findings: rotate the credential first, then delete it from code.
3. `WARNING` findings on code that touches untrusted input.
4. Everything else goes into a tracked backlog, not a silent ignore.

## Via the MCP server

The bundled server (`semgrep mcp`, stdio by default) exposes scan tools, custom
rule scans, AST dumps, and platform findings retrieval. Same rule syntax, same
local execution; useful when you want scans inside an agent loop with results
returned as structured data.
