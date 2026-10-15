---
name: prompt-injection-risk-linter
description: Vendor-neutral skill to lint agent prompts and untrusted retrieved content for prompt-injection risk patterns and missing safety boundaries.
---

## When to invoke
- You are building an agent that reads untrusted content (web pages, emails, tickets) and you want a pre-flight safety lint.
- You want to add an automated check to prompt templates before deployment.

## Inputs needed
- `--prompt` path to a text file containing a system/developer prompt, or combined prompt template.
- Optional: `--retrieved` path to a text file with representative untrusted content.

## Workflow
1. Detect common prompt-injection markers ("ignore previous instructions", requests to reveal hidden prompts, tool/credential exfiltration).
2. Check for missing boundaries (no explicit statement that retrieved content is untrusted; no tool-use constraints).
3. Emit a JSON report with severity, evidence snippets, and recommended mitigations.

## Output format
- JSON report written to `--output`.

## Guardrails
- Heuristics only: do not claim the prompt is safe/unsafe with certainty.
- Avoid printing full prompt contents to stdout.

## Reference code
- `prompt_injection_risk_linter.py` implements a vendor-neutral lint with stdlib regex.
