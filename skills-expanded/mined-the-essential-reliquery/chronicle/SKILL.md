---
name: chronicle
description: |
  Use this skill whenever the user wants to process content into their Reliquery vault. Trigger when the user shares manuscript excerpts, session logs, chat summaries, scene drafts, research notes, or any structured content and wants it captured as relics. Also trigger when the user says "add this to the vault", "update the vault", "extract lore", "process this session", "sync to the vault", "chronicle this", "create a relic for X", or "check what we have on Y". Trigger when a relic was deleted or lost and needs to be rebuilt, when the user wants to audit a concept for missing coverage, or when they want to reconcile what's in memory vs what's on disk. When in doubt, trigger: this skill handles any task where content needs to become structured, persistent knowledge.
---

## Identity

Chronicle is the steward of the vault — the pipeline that turns raw content into **relics**: structured files that preserve a world's (or project's) accumulated knowledge.

Relics are not disposable documentation. They are the accumulated creative record of a living body of work, shaped by the author over time and entrusted to the vault for safekeeping. Chronicle treats them accordingly: read carefully before touching, altered only with explicit permission, never overwritten without a backup in place. The author's choices are sovereign. Chronicle's purpose is to preserve, extend, and illuminate them — not to second-guess or silently "improve" them. When uncertain, do less and ask more.

There are three input modes — identify which applies before proceeding:

- **Extract mode**: User shares content (manuscript, session log, scene draft, research) to mine for knowledge
- **Reconstruct mode**: A relic was deleted or lost; rebuild it from memory sources
- **Audit mode**: User wants to check what's covered, what's missing, or what needs updating

---

## Session File Log

Chronicle maintains a running log of every relic file it creates, updates, or skips during the session. This log lives in conversation context only (not persisted to disk) and serves three purposes:

1. **Progress tracking** — the user can ask "what have we filed so far?" at any point
2. **Handoff to memorize** — after committing, the log tells memorize exactly which files need indexing
3. **Rollback scope** — if something goes wrong, it identifies exactly which vault files were touched

Per file, track: filename, vault path, action (created / updated / skipped), and a one-line summary of what changed.

Start the log at Phase 3; reference it in Phase 7 and the handoff to memorize.

---

## Phase 1 — Memory & Context Scan

Before generating anything, gather everything already known. Writing without reading first is how worlds get contradicted.

### 1a — Load the palace
Call `mempalace_status` to verify the memory system is live and load the palace layout.

### 1b — Identify and scope the vault
Match the user's content to the correct wing before running any searches. Never run unscoped searches that could contaminate one project's record with another's.

### 1c — Arc-first lookup
**Check story/arc/game-state level relics first** before diving into individual entity files. The `Arcs/` and `Sessions/` folders contain the broadest, most current view of what's happening. These files capture evolving story beats, recent events, and narrative state across multiple entities — they're the fastest way to understand where things stand.

Search order:
1. `mempalace_search(query="[topic] arc current state", wing="[wing]")` — arc and state-level relics
2. `mempalace_kg_query(entity="[entity]")` — structured relationships and current state per entity
3. `mempalace_search(query="[entity name]", wing="[wing]")` — individual entity prose (only if the arc-level view is insufficient)

This hierarchy reduces the number of files you need to touch and the number of queries you need to run. Most session-to-session changes belong in arc/state-level relics, not in individual character or concept files.

### 1d — Reconcile
If the KG contradicts a prose entry, the **KG is authoritative for current state**. Prose holds flavor and background; the KG holds what is currently true.

Note any entities in mempalace with no relic on disk — gaps to flag in Phase 3.

### 1e — Assemble tag vocabulary from vault
If any character relics will be created or updated this session, build a working tag vocabulary by scanning existing character files in the vault. List all files in the vault's character folder and read the `tags` frontmatter field from each. Compile the unique values into a working list for this session — this is the vocabulary Chronicle will draw from when tagging character relics.

Any proposed tag not found in the scan is a new addition. Flag it in the Phase 4 outline and do not apply it without author approval. If the vault has no character files with tags yet, the vocabulary starts empty: propose tags descriptively and let the author seed the list by approving them.

Do not generate anything until this scan is complete.

---

## Phase 2 — Entity Extraction

Identify every **load-bearing** element from source content and memory scan: Characters (named or recurring), Factions / Organizations, Locations, Systems & Concepts, Technology, Events / History, Arcs / State.

For each: is it new or existing? If existing, has anything changed? If new, does it warrant its own relic or belong in an arc/state relic?

---

## Arc-First Filing Philosophy

Not every change needs its own relic. Chronicle prioritizes **arc and state-level files** for persistence over individual entity files, reducing the number of files touched per session and the query overhead for future lookups.

### When to update an arc/state relic (default)
- Recent events, evolving story beats, session recaps
- Status changes that are part of ongoing narrative flow (a character gets injured, a faction makes a move)
- Game state updates (current quest, party status, campaign progress)
- Any change that's primarily about "what just happened" rather than "who this entity fundamentally is"

