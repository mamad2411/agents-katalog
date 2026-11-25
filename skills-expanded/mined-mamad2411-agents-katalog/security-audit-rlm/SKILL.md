---
name: security-audit-rlm
description: Run and troubleshoot privacy-preserving, local DSPy RLM security audits for large legacy .NET codebases. Use when asked to scan repositories for vulnerabilities, tune RLM/tool limits, fix truncation/stall issues, or produce actionable markdown/json audit outputs without loading entire codebases into model context.
---

# Security Audit RLM

Use this skill to operate `audit.py` as a tool-driven RLM workflow for large repositories.

Repository: `https://github.com/mitkox/megacode`

## Execute

1. Verify prerequisites:
   - `deno --version`
   - model endpoint is reachable (default `http://localhost:8000/v1`)
2. Run a baseline audit:
   - `AUDIT_VERBOSE=1 python audit.py --source-root <repo-path>`
3. Confirm outputs:
   - `security_audit_report.md`
   - `security_audit_metadata.json`
   - `security_audit_manifest.jsonl`

## Tune For Large Legacy Repos

- Lower planner churn:
  - `--max-iterations 8..12`
  - `--rlm-max-llm-calls 60..100`
- Bound REPL noise:
  - `--rlm-max-output-chars 15000..30000`
- Bound tool payloads:
  - `--tool-max-lines 200..400`
  - `--tool-max-chars 20000..40000`
  - `--search-max-files 800..2000`
  - `--search-max-matches 200..600`
- Control runtime:
  - `--timeout-seconds 600..1800`
  - `--retries 1..2`

## Operating Rules

- Keep analysis local when privacy constraints require it.
- Use RLM tool access, not full-context repository injection.
- Keep intermediate output concise and deterministic.
- Prioritize high-severity findings with file/line evidence and concrete fixes.

## Troubleshooting

- If run appears stalled:
  - enable verbose mode
  - reduce `--max-iterations`
  - reduce `--rlm-max-output-chars`
- If model truncates:
  - raise `--lm-max-tokens` if backend supports it
  - reduce tool output and iteration count
- If path/file access errors appear in RLM steps:
  - ensure tool-only repository access is used by the audit flow
  - re-run after confirming current `audit.py` includes `list_manifest/read_file/search_pattern` tools

## Deliverable Format

Ensure report sections remain:

1. Executive Summary
2. Critical Findings (CRITICAL/HIGH)
3. Other Findings (MEDIUM/LOW)
4. Remediation
