---
name: open-dossier
description: Turn any project folder into a source-driven knowledge dossier that compounds over time — ingest documents into traceable analyses, a living wiki, plans, actions and decisions. Use this skill whenever the user wants to process source documents (reports, transcripts, emails, decks, papers) into structured knowledge; asks to "ingest", "process" or "verwerk" a document, even a bare filename with no other context; wants a knowledge base, wiki or "second brain" for a project or client engagement; wants plans and action items derived from documents and traceable to their source; wants an existing pile of notes, summaries or already-processed documents restructured into a traceable knowledge base with an audit trail of where each fact came from; asks what a dossier knows ("query the dossier", "what do we know about X"); wants a briefing or one-page current-state synthesis of a case or file, especially when they need established fact separated from assumption or open question; or asks for a health check of the knowledge base. Also trigger on mentions of "dossier", "source-driven", "traceable to the source", "bronregister", "LLM wiki", or maintaining a decision log / action register from meeting notes. Prefer this skill over writing a one-off summary whenever the user's documents are meant to accumulate into knowledge they will come back to later.
license: MIT
---

# Open Dossier

A dossier is a folder that turns documents into decisions. It combines two ideas:

1. **The LLM wiki** (after Karpathy): instead of retrieving document chunks fresh on every question, the model maintains a persistent, compounding set of markdown pages. Each ingested source improves the whole; nothing is re-derived from scratch.
2. **Source-driven execution**: the goal is not to summarize documents but to extract what leads to a decision, a plan or an action — and to keep every claim traceable to where it came from.

Humans curate sources and make decisions. You do the bookkeeping: conversion, analysis, cross-referencing, index maintenance, consistency checks. You do this reliably at near-zero cost, which is exactly why a dossier compounds where human-maintained wikis rot.

## The four layers

| Layer | Contents | Who writes it |
|---|---|---|
| Sources | `sources/originals/` (immutable), `sources/converted/` (markdown) | Humans drop originals; you convert |
| Knowledge | `sources/analyses/`, `wiki/` | You, from sources |
| Execution | `plans/`, `actions.md`, `decisions.md`, `backlog.md` | You, traceable to sources or decisions |
| Meta | `DOSSIER.md` (schema), `index.md` (catalog), `log.md` (journal), `briefing.md` (living synthesis) | You maintain; humans configure DOSSIER.md |

Originals are never modified. Everything else is yours to keep correct.

## Traceability labels

Every substantive statement in analyses, wiki pages, plans and the briefing carries one of four labels. This is the epistemic backbone of the dossier — it lets a reader (human or a future session) instantly see what is fact, what is inference and what still needs confirmation:

- `[SOURCE]` — stated literally in a source document (cite the source ID)
- `[INTERPRETATION]` — your analysis or inference from sources
- `[HYPOTHESIS]` — an assumption that still needs discussion or confirmation
- `[DECISION]` — a choice that has been made (by a human, logged in `decisions.md`)

When a hypothesis gets confirmed, promote it to a decision and log it. When a source contradicts an interpretation, revise the interpretation and note the correction in `log.md`.

## Operations

The skill supports five operations. Infer which one the user wants; when they invoke the skill with arguments (e.g. `/open-dossier ingest report.pdf`), the first word selects the operation.

### init — create a new dossier

1. Ask (briefly) what the dossier is about: domain, purpose, who the actors/organizations are, and whether the execution layer (plans/actions) is needed or only knowledge.
2. Create the structure below and fill `DOSSIER.md` using the template in [references/templates.md](references/templates.md). `DOSSIER.md` is the schema: it tells any future session what this dossier covers, which conventions apply, and how to behave. If the folder is a Claude Code project, also reference or symlink it from `CLAUDE.md` so sessions load it automatically.
3. Seed `briefing.md`, `index.md`, `log.md`, `actions.md`, `decisions.md` and `backlog.md` from the templates — header structure only, no example rows; the briefing simply states there is nothing yet. Write the first `log.md` entry (init). Leave `wiki/` and `plans/` empty: pages earn their existence through ingests, never scaffold empty stubs.

```
dossier-root/
├── DOSSIER.md          # schema: scope, conventions, actors
├── briefing.md         # living synthesis: current state in one page
├── index.md            # catalog: every page, one line each
├── log.md              # append-only journal
├── sources/
│   ├── originals/      # immutable input documents
│   ├── converted/      # markdown conversions, one per original
│   └── analyses/       # compact analysis per source
├── wiki/               # entity and topic pages
├── plans/              # numbered living plans (01-, 02-, ...)
├── actions.md          # central action register
├── decisions.md        # decision log (+ open hypotheses)
└── backlog.md          # open questions, sources still to process
```

### ingest — process a source document

This is the core loop. For each new source:

