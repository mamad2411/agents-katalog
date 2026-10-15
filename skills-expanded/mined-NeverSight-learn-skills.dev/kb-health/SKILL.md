---
name: kb-health
description: Run a deep health check on a Karpathy-style Obsidian knowledge base. Use this skill whenever the user says "kb health", "health check", "lint wiki", "find contradictions", "find orphan notes", "stale claims", "broken wikilinks", "missing cross references", "my notes feel disconnected", "my wiki is outdated", "broken Obsidian rendering", "malformed index", "检查知识库", "知识库体检", "笔记越来越乱", or wants a periodic maintenance pass over a compiled wiki, including stale Q&A, alias drift, duplicate entities, search-upgrade recommendations, and mechanical Obsidian rendering problems. Prefer this skill over the package router when the main request is maintenance, drift diagnosis, or lint-and-repair rather than setup or compilation.
---

# KB Health

Deep lint and maintenance workflow for a compiled knowledge base.

Use this skill for scheduled quality review, not for routine ingestion. `kb-compile` may run a lightweight post-compile sanity check, but `kb-health` owns the full diagnosis.

## Read before running

Read these shared references first:

- `../obsidian-notes-karpathy/references/file-model.md`
- `../obsidian-notes-karpathy/references/health-rubric.md`
- `../obsidian-notes-karpathy/references/lifecycle-matrix.md`
- `../obsidian-notes-karpathy/references/schema-template.md`
- `../obsidian-notes-karpathy/references/search-upgrades.md`
- `../obsidian-notes-karpathy/references/activity-log-template.md`
- `../obsidian-notes-karpathy/references/obsidian-safe-markdown.md`

Then read the vault's local `AGENTS.md` and `CLAUDE.md` if present.

If `../obsidian-notes-karpathy/scripts/lint_obsidian_mechanics.py` exists, run it first. Treat its JSON output as the deterministic baseline for mechanical issues such as alias-style wikilinks inside table cells, duplicate concept aliases, stale Q&A flags, broken wikilinks, and orphan pages before you do the deeper rubric-based audit.

If one or more shared references are missing, continue with the minimum compatible contract and surface the missing files in the report summary. Missing support files are part of the diagnosis, not an excuse to skip the pass.

## Scope

Inspect primarily the compiled and generated layers:

- `wiki/`
- `outputs/qa/`
- `outputs/health/`

Reference `raw/` only when provenance or staleness requires a spot check.

Do not rewrite `raw/`.

## Audit checklist

Evaluate the knowledge base across these dimensions:

1. Consistency
   - conflicting definitions across concept pages
   - alias drift or duplicate concepts that should likely be merged
   - duplicate entities that should likely be merged
   - claims superseded by newer sources or newer Q&A
2. Completeness
   - sparse concept pages
   - sparse entity pages
   - summaries missing key concepts, evidence, or source metadata
   - major topics present in sources but absent from concept or entity pages
3. Connectivity
   - orphan summaries
   - orphan concepts
   - orphan entities
   - orphan Q&A notes
   - weakly linked clusters
   - missing obvious wikilinks or reciprocal `related` fields
4. Freshness
   - concepts or entities not updated for a long time despite new relevant sources
   - old Q&A that should be superseded or annotated
5. Provenance
   - concept or entity pages without enough source backing
   - archived answers with weak evidence trails
   - summaries that make claims without concrete support
6. Asset integrity
   - missing local image references
   - image references that are never reviewed even though they likely affect understanding
7. Syntax and render integrity
   - alias-style wikilinks inside Markdown table cells
   - malformed tables that render incorrectly in Obsidian
   - generated markdown that looks plausible in plain text but breaks Obsidian navigation or layout
8. Search posture
   - whether markdown-first navigation is still sufficient
   - whether the vault now justifies Backlinks/Properties discipline, qmd, DuckDB, or full vector retrieval

## Output

Write a report to `outputs/health/health-check-{date}.md` using the rubric from `../obsidian-notes-karpathy/references/health-rubric.md`.

The report must include:

- overall score out of 100
- sub-scores for Completeness, Consistency, Connectivity, Freshness, and Provenance
- critical issues
- warnings
- suggested follow-up questions or source gaps
- search upgrade recommendation
- explicit fixes the LLM can perform now versus items that need human judgment

## Remediation posture

- Fix safe, mechanical issues immediately when the user asked you to lint and repair:
  - add missing wikilinks
  - repair obvious reciprocal relations
  - update derived indices
  - normalize clearly duplicated aliases into one concept or entity page when the mapping is unambiguous
  - annotate clearly stale Q&A with updated context when the evidence is obvious
  - replace alias-style wikilinks inside Markdown table cells with plain wikilinks or standard Markdown links when the target is unambiguous
- Put uncertain but probably good fixes under `Propose Fix`.
- Do not silently rewrite disputed claims. Flag them and preserve provenance.

## Log the maintenance pass

After writing the report, append a `health` entry to `wiki/log.md` using `../obsidian-notes-karpathy/references/activity-log-template.md`.
