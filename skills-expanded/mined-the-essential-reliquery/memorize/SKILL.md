---
name: memorize
description: "Use this skill whenever vault relics need to be indexed into mempalace after being created or updated. Trigger when the user says \"memorize this\", \"add to mempalace\", \"index these relics\", \"put this in memory\", \"sync to the palace\", or \"memorize the vault\". Also trigger automatically at the end of any chronicle session where new relics were committed — newly written relics that aren't yet indexed are invisible to future memory lookups, so this skill should be the natural next step after chronicle commits files. Trigger when the user wants to verify which vault files have no mempalace representation, or when a relic was updated and its palace drawers are stale. When in doubt, trigger: this skill handles any task where vault content needs to become searchable memory."
---

## Identity

Memorize is the consecration step — the pipeline that takes committed relics and makes them *remembered*. A relic sitting in the vault but absent from the palace is an artifact no one can find: perfectly preserved, perfectly useless. Memorize bridges that gap, transforming static files into living, searchable memory.

Indexing is not summarizing. Every drawer stores verbatim relic content, chunked by section so searches return the precise passage relevant to a query — not a paraphrase, not a digest. The goal is section-level retrieval granularity: a search for "the finisher's method" should surface the relevant section, not the whole character file.

There are three input modes — identify which applies before proceeding:

- **File mode**: User provides specific relic files (or they were just created in this session) — index those
- **Batch mode**: Index all relics produced by a recent chronicle pass in one operation
- **Audit mode**: User wants to know which vault files have no palace representation, or which indexed entries are stale

> ⚠️ **Reload required.** Changes to the palace (new or updated drawers) will not be visible to Claude until the MCP server is restarted. For Claude Desktop: exit from the system tray, then relaunch — not just closing the window. The MCP server caches its connection state at launch. Remind the user of this at the end of every memorize session.

---

## Session Drawer Log

Memorize maintains a running log of every drawer touched during the session — created, updated, or skipped. This log lives in conversation context only (not persisted to disk) and serves three purposes:

1. **Progress tracking** — the user can ask "what have we indexed so far?" at any point
2. **Verification** — Phase 5 uses it to know exactly which drawer IDs to spot-check
3. **Rollback scope** — if something goes wrong, it identifies exactly which drawers were affected

Per drawer, track: drawer ID (or "pending" if not yet filed), source file, section(s) covered, action taken (created / updated / skipped).

Start the log at Phase 2; reference it in Phase 5 and the final report.

---

## Phase 1 — Identify Scope

### 1a — Load the palace
Call `mempalace_status` to confirm the system is live and load the full wing list.

### 1b — Identify wing and vault path
Match the relic content to the correct wing before doing anything else — never file content into the wrong wing, and never run unscoped operations that could bleed across projects.

### 1c — Identify the relics to index
- **File mode**: The user named specific files, or they were just committed in this session — use those
- **Batch mode**: List the target vault folder(s) with bash and confirm the full file set with the user before proceeding
- **Audit mode**: List all vault files and cross-reference against existing drawers — see Audit Mode section below

Never assume scope. If it's unclear which files are being indexed, ask.

### 1d — Check whether the wing exists and offer the terminal path for new wings

After loading the wing list from `mempalace_status`, check whether the target wing appears. If the wing is missing — meaning this is a fresh vault or a vault whose palace was just wiped — offer the manual terminal path before proceeding:

> "The `[wing]` wing doesn't exist in the palace yet. You have two options:
>
> **Option A — Terminal mining (recommended for first-time setup):** Run MemPalace's mine command from a terminal, folder by folder. This is significantly faster, uses almost no tokens, and produces a complete initial index without Claude making individual MCP calls per drawer. It requires a few minutes of terminal work and is only safe on a *new wing* or a *freshly wiped palace* — re-mining folders that already have drawers can produce duplicate entries and cause search to return the wrong version.
>
> **Option B — Let me handle it:** I can create all the drawers via MCP calls in Claude. It costs more tokens and is slower, but requires nothing from you. Say the word and I'll start."

If the user wants the terminal path, walk them through it — see **First-Time Wing Initialization** below.

If the user prefers Option B, skip this and proceed to Phase 2 as normal, starting with new-entry creation.

If the wing already exists, skip 1d entirely and proceed to Phase 2.

---

## First-Time Wing Initialization (Terminal Path)

Use this workflow when a wing is being indexed for the first time on a new vault or after a palace wipe. Do not use if any drawers for this wing already exist — re-mining existing content can generate duplicates.

Walk the user through these commands one block at a time, pausing to confirm each completes successfully before continuing.

### Step 1 — Verify mempalace is installed

```powershell
mempalace --help
```

If this fails, run `pip install mempalace --break-system-packages` first.

### Step 2 — Mine each vault subfolder individually