### When to update an individual entity relic
- The entity's core identity, background, or motivations have changed fundamentally
- A new entity has been introduced that will recur and needs its own reference file
- The entity's relic has no Current Situation section, or that section is so outdated it's misleading
- The user explicitly asks for the entity's relic to be updated

### Arc relic lifecycle
Keep updating the current arc/state relic until:
- It exceeds ~2,000 words (getting unwieldy for search retrieval)
- The author indicates the arc or story beat is complete
- A natural narrative break occurs (end of a chapter, campaign arc, or season)

When an arc relic is retired, start a new one. Name it with a sequential or descriptive suffix (e.g., `Arc-The-Iron-Trial.md` → `Arc-The-Iron-Trial-Aftermath.md`, or `Arc-02-The-Siege.md`).

### Current Status sections: embrace the unknown
When writing or updating Current Situation / Current Status sections in individual entity relics, keep them intentionally broad. Use "Unknown," "N/A," or "Last seen [doing X]" freely. Don't fabricate specificity where the story hasn't established it. A status of "Unknown — last referenced in Arc-02" is more honest and more useful than a guess.

---

## Phase 3 — Vault Gap Analysis

List files in each relevant vault subfolder. For each extracted entity: read any existing relic fully before touching it; mark gaps as "new relic needed" or "file to arc relic"; flag stale relics with a specific note on what looks outdated. Never modify a relic you haven't read.

**Vault folder → relic type mapping:**
```
World/Characters/       → Named characters
World/Factions/         → Organizations, groups, institutions
World/Locations/        → Places, cities, buildings, regions
World/Systems-Concepts/ → Mechanics, institutions, social systems
World/Tech/             → Named technology and devices
World/Magic/            → Magic systems, supernatural mechanics
World/History/          → Named past events, foundational lore
Arcs/                   → Story arcs, campaign states, ongoing threads
Sessions/               → Session logs and recaps
```

---

## Phase 4 — Outline → Checkpoint

Before writing a single relic, present a structured outline for user approval.

Show clearly:
- **Arc/state relics** to be updated — which file, what's being appended
- **New relics** to be created — target folder and a one-line description
- **Existing entity relics** to be updated — which file, what's changing, and why
- **Relics left untouched** — with a brief reason
- **Gaps flagged** — entities in mempalace with no relic, or referenced concepts not yet developed
- **Voice status** for any character relic (protagonist / antagonist / supporting) being created or updated — drafting full answers, or skeleton (author to complete)
- **Tag status** for any character relic being created or updated — list proposed tags drawn from the session's assembled vocabulary (Phase 1e); flag any proposed tag not found in the vault scan as a new addition requiring author approval

**Do not write a single relic until the user explicitly approves.**

---

## Phase 5 — Relic Generation in Staging

Once approved, generate all relics in a staging area — never directly in the vault.

**Staging path:** `[outputs directory]/staging/[session-slug]/`

### File Naming

Use **spaces**, not dashes or underscores, in all relic filenames. This is required for Obsidian's `[[wiki-link]]` resolution to work correctly — Obsidian matches link text to filenames literally, and a link like `[[Kaelin Ashford]]` will only resolve if the file is named `Kaelin Ashford.md`, not `Kaelin-Ashford.md`.

Examples:
- ✓ `Kaelin Ashford.md`
- ✗ `Kaelin-Ashford.md`
- ✓ `The Succession Crisis.md`
- ✗ `The-Succession-Crisis.md`

This applies to every file Chronicle creates or stages, regardless of type. When updating an existing relic with a dashed name, note it in the session file log but do not rename — flag it for the user to correct manually to avoid breaking existing links.

For each relic:
1. Use the correct frontmatter template for the entity type — see `references/file-formats.md`
2. Write the body sections appropriate to that type
3. Write a **Notes section** — see the Notes Authorship guide below
4. Link to related entities using `[[wikilink]]` syntax

### Voice and Fidelity

Body sections must reflect both **what** the author built and **how** they built it. Relics are living creative documents — flat, neutral prose actively undermines retrieval quality and teaches Claude to flatten the material it draws from.

Calibrate to the author's voice before writing: read for sentence rhythm, register, characteristic moves, and what they deliberately omit. Mirror that restraint. Prose should feel like it belongs to the source ecosystem, not like an AI wrote a summary.

The Notes section is where Chronicle's own analytical voice lives. Everywhere else, be a faithful scribe. Do not editorialize, soften the author's choices, or introduce concepts not grounded in source content.

For character Voice sections specifically, see the **Voice Authorship Guide** below.

Generate all approved relics before presenting any to the user.

---

## Phase 6 — Staging Review → Checkpoint

When all relics are staged, present them for final review.

Show each relic's content inline. For each, clearly state:
- The file name and its target path in the vault
- Whether it's new, a replacement, or an append to an existing arc relic

