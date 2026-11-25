---
name: obsidian-vault
description: Save notes, learnings, decisions, meeting notes, people profiles, project docs, brag entries, how-to guides, and any other knowledge to the user's Obsidian vault. Use when the user says "save this to my vault", "make a note about", "add to obsidian", "remember this", "log this decision", "create a vault note", "save this learning", "add a brag", or wants to persist any piece of context, knowledge, or reference for future retrieval. Also use when asked to look up, search, or retrieve information from the vault.
---

# Obsidian Vault Skill

Save and retrieve knowledge from the user's Obsidian vault.

## Vault Path

**All operations target the current project directory** (`$CLAUDE_PROJECT_DIR`). This skill ships inside `starter-vault/.claude/skills/` in the workshop repo and travels with the vault when the participant copies `starter-vault/` into their chosen location, so by the time this skill runs the vault *is* the working directory. If you need the absolute path (e.g. to build paths for tool calls that don't inherit CWD), read it from `SETUP.md` in the workshop repo, under the **Path A -- Obsidian vault** section -> **Vault path (absolute)**.

If `SETUP.md` is not filled in yet, the participant has not completed bootstrap. Route them to `START_HERE.md` rather than guessing a path.

## Quick Reference: Where to Put Things

| Content | Type | Folder | Template |
|---------|------|--------|----------|
| Atomic idea, concept, snippet | `note` | `Notes/` | Note |
| Book/article/video summary | `learning` | `Learning/` | Learning |
| Decision with options/rationale | `decision` | `Notes/` | Decision |
| Meeting notes | `meeting` | `Meetings/` | Meeting |
| Person profile | `person` | `Personal/People/` | Person |
| Project documentation | `project` | `Projects/` | Project |
| Work achievement / win | `brag` | `Notes/` | Brag |
| How-to / SOP for yourself | `how-to-guide` | `Reference/` | How-To Guide |
| Reference material | `resource` | `Reference/` | Note |
| Daily note | `daily` | `Personal/` | — |

## Before Creating Any Note

**SEARCH FIRST** — the vault's value is in connections, not isolated notes.

1. `grep` the vault for keywords from the topic (search the current directory with `--glob '*.md'`)
2. `find` files by name pattern to check if a note already exists
3. Search synonyms and related terms
4. If a note exists, **update it** instead of creating a duplicate

## Frontmatter (REQUIRED on every note)

```yaml
---
type: <type>
created: DD.MM.YYYY
tags: []
related: []
---
```

### All Valid Types

`note` · `project` · `meeting` · `daily` · `resource` · `person` · `decision` · `learning` · `how-to-guide` · `brag`

### Type-Specific Extra Fields

| Type | Extra Fields |
|------|-------------|
| `project` | `status: planning\|active\|on-hold\|completed\|archived`, `due: YYYY-MM-DD` |
| `meeting` | `date: DD.MM.YYYY`, `attendees: []` |
| `person` | `last_contact: DD.MM.YYYY` |
| `decision` | `status: active`, `revisit: YYYY-MM-DD` |
| `learning` | `source:`, `author:`, `status: draft\|active\|completed` |
| `how-to-guide` | `last_updated: DD.MM.YYYY` |
| `brag` | `date: DD.MM.YYYY` |

### Tag Conventions

Hierarchical tags for cross-cutting concerns:
- `#status/todo`, `#status/in-progress`, `#status/done`, `#status/waiting`
- `#source/book`, `#source/article`, `#source/video`, `#source/podcast`
- `#area/work`, `#area/health`, `#area/finance`

## File Naming

- General: `Human Readable Name.md` (title case with spaces)
- Meetings: `YYYY-MM-DD Meeting Topic.md`
- Daily: `YYYY-MM-DD.md`

## Linking Rules

- **ALWAYS** use `[[wiki links]]` for internal references, never markdown links
- **Link when the connection is real.** A note with substantial content and 1 honest link beats a note with thin content and 7 invented links. Do not add links to hit a count.
- **Search before concluding a note is isolated.** If a draft has 0 links, search the vault again for synonyms and related names. If nothing relevant exists, leave the note unlinked — that is not a failure.
- `related:` in frontmatter is **optional**. Use it only for relationships the body does not already express via inline `[[wikilinks]]`. Do not duplicate.
- **Backlinks only when reciprocal.** Update an older note to link back only if the reverse link is also meaningful.

### Ghost-link discipline (CRITICAL)

A ghost-link is a `[[wikilink]]` pointing to a file that does not exist yet. Ghost-links themselves are fine — Obsidian tracks them in Unresolved Links and they act as forcing functions.

What is **not** fine: writing a paraphrased gloss next to a ghost-link that makes a factual claim the source cannot back. Example of the failure mode: writing `- [[Pilot to Production]] — why 75% of AI pilots don't scale` when the source actually said "25% moved 40%+ into production." The inverted number is an agent interpretation that now lives in the vault as if it were fact.

Acceptable patterns:
1. **Bare ghost-link:** `[[Pilot to Production]]` with no gloss.
2. **Stub with direct source quote:** create the target file with 1-2 lines quoting or citing the source, attributed.

Never write an agent-authored paraphrase next to a ghost-link whose target file is empty. That is how hallucinations enter the vault disguised as linked knowledge.

## Note Templates

### note / resource
```markdown
---
type: note
created: DD.MM.YYYY
tags: []
related: []
---

# Title

Content here. Link to [[Related Concept]] and [[Another Note]].
```

### learning
```markdown
---
type: learning
created: DD.MM.YYYY
tags: []
source:
author:
status: draft
related: []
---

# Title

> [!info] Source
> **Type**: #source/book | #source/article | #source/video | #source/podcast | #source/course
> **Author**:
> **Link**:

## Summary

## Key Takeaways
1.
2.
3.

## How I'll Apply This

## Related Ideas
-
```

### decision
```markdown
---
type: decision
created: DD.MM.YYYY
tags: []
status: active
revisit:
related: []
---

# Title

## Context

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
|  |  |  |

## Decision
**Chosen**:
**Why**:
```

### meeting
```markdown
---
type: meeting
created: DD.MM.YYYY
date: DD.MM.YYYY
attendees: []
tags: [meeting]
related: []
---

# Meeting: Title

**Date:** DD.MM.YYYY HH:mm
**Attendees:**

## Agenda
-

## Notes

## Action Items
- [ ]

## Decisions
```

### person
```markdown
---
type: person
created: DD.MM.YYYY
tags: []
last_contact:
related: []
---

# Name

## How We Met

## Interests
-

## Gift Ideas
-

## Notes
```

### brag
```markdown
---
type: brag
created: DD.MM.YYYY
tags: []
date: DD.MM.YYYY
related: []
---

# Title

## What I Did

## Why It Matters

## The Challenge

## How I Solved It

## Impact / Results

## Skills Demonstrated
-
```

### project
```markdown
---
type: project
created: DD.MM.YYYY
status: active
due:
tags: [project]
related: []
---

# Title

## Overview

## Goals
- [ ]

## Tasks
- [ ]

## Notes

## Resources
```

### how-to-guide
```markdown
---
type: how-to-guide
created: DD.MM.YYYY
tags: []
last_updated: DD.MM.YYYY
related: []
---

# Title

## When to Use

## Prerequisites
-

## Steps

### 1.

### 2.

## Troubleshooting

| Problem | Solution |
|---------|----------|
```

## Date Format

- Display/frontmatter: `DD.MM.YYYY` (e.g., `04.04.2026`)
- Filenames: `YYYY-MM-DD` (for sorting)

## Hard Rules

- NEVER create notes without frontmatter
- NEVER use markdown-style `[text](link)` for internal links
- NEVER manually edit anything in the vault's `.obsidian/` directory (that is Obsidian's own state)
- ALWAYS search before creating
- ALWAYS add wiki links and related notes
- ALWAYS use absolute paths when writing outside the CWD (resolve the vault root from `$CLAUDE_PROJECT_DIR` or `SETUP.md`)
