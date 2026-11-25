---
name: vault-memory
description: Treat the Obsidian vault as operational memory, not just note storage. Focus on retrieval quality, metadata integrity, and safe consolidation.
metadata:
  {
    "version": "1.0.0",
    "author": "openclawgotchi",
    "capabilities": ["retrieval", "memory-integrity", "obsidian", "knowledge-recall"],
    "openclaw": {
      "emoji": "🧠",
      "always": false
    }
  }
---

# Vault Memory

Use this skill when the task is about remembering, recalling, organizing, deduplicating, or validating project knowledge stored in `.workspace/knowledge/`.

This skill is about **memory quality**, not visual note polish.

## Goals

1. Make recall reliable.
2. Keep metadata internally consistent.
3. Preserve stable links and note identities.
4. Avoid creating duplicate notes when extending existing knowledge is better.

## Mental Model

Treat the vault as four layers:

1. `inbox/` - raw intake log
2. `notes/` - atomic working knowledge
3. `projects/` and `topics/` - hub/index layer
4. frontmatter + links + tags - retrieval surface

If recall is poor, first inspect layer 4 before rewriting layer 2.

## Required Invariants

Every operational note should have:

- `id`
- `type`
- `note_type`
- `created`
- `source`
- `project`
- `topic`
- `status`
- `tags`

And these must stay consistent:

- `status` must match a `status/*` tag if such tags are used
- `project` should match the linked project hub when obvious
- `topic` should match the linked topic hub when obvious
- filenames, titles, and links should remain stable unless there is a strong reason to rename

## Retrieval-First Rules

When writing or updating notes, optimize for future retrieval:

1. Prefer explicit titles over clever titles.
2. Put canonical terms in the title or first paragraph.
3. Keep the first 2-4 lines dense with searchable meaning.
4. Preserve important domain terms from the source text.
5. If the note is about a named system, product, or workflow, mention that exact name early.
6. If the same concept appears in multiple languages, keep the original wording somewhere in the note.

## Duplicate Policy

Before creating a new note:

1. Search the vault for the core entity and concept.
2. If an existing note already owns the topic, extend it instead of creating a sibling.
3. Only create a new note when the new material has a distinct purpose:
   - different artifact type
   - different project
   - different time-bounded report
   - different decision or workflow

## What This Skill Should Encourage

- extending an existing note over creating near-duplicates
- fixing metadata drift before large cleanup passes
- validating retrieval assumptions with targeted searches
- keeping raw source excerpts when they improve multilingual recall

## What This Skill Should Avoid

- mass rewrites without an audit step
- changing filenames casually
- flattening everything into tags only
- relying on visual formatting as a substitute for searchable structure
- deleting notes when archiving or merging is safer

## Recommended Workflow

1. Audit:
   - run a vault integrity check
   - inspect status/tag/project/topic mismatches
   - inspect likely duplicates

2. Recall test:
   - run retrieval debug queries for real user phrasings
   - verify which notes actually surface

3. Repair:
   - fix metadata invariants
   - merge or archive duplicates cautiously
   - add missing linking or canonical terms where needed

4. Consolidate:
   - only after audit + recall results are understood

## Local Helper Tools

Use these scripts when available:

- `python3 scripts/vault_audit.py`
- `python3 scripts/vault_recall.py "query"`

The audit script is for integrity and duplicate signals.
The recall script is for testing whether real user phrasing can find the right notes.
