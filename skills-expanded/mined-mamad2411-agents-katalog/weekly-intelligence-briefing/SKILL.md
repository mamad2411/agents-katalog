---
name: weekly-intelligence-briefing
description: "Analyze Lou's active Claude Code / Cowork sessions from the past week and produce an AIMM Weekly Intelligence Briefing — distilled R&D coverage with deep dives on high-value projects, operational session summaries, an assets table, and a developing-threads watch list. Publishes as a child page under the Weekly Intelligence Briefings hub in Notion. Trigger: 'run the weekly briefing', 'generate this week's intelligence briefing', 'aimm briefing', or scheduled invocation with no args."
---

# AIMM Weekly Intelligence Briefing

Distill Lou's active R&D week (Claude Code / Cowork sessions) into a structured intelligence briefing for AIMM members. Not session minutes — a curated, opinionated digest of the tools built, frameworks discovered, and assets that members can put to work immediately.

**Community:** AI Mastermind for Leaders (AIMM)
**Audience:** Knowledge entrepreneurs — coaches, consultants, course creators, advisors using AI seriously enough to feel friction
**Notion hub:** `34bbe0e844bb81c98585ecce16806292` (Weekly Intelligence Briefings, child of AIMM Report Hub)
**Title format:** `🧠 Week of [Month Day–Day, Year] — Intelligence Briefing`

