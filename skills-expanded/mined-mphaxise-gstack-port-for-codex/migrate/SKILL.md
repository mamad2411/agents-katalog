---
name: migrate
description: GBrain-inspired migration workflow for Codex. Use when importing notes, markdown, wiki exports, or structured files into a Codex-side package or tracker.
---

# Migrate

Use this skill when the user wants to move content from another note or wiki system into a Codex-friendly layout.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Workflow

1. Assess the source:
   - markdown
   - CSV
   - JSON
   - Notion export
   - Obsidian or Logseq vault
2. Define the target structure in Codex terms:
   - docs
   - task trackers
   - reports
   - future memory-substrate inputs
3. Test on a small sample first.
4. Verify the sample by reading it back from the target structure.
5. Only then migrate the broader set.

## Current Upstream Coverage

Support Obsidian, Notion, CSV, and generic Markdown imports through a source-specific mapping plan. Preserve originals, migrate a representative sample first, verify field and link fidelity, then run the full import with a reconciliation report.

## Guardrails

- Never modify or destroy the source data.
- Do not bulk-import before a sample pass succeeds.
- Keep the mapping explicit so future updates are repeatable.
