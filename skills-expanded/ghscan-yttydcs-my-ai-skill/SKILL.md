# m:thesis-aigc-revision Skill Spec

## Architecture Overview

The capability is packaged as `skills/m-thesis-aigc-revision` with one small reference file and one deterministic helper script. The main `SKILL.md` stays trigger-friendly and describes the end-to-end revision workflow.

## Package Contract

- Source package: `skills/m-thesis-aigc-revision`
- UI metadata: `skills/m-thesis-aigc-revision/agents/openai.yaml`
- Install metadata: `manifests/m-thesis-aigc-revision.json`
- Install flow:
  - source -> `dist/codex/m-thesis-aigc-revision` -> `C:\Users\HelloWorld\.codex\skills\m-thesis-aigc-revision`

## Trigger Contract

The skill should trigger when the request is about revising thesis prose that is flagged as overly generic, repetitive, or template-like, especially when the user mentions:

- AIGC report
- suspicious segment summary
- lowering AIGC-like writing signals
- revising thesis paragraphs after a detector report
- Chinese undergraduate thesis polishing with tighter factual grounding

The skill must not position itself as a fabrication or detector-evasion tool.

## Workflow Contract

The skill workflow must require these steps:

1. collect the thesis draft, report, and evidence
2. extract suspicious segments from the report when available
3. map the report segments back to real draft paragraphs
4. diagnose the linguistic cause of each high-risk paragraph
5. rewrite paragraph by paragraph with stronger project anchors and narrower claims
6. re-check implementation boundaries and unsupported claims
7. smooth local section tone after the targeted rewrite

## Reference Contract

- `references/revision-patterns.md` must cover:
  - common high-risk signals
  - rewrite moves
  - section-specific heuristics
  - a final safety checklist

## Script Contract

- `scripts/extract_report_segments.py` must:
  - accept a report HTML path
  - extract suspicious-segment rows from the `疑似AIGC片段汇总` table
  - print index, ratio, word count, and a preview
  - use only the Python standard library

## Output Contract

- Lead with the revision outcome and highest-priority remaining issue.
- For several revised segments, use a compact source-location / risk-signal / status / evidence table.
- Link local source, report, and revised artifacts with absolute clickable paths.
- Keep full before/after prose outside table cells.
- Use Mermaid only when ordering or chapter dependencies are genuinely difficult to follow.

## Validation Contract

- The skill must pass `tools/validate-skills.ps1 -Skill m-thesis-aigc-revision`.
- The skill must sync through `tools/sync-skills.ps1 -Skill m-thesis-aigc-revision`.

## Related Requirements

- [../requirements/m-thesis-aigc-revision-skill.md](../requirements/m-thesis-aigc-revision-skill.md)

## Related Changes

- [2026-07-15 visual output components](../change/2026-07-15_visual-output-components.md)