1. **Preserve.** Copy the original into `sources/originals/` (move only if the user prefers their inbox emptied); the dossier copy is canonical from here on. Never edit it.
2. **Convert.** Produce a faithful markdown version in `sources/converted/`, named `YYYY-MM-DD-short-slug.md` (date = document date, not today). Extract text, tables and comments; note anything that did not survive conversion in an HTML comment at the top. If the original is already markdown or plain text, the converted file is a verbatim copy with a one-line provenance comment — mention there when the true original (e.g. the .docx behind an export) was never provided.
3. **Register.** Assign the next source ID (S001, S002, …) and add the source to the register in `index.md` with origin, type and status. Status runs new → converted → analyzed → processed; the intermediate values exist for interrupted or batch work — in an uninterrupted ingest, write the row here and set `processed` in step 7.
4. **Analyze.** Write a compact analysis in `sources/analyses/` (same filename as the converted file) using the analysis template: context, key points, decisions found, risks, and — most importantly — which plans and actions follow. Label every point. Fill in the "Follows from this source" IDs once they exist (the same pass is fine if you already know what steps 5–6 will create). An analysis is working context, not a re-narration: capture only what someone acting on this dossier needs.
5. **Compound.** Update the affected `wiki/` pages: entity pages for recurring actors/systems, topic pages for recurring themes. Create a page when a subject recurs across two or more sources or clearly will; the Actors table in `DOSSIER.md` covers the roster, so an actor earns an entity page only when there is substantive knowledge about it beyond name and role. Revise existing claims rather than appending contradictions; when a genuine contradiction appears between sources, record both with their source IDs and flag it in `backlog.md`.
6. **Execute.** Update affected `plans/`, add new actions to `actions.md` (next A-ID, with origin, owner, priority, status, due date), log decisions and new hypotheses in `decisions.md`, and put open questions in `backlog.md`. A decision humans already made in a source is logged with its original date, no confirmation needed; your own inferences stay hypotheses until the user confirms them. Upcoming meetings and milestones belong in the relevant plan or the briefing, not in `actions.md`.
7. **Close the loop.** Update `briefing.md` (what changed in the overall picture?), update `index.md` entries for every page you touched, and append one entry to `log.md`: timestamp, source ID, pages touched, one-line gist.

A good ingest touches many files; that is the point. The compounding value comes from step 5–7 — skipping them turns the dossier back into a pile of summaries.

### query — answer from the dossier

1. Start from `index.md` and `briefing.md` to locate relevant pages; read only what you need.
2. Answer with citations: source IDs for `[SOURCE]` claims, page names for wiki/analysis claims. Distinguish labels in the answer — do not present a hypothesis as fact.
3. If the answer required synthesis that is worth keeping (a comparison, a timeline, an overview that took real work), file it into the appropriate `wiki/` page and log the query in `log.md`. Trivial lookups need no logging.
4. If the dossier cannot answer, say so explicitly and add the gap to `backlog.md`.

### lint — health check

Walk the dossier and report (then fix what is mechanical, propose what needs judgment):

- **Contradictions**: claims that conflict between pages or with a newer source
- **Stale state**: briefing or plans that predate recent ingests; actions past their date without status change
- **Orphans**: pages not referenced from `index.md`; sources in `originals/` without conversion, register entry or analysis; converted files without originals
- **Traceability gaps**: substantive claims without labels; actions without origin or owner; decisions not in `decisions.md`
- **Drift**: `index.md` entries that no longer match page contents; broken relative links
- **Hypotheses aging**: `[HYPOTHESIS]` items that have been open a long time — list them for the user to confirm or kill

Fix index drift, broken links and missing register entries yourself. Contradictions and stale hypotheses go to the user: those are decisions, not bookkeeping. Log the lint in `log.md`.

### brief — refresh the synthesis

Regenerate `briefing.md` from the current state: purpose, actors, current status, key facts, open points. One page, labeled, readable by someone with zero context. This is the page a new session (or a new colleague) reads first, so optimize it for exactly that reader.

## Conventions

- **IDs**: sources S001…, actions A001…, sequential, never reused. Plans are numbered files (`01-topic.md`); the filename is the order.
- **Dates**: absolute (2026-06-29), never "yesterday" or "last week" — a future session has a different "now".
- **Status values** for sources: new → converted → analyzed → processed. For actions: open, in progress, blocked, done, dropped.
- **Language**: write the dossier in the language of its sources and users; set it in `DOSSIER.md`. Keep the label vocabulary (`[SOURCE]` etc.) as-is or map it once in `DOSSIER.md` (e.g. Dutch `[BRON]`, `[INTERPRETATIE]`, `[WERKHYPOTHESE]`, `[BESLUIT]`) — one vocabulary per dossier, never mixed.
- **Style**: compact and concrete, aimed at execution. Write for the next reader, not for completeness.
- **Sensitive content**: when a source marks something confidential, record it (traceability wins) but flag it `(sensitive)` where it appears, and warn the user before the dossier is shared, pushed or exported.
- **Git**: if the dossier is a git repo, commit after each ingest/lint with a message naming the source or operation. Suggest `git init` if it is not.

All file templates (DOSSIER.md, analysis, wiki page, plan, actions table, decisions log, index, log, briefing) live in [references/templates.md](references/templates.md) — read it when creating any of these files for the first time.

When the source is an email, mail thread or mail attachment, also read [references/email-sources.md](references/email-sources.md): it covers acquiring mail via whatever mail tooling the session has (MCP tools, a CLI, or exports), thread conversion, and when attachments become their own sources.
