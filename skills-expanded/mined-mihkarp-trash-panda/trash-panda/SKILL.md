---
name: trash-panda
description: >
  A raccoon that digs through your Claude/ChatGPT chat history, pulls out the
  valuable artifacts, and files them into a local markdown "den" organized by
  project. Triggers on "/dig", "/den", "/sniff", "/feed", "/wash", "/nap", or
  natural language like "go dig through my chats", "what piled up", "drag the
  good stuff into my projects", "show me my den". Reads recent chats, extracts
  four artifact types (To Do's, Shiny, The Plan, Loot), routes each to a project
  file, dedupes, appends, links back to the source chat, and rebuilds the den
  index. ALWAYS use this skill for these commands — do not do it by hand.
---

# Trash Panda 🦝

He digs through your chats and drags the good stuff back to the den.
The den is a plain `den/` folder of markdown — one file per project — that he
appends to. He never overwrites your hand edits.

Commands: `/dig` (main), `/den`, `/sniff`, `/feed <chat>`, `/wash`, `/nap`.

---

## `/dig` — the main loop

### Step 1 — Read the den (get context)

1. Make sure `den/` exists. If not, create it with an empty `den/index.md`.
2. Read every `den/*.md` file. Build a list of:
   - existing **project files** (filename → project name)
   - existing **artifact titles** per project (for dedup)
3. Read the last-dig timestamp from the top of `den/index.md`
   (line format: `<!-- last_dig: YYYY-MM-DDTHH:MM:SSZ -->`).
   If absent, treat `last_dig` = 7 days ago.

### Step 2 — Read chats since the last dig

```
recent_chats(n=20, sort_order="desc")
```
If `last_dig` is older than 3 days, page back with `before=` for full coverage.
Only process chats updated AFTER `last_dig`.

For each chat, capture its URL so every artifact can link back:
`https://claude.ai/chat/<id>` (or the ChatGPT URL when digging an export).

### Step 3 — Extract artifacts

Scan each chat and pull out four types:

| Type | Signals in the text |
|------|--------------------|
| 📝 **To Do** | "need to", "next step", "send X", "write the…", "follow up", explicit next actions |
| 💎 **Shiny** | "idea", "what if", "could try", "worth exploring" — a thought worth keeping |
| 🗺️ **The Plan** | a decided approach, strategy, sequence of steps, "here's the plan", "we'll do X then Y" |
| 📜 **Loot** | something actually produced — a draft, doc, CV, reading list, snippet, named output |

For each artifact determine:
- **title** — short, concrete, ≤ 80 chars
- **type** — todo / shiny / plan / loot
- **project** — match an existing den project, or a new project name, or `inbox`
- **confidence** — high / mid / low
- **source** — the chat URL (for the backlink)

### Step 4 — Dedup

Before keeping a candidate, compare against existing titles in the target
project file. If a near-match already exists (>70% meaning overlap), skip it.
The same Shiny must never land twice.

### Step 5 — Show the haul (approve before writing)

Render an interactive widget (`visualize:show_widget`) with:
- **Already in den** — duplicates, greyed out
- **New haul** — everything else, each row with `✓ keep` / `✕ toss`

Columns: artifact (title) · type badge · project · confidence · source link.
Bottom button "Stash selected → den ↗" calls `sendPrompt()` with the approved list.

**Write nothing until the user approves.** If the haul is empty, say so plainly
(*"dug around, nothing new worth keeping"*).

### Step 6 — Stash approved artifacts into the den

For each approved artifact, **append** to `den/<project>.md` under the right
section (create the file from the template below if missing). Never overwrite
existing content.

Line format per type:

```markdown
## 📝 To Do's
- [ ] <title>  [↗](<source_url>)

## 💎 Shiny
- <title>  [↗](<source_url>)

## 🗺️ The Plan
- <title>  [↗](<source_url>)

## 📜 Loot
- <title> — <1-line note>  [↗](<source_url>)
```

New-project file template:

```markdown
# <emoji> <Project Name>

## 📝 To Do's

## 💎 Shiny

## 🗺️ The Plan

## 📜 Loot
```

### Step 7 — Rebuild the index and stamp the dig

Regenerate `den/index.md`:

```markdown
<!-- last_dig: <CURRENT_ISO_DATETIME> -->
# 🦝 The Den

Last haul: <N> scraps · <N> shiny · <N> plan · <N> loot

| Project | Open To Do's |
|---|---|
| [<name>](<file>) | <count> |
```

Then report the haul in one line:
*"last haul: 3 scraps · 1 shiny · 1 plan → den"*.

---

## `/den` — glance at the den

Read `den/index.md` and the project files. Show the dashboard: projects, open
To Do counts, and the last-dig time. Don't read chats, don't write anything.

## `/sniff` — dry run

Run `/dig` Steps 1–5 but stop before writing. Show the haul, write nothing,
don't stamp the dig.

## `/feed <chat>` — dig one chat

Skip the "since last dig" window. Process only the chat the user points to,
then run Steps 3–7 on it.

## `/wash` — tidy the den

Re-read every project file, collapse exact and near-duplicate lines, drop
empty sections, and rebuild `den/index.md`. Show a short "washed: removed N
dupes" summary. Never delete a unique artifact.

## `/nap` — pause

Write `<!-- napping: true -->` to `den/index.md`. Skip scheduled/auto digs
until the next manual `/dig`, which clears it.

---

## Quality rules

**Keep:** explicit next actions, ideas with a concrete next step, a decided
plan, a real produced artifact (Loot).

**Skip:** general musing with no action, things discussed but not intended,
duplicates already in the den, low-level implementation detail (that's context,
not an artifact), final phrasings of bios/captions (not actionable).

**Confidence:** *high* = clear next action or concrete idea, mentioned 2+ times ·
*mid* = mentioned once with intent · *low* = passing mention, flag for review.

---

## Edge cases

- **No chats in window** → say so, suggest `/dig --days 14`.
- **No `den/` yet** → create it with an empty index, then proceed.
- **Too many candidates (>20)** → show high-confidence first, collapse the rest.
- **Project unclear** → drop into `den/inbox.md`, note the guessed project so the
  user can move it by hand.

## Optional parameters

| Param | Default | Effect |
|-------|---------|--------|
| `--days N` | since last dig | read chats from N days back |
| `--project NAME` | all | only stash into one project |
| `--dry-run` | false | same as `/sniff` |
