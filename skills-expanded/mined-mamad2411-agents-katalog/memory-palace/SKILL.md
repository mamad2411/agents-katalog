---
name: memory-palace
description: >
  Cross-conversation memory system using a "Memory Palace" metaphor (wings, rooms, tunnels).
  Gives AI persistent context across sessions by storing research notes, decisions, and discoveries
  in a structured file hierarchy. Use whenever the user says "save to palace", "remember this",
  "what did we discuss last time", "recall", "read palace", "palace status", "store today's notes",
  "update memory", "show palace map", "palace stats", or "export palace". Also triggers when
  the user starts any task that needs prior conversation context (e.g. "continue working on X",
  "last time we talked about Y", "where did we leave off"). If a memory/ directory with PALACE.md
  exists in the project, always read it at conversation start.
user-invocable: true
---

# Memory Palace — Cross-Conversation Memory System

A file-based memory system inspired by [MemPalace](https://github.com/milla-jovovich/mempalace)
and the ancient Greek *Method of Loci*. It organizes AI conversation history into a navigable
"palace" structure, so every new conversation can pick up exactly where the last one left off.

## Why This Exists

The #1 frustration with AI assistants: **they forget everything between conversations.**
You spend an hour discussing architecture decisions, reading papers, analyzing data — then next
session, it's all gone. Memory Palace solves this by persisting the important parts as structured
files that the AI reads at the start of each new conversation.

## Architecture

```
memory/
├── PALACE.md              ← Lobby: global index + hot cache (always read first)
├── wings/                 ← Topic-based memory sections
│   ├── <wing-name>/
│   │   ├── YYYY-MM-DD_topic.md   ← Notes from a conversation
│   │   └── ...
│   └── ...
└── tunnels/               ← Cross-wing conceptual links
    └── <connection-name>.md
```

**Wings** = major topics or projects (like floors of a building)
**Notes** = conversation summaries within a wing (like rooms on a floor)
**Tunnels** = cross-references connecting related ideas across different wings (like secret passages)

## Locating the Palace

Search for the palace in this order:

1. `memory/PALACE.md` in the current working directory
2. `memory/PALACE.md` in any mounted/workspace folder
3. If not found, **trigger the First-Run Onboarding flow below**

## First-Run Onboarding (No Palace Found)

When no `memory/PALACE.md` exists, Claude should NOT just say "no palace found" and wait.
Instead, proactively guide the user through setup with a friendly, conversational flow.

### Step 1: Introduce the Concept (2-3 sentences)

Explain what Memory Palace does in plain language. Avoid jargon. Example:

> "I have a memory system called Memory Palace that lets me remember things across our
> conversations. Right now I don't have one set up for this project. Want me to create
> one? It takes about 30 seconds."

If the user says yes, continue. If no, drop it and proceed with the conversation normally.

### Step 2: Ask About Their Project (1 question)

Ask what major topics or projects they're working on. These become wings. Example:

> "What are the main topics you're working on? For example: 'paper writing, experiment,
> job search' or 'frontend, backend, devops'. I'll organize your memory around these."

### Step 3: Initialize (automatic)

Run `palace_init.py` with the wings they mentioned:

```bash
python <skill-path>/scripts/palace_init.py <target-dir> \
  --wings <wing1> <wing2> <wing3> \
  --name "<project name>"
```

### Step 4: Confirm and Explain What Happens Next (brief)

Tell them:
- "Done! I'll remember key things from our conversations automatically."
- "You don't need to do anything special. At the end of each chat, I save what matters."
- "If you ever want to check what I remember, just say 'palace status' or 'show palace map'."

### What NOT to Do During Onboarding

- Don't overwhelm with technical details (wings, tunnels, hot cache, tokens)
- Don't show the directory structure unless they ask
- Don't explain every feature. Let them discover features naturally over time.
- Don't make it feel like a configuration wizard with 10 steps

The goal is: **30 seconds from "want me to set up memory?" to "done, I'll remember things now."**

## Auto-Save Behavior (Transparent Memory Persistence)

The most important improvement over manual-only saving. Claude should **always** save session learnings without waiting for the user to say "save to palace."

### When to Auto-Save

At the **end of every conversation** where any of these happened:
1. A research insight or "aha moment" was discussed
2. A decision was made (why A over B)
3. Experiment results with specific numbers were produced
4. A new cross-topic connection was discovered
5. The user's project status meaningfully changed

### How to Auto-Save

Use `palace_autosave.py` or write directly:

```bash
python <skill-path>/scripts/palace_autosave.py <memory-dir> \
  --wing <detected-wing> \
  --summary "One-line session summary" \
  --discoveries "Key finding 1; Key finding 2" \
  --decisions "Decision 1; Decision 2"
```

Or write the note manually following the note format in Action 2.

### What NOT to Auto-Save
- Pure debugging sessions with no conclusions
- Conversations that only read/reviewed existing content
- Sessions where the user explicitly said "don't save this"

### For Claude Code Users: Hook Setup
See `hooks/README.md` for how to configure automatic triggering via Claude Code's Stop hook.

### For Cowork Users
The SKILL.md instructions handle this automatically — Claude will save at conversation end
when it detects saveable content.

## Core Actions

### Action 1: Load Memory (every new conversation)

This is the most important action. At conversation start, or when the user's question involves prior work:

1. **Read PALACE.md** — scan the Hot Cache table for each wing's latest status
2. **Read relevant wing notes** — based on what the user is asking about (don't read everything)
3. **Scan tunnels/** — check for cross-topic links that add useful context

After loading, proactively tell the user what you remember:

> "I see from your palace that you were working on X last time (Apr 8), and discovered Y.
> Want to continue from there?"

This matters because the user's biggest pain point is "AI amnesia." Showing you remember
builds trust and saves them from re-explaining context.

### Action 2: Save to Memory (end of conversation or on significant progress)

Triggers: user says "save to palace", "remember this", "store today's notes", or you judge
there's something worth recording.

1. **Determine the right wing** — classify by topic
2. **Write a note file** — save to `wings/<wing>/YYYY-MM-DD_<topic>.md`
3. **Update PALACE.md** — modify the Hot Cache table for that wing
4. **Create tunnels** — if you discovered cross-topic connections

#### Note Format

```markdown
# Title

> Date: YYYY-MM-DD
> Source: conversation / paper / experiment / tool review
> Type: concept-learning / experiment-result / decision-record / paper-analysis / tool-evaluation

## Key Content
(Write for "future you who forgot the details" — clear but not verbose)

## Connection to Current Work
(How does this relate to what the user is working on?)

## References
(URLs, paper IDs, file paths)
```

Writing principles:
- Write for someone reading this 3 months later with no memory of the conversation
- Include specific numbers and conclusions, not just "discussed X"
- The "Connection to Current Work" section is the anchor for future recall — always fill it in

#### Tunnel Format

```markdown
# Tunnel: <connection-name>

> Created: YYYY-MM-DD
> Connects: wing-A ↔ wing-B

## Core Insight
(Why are these two topics related? What new perspective does this connection provide?)

## Where to Apply
(Research statement? Paper? System design? Email to professor?)
```

**Saving with import:** If the user has a conversation transcript to import, you can use:

```bash
python <skill-path>/scripts/palace_import.py <transcript-file> <path-to-memory-dir> --wing <target-wing> [--dry-run]
```

The `--dry-run` flag shows you what notes will be created without actually writing them, so you can review before committing.

### Action 3: Initialize New Palace

If no palace exists, automate setup with:

```bash
python <skill-path>/scripts/palace_init.py <target-dir> [--wings wing1,wing2,... --name "Palace Name" --force -v]
```

This creates the directory structure and initial PALACE.md automatically. Alternatively, guide the user through setup manually:

1. Ask what major topics/projects they want to track (→ becomes wings)
2. Create the `memory/` directory structure
3. Write an initial `PALACE.md` with an empty Hot Cache table
4. Create wing directories
5. If the project has a `CLAUDE.md`, add Memory Palace instructions to it

The script can automate all of this. Use `--wings` to pre-define wings, `--name` to customize the palace name, `--force` to overwrite an existing palace, and `-v` for verbose output.

### Action 4: Visualize Palace (when user asks "show palace map" or "visualize")

Generate a Mermaid diagram showing the palace structure. Run:

```bash
python <skill-path>/scripts/palace_map.py <path-to-memory-dir>
```

This produces a `.mermaid` file showing wings, notes, and tunnel connections.
If the user is in Cowork, also generate an HTML version they can open in their browser.

### Action 5: Show Palace Stats (when user asks "palace stats" or "how big is my palace")

Run:

```bash
python <skill-path>/scripts/palace_stats.py <path-to-memory-dir>
```

This outputs:
- Total wings, notes, and tunnels
- Most active wing (by note count)
- Most recent activity per wing
- Estimated token count for full palace load vs. hot-cache-only load
- Timeline of note creation

### Action 6: Import/Export (when user asks "export palace" or "import conversations")

**Export to Obsidian vault:**
```bash
python <skill-path>/scripts/palace_export.py <path-to-memory-dir> --format obsidian --output <output-dir>
```

**Export to single Markdown:**
```bash
python <skill-path>/scripts/palace_export.py <path-to-memory-dir> --format markdown --output palace_export.md
```

**Import from conversation transcript (Claude/ChatGPT JSON export):**
```bash
python <skill-path>/scripts/palace_import.py <transcript-file> <path-to-memory-dir> --wing <target-wing> [--dry-run]
```

The import script extracts key decisions, discoveries, and action items from conversation
transcripts and creates note files in the appropriate wing. Use `--dry-run` to preview
what will be imported without writing files.

### Action 7: Search Notes (when user asks "search palace", "find in notes", "where did I mention X")

Run:

```bash
python <skill-path>/scripts/palace_search.py <path-to-memory-dir> <query> [--wing wing-name --case-sensitive --context --no-color]
```

**Options:**
- `--wing <name>` — limit search to a specific wing
- `--case-sensitive` — match case exactly (default: case-insensitive)
- `--context` — show lines before and after each match (default: just matching line)
- `--no-color` — disable colored output

**Example usage:**
```bash
# Search across entire palace for "router"
python scripts/palace_search.py ./memory "router"

# Search only in the "enterprise-multi-agent" wing
python scripts/palace_search.py ./memory "agent routing" --wing enterprise-multi-agent

# Show full context around matches
python scripts/palace_search.py ./memory "baseline" --context

# Case-sensitive search for "R4" (not "r4")
python scripts/palace_search.py ./memory "R4" --case-sensitive
```

This is much faster than reading through individual wing files when you're looking
for a specific insight or decision you recorded earlier.

### Action 8: Health Check (when user asks "check palace health", "validate palace", "is my palace ok")

Run:

```bash
python <skill-path>/scripts/palace_health.py <path-to-memory-dir> [--fix --json --stale-days 30 -v]
```

**Options:**
- `--fix` — automatically fix detected issues (broken links, orphaned files, etc.)
- `--json` — output results as JSON instead of human-readable text
- `--stale-days <N>` — flag wings with no activity in the last N days (default: 60)
- `-v` — verbose output showing detailed checks and explanations

**What it checks:**
- Structural integrity (missing PALACE.md, invalid directory structure)
- Broken references (tunnels linking to non-existent wings, dead links in notes)
- Orphaned files (note files in wings not listed in PALACE.md)
- Activity patterns (which wings are stale, which are most active)
- File format consistency (note headers, metadata, formatting)

**Example:**
```bash
# Quick health check
python scripts/palace_health.py ./memory

# Check and auto-fix issues
python scripts/palace_health.py ./memory --fix

# Find wings inactive for 90+ days
python scripts/palace_health.py ./memory --stale-days 90

# Full diagnostic with explanations
python scripts/palace_health.py ./memory -v
```

Run this periodically to keep your palace well-maintained and catch dead links or
stale sections that need attention.

### Action 9: Fast Palace Initialization (new palace setup automation)

Run:

```bash
python <skill-path>/scripts/palace_init.py <target-dir> [--wings wing1,wing2,wing3 --name "Palace Name" --force -v]
```

**Options:**
- `--wings <list>` — comma-separated list of wing names to create (optional; will prompt if not provided)
- `--name <name>` — custom name for the palace in PALACE.md (default: "Memory Palace")
- `--force` — overwrite existing palace (use with caution)
- `-v` — verbose output showing what was created

**Example:**
```bash
# Interactive setup (will prompt for wings)
python scripts/palace_init.py ./memory

# Pre-define wings
python scripts/palace_init.py ./memory \
  --wings "paper1-cost-router,paper2-tau-bench,enterprise-multi-agent,grad-application,research-learning" \
  --name "Research & Grad Application Palace"

# Reinitialize (backup first!)
python scripts/palace_init.py ./memory --force --name "Fresh Start"
```

This is the automated version of Action 3 (Initialize New Palace). It creates the full
directory structure, an initial PALACE.md with your specified wings, and empty wing folders,
all in seconds.

## PALACE.md Hot Cache Format

```markdown
# Memory Palace — <Project Name>

## Wings Summary (Hot Cache)

| Wing | Status | Recent Activity | Key Numbers/Conclusions |
|------|--------|----------------|------------------------|
| wing-name | active/done/paused | YYYY-MM-DD: what happened | important data points |

## Tunnels

| Tunnel | Connects | Core Insight |
|--------|----------|-------------|
| [name](tunnels/file.md) | A ↔ B | one-line description |
```

The Hot Cache is designed after MemPalace's wake-up mechanism — use minimal tokens (~200 lines max)
to restore the AI to the previous session's state. Only dive into wing notes when details are needed.

## What to Save vs. Skip

**Worth saving:**
- Research insights and "aha moments"
- Decisions and their reasoning (why A over B)
- Experiment results with specific numbers
- Paper reading notes with connections to current work
- New conceptual frameworks learned
- Unexpected cross-topic connections

**Not worth saving:**
- Code itself (it's in the repo)
- Git history (`git log` is authoritative)
- Pure engineering details (better in DEVLOG)
- Temporary debugging steps

## Tunnel Auto-Suggest (Proactive Cross-Topic Linking)

Claude should **proactively suggest** creating a tunnel when it detects cross-wing connections.
Don't auto-create tunnels silently — suggest them to the user first.

### When to Suggest a Tunnel

During any conversation, if you notice that:
1. **Two different wings share a concept** — e.g., "cost-aware routing" appears in both paper1 and enterprise notes
2. **A decision in one wing affects another** — e.g., a paper finding changes the enterprise system design
3. **A research insight bridges two projects** — e.g., a technique from research-learning applies to paper2

Then proactively tell the user:

> "I noticed that [concept X] connects your [wing-A] and [wing-B] work. Want me to create
> a tunnel documenting this link? It would help future sessions spot this connection."

### When NOT to Suggest

- If a tunnel already exists connecting those wings on the same topic (check tunnels/ first)
- If the connection is trivial or obvious (e.g., all wings relate to "research")
- If the user is in the middle of focused work and the suggestion would be disruptive

## Hall Classification (Optional Wing Sub-Organization)

When a wing accumulates many notes (15+), flat organization becomes hard to navigate.
The original MemPalace uses "halls" as sub-categories within wings.

### Available Hall Types

| Hall | Purpose | Example Notes |
|------|---------|--------------|
| `facts/` | Established knowledge, reference data | API specs, benchmark numbers, paper citations |
| `events/` | Time-bound happenings | experiment runs, meetings, deadlines |
| `discoveries/` | Insights and aha moments | cross-topic connections, unexpected results |
| `decisions/` | Choices made and their reasoning | architecture decisions, paper strategy |

### When to Use Halls

- **Don't use halls by default.** Flat wings are simpler and work fine for <15 notes.
- **Suggest halls** when a wing hits 15+ notes and the user is having trouble finding things.
- **Migration is safe** — just create subdirectories and move existing notes. Update any
  references in PALACE.md or tunnels.

### Directory Structure with Halls

```
wings/
├── paper1-cost-router/
│   ├── facts/
│   │   └── 2026-04-08_benchmark-numbers.md
│   ├── events/
│   │   └── 2026-04-08_paper-review-round4.md
│   ├── discoveries/
│   │   └── 2026-04-08_setfit-beats-llm.md
│   └── decisions/
│       └── 2026-04-05_acl-workshop-format.md
```

## Archive & Aging (Keeping the Palace Lean)

Over time, palaces accumulate stale notes and PALACE.md grows beyond the ideal ~200 lines.
Use `palace_archive.py` to manage this:

```bash
# Preview what would be archived (safe, no changes)
python <skill-path>/scripts/palace_archive.py <memory-dir> --dry-run

# Archive notes older than 90 days, keep max 20 per wing
python <skill-path>/scripts/palace_archive.py <memory-dir> --archive-age 90 --max-notes-per-wing 20

# Archive with PALACE.md line limit check
python <skill-path>/scripts/palace_archive.py <memory-dir> --max-lines 200
```

Archived notes are **moved, not deleted**, to `memory/archive/wings/<wing>/`. A manifest
(`_archived.txt`) records what was moved and when, so nothing is ever lost.

## Maintenance Principles

- **Keep PALACE.md lean** — Hot Cache table should have ≤10 wings, ≤200 lines total
- **Notes can grow freely** — each wing can have many notes, find them by date and title
- **Don't delete outdated notes** — archive them with `palace_archive.py` instead
- **Tunnel quality over quantity** — only record genuinely insightful cross-topic links
- **Auto-save by default** — save session learnings without waiting for user to ask
- **Suggest tunnels proactively** — when cross-wing connections emerge, offer to link them
- **Halls are optional** — only introduce sub-organization when a wing gets crowded (15+)
