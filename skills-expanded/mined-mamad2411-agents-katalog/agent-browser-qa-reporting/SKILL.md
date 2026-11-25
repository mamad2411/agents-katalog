---
name: agent-browser-qa-reporting
description: "Create browser QA handoffs with coverage, evidence, severity, verdicts, and retest gaps."
---

# Agent Browser QA Reporting

Use this skill to turn `agent-browser` dogfood, pre-QA validation, focused reproduction, or fix-verification output into a clear QA report and tester handoff.

## Trigger boundary

Use it when browser evidence must become a QA handoff with coverage, findings, severity, release verdict, or retest gaps.

Do not load it for a small local check that needs only an immediate pass/fail note and no coverage matrix, evidence index, or handoff; report the result directly.

## Process

1. Confirm the reporting contract: tested scope, target environment, deployment/build, browser or device set, roles, acceptance criteria, artifacts, and who will consume the report.
2. Before any command-sensitive `agent-browser` work, check the installed command surface first:
   - `agent-browser --version`
   - `agent-browser --help`
3. If the installed CLI version supports versioned or local guidance such as `agent-browser skills get core` or `agent-browser skills get dogfood`, load it and treat it as the source of truth for exact commands, flags, artifact paths, and behavior. Older versions may not provide those commands.
4. Treat static CLI examples as patterns only.
5. Build the coverage matrix before writing conclusions. Mark each area as covered, partially covered, blocked, untested, or not applicable, and state why.
6. Normalize findings with type, severity, priority, confidence, reproducibility, evidence, and next verification. Do not file a product bug from tooling failure alone.
7. Redact secrets, PII, tokens, cookies, auth state, authorization headers, tenant-sensitive data, and sensitive payloads before sharing the report or evidence.
8. Separate facts from hypotheses. Keep suspected owners and root-cause notes provisional unless implementation evidence confirms them.

## Output Standard

Every QA report should include:

- summary and release or QA verdict
- coverage matrix and untested or blocked areas
- findings grouped by severity, with evidence references
- environment and deployment metadata
- evidence index with redaction status
- regression follow-up or retest scope when fixes are involved

Every actionable finding should include title, environment, steps, expected result, actual result, evidence, scope or impact, suspected owner, repro confidence, and suggested next verification.

## Coordination

Use with `agent-browser-dogfood-workflow` when the session still needs exploration or coverage expansion. Use with `agent-browser-diagnostics-evidence` when findings need stronger console, network, screenshot, video, HAR, trace, profiler, or Web Vitals evidence. Use with QA, security, accessibility, performance, or framework-specific skills when the report identifies deeper specialist risks.

## Reference Routing

- Coverage matrix, finding classification, severity, priority, confidence, and minimum finding fields: read [01-coverage-findings-taxonomy.md](./references/01-coverage-findings-taxonomy.md).
- Report structure, QA handoff, evidence index, verdict language, and sensitive-data rules: read [02-report-template-handoff.md](./references/02-report-template-handoff.md).
- Regression retest scope, fixed-versus-new classification, closure proof, and reopen criteria: read [03-regression-follow-up.md](./references/03-regression-follow-up.md).

## Command Version Policy

- Before command-sensitive `agent-browser` work, run `agent-browser --version` and `agent-browser --help` to identify the installed command surface.
- If that CLI version supports versioned or local guidance such as `agent-browser skills get core` or `agent-browser skills get dogfood`, load it and treat it as the source of truth for exact syntax, flags, output paths, and behavior.
- Older CLI versions may not provide `skills get`; do not require those commands as always available.
- Treat command snippets as patterns. Installed local guidance wins when syntax, flags, output paths, or behavior differ.
- Record the `agent-browser` version and report source artifacts when available, but do not depend on memorized command syntax.

## Reporting Rules

- Report user-visible behavior and evidence first, then hypotheses.
- Keep raw artifacts separate from report text. Reference safe artifact paths and summarize only redacted content.
- Do not include secrets, PII, tokens, cookies, auth state, authorization headers, or sensitive business payloads.
- Do not turn blocked setup, stale snapshots, missing test data, CLI failures, or environment outages into product defects unless the app behavior is independently reproduced.
