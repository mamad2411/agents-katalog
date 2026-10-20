# Claude Code & Cursor at Solo Tier

## Summary

**One-sentence:** Generates a solo-developer AI-pair-coding loop spec: model + IDE choice, repo conventions, prompt budget, and a spec-driven workflow for Claude Code and Cursor.

**One-paragraph:** At the Solo tier the developer codes with Claude Code or Cursor against their own SaaS. This methodology codifies the AI-pair-coding loop: model selection (Opus for design/creative; Sonnet for routine), IDE choice (Claude Code for terminal-native; Cursor for inline edit), repo conventions (CLAUDE.md / AGENTS.md / CONVENTIONS.md), prompt-budget discipline (≤2K tokens of context per task), and the spec-driven workflow that prevents 'AI wrote 800 LOC nobody understands'. Output: a per-repo Solo AI-pair config + a workflow checklist.

**Ефективно для:**

- Solo SaaS builder adopting Claude Code or Cursor for the first time.
- Migrating off GitHub Copilot's vanilla inline-only flow.
- Configuring repo conventions so AI sessions stay consistent.
- Cap-discipline: keep monthly LLM spend on prompts predictable.

## Applies If (ALL must hold)

- Operator codes solo (no team workflow to coordinate).
- Repo is small to medium (≤200K LOC).
- Operator has a Claude or Cursor subscription on the Solo plan.
- Operator has authority to add CLAUDE.md / AGENTS.md to the repo.

## Skip If (ANY kills it)

- Team of ≥3 — coordination overhead requires Pro-tier methodologies.
- Pre-revenue exploration phase where structure is premature.
- Operator using a sealed enterprise IDE that cannot run Claude Code / Cursor.
- Operator's repo has no convention surface (Python notebook scratchpads only).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo root access | ability to add CLAUDE.md / AGENTS.md | operator |
| Active subscription | Claude or Cursor Solo-tier active | operator |
| Primary task type | what kind of tasks dominate (refactor / new feature / bug fix) | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[freelancer-discovery-call-template]] | BA discipline before building |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-instance judgment. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-code-and-cursor-at-solo-tier.json` | JSON skeleton for the Solo AI-pair-config artefact |
| `templates/claude-code-and-cursor-at-solo-tier.md.j2` | Markdown checklist for the workflow |
| `templates/claude-code-and-cursor-at-solo-tier.md` | Markdown checklist for the workflow Generated from `templates/claude-code-and-cursor-at-solo-tier.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-code-and-cursor-at-solo-tier.py` | Validate claude-code-and-cursor-at-solo-tier artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[freelancer-discovery-call-template]]

## Decision tree

See `content/06-decision-tree.xml`. Gates on convention-file presence first; without it the loop produces token-burn. Otherwise routes by task type to model + context-budget rule.
