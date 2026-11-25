---
name: finding-synthesis
description: Merge findings from architecture, security, performance, and style reviewers into a single prioritised report. Reads _workspace/{architecture,security,performance,style}_findings.md, dedupes overlapping findings across reviewers, sorts by severity and category, and writes a final report. Invoked by the report-synthesizer agent at the end of any code-review or code-development workflow; trigger via "merge the findings", "synthesize the review", "produce the final report", "consolidate", or "combine review results".
---

# Finding synthesis

You are consolidating findings from four parallel reviewers into a single
report. Your job is dedup + prioritisation + presentation — NOT
re-reviewing.

## Inputs

Read all four:

- `_workspace/architecture_findings.md`
- `_workspace/security_findings.md`
- `_workspace/performance_findings.md`
- `_workspace/style_findings.md`

If any file is missing, note it in the report's header under
"Reviewer failures" — proceed with the rest. Do NOT invent findings
from a missing reviewer.

## Output

Write the final report to `_workspace/report.md`. Structure:

```markdown
# Code review report

- **Scope:** {from the reviewers' headers — should match}
- **Generated at:** {ISO-8601 UTC}
- **Reviewers run:** {list of 4; any missing flagged explicitly}
- **Total findings:** {N} ({critical} critical, {high} high, {medium} medium, {low} low, {info} info)

## Summary

3-6 sentence executive summary. Name the top 1-2 most important findings.
No list of every finding. No "everything looks great" padding — if
there are zero findings, say so in one sentence and stop.

## Critical findings

One finding per section, full detail. Omit the heading entirely if
there are none.

## High-priority findings
## Medium-priority findings
## Low-priority findings
## Informational

{All findings, in severity order; within a severity, by category
(architecture → security → performance → style) then file path.}

## Cross-cutting concerns

Only include if 2+ reviewers flagged variations of the same issue.
State the consolidated concern once, note which reviewers saw it, and
cross-link to the individual findings. 0-3 items expected.

## Reviewer stats

| Reviewer | Findings | Time |
|---|---|---|
| architect | {N} | — |
| security | {N} | — |
| performance | {N} | — |
| style | {N} | — |
```

## Dedup rules

Two findings are duplicates if they point at the same `file:line` range
AND describe the same concern. When deduping:

1. **Keep the highest severity**. If security flags `critical` and
   architect flags `medium` on the same line, it's `critical`.
2. **Merge the descriptions** into a single paragraph that preserves
   each reviewer's angle. Attribute: "(security + architect)".
3. **Merge suggestions**. If they conflict, present both and mark
   "REVIEW: reviewers disagreed".

Do NOT dedupe findings that HAPPEN to be in the same file but describe
different concerns — those stay separate.

## Re-ranking

After dedup, sort by severity then category then file path. Then
cross-check against the severity guide in `references/severity-guide.md`
— if a finding feels over- or under-ranked, adjust and note "(synth
re-ranked from {original})".

The goal is a report the user can act on in order from top to bottom.
Critical first. Info last. Anything below `low` is safe to skim.

## Hard rules

- **Don't add your own findings.** If you notice something the
  reviewers missed, write it as a new finding and label its reviewer
  as "synthesiser (cross-cutting)" — but only if it genuinely
  bridges multiple reviewer outputs.
- **Don't soften or sharpen** without noting the change. Re-ranking
  IS visible in the output.
- **Don't paraphrase findings into your own words** for individual
  items. Keep the original descriptions intact in the final listing.
  You're a librarian, not a re-reviewer.
- **Do fix obvious issues**: broken markdown, inconsistent severity
  labels (e.g. one reviewer wrote "High" instead of "high"),
  schema deviations that make the report unreadable.
