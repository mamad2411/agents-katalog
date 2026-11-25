---
name: project-llm-wiki
description: Use when creating, auditing, or maintaining a schema-driven Project-LLM-Wiki system with a lightweight development harness, raw source intake, durable project wiki, and runtime wiki graph checks for AI coding agents.
---

# Project-LLM-Wiki

Use this skill to help a codebase become AI-maintainable through two durable
layers:

- `.harness/`: how AI agents should develop, verify, and update knowledge.
- `.project-wiki/`: what durable project knowledge is true, sourced, and worth
  preserving.
- `raw/`: optional unstructured source intake before wiki promotion.
- runtime wiki graph: a disposable graph derived from `.project-wiki/`
  metadata for related-knowledge traversal and wiki health checks.

The goal is not to write more docs. The goal is to create a maintenance loop:

```text
task -> harness routing -> wiki lookup -> code verification -> implementation -> verification -> wiki/harness update
```

## Core Principles

- Current code is the immediate source of truth.
- Backward compatibility is usually the highest production risk.
- Architecture mistakes are high risk.
- Historical docs are not automatically true.
- Keep entry files short; they should launch the harness, not contain it.
- Prefer progressive development: easiest valid step first, one main variable at
  a time.
- Keep UI, code, and process minimal.
- Surface material uncertainty before encoding it into code or wiki.

## Workflow

1. Inspect the target repository's current AI entry files:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `CODEX.md`
   - Cursor or other agent rules
2. Inspect current docs, historical notes, skills, prompts, plans, and README
   files.
3. Create or update `.harness/` from `assets/templates/.harness/`.
4. Create or update `.project-wiki/` from `assets/templates/.project-wiki/`.
5. Keep root entry files as launchers into `.harness/index.md`.
6. Classify existing knowledge sources as:
   - `current`
   - `historical`
   - `conflict`
   - `needs-verification`
   - `raw`
7. Seed only high-value, verified project knowledge into `.project-wiki/`.
8. Add lightweight verification scripts when the repository is ready for
   mechanical checks.
9. Preserve rough transcripts, audits, notes, and research in `raw/` before
   promoting claims into structured wiki entities.
10. Use the runtime wiki graph helper when a task needs related wiki entities,
    source paths, or link health checks.

## Bundled Scripts

Use these scripts from the skill root when the repository has this skill
installed, or from this repo during local development:

```bash
node scripts/init-project-llm-wiki.mjs /path/to/target-repo
node scripts/verify-project-llm-wiki.mjs /path/to/target-repo
node scripts/wiki-graph.mjs /path/to/target-repo
node scripts/wiki-graph.mjs /path/to/target-repo --seed feature.example
```

The runtime graph is generated from Markdown entity metadata and is disposable.
Fix graph issues by editing `.project-wiki/` pages, not by preserving generated
graph output.

## Read As Needed

- For the full method: `references/method.md`
- For wiki entity schema: `references/schema.md`
- For harness design: `references/harness.md`
- For migrating old docs or skills: `references/migration.md`

## Output Expectations

When applying this skill to a repository, produce:

- a concise implementation plan
- the `.harness/` structure
- the `.project-wiki/` structure
- seed wiki pages for the highest-risk current knowledge
- a migration map for old docs or skills
- verification commands or scripts appropriate to the repo
- raw source preservation when useful
- runtime wiki graph results or warnings when useful

Do not copy project-specific rules from one codebase into another unless they
are clearly generic.
