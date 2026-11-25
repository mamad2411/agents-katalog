# Split ADR files into decision + analysis

## Why

ADR files serve different readers at different stages:
- **Plan/Implementation agents** need only the decision: what was chosen, what constraints it creates. They should NOT waste context on rejected options, detailed rationale, or code examples.
- **ADR reviewers** need the full analysis to verify the reasoning.
- **Developers** scan the decision file for quick reference, and dive into analysis only when they need to understand WHY.

A 500-line ADR with options, pseudocode, and rationale pollutes the context of every downstream agent that reads it. Splitting keeps decision files under 50 lines — compact enough to load all project ADRs at once.

## What to do

For each ADR file in the `docs/adr/` directory that is larger than ~5KB:

1. Read the file
2. Read the templates:
   - Decision template: `assets/adr-decision-template.md`
   - Analysis template: `assets/adr-analysis-template.md`
3. Split the content into two files:

### Decision file (`ADR-{NNN}.md`)

Extract and rewrite into the decision template:
- **Summary** — add if missing. One-sentence Question (what was decided) + one-sentence Decision (what was chosen).
- **Decision** — keep only 2-3 paragraphs with the key trade-offs. Remove detailed rationale, gas calculations, code examples. Those go to analysis.
- **Consequences** — keep as-is (easier / harder / new constraints).
- **Pattern Library Update** — keep as-is.

The decision file MUST be self-contained — a reader should understand the decision without opening the analysis.

### Analysis file (`ADR-{NNN}-analysis.md`)

Move everything else here:
- **Context** — problem description, referenced requirements
- **Existing Patterns** — pattern library analysis
- **Options** — all options with pros/cons/risks
- **Rationale** — detailed comparison, code examples, pseudocode, interface definitions, diagrams, gas analysis

Add a link back to the decision file at the top.

## Rules

- Do NOT change the substance of any decision or consequence
- Do NOT add new content — only reorganize existing content
- Do NOT touch small files (<5KB) — they are likely pre-decided ADRs that don't need splitting
- Preserve all code blocks, diagrams, and formulas exactly as they are
- Keep the same Status (PROPOSED / ACCEPTED / etc.)
