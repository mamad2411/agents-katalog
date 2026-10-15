---
name: log-redaction-auditor
description: Vendor-neutral skill to audit application logs for potential sensitive-data leakage and redaction coverage.
---

## When to invoke
- You have application logs (text) and want to check whether secrets/PII might be present.
- You want a repeatable, automated check in CI/CD before sharing logs externally.

## Inputs needed
- `--input` path to a log file (UTF-8 text).
- Optional: `--config` path to a JSON config overriding patterns and allowlists.

## Workflow
1. Scan log lines with conservative rules for likely secrets/PII.
2. Apply allowlists (known test keys/domains) to reduce false positives.
3. Emit a JSON report with counts, examples, and line numbers.

## Output format
- JSON written to `--output` with:
  - `summary`: counts by severity and rule.
  - `findings`: list of matches with `severity`, `rule_id`, `line_number`, `match`, and `context`.

## Guardrails
- Do not modify the input logs.
- Avoid printing raw secrets to stdout; only write to output file.
- Provide an allowlist mechanism to reduce false positives.

## Reference code
- `log_redaction_auditor.py` implements the scanner using Python stdlib regex + JSON.
