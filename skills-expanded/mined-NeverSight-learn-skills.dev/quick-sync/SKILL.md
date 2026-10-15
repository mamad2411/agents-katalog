---
name: quick-sync
description: Session-end synthesis, daily version. Processes inbox, logs decisions, enriches wiki pages, updates journal/NOW.md + TODO.md + DONE.md, appends log.md, commits. No deep rigor — fast and clean. Run at the end of every work session.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Synthesize the current session into the brain. Fast, clean, no deep review.

## Steps

### 1. Process inbox

For every file in `inbox/*.md` with frontmatter `status: raw` (or no status):
- Call `/ingest <path>` on it
- On success, update its frontmatter to `status: ingested`
- If user explicitly marks a note for orphaning (e.g., not relevant), set `status: orphaned` and skip

If the inbox is empty, skip.

### 2. Capture decisions from session

Scan the session conversation for statements of the form:
- "we decided ..."
- "going with ..."
- "let's [choose/go/pick] X"
- "X over Y because ..."

For each, write a `decisions/<YYYY-MM-DD>-<slug>.md` file with frontmatter:

```yaml
---
title: <one-line title>
date: <ISO date>
status: decided
builds_on: [<prior decision slugs if any>]
touched: []
---

# Decision: <title>

## Context
<what prompted this>

## Decision
<what was decided>

## Consequences
<what changes>

## Builds on
- [[<prior decision>]] (if any)
```

If a decision supersedes a prior one, add `## Superseded by: <new slug>` to the old file.

### 3. Enrich wiki pages

Based on session topic, identify 1-3 wiki pages that should have new facts appended. For each, append under a new dated section:

```markdown
## <YYYY-MM-DD>: <what was learned>
<paragraph, with inline [Source: ...] markers pointing to this session or a source file>

(enriched YYYY-MM-DD from session)
```

Enrichment is additive only. Never edit existing paragraphs.

### 4. Update journal

- `journal/NOW.md` — refresh this week's tracks, open decisions, blockers. Update `Last updated:` date.
- `journal/TODO.md` — move completed items to `journal/DONE.md`. Add new tasks surfaced this session.
- `journal/DONE.md` — append items completed.

### 5. Append to log.md

```
## [YYYY-MM-DD] quick-sync
- Inbox processed: N
- Decisions logged: N
- Pages enriched: [list]
- Tasks closed: N
```

### 6. Commit and push

```bash
git add -A
git commit -m "quick-sync: <short summary of session>"
git push
```

If there are no changes to commit, skip.

## Failure modes

- `/ingest` fails on an inbox note → leave the note with `status: raw`, note in log.md, continue with rest
- Git push fails → commit locally, print the error, let user resolve
