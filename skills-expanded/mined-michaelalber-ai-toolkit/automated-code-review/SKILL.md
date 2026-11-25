---
name: automated-code-review
audience: team
description: Systematic review execution engine -- transforms structured human review coaching patterns into autonomous review checklists with pass/fail gates, convention detection, and structured finding production. Use when running autonomous code reviews to ensure systematic coverage and consistent quality.
---

# Automated Code Review

> "Inspection at the source is called prevention. Inspection after the fact is called sorting."
> -- W. Edwards Deming

## Core Philosophy

Code review coaching teaches humans how to review; automated code review teaches agents how to
execute reviews systematically — the difference between a textbook and a manufacturing process.
This skill converts the CACR (Challenge-Attempt-Compare-Reflect) coaching framework into an
execution framework: systematic checklists with explicit pass/fail gates that prevent superficial
reviews, and convention detection that calibrates findings to the project's own standards rather
than abstract ideals. A coaching skill teaches a human to ask "did I check error handling?"; this
skill tells the agent exactly HOW — enumerate every fallible call, verify each has an error path,
verify the path handles rather than swallows, verify the message carries diagnostic context.

It does NOT teach review principles — it assumes those from the reviewer and the matching
`<lang>-security-review` skill. It provides the operational framework: checklists, gates, convention
detection, and structured output that turn review knowledge into consistent execution.

**Non-Negotiable Constraints:**
1. SYSTEMATIC COVERAGE — every category is checked against a concrete checklist; the checklist is the floor, never skipped.
2. CONVENTION CALIBRATION — detect the project's conventions before reporting any style finding; external-standard findings on a differing project are false positives.
3. PASS/FAIL GATING — each phase has explicit exit gates; a phase cannot advance until its gate passes.
4. EVIDENCE PER FINDING — every finding carries line numbers + snippet; severity reflects impact in the project's actual context.
5. FALSE-POSITIVE PREVENTION — verify against framework, middleware, and surrounding code before reporting; ambiguous findings are flagged "needs verification."

Full principle table, knowledge-base grounding, detailed phase gates, the finding pipeline, and the
minimum checklists live in `references/conventions.md`.

## Workflow

```
SCAN        Define scope; enumerate files with languages; detect project conventions (procedures in
            references/convention-detection.md). GATE: scope defined, conventions detected, ≥3 files sampled.

ANALYZE     Read each file completely. Run all five category checklists per file (floor in
            conventions.md; detail in review-checklist-engine.md). The maintainability category
            uses the Fowler code smell catalog (references/code-smells.md) as its canonical
            checklist, with the "repo overrides" suppression rule. Record findings via the finding
            pipeline. GATE: every file analyzed, every category checked, every finding has evidence +
            severity + false-positive check.

SYNTHESIZE  De-duplicate, cross-reference, rank by severity, group into themes. GATE: consolidated
            list false-positive reviewed.

REPORT      Produce structured output (templates in references/output-templates.md). GATE: every
            finding has evidence/category/severity/fix; ordered critical-first; positives + stats included.
```

**Exit criteria:** all five categories evaluated for every in-scope file against detected
conventions; every finding evidenced and severity-justified; false positives filtered; structured
report produced with positive observations and statistics.

## State Block

```
<automated-review-state>
phase: SCAN | ANALYZE | SYNTHESIZE | REPORT | COMPLETE
scope: [diff | files | directory | PR]
conventions_detected: true | false
files_total: [N]
files_analyzed: [N]
findings: [count by severity — C/H/M/L/Nit]
false_positives_filtered: [N]
last_action: [description]
next_action: [description]
</automated-review-state>
```

## Output Template

- **Per-file analysis log, consolidated report, review statistics** — `references/output-templates.md`.
- **Detailed per-category checklists, pass/fail criteria, language extensions** — `references/review-checklist-engine.md`.
- **Fowler code smell catalog (the maintainability-category checklist) + repo-overrides rule** — `references/code-smells.md`.
- **Convention detection procedures (naming, error handling, logging, testing)** — `references/convention-detection.md`.
- **Principle table, KB lookups, full phase gates, finding pipeline, minimum checklists** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `dotnet-security-review` | Deep, stack-specific OWASP patterns (also `python-`, `php-`, `rust-`, `react-`, `vue-security-review` for those stacks). The security checklist here is a minimum; the language review expands it. |
| `pr-feedback-writer` | Shapes how findings are communicated. After this skill produces findings, pr-feedback-writer frames them as constructive, actionable PR comments. |
