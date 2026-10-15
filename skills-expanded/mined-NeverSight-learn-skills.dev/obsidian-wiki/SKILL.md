---
name: obsidian-wiki
description: Use when a repo should keep a persistent, agent-maintained knowledge wiki (the Karpathy "LLM wiki" pattern) in an Obsidian vault — when first setting up such a wiki, or when an agent should read, update, or lint an existing one.
---

# Obsidian Wiki

## Overview

A persistent, agent-maintained knowledge wiki in an Obsidian vault, following
Karpathy's "LLM Wiki" idea. Three layers: **raw sources** (cited, never
duplicated), **the wiki** (agent-maintained markdown), **the schema**
(`wiki/meta/`).

**Core principle:** synthesize once, maintain forever. The wiki is as much the
agent's memory of its own decisions as it is a digest of external docs. The
tedious part of a knowledge base is the bookkeeping — exactly what an agent
does well.

## When to Use

- **Setup:** a repo accumulates design knowledge and has no wiki — run init.
- **Maintenance:** the end of a session that produced durable insight; a
  question needing synthesis across sources; a periodic health check.

Not for: ephemeral task state (use a task list); duplicating canonical specs
(cite them instead).

## Setup

Run the init script from the repo root:

```bash
node /path/to/obsidian-wiki/scripts/init-wiki.mjs
```

Environment variables: `WIKI_TARGET` (vault path; default sibling
`../<project>-wiki`), `WIKI_PROJECT` (project name; default repo dir name).
The script is idempotent. Then inject the managed agent block — see
`references/init.md` for the full procedure.

## The Four Operations

- **Ingest** — an external source appears (docs, research, a webpage). Read it
  fully; create or update topic pages (one source touches several); update
  `index.md`; append a `log.md` entry.
- **Record** — self-document durable insight you produced by *doing the work*:
  decisions and rationale, architectural commitments, hard-won findings,
  synthesis worth keeping. Its own trigger, not a side-effect of Ingest. This
  is the long-term-memory half of the wiki.
- **Query** — read `index.md` first, drill into relevant pages, synthesize
  with citations. File non-obvious answers back as pages.
- **Lint** — periodic deep sweep: contradictions, stale claims, orphan pages,
  missing cross-links, format drift, and outstanding `*[needs verification]*`
  flags.

## Clean As You Go

Every Ingest, Record, and Query also fixes what it touches. When you
confidently identify stale or superseded content, consolidate or correct it
*then* — do not wait for Lint. Only act on staleness you can confidently
identify; flag uncertain cases `*[needs verification]*`, never silently
delete. Lint then resolves every outstanding flag.

## Parallel Projects

One vault holds many domains. Each project or topic is its own folder under
`wiki/`; `index.md` is sectioned per domain; `log.md` is append-only. Two
sessions on different projects never contend for the same pages. See the
domain-isolation section of `wiki/meta/conventions.md`.

## Single-Writer Rule

Only the parent agent in a session writes the wiki. Subagents surface findings
in their final report; the parent decides what persists. Prevents concurrent
edits and bloat.

## Page Format

The page-format spec — frontmatter fields, naming, citations, `## Related`
sections, lint rules — lives in `wiki/meta/conventions.md`. Read it before
writing any page. This skill does not restate it: the vault's `meta/` files
are the single source of truth.

## End-of-Session Checklist

See `wiki/meta/update-rule.md` — the durable-insight bar, good vs bad
candidates, and the checklist.

## Common Mistakes

- Capturing ephemeral task state instead of durable insight.
- Duplicating canonical specs instead of citing them.
- Editing the wiki from a subagent.
- Forgetting the `index.md` + `log.md` update after a wiki edit.
- Deleting content on *suspected* rather than *confirmed* staleness.
- Cross-domain link sprawl — link freely within a domain, sparingly across.
