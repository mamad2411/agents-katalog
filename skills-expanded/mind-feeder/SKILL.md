---
name: mind-feeder
description: Feed new content into the owner's central mind (this brain repo) — the ONLY way anything gets written into the brain. Use this whenever the owner says "feed this into my brain", "add this to my mind", "update my mind", "save this to the brain", or provides any new source to be remembered — a video, transcript, blog post, social post, repo, planning doc, book chapter, or a raw thought. Also use when they ask to update a project's status in the mind. Runs as a HARD-GATED flow (classify → propose extraction → wait for approval → write → commit), so never write before approval.
---

# Mind Feeder — the compiler

You are the write gate of the owner's central mind. You turn raw sources
into distilled, provenance-linked notes and updated project cards. You
NEVER write without approval. Read `CLAUDE.md` at the repo root before
doing anything — it is the contract; its rules override anything here if
they ever conflict.

## Hard gates

```
STAGE 1: CLASSIFY & PROPOSE  →  [GATE: the owner approves]  →
STAGE 2: WRITE AS ONE COMMIT →  done
```

Never run ahead of the gate. Never combine stages in one turn.

## STAGE 1 — Classify & propose

1. **Ingest the source.** If it's a URL, fetch it. If it's a video, get the
   transcript. If it's a repo/doc, read the relevant parts. If it's a raw
   thought, use it as-is.
2. **Classify**: What is this? Which entities does it touch (check
   `INDEX.md` and `projects/`)? Published or unpublished (→ default
   visibility per CLAUDE.md §4)?
3. **Scope check**: extract the *about*-layer, not the artefact. If the
   source is a large corpus (a manuscript, a dataset, a full codebase),
   take the lessons, architecture and status — the corpus itself never
   enters the repo (CLAUDE.md §2).
4. **Extract conservatively**: propose 2–4 notes maximum — only the
   strongest takes/stories/lessons/facts. For every proposed `take` or
   `story`, include the VERBATIM quote you will preserve (the owner's
   literal words from the source). One idea per note.
5. **Reconcile**: grep `knowledge/` for related notes on the same topics.
   For each proposed note, state: NEW / DUPLICATE-of-id (recommend
   keep-both if unsure) / SUPERSEDES-id (or "both stay current, different
   scopes" — see CLAUDE.md §5.3).
6. **Card updates**: list the exact changes to `projects/*.md` cards and
   `INDEX.md` lines (status, numbers, last-verified), and any new
   `content-catalog/` row if the source is the owner's own published
   content.
7. **Present the proposal** as a compact plan: source → notes (with type,
   topics, visibility, verbatim quote) → reconciliation decisions → card
   and catalog diffs. Then STOP and wait.

## GATE

Proceed only when the owner approves. If they edit the plan, apply their
edits — their wording beats yours, always. If they reject a note, drop it
silently.

## STAGE 2 — Write

1. Create the note files in `knowledge/<type>/` using the exact frontmatter
   schema from CLAUDE.md §3. File name = the note `id`.
2. Apply supersessions: edit the old note's `status` and `superseded_by`
   only. Never delete, never rewrite old bodies.
3. Update touched `projects/` cards (including `last-verified: <today>`),
   `INDEX.md`, and `content-catalog/` rows.
4. If the source itself should be archived, save the full text to `raw/`
   or add a pointer file.
5. Commit everything as ONE commit: `feed: <source-id>`. Show the owner a
   summary of what was written.

## Absolute rules

- No note without `source` + `source_url` (provenance, CLAUDE.md §5.2).
- Never invent, enrich, or "improve" a claim beyond what the source says.
- Topics come ONLY from the taxonomy in CLAUDE.md §7. If a needed tag is
  missing, propose adding it in Stage 1 — it becomes part of the same
  approved commit.
- When unsure between duplicate/merge/supersede: keep both, flag it.
- Verbatim quotes are copied character-for-character. Voice is sacred.
