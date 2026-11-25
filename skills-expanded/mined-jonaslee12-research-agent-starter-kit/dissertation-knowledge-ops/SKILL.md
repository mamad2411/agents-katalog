---
name: dissertation-knowledge-ops
description: Manage dissertation project knowledge across research-wiki, knowledge-base, Obsidian, source registers, LMS notes, supervisor or public resource notes, and task-state files with deduplication, source-of-record rules, indexes, and privacy boundaries.
---

# Dissertation Knowledge Ops

Use this skill when saving, organizing, syncing, deduplicating, or auditing dissertation knowledge across local project memory, the knowledge base, and Obsidian.

## Purpose

Adapt ECC knowledge-ops to this dissertation project. The core rule is: choose one canonical home for each kind of knowledge, then add lightweight cross-links instead of duplicating full content everywhere.

## Knowledge Layers

| Layer | Path | Role |
|---|---|---|
| Project rules | `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `.agents/skills/` | operating rules |
| Current state | `research-wiki/TASK_STATE.md` | task handoff and latest decisions |
| Project memory | `research-wiki/` | concise decisions, design rationale, open questions |
| Source register | `knowledge-base/SOURCE_REGISTER.md` | source inventory and evidence status |
| Source notes | `knowledge-base/sources/` | source-of-record notes |
| Obsidian vault | `<OBSIDIAN_VAULT_PATH>` | reading/thinking/navigation layer |
| Private data boundary | Obsidian private folder or restricted local folders | sensitive or participant-related material |

## Storage Decisions

Use:

- `TASK_STATE.md` for what changed, open confirmations, and next action
- `PROJECT_OVERVIEW.md` for stable project facts
- `LITERATURE_MAP.md` for literature clusters and gap logic
- `SOURCE_REGISTER.md` for source status and citation readiness
- Obsidian for navigable thinking pages and links
- system audit files for maintenance reports

Do not store:

- raw participant data in general notes
- unredacted sensitive information in Obsidian public layers
- duplicate full notes in both research-wiki and Obsidian unless one is clearly the source of record

## Workflow

1. Classify the knowledge type:
   - project rule
   - task state
   - literature/source evidence
   - methodology/design decision
   - supervisor feedback
   - system maintenance
   - private/sensitive data
2. Search existing locations before creating a new note.
3. Choose the canonical home.
4. Add cross-links or index entries.
5. Mark evidence status:
   - `CONFIRMED`
   - `INFERENCE`
   - `CONTEXTUAL SOURCE`
   - `NEEDS VERIFICATION`
   - `TO CONFIRM`
6. Run a link/index check when updating Obsidian or source registers.

## Output Format

```text
Knowledge operation:
- Type:
- Canonical home:
- Files updated:
- Duplicates avoided:
- Evidence boundary:
- Next index/check:
```

## Guardrails

- Do not duplicate long content across layers.
- Do not move source-of-record facts without updating references.
- Do not store raw participant data in general knowledge layers.
- Do not treat Obsidian as the source of record when a project file is canonical.
