---
name: clean-mk-dump
version: 1.0.0
description: Distills the latest monkey-brain dump into a clean structured summary, then writes it back to the dump file on approval. Use when user runs /clean-mk-dump or wants to clean and summarise their latest dump session.
user-invocable: true
---

# clean-mk-dump

Organises a raw dump into a structured summary. Role: thinking organiser — surface all ideas, branches, and open questions. Don't resolve; just map clearly so `kick-mk-dump` can challenge them.

## Flow

1. Read `docs/monkey-brain/dump-index.md` → find sessions with status `uncleaned`
   - Multiple uncleaned → ask user which to clean
   - None found → tell user to run `/add-mk-dump` first
2. Read the dump file
   - `## Summary` already filled → ask "Re-clean? (y/n)" → n: stop
3. Generate summary (see format below)
4. **Output the full summary as plain text** in the conversation so the user can read it, including the proposed new filename
5. Ask: Approve / Request edits / Reject
   - Request edits → ask what to change → back to step 3
   - Reject → stop
6. Write summary into `## Summary` section, rename file, update index

## Processing

Analyse whatever sections exist in the file — if the template has been customised, map content to the nearest field or include it under Core Dump. Key signals:

- **What/Why/How** — clearest statement of intent from the Dump section
- **Emotional** — the feeling/state described
- **[BRANCH]** — user listed options without choosing; flag each one
- **[UNCLEAR]** — vague or half-formed ideas; flag each one
- **Root cause** — from 5Why; preserve branches if the chain didn't fully resolve
- **short-topic** — 2–4 words, kebab-case (e.g. `skill-design`), for the renamed filename
- **Structure preservation** — if an idea has conditions (if X then Y), constraints, or multiple sub-parts, keep them as sub-bullets. Never flatten a multi-part idea to a single line just to be brief. Brevity loses decisions.

## Summary Format

Write into `## Summary`, replacing any placeholder text:

```
## Summary
_Cleaned: {yyyy-mm-dd} · {short-topic}_

**What:** [one sentence]
**Why:** [one sentence]
**How:** [one sentence]
**Emotional:** [one line]

**Core Dump:**
- [theme]: [idea] *(mark BRANCH or UNCLEAR where needed)*
  - [sub-detail, condition, or constraint — include if it affects a decision]
  - [sub-detail]

**Root Cause:**
- [deepest cause] *(or: BRANCH — unresolved)*

**Re-Think:**
- Past / Future / Emotional / Time / Money / Motivation / Environment: [one line each, omit if blank]

**Unclear / Decision Trees:**
- [all BRANCH and UNCLEAR items — primary input for kick-mk-dump]
  - [conditions, constraints, or options — preserve if they affect the decision]

**Open Questions:**
- [explicit questions from the dump]
```

## After Approval

> Dump file content is already in context from Flow Step 2 — do not re-read before writing back. Use content already loaded.

1. Write the summary content into `## Summary` in the dump file
2. Rename file: replace `-temp` with `-{short-topic}` (e.g. `2026-05-23-001-skill-design.md`)
   - Legacy filename → rename to `{yyyy-mm-dd}-{run}-{short-topic}.md` in the same directory
3. Update `dump-index.md`:
   - Session status → `cleaned`
   - Update filename in Sessions table if renamed
   - Update `latest:` to the final full path from project root

## Index Format

See `/init-mk-dump` for the `dump-index.md` format.