**Voice reference:** Always read `reference-example.md` (in this skill's directory) before drafting. It is the canonical stylistic anchor — match its voice, structure, and depth.

---

## What This Skill Produces

A Notion page with the following sections, in this exact order:

1. **Callout block** — "For AIMM Members" orientation with ⭐ marker explanation
2. **🗂 At a Glance** — Table: Session date | Topic | Member Relevance (⭐ for high-value)
3. **🔑 This Week's Big Themes** — 3–4 numbered, bolded theme claims, each unpacked in a paragraph
4. **📦 Project Deep Dives** — Numbered H3 sections (typically 3–5), 400–800 words each, for high-value R&D work
5. **🔧 Operational Sessions** — Client work, grouped by client name, 2–3 sentences each
6. **🧰 Assets Available This Week** — Table: Asset | Description | Status
7. **🔭 Watch List — Developing Threads** — Bullet list of open threads, blockers, upcoming work
8. **Footer** — Two italic lines: date range + "Compiled for AIMM members."

---

## Inputs

This skill runs in one of two modes:

**Auto mode (default)** — no arguments. Analyze every session modified in the last 7 days, pulled from **two sources**:
1. `~/.claude/projects/*.jsonl` — live Claude Code session transcripts (raw)
2. `~/vault/weekly-briefing-inbox/*.md` — pre-summarized session records from claude.ai and Cowork, dropped here by the companion extraction prompts (see `extraction-prompts.md` in this skill's directory)

**Manual mode** — user provides a date range (e.g., "for May 3–9") or specifies "look back 14 days." Adjust the window accordingly.

**Output destination:** Notion page under hub `34bbe0e844bb81c98585ecce16806292`, plus a local markdown copy at `~/Downloads/aimm-briefings/[date-range].md`.

---

## How to Generate the Briefing

### Step 1: Determine the date window

Default: the 7 days ending today (Sunday week-end if today is Saturday/Sunday; otherwise today-back-7).

Format the window as `[Month Day]–[Day, Year]` (e.g., `May 4–10, 2026`). If it crosses a month boundary, use `Apr 28–May 4, 2026`.

### Step 2: Inventory the sessions

Pull from **both sources** in parallel.

**Source A — Claude Code transcripts (raw .jsonl):**

```bash
find ~/.claude/projects -name "*.jsonl" -newermt "$(date -v-7d +%Y-%m-%d)" -type f
```

For each transcript:
- **Session date** = file mtime
- **Project** = parent directory name (decoded from the slug, e.g., `-Users-loudalo-Downloads-foo` → `~/Downloads/foo`)
- **First substantive user message** = often the session's intent — read the first 2-3 user turns
- **Outputs** = files written/edited (grep for `"name":"Write"` and `"name":"Edit"` tool_use events)
- **Topic** = derive from the user's framing, not from tool output

For sessions over ~200 turns, sample: first 5 user turns, last 5 user turns, and any turn with a `Write` of a markdown file in a non-trivial path.

**Source B — Inbox records (pre-summarized markdown):**

```bash
find ~/vault/weekly-briefing-inbox -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)" -type f
```

These files come from claude.ai exports and Cowork sessions via the companion extraction prompts (`extraction-prompts.md`). They're already structured — read the YAML frontmatter (`source`, `date`, `title`, `type`) and the section bodies (Intent, Outputs/Artifacts, Key Threads, Open Threads, Notable Verbatim). Use the `source:` field for attribution in the At a Glance table (mark `chat` and `cowork` items distinctly from Claude Code).

Skip any inbox file whose body is exactly `SKIP — no compounding value` — the extraction prompt uses that sentinel to signal a throwaway session that should be ignored.

**Merged inventory:**

Build a single list of sessions from both sources, sorted by date. Each item has: source (`code` | `cowork` | `chat`), date, title, type, outputs/artifacts, key threads, open threads. From here on, the synthesis steps treat all three sources equivalently.

**Important:** Don't enumerate every session in the briefing. The At a Glance table includes only sessions that produced something worth surfacing — drafts, frameworks, decisions, artifacts. Throwaway debugging or one-off lookups don't belong in the table.

### Step 3: Classify each session

Two buckets:

- **R&D / framework work** → candidate for deep dive. These are sessions where Lou built something reusable: a skill, a framework, a teaching artifact, a system design.
- **Operational / client work** → goes in the 🔧 Operational Sessions block. Anything in `GEO Folder/`, named after a client, or about delivery/execution rather than discovery.

Mark high-value R&D sessions with ⭐ — these are the ones AIMM members can directly apply. Typical week has 3–5 starred items, not 10.

### Step 4: Extract the Big Themes (3–4)

These are the most important paragraphs in the briefing. They're not summaries — they're **transferable claims** that emerge from looking across the week.

Process:
1. Read across all R&D deep-dive candidates
2. Ask: what insight do these collectively point at? What did this week *prove*?
3. Write each theme as an assertion: `**N. [Bold claim sentence.]**` followed by 3–5 sentences unpacking it

Themes take a position. They never hedge ("this might suggest", "potentially this means"). If you can't take a position, the theme isn't ready — keep digging.

### Step 5: Write the Deep Dives (3–5 sections)

Only for ⭐ R&D sessions. Each one:

- **H3 title** with optional `⭐ HIGH MEMBER VALUE` tag
- **Session:** brief description of which session(s)
- **Output:** exact file path or artifact name — never paraphrase this
- 400–800 words of narrative covering: the trigger/problem, the core logic, the artifact produced, and how a member can use it
- Tables when structure helps (file inventories, principles, comparison)
- End with an actionable closer: `**How to use:**` or `**To start:**` — one paragraph that tells the reader exactly what to do

Voice: practitioner-direct, no fluff. Show artifacts (file paths, code, specific examples) before explaining them. First-person past tense for the doing ("The session started from a question..."), present tense for what the artifact does.

### Step 6: Write Operational Sessions

Grouped by client or workstream. Each entry:

```markdown
**Client Name — Project** — Status sentence. Specific concrete items handled this week. Any blocker or next move.
```

2–3 sentences max. No deep dive treatment. If a client wasn't worked on this week, skip them entirely.

### Step 7: Build the Assets Table

Three columns: **Asset | Description | Status**

Include: new frameworks, new skills, distributable zips, new reference docs, anything members could request or download. Status is concrete: "In `[folder]`", "Live command", "Ready to distribute", "Ask Lou".

### Step 8: Build the Watch List

Bullets covering: deferred work with explicit version targets ("AIF v0.2"), blockers waiting on external input, threads expected to land next week, calibration thresholds for in-flight projects.

Each bullet names the thread and the developing fact — not aspirations.

### Step 9: Assemble + draft locally

Write the full briefing to `~/Downloads/aimm-briefings/[YYYY-MM-DD]-week-of-[range].md` first. Verify:

- 🗂 At a Glance table is populated
- 3–4 themes, each as a bold claim
- 3–5 deep dives, each with Session + Output named
- Operational sessions concise
- Assets table specific (no vague "various assets")
- Watch List has concrete threads, not wishes
- Footer is exact: two italic lines

### Step 10: Publish to Notion

Use the Notion MCP via a sub-agent (the tools disconnect intermittently in main context — delegate to ensure reliability).

The sub-agent should:
1. Create a new page under parent `34bbe0e844bb81c98585ecce16806292`
2. Title: `🧠 Week of [date range] — Intelligence Briefing`
3. Icon: 🧠
4. Body: the assembled markdown from Step 9
5. Return the new page URL

If Notion is unavailable, report the local markdown path and ask Lou to publish later.

---

## Style Constraints

These are non-negotiable. They define the difference between a useful briefing and a generic AI digest.

- **Take a point of view.** Themes are claims. Deep dives have opinions. Never measured, never balanced.
- **Concrete over abstract.** Every deep dive names a file path or artifact. Vague capability descriptions are a smell.
- **Show, then explain.** Quote the actual prompt, the actual decision, the actual file structure. Don't paraphrase Lou's thinking.
- **No filler phrases.** Banned: "In conclusion," "It's worth noting that," "This is important because," "At the end of the day."
- **No hedge language.** "Potentially," "might suggest," "could be valuable" — kill all of these. Make the call.
- **First-person past tense for the doing.** "The session started from..." not "When you start a session..."
- **Present tense for the artifact's behavior.** "The template includes 21 files..." — these are stable facts about the thing.
- **The reader is a peer practitioner.** They don't need definitions of "skill" or "harness." They need to know what was built and how to use it.

---

## Verification Before Publishing

Run this checklist before sending to Notion:

1. **At a Glance table** matches the deep dives — every ⭐ in the table appears as a deep dive section
2. **No deep dive lacks an Output line.** If you can't name the artifact, it doesn't belong as a deep dive
3. **Operational sessions don't drift into deep-dive length.** 2–3 sentences each, max
4. **Assets table status column is specific** — no "various", "multiple", or "TBD"
5. **Watch List items name the next state**, not just the current state ("Awaiting Kasimir's approval on 11 terms" not "MindMastery is ongoing")
6. **Voice is Lou's** — practitioner-direct, takes positions, no AI hedge phrases. If a paragraph reads measured, rewrite it
7. **Footer is exact:** two italic lines, date range + "Compiled for AIMM members."

---

## Memory & Continuity

After publishing, append one line to `~/Downloads/aimm-briefings/index.md`:

```
- [Week of [range]] — [Notion URL] — [N deep dives, N starred]
```

This lets future runs see what was covered recently (avoid repeating a theme that just landed) and gives Lou a chronological index outside of Notion.
