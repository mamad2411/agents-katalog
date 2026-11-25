---
name: vault-skill
version: 0.1.0
description: >-
  Persistent project memory in a local Obsidian vault (.claudevault). Use
  PROACTIVELY — do not wait to be asked — whenever any of these happen: an
  architecture/design decision is made ("we decided", trade-offs weighed,
  alternatives chosen); a work session ends or is being wrapped up; project
  context/goals/stack change; reference knowledge worth keeping again surfaces
  (research, specs, findings hard to re-derive); the user wants to init the
  vault, read context at the start of a session, process the raw/ intake folder,
  or generate a report/briefing into outputs/. Creates interlinked markdown
  notes (decisions, logs, knowledge) that reference each other with [[wikilinks]]
  and all link back to context.md.
triggers:
  - save this decision
  - log this session
  - update the vault
  - read the vault
  - process raw folder
  - init the vault
  - what have we decided
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

## When to invoke this skill

This is the **parallel skill twin** of the `vault` MCP server. It manages a
local Obsidian knowledge vault at `.claudevault/` in the project root, using
plain markdown files linked with `[[wikilinks]]`. The whole system is
file-based — no server required, just Read/Write/Edit/Glob/Grep.

Invoke it — **proactively, without being asked** — when:

- **A decision is made** → create an ADR in `decisions/NNN-title.md`
- **A session ends / is wrapped up** → create/append `logs/YYYY-MM-DD.md`
- **Project context changes** → update `context.md`
- **Reusable knowledge surfaces** → create a note under `knowledge/`
- **Session starts** → read `context.md` + the most recent log
- **User says** "process raw", "what's in raw?" → classify `raw/` intake
- **User asks for a report/briefing/gap-analysis** → write to `outputs/`
- **Vault doesn't exist yet** → run Init

## Core principle: maximum linkage

Every note links to everything relevant. The test: *if two notes are related
in any way, there should be a link between them.* When in doubt, link.

Always-apply rules:
- Every note links back to `[[context]]`
- Every decision links to the session log where it was made
- Every decision links to the knowledge notes that informed it
- Every session log links to the decisions/knowledge/context changes that session
- Every knowledge note links to the decisions and logs that reference it
- Related decisions link to each other; superseded decisions cross-link to replacements

Wikilink syntax: `[[context]]` · `[[decisions/001-use-postgres]]` ·
`[[decisions/001-use-postgres|ADR 001]]` · `[[context#Stack]]`

**Link-target convention (so links resolve deterministically):** always write
the target as the note's path **relative to `.claudevault/`, without the `.md`
extension** — e.g. `[[decisions/001-use-postgres]]`, `[[logs/2026-07-21]]`,
`[[knowledge/research/pgvector-benchmarks]]`. The two exceptions are the hub
note `[[context]]` and heading links like `[[context#Stack]]`. Never use a bare
filename (`[[001-use-postgres]]`) — the health check resolves every `[[...]]`
against an actual file at that path, and bare names are ambiguous.

## Reading the vault (session start)

```
Read: .claudevault/context.md          ← always
Read: .claudevault/logs/               ← most recent log only
Read: .claudevault/decisions/          ← any relevant ADRs
Read: .claudevault/knowledge/          ← only if relevant to today's work
Do NOT read: .claudevault/raw/         ← only when user asks
Do NOT read: .claudevault/outputs/     ← only when user references
```
Follow wikilinks to pull in connected notes as needed.

## Init (only if `.claudevault/` is absent)

```bash
if [ -d ".claudevault" ]; then
  echo "Vault already exists — skipping init"
else
  mkdir -p .claudevault/{raw,outputs,decisions,logs,knowledge/{research,references,external,people-and-teams}}
  echo "Vault scaffolded — now write seed files"
fi
```
Then write the seed files below with the Write tool.

### Seed: `.claudevault/context.md`
```markdown
# Project Context

parent:: (root)

## Overview
[Brief description of the project]

## Stack
[Languages, frameworks, tools]

## Goals
[What this project aims to achieve]

## Key People / Teams
See [[knowledge/people-and-teams/overview]]

---

## Decisions
_[[decisions/]] — links added as ADRs are created_

## Session Logs
_[[logs/]] — links added each session_

## Knowledge
_[[knowledge/]] — links added as reference material is saved_

## Raw Intake
_[[raw/]] — unprocessed material awaiting classification_

## Outputs
_[[outputs/]] — AI-generated reports and analyses_
```