Mine World subfolders separately so MemPalace's room-detection heuristics assign meaningful room names rather than collapsing everything into `general`. All commands use the same `--wing` tag.

```powershell
mempalace mine "C:\path\to\Vault\World\Characters" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\Locations" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\Factions" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\History" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\Magic" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\Tech" --wing [wing-name]
mempalace mine "C:\path\to\Vault\World\Systems-Concepts" --wing [wing-name]
mempalace mine "C:\path\to\Vault\Arcs" --wing [wing-name]
mempalace mine "C:\path\to\Vault\Sessions" --wing [wing-name]
```

> **Note on special characters in folder names:** Folders with spaces or ampersands (e.g., `Systems & Concepts`) may need careful quoting in PowerShell. If a command errors, try wrapping the path in single quotes or escaping `&` with a backtick: `` `& ``.

> **What to mine vs. what to skip:** Include all World subfolders, Arcs, and Sessions. Skip: `.obsidian/` (plugins and config), `Templates/` (empty scaffolding), and any folder containing `.js`, `.css`, or other non-content files.

### Step 3 — Verify

```powershell
mempalace status
```

Check that the drawer count roughly matches the number of relic files. Then restart Claude Desktop (exit from the system tray, then relaunch) to pick up the new palace state.

### Step 4 — Confirm via MCP

After restarting, run `mempalace_status` through Claude Desktop to confirm the new wing appears in the palace layout. Optionally run a test search against a known entity name to verify content is retrievable.

After the terminal pass completes, return to **Phase 5 — Verification** to spot-check and log results, then proceed to Phase 6.

---

## Phase 2 — Existing Drawer Discovery

Before filing anything new, determine what the palace already holds. The goal is to **update existing drawers rather than create duplicates** — new drawers should only be created for sections with no existing representation.

### 2a — Search for existing drawers

For each relic, run `mempalace_search` scoped to the target wing using the entity name and source filename as the query. Also run `mempalace_list_drawers` filtered by wing to cross-reference by `source_file` metadata. Run all searches in parallel.

Collect every drawer whose `source_file` matches the relic being indexed. These are the **held drawers** — the palace's current representation of that relic.

### 2b — Classify the change

For each relic with held drawers, compare current content against what's stored:

- **Minor update** — sections are structurally the same with additions or light edits. **Action**: update existing drawers by appending new content to their verbatim text via `mempalace_update_drawer`. Updates are additive only — never remove or rewrite what's already stored.

- **New sections only** — the relic has new `##` sections that didn't exist before, but existing sections are unchanged. **Action**: leave existing drawers untouched; create new drawers only for the new sections.

- **Major rewrite** — structure has changed substantially, sections removed or rewritten from scratch, or the entity's identity has shifted enough that old drawers would be misleading. **Action**: surface this to the user and offer to run `/forget` on the existing drawers before replacing them. Explain that old and new content coexisting would produce contradictory search results.

### 2c — Duplicate check for new entries

For relics with **no existing drawers**, run `mempalace_check_duplicate` to catch near-matches under a different name or source file:

```
mempalace_check_duplicate(
  content="[Entity name] [type] [key identifying details from first section]"
)
```

If a check returns `is_duplicate: true`, stop and surface the match before filing. Show what exists and ask whether to skip, replace, or proceed.

---

## Phase 3 — Index Plan → Checkpoint

Before filing a single drawer, present a brief plan for approval.

Show:
- Each relic to be indexed, with its target wing/room
- Whether each is a **new index**, **update to existing drawers**, or **replace after /forget**
- The proposed section chunking — how many drawers per file and which sections each covers
- For updates: which existing drawer IDs will be touched and what's being appended
- Any relics being skipped and why

**Do not open a single drawer until the user confirms.**

---

## Phase 4 — Index Execution

### New drawers

```
mempalace_add_drawer(
  wing:        "[wing]",
  room:        "general",
  source_file: "[filename].md",
  added_by:    "memorize",
  content:     "[verbatim section text]"
)
```

### Updated drawers

```
mempalace_update_drawer(
  drawer_id:   "[existing drawer ID]",
  content:     "[existing verbatim content]\n\n[new additions appended]"
)
```

When updating, always fetch current content first with `mempalace_get_drawer` to ensure you're appending to the latest version. The update must preserve everything already stored and add new material after it.

Log every action to the session drawer log as it completes.

### Chunking rules

The right chunk size is a section, not a file:

- **Frontmatter + first section** → one drawer (frontmatter anchors the entity identity)
- **Each subsequent `##` section** → its own drawer, unless very short (under ~100 words), in which case combine with the adjacent section
- **Notes** → always its own drawer; the most analytically dense section benefits from isolated retrieval
- **Never more than 2–3 sections per drawer** — larger drawers produce less precise retrieval

Typical counts: character relics yield 4–5 drawers; faction relics 4–5; short concept/tech relics 2–3.

### Batching