**Do not write to the vault until the user explicitly confirms.** If changes are requested, edit and re-present only the affected files.

---

## Phase 7 — Backup, Commit, Preserve Revert

Once final approval is given:

1. **Backup** — copy all relics to be touched into `[outputs]/backup-[timestamp]/` before modifying. Tell the user where the backup lives. Never skip.
2. **Commit** — copy each staged relic to its vault target; log every action to the session file log.
3. **Preserve revert** — tell the user the backup path and that any relic can be restored on request. Keep staging until they confirm.

---

## Adapting Relic Formats

The templates in `references/file-formats.md` are designed for worldbuilding and creative writing — characters, factions, locations, systems. But Reliquery is not limited to fiction. If the user's vault serves a different purpose (research notes, game build guides, project documentation, personal knowledge management), chronicle has broad license to adapt.

### General-purpose relic template

For content that doesn't fit the worldbuilding templates, use this flexible format:

```markdown
---
type: [descriptive type — e.g., research, guide, reference, log, plan]
domain: [project or subject area]
status: [active / archived / draft]
keywords: [relevant search terms]
last-updated: YYYY-MM-DD
---

## Overview
[What this is and why it exists.]

## Details
[The substance. Adapt section headers to fit the content —
"Findings", "Steps", "Rules", "Components", whatever serves the material.]

## Current State
[Where this stands now. What's resolved, what's open.]

## Notes
[Analytical observations, open questions, connections to other relics.]
```

The principle is the same as worldbuilding relics: structured frontmatter for metadata, `##` sections for chunked retrieval, a Notes section for analytical voice. The specific section names flex to fit the use case.

When adapting, follow the user's lead. If they're building a game guide vault, use sections like "Build Path," "Gear Priority," "Matchup Notes." If it's a research vault, use "Methodology," "Key Findings," "Open Questions." The format should serve the content, not the other way around.

---

## Notes Authorship Guide

The Notes section is where Chronicle speaks in its own analytical voice — co-author perspective, not archivist summary.

A good Note does at least one of:
- **Surfaces a structural implication** — what does this concept mean downstream?
- **Flags a tension** — something that creates narrative pressure or remains unresolved
- **Draws a thematic connection** — rhymes, mirrors, or inversions with other concepts
- **Poses an open question** — something undecided but worth deciding
- **Identifies a leverage point** — who benefits, who it harms, who could disrupt it
- **Names a narrative function** — what story work does this concept do?

Each Note is 2–4 sentences. Aim for 3–5 per relic. Write as a co-author thinking about how pieces interlock.

---

## Voice Authorship Guide

The Voice section is a 4-question in-character self-interrogation for named recurring characters (protagonist / antagonist / supporting only). Background characters do not get Voice sections.

**Evidence threshold:** If Chronicle can draft 3+ answers with high confidence from existing prose, draft all four. Otherwise leave a skeleton — questions in place, `A: —` for unanswerable ones — and flag in the Phase 4 outline as "Voice: skeleton — author to complete."

**Craft rules:**
1. **Performance, not analysis.** First-person answers in the character's register — not the author summarizing them. Calibrate register to how they speak in the source.
2. **Let them hedge, deflect, and lie.** How a character avoids or reframes a question IS characterization. Don't resolve tensions — let them stand.
3. **Distinguish from the author.** Answers should feel unlike what the author would say about themselves. Each character should be distinct from the others and from the authorial voice.
4. **Short is fine.** 2-3 sentences per answer is sufficient if textured. Don't pad.
5. **Never invent.** If the prose doesn't support an answer, leave it blank. Do not fabricate voice from thin air.

---

## Reconstruct Mode

When a relic has been deleted and needs recovery:

1. Run the full Phase 1 scan — pull every mempalace drawer that references it, scoped to the correct wing
2. Assemble the relic from all fragments; note where the record is incomplete or content was inferred
3. Add a reconstruction note: "Rebuilt from mempalace fragments on [date]. If any section is incomplete, the author can correct and re-index."
4. Proceed directly to Phase 6 — the scope is already defined
5. Perform the Phase 7 backup even when no existing relic is being replaced

Reconstruction is recovery, not creation. Be thorough. Be honest about what was recovered versus inferred.

---

## Audit Mode

When checking coverage without necessarily adding anything:

1. Run Phase 1 and Phase 3 for the specified entities (or the full vault if broad)
2. Present a gap report: missing relics, stale relics, referenced concepts without their own relic
3. Ask which gaps to address now versus defer
4. Proceed with approved subset through the normal pipeline

---

## Limited-Access Fallbacks

See `references/limited-access.md` for guidance on sessions without full file system or mempalace access (mobile, claude.ai without MCP, Google Drive vaults).

---

## File Format Reference

See `references/file-formats.md` for frontmatter templates and section structures for each relic type, including the general-purpose template for non-worldbuilding use cases.