On init, scan the project to pre-populate `context.md`: detect stack from
`package.json` / `pyproject.toml` / `Cargo.toml` / etc., read `README.md`, and
create ADRs for any already-documented decisions.

## Templates

### Decision — `decisions/NNN-title.md`
```markdown
# [NNN] — [Decision Title]

parent:: [[context]]
date:: YYYY-MM-DD
status:: proposed | accepted | superseded
superseded-by:: [[decisions/NNN-title]] ← remove if not applicable

## Context
[Why this decision was needed]
See [[context#Stack]] for project background.

## Research that informed this
- [[knowledge/research/topic]]
- [[knowledge/references/spec-name]]

## Decision
[What was decided]

## Consequences
[Trade-offs, implications]

## Related decisions
- [[decisions/NNN-related]]

## Session
- [[logs/YYYY-MM-DD]] ← when this was decided
```
Numbering: next zero-padded integer after the highest existing ADR (Glob
`decisions/*.md`). If you are creating **several ADRs in one pass**, allocate all
their numbers up front from that Glob result — don't re-Glob between writes, or
two new ADRs can claim the same number. After creating: (1) link it in
`context.md` under Decisions,
(2) link it in today's log, (3) link informing knowledge notes, (4) cross-link
related ADRs.

### Session log — `logs/YYYY-MM-DD.md`
```markdown
# Session — YYYY-MM-DD

parent:: [[context]]

## What we did
[Summary]

## Decisions made
- [[decisions/NNN-title]]

## Knowledge saved
- [[knowledge/research/topic]] ← why it was saved

## Context changes
[Updates made to [[context]]]

## Open questions
[Unresolved items]

## Next steps
[What to pick up next session]
```
One log per day. If today's log exists, **append** rather than overwrite: first
`Read` the existing file, then use `Edit` to add the new content under the right
heading (or `Write` back the full merged document). Never `Write` a fresh
template over a log that already has content — it destroys the earlier entry.
Then link it in `context.md` under Session Logs.

### Knowledge — `knowledge/research/NNN-topic.md` (or references/ external/ people-and-teams/)
```markdown
# [Topic]

parent:: [[context]]
source:: [URL or origin]
date:: YYYY-MM-DD
saved-because:: [one sentence: why this is worth keeping]

## Summary
[Key findings in Claude's own words — NOT raw copied content]

## Relevance to this project
[Why this matters here specifically]

## Used in
- [[decisions/NNN-title]]
- [[logs/YYYY-MM-DD]]
```

## What to save (the "worth keeping" test)

**Always save:** architecture decisions + reasoning, session summaries, context changes.

**Save knowledge only if** it answers yes to any: Will this be needed in a
future session? Did it change a decision/direction? Is it hard to re-derive? Is
it project-specific (not general docs)?

**Never save:** scaffolding tool results, web searches that changed nothing,
file contents already in the repo, general knowledge Claude already has.

## Subfolders
- `knowledge/research/` — articles, spikes, benchmarks, findings
- `knowledge/references/` — specs, schemas, API/DB contracts, fed-in files
- `knowledge/external/` — tool/API call results worth keeping (summarized, not dumped)
- `knowledge/people-and-teams/` — org context, stakeholders, constraints

## raw/ — intake junk drawer
Never modify files in `raw/`; never read it automatically. When the user asks to
"process raw": read each file, classify it (decision / reference / research /
people / context / skip) using the same rules as a doc migration, promote it
into the right vault location **summarized in your own words**, leave the raw
original in place, and log what was processed.

## outputs/ — derived artifacts
For generated reports/briefings/gap-analyses spanning multiple notes. Name
descriptively (`outputs/auth-architecture-briefing.md`). Include `date::` and a
`sources::` list of the wikilinks it drew from. Do NOT link outputs into
`context.md` — they're ephemeral. If an output reveals something worth keeping,
promote it into a `knowledge/` note.

## Health check (on request)
Audit for: broken wikilinks (targets that don't resolve to a file), orphaned
notes (nothing links to them), missing metadata fields, and stale content. Use
Glob + Grep to cross-check `[[...]]` targets against actual files.

## Date handling
Always use the real current date for `date::` fields and `logs/` filenames.
Convert relative references ("today", "last week") to absolute `YYYY-MM-DD`.
