---
name: asvs-security-review
description: Perform security reviews of source code, architecture notes, and API/backend/frontend implementations using OWASP ASVS 5.0. Use this skill when asked to run an ASVS-based review, map findings to ASVS control IDs, prioritize gaps by ASVS level (L1/L2/L3), or produce remediation guidance tied to ASVS requirements.
---

# ASVS Security Review

Use OWASP ASVS 5.0 as the baseline and produce evidence-backed findings mapped to concrete requirement IDs.

## Keep It Right-Sized

- Default to a focused review, not exhaustive certification-style coverage.
- Prioritize controls tied to actual attack surface in the target app.
- Start with the highest-risk gaps first and expand coverage only when asked.

## Inputs To Collect

Collect these inputs before reviewing:
- Target scope: repository, service boundary, or specific modules.
- Target level: `L1`, `L2`, or `L3` (default to `L1` if not provided).
- Runtime context: auth model, data classification, internet exposure, privileged operations.
- Evidence sources: code, config, IaC, CI/CD, docs, API specs, tests.

If level/scope is missing, infer conservatively and state assumptions explicitly.

## Source Of Truth

Use ASVS 5.0 machine-readable files:
- Bundled primary requirements dataset: `references/OWASP_Application_Security_Verification_Standard_5.0.0_en.flat.json`
- Optional external dataset: `<asvs-repo>/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.flat.json`
- Optional chapter markdowns for extra context: `<asvs-repo>/5.0/en/`
- Quick chapter map in this skill: `references/asvs-v5-quick-map.md`

Use `scripts/asvs_lookup.py` to shortlist relevant controls by keyword/chapter/level.
- Default is the bundled dataset; pass `--data` or set `ASVS5_FLAT_JSON` to override.

## Review Workflow

1. Build a threat-aware review focus.
- Map exposed attack surfaces (auth, session/token handling, input validation, file handling, crypto, logging, config, frontend/API boundaries).
- Select likely ASVS chapters first; avoid claiming full coverage unless all chapters are reviewed.

2. Gather implementation evidence.
- Trace code paths and configuration that satisfy or violate controls.
- Prefer concrete evidence: file paths, functions, middleware, schema constraints, test coverage, and security control placement.

3. Map evidence to ASVS requirements.
- For each finding, map to one or more `req_id` values (`Vx.y.z`).
- Include requirement text summary and explain why evidence is compliant/non-compliant/uncertain.

4. Rate severity and confidence.
- Severity: `Critical`, `High`, `Medium`, `Low`.
- Confidence: `High`, `Medium`, `Low` based on evidence quality.
- Mark uncertain items as `Needs validation` instead of assuming pass/fail.

5. Recommend remediation.
- Provide minimal secure code/config changes.
- Tie each remediation directly to ASVS requirement IDs.
- Include verification suggestions (tests, static checks, runtime checks).

## Fast Start For A Web App

Run a quick query when mapping controls:

```bash
scripts/asvs_lookup.py session --chapter V7 --level 2 --limit 10
scripts/asvs_lookup.py jwt --chapter V9 --limit 10
```

For a first-pass review, prioritize chapters usually most relevant to web apps:
- `V1`, `V2`, `V3`, `V4`, `V6`, `V7`, `V8`, `V9`, `V10`, `V12`, `V13`, `V14`, `V16`
- Include `V5`, `V11`, `V15`, `V17` only when those technologies/features are in scope.

## Output Format

Return findings first, then coverage summary.

For each finding use:
- `Title`
- `Severity`
- `ASVS`: list of requirement IDs (for example `V6.2.1`, `V6.2.2`)
- `Level`: applicable ASVS level(s)
- `Evidence`: concrete code/config references
- `Risk`: exploitation impact in this system context
- `Remediation`: specific code/config actions
- `Validation`: how to verify fix

Then include:
- `Coverage Summary`: chapters reviewed, chapters skipped, assumptions.
- `Top Next Checks`: highest-value remaining ASVS checks for this codebase.

## Guardrails

- Do not invent ASVS requirement IDs.
- Do not claim certification/compliance; report observed evidence only.
- Distinguish `Not observed` from `Not implemented`.
- Keep findings actionable and codebase-specific, not generic ASVS advice.