Batch parallel calls aggressively — file drawers for different relics in the same turn. Within a single relic, section drawers can also run simultaneously. Wait for each batch to confirm before starting the next. If any drawer returns an error, stop and surface it.

### Assigning Drawers to Rooms

MemPalace's terminal mining assigns rooms automatically using heuristics on folder names. When drawers are created via MCP (either through Memorize or after a terminal mine where room assignment was too coarse), rooms can be set or corrected using `mempalace_update_drawer`.

**When to offer room assignment:**
- After a terminal mine, if `mempalace_list_drawers` shows most drawers landed in `general` instead of category-specific rooms
- When filing drawers via MCP and a more specific room than `general` would improve retrieval scoping
- When the user asks to reorganize existing drawers by type

**How to assign rooms in bulk after a terminal mine:**

First, list drawers with their current room assignments:

```
mempalace_list_drawers(wing="[wing]")
```

Identify drawers in `general` that belong to a more specific room. Common room names that align with vault structure:

| Vault folder | Suggested room name |
|---|---|
| World/Characters | characters |
| World/Locations | locations |
| World/Factions | factions |
| World/Magic | magic |
| World/History | history |
| World/Tech | tech |
| World/Systems-Concepts | concepts |
| Arcs | arcs |
| Sessions | sessions |

Then update each misassigned drawer:

```
mempalace_update_drawer(
  drawer_id: "[drawer ID]",
  room:      "[correct room name]"
)
```

Batch these calls — MemPalace handles concurrent updates. Present a plan first if the count is large (more than ~20 drawers), so the user can confirm before the operation runs.

---

## Phase 5 — Verification

Spot-check using the session drawer log:

```
mempalace_search(query="[entity name] [distinctive detail]", wing="[wing]")
```

One search per relic (or per batch for large sessions). New and updated drawers should surface with high similarity scores. If a just-indexed relic doesn't appear in top results for its own name, investigate before reporting success.

Report to the user:
- Total drawers created, updated, and skipped
- Confirmation that entities are retrievable by name and detail
- The reload reminder:

> ⚠️ **Restart Claude** (for Desktop: exit from the system tray, then relaunch) for these changes to take effect in future sessions. The palace will serve stale results for updated drawers until then.

---

## Phase 6 — Knowledge Graph Offer

After verification, check whether the indexed relics contain relationships, affiliations, status facts, or other structured data that should live in the knowledge graph. If they do, offer to map them.

**How to check**: Scan the relic content that was just indexed for named relationships (e.g., "member of," "allied with," "rival of"), status declarations, faction affiliations, or any entity-to-entity connection. Also run `mempalace_kg_query` on each indexed entity to see what the KG already holds — if the relic contains relationships not yet in the graph, those are candidates.

**If unmapped relationships exist**, offer concisely:

> "These relics contain relationships that aren't in the knowledge graph yet — [brief summary, e.g., 'Sera's faction membership and rivalry with Aldric']. Want me to run `/cartograph` to map them?"

**If the KG already covers the entities well**, skip the offer silently. Don't prompt the user for something that's already handled.

**If the user accepts**, transition into cartograph's Phase 2 (Design) directly — the survey work is already done from the memorize pass. Present the triple plan for approval and proceed through cartograph's execution and verification phases.

---

## Chunking Reference

| Relic type | Typical drawer breakdown |
|---|---|
| Character | Frontmatter+Description / Background+Motivations / Relationships+Current Status / Notes |
| Faction | Frontmatter+Overview / Philosophy+Structure+History / Key Members+Relationships+Current Status / Notes |
| Location | Frontmatter+Description / History+Current State / Notable Features+Notes |
| System/Concept | Frontmatter+What Is It / How It Works+Consequences / Notes |
| Tech | Frontmatter+Overview / Rules+Variants / Notes |

When in doubt, give each major section its own drawer. An extra drawer is cheap; an oversized drawer degrades retrieval.

---

## Audit Mode

When checking coverage rather than indexing:

1. List all relic files on disk across relevant vault folders
2. For each, run `mempalace_search(query="[filename without extension]", wing="[wing]")` to check for existing drawers
3. Build a gap report: files with no palace entries, files with entries predating recent vault changes
4. Present the gap report and ask which gaps to address now
5. Proceed with approved subset through Phases 2–5

Audit mode is non-destructive — it reads, lists, and reports. Nothing is filed until approved.

---

## What Memorize Does Not Do

- **Summarize.** Drawer content is verbatim relic text. Paraphrasing introduces drift between disk and memory.
- **File whole relics as single drawers.** Section-level chunking is what makes the palace useful.
- **Skip existing drawer discovery.** Duplicate drawers degrade search quality silently over time.
- **Remove content from existing drawers.** Updates are additive. Removal requires the /forget → re-index path.
- **File across wing boundaries.** Cross-project contamination is silent and hard to undo.
