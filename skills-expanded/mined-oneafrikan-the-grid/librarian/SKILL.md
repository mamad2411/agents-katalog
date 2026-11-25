<!--
  SKILL.md — Librarian operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD — no
  assumptions about a specific wiki root, vault tool, or search infra unless
  injected via overlay. Injection points are marked `STACK: ...`.
-->

# Skill: Librarian

## Invocation

```
/librarian ingest <source>
/librarian query <question>
/librarian lint [domain]
/librarian new-domain <name>
```

Ingest triggers three ways, in order of how it's meant to be used:

1. **Inbox drop (primary, standalone use).** A file lands in
   `<wiki-root>/<domain>/inbox/` — from a human, a sync tool, or any process
   that can write a file to a folder. The dropper needs no knowledge of this
   agent, OpenClaw, or any signal convention. Whatever's watching the inbox
   (a cron poll or a filesystem watcher — mechanism injected per deployment,
   see STACK note below) invokes ingest per new/changed file.
2. **Direct invocation** — `/librarian ingest <source>` run by hand.
3. **Signal Protocol pickup** — an OpenClaw teammate hands off a filed
   research report via `signals/→librarian.md`. This is agent-to-agent
   coordination internal to OpenClaw, not something a human dropping a file
   needs to know about, and not the inbox's job.

Either way: identify which operation this is (ingest / query / lint /
new-domain) before doing anything — they have different methods below.

<!-- STACK: wiki root path(s) and per-domain directory layout injected here.
     Default assumed shape (one root per domain, or a single root with a
     subdirectory per domain — either works, injected at setup time):
       <wiki-root>/<domain>/inbox/     — drop zone: new/updated files land
                                          here to trigger ingest
       <wiki-root>/<domain>/sources/   — raw, immutable archive; a file moves
                                          here from inbox/ once ingested
       <wiki-root>/<domain>/wiki/      — your pages (entities, concepts, comparisons)
       <wiki-root>/<domain>/index.md   — catalog of every page + one-line summary
       <wiki-root>/<domain>/log.md     — append-only, greppable operations log
     How the inbox is watched (cron poll interval vs. a filesystem watcher
     like fswatch/launchd/inotify) is also injected here per deployment —
     this file assumes only that ingest gets triggered per new/changed file,
     not how.
-->

---

## Operation: Ingest

Triggered by a file in the inbox, a direct invocation, or a filed research
report (see Invocation above).

1. **Identify the domain.** Which existing domain wiki does this belong to?
   If none fits, escalate — propose `new-domain` rather than force-fitting.
2. **Read it fully.** Don't skim — the pages you create are only as good as
   your read of the source.
3. **Check the index for existing entities/concepts** this source touches,
   to avoid creating duplicate pages — update the existing page instead of
   forking a second one.
4. **Create/update pages** (typically 10–15 for a substantial source):
   entity pages, concept pages, comparison pages as the content calls for.
   Every page's frontmatter carries:
   ```yaml
   ---
   tier: <as given by the filing source — never invented by you>
   confidence: <H/M/L, as given>
   date: <source date>
   source: <citation/identifier>
   filed_by: <which agent/human filed this>
   refs: [<other page slugs this links to>]
   ---
   ```
5. **Update `index.md`** — one row per page, one-line summary, updated
   metadata.
6. **Append to `log.md`**:
   `## [YYYY-MM-DD] ingest | <source title> — <N> pages created/updated`
7. **If triggered by an inbox drop, move the file from `inbox/` to
   `sources/`** once ingested. This is what makes re-polling the inbox
   idempotent — a file already sitting in `sources/` is never re-ingested,
   so a watcher can safely re-check the inbox on every run without risking a
   duplicate ingest.

---

## Operation: Query

Triggered by a question against an existing wiki.

1. **Search `index.md`** for relevant pages — this is how you navigate at
   scale, not full-text scanning every page.
2. **Synthesise an answer** from the compiled pages, citing which page(s)
   each part of the answer comes from (and, through them, the original
   source/tier).
3. **If the synthesis is substantial** (not just restating an existing
   page), file it back as a new page, so the next query on this topic
   doesn't require re-synthesis.
4. **Append to `log.md`**: `## [YYYY-MM-DD] query | <question> — answered from N pages`
5. If no wiki covers the question's domain, say so — don't answer from
   general knowledge and imply the wiki backs it.

---

## Operation: Lint

Triggered periodically or on request. Per domain (or across all domains):

- **Contradictions** — pages making incompatible claims, especially where
  one is a lower tier than the other and still stands unflagged.
- **Staleness** — a claim superseded by a newer/higher-tier source that
  hasn't been reconciled into the older page yet.
- **Orphans** — pages with no inbound links from `index.md` or other pages.
- **Missing cross-references** — two pages clearly about related entities
  that don't link to each other.
- **Gaps** — questions the domain wiki can't currently answer, worth
  flagging to the relevant researcher.

Append findings to `log.md`: `## [YYYY-MM-DD] lint | <domain> — N issues found`
and report the list. Do not silently fix a contradiction by picking a side —
surface it per SOUL.md's escalation rules.

---

## Operation: New-domain

Triggered when a source or request doesn't fit any existing domain wiki.

1. Confirm with the human before creating a new wiki root — this is a
   structural decision, not a routine one.
2. Scaffold: `sources/`, `wiki/`, `index.md` (empty, headers only),
   `log.md` (empty, headers only).
3. Note the new domain and its scope in the top-level wiki-of-wikis index,
   if one exists in this setup.

---

## Source-quality checklist

- [ ] Every page's frontmatter has tier, confidence, date, source, filed_by
- [ ] No tier invented or altered from what the filing source provided
- [ ] Index updated on every ingest
- [ ] Log appended for every ingest/query/lint operation, never edited after
      the fact
- [ ] No duplicate entity/concept pages — checked index before creating
- [ ] Contradictions surfaced, not silently resolved
