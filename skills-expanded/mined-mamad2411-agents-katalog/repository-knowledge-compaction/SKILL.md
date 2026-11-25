---
name: repository-knowledge-compaction
description: Compress repository findings into durable human-readable and machine-readable memory so later agents can reuse repo knowledge efficiently.
---

# Repository Knowledge Compaction

Use this skill after repository exploration or when refreshing an existing repository brief.

## Goals
- Preserve repository knowledge in a compact, reusable form.
- Make later retrieval cheap for both humans and agents.
- Avoid stale or bloated memory artifacts.

## Required Inputs
- Raw repository findings
- Existing repository brief or facts file, if any
- `.ai-team/framework/memory/wiki/repositories/` for existing entries

## Required Outputs
- Updated `brief.md` in `wiki/repositories/<repo-slug>/`
- Updated `facts.yaml` in `wiki/repositories/<repo-slug>/`
- Updated `wiki/repositories/_index.yaml` when needed

## Compaction Rules
- Keep only high-value facts that downstream roles are likely to reuse.
- Prefer stable facts over transient implementation trivia.
- Record source path, revision, and last-updated timestamp in the machine-readable file.
- Use arrays and short strings in `facts.json` so other tooling can parse it easily.
- Archive uncertainty as `open_questions` instead of hiding it inside prose.
