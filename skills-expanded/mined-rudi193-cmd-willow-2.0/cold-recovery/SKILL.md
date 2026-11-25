---
name: cold-recovery
description: Cold instance context recovery — five-step continuity pass with runtime-specific index adapters. Use when picking up work across sessions without full boot.
---

# /cold-recovery

> **Continuity gate.** Reconstruct session state before first response. Lighter than `/boot` — no fleet hard-stop, no persona picker, no sentinel.
>
> **When to run:**
> - User says "keep working", "pick up where we left off", or pastes the cold-recovery protocol
> - New session after runtime switch (claude.ai ↔ Claude Code ↔ Cursor)
> - Agent detects cold start and continuity is the bottleneck (not infrastructure)
>
> **When not to run:**
> - User explicitly skips context ("sandbox", "load without context", "no startup", "don't run boot") — run cold-recovery only; do **not** run `/boot`
> - Infrastructure is the question — use `/boot` or `/startup` instead
> - Physical or personal emergency — respond first, recover after

---

## Relationship to boot

| | **Cold recovery** | **Boot (`/boot`)** |
|---|---|---|
| Steps | 5 | 14 |
| Postgres gate | No hard stop | Hard stop if down |
| Grove / ledger / SOIL stack | Skip unless a gap requires it | Full pass |
| Persona picker | Skip unless user asks | Render picker |
| Primary source | Conversation + indexes | Infrastructure + handoffs |
| Latency target | One parallel batch | Full fleet orientation |

**Rule:** Cold recovery answers *"where were we?"* Boot answers *"is the fleet healthy and wired?"*

Use cold recovery when continuity is the bottleneck. Use boot when infrastructure is the bottleneck. They are not replacements for each other.

---

## Step 0 — Detect runtime

Identify which index layer exists. **Do not assume** claude.ai native tools.

| Runtime | Signals | Index layer |
|---------|---------|-------------|
| **claude.ai (web)** | `recent_chats`, `conversation_search` in tool list | Platform thread index |
| **Claude Code** | CLI, `~/.claude/projects/`, hooks | Transcripts + handoffs + history |
| **Cursor** | Cursor hooks, `[CROSS-RUNTIME]` in anchor | Same as Claude Code + cross-runtime block |
| **Codex / other** | Read tool + MCP available | Handoffs + git + KB search |

If native tools exist → use them (Step 1–2 branches below).
If not → **do not stop**. Switch to the substitute index. Missing native tools triggers substitute lookup, not abort.

---

## Parallel batch (CLI runtimes — run before writing Step 1)

Run in parallel where marked:

```
handoff_latest(app_id=<agent>)
handoff_search(app_id=<agent>, query=<topic from user message>, limit=5)
git branch --show-current && git log -3 --oneline
```

Also use (no MCP required):
- `[CROSS-RUNTIME]` block from SessionStart anchor — already injected; do not re-fetch
- Last ~20 lines of `~/.claude/history.jsonl` if present
- Newest 1–2 agent transcript JSONL files under the IDE projects folder

Add only if Step 2 pointer requires verification:
```
gh pr view <n> --json state
kb_search(app_id=<agent>, query=<topic>, limit=5, continuity=true)
Grep session JSONL for closing exchange
```

**Stop condition:** Steps 1–5 complete. Do not proceed to implementation unless the user directs a thread.

---

## Step 1 — Recent state

**Intent:** What was happening? Reverse chronological. Terminal state first.

### claude.ai (web)

```
recent_chats(n=5)
```

Read newest first. Note: last user message, last assistant action, whether the thread closed cleanly.

### Claude Code / Cursor (substitute)

| Source | What it gives |
|--------|---------------|
| `[CROSS-RUNTIME]` in SessionStart anchor | Compressed recent sessions across IDE/CLI |
| `handoff_latest(app_id=<agent>)` | Last documented session close |
| `~/.claude/history.jsonl` (tail) | User message timeline across sessions |
| Agent transcript JSONL (newest 1–2) | Full closing exchanges |
| `git branch` + `git log -3` | Repo terminal state |

**Synthesis rule:** Build a table: `# | runtime | session | terminal state`. Newest row = what happened immediately before this message.

**Do not** treat "tools don't exist" as completion of Step 1.

---

## Step 2 — Topic threads

**Intent:** Locate thread clusters. Pointer layer only — don't read everything.

### claude.ai (web)

```
conversation_search("<project or topic>")
```

One search per active topic. Record thread id/title, where it lives, one-line status.

### Claude Code / Cursor (substitute)

| Tool / source | Query pattern |
|---------------|---------------|
| `handoff_search(app_id, query=<topic>, limit=5)` | Project names from user message or Step 1 |
| `kb_search(app_id, query=<topic>, limit=5, continuity=true)` | Canonical decisions only |
| Grep `$WILLOW_HOME/handoffs/<agent>/` | Filename + summary match |
| Grep `~/.claude/projects/` session JSONL | Session ids tied to topic |

**Output:** pointer table only.

| Topic | Where it lives | Status pointer |
|-------|----------------|----------------|
| *example* | path or handoff filename | one-line status |

Stop at pointers. Full reads happen in Step 3.

---

## Step 3 — Calibration

**Intent:** The last session's **closing exchange** is current state. Everything before it is history.

### All runtimes

1. Open the **newest relevant** session for the active topic (from Step 2).
2. Read the **last 3–5 turns** — user message + assistant response.
3. Extract:
   - What the user asked for last
   - What the agent delivered or failed to deliver
   - Explicit "next bite" if stated

### Source priority (when multiple exist)

1. **Live thread** (claude.ai or current JSONL transcript) — most authoritative for tone and intent
2. **`handoff_latest`** — most authoritative for structured open threads
3. **Cross-runtime hook summary** — fast pointer; verify if stale

### Conflict rule

If handoff says X is open but git/PR/gh says X is closed → flag staleness in Step 4. Thread closing exchange wins on *intent*; external verification wins on *facts*.

---

## Step 4 — Gaps

**Intent:** What was explicitly left open, deferred, or unknown.

Extract from Step 3 closing exchange + handoff `open_threads`:

| Gap type | Examples |
|----------|----------|
| **Blocking** | Needs user action (browser devtools, API key, decision) |
| **Deferred** | Acknowledged but deprioritized |
| **Unknown** | Root cause unconfirmed |
| **Stale** | Documented open but externally resolved (e.g. PR merged) |
| **Meta-gap** | Previous session didn't document parallel threads |

If the previous session wrote no handoff and left no closing exchange → **record that as a gap**.

Do not invent gaps. Do not collapse gaps into tasks unless the user asks.

---

## Step 5 — Register

**Intent:** How did the person arrive vs how they usually arrive? Adjust tone and scope before acting.

Observe:

| Signal | Usual | Tonight |
|--------|-------|---------|
| Opening shape | Task directive | ? |
| Boot / recovery | Implicit or `/boot` | Explicit skip or protocol paste? |
| Persona | Builder | Witness / other? |
| Thread count | One product thread | One or many? |
| Mode | Execute | Observe / compare / test? |

**Adjustment rules:**

- Protocol paste without task → recover first, don't build
- "don't run boot" → cold recovery only; no fleet gate drama
- "test something" → name what is being tested; don't treat as production work
- Multiple parallel threads → Step 2 must list all; Step 5 must not assume one

End Step 5 with: **one-line current state** + **ask which thread to pick up** (not a long menu).

---

## Output format (mandatory)

Deliver all five steps visibly. The user should see the recovery pass, not just conclusions.

```markdown
## Step 1 — Recent state
[table, reverse chronological]

## Step 2 — Topic threads
[pointer table]

## Step 3 — Calibration
[closing exchange — quoted or paraphrased tightly]

## Step 4 — Gaps
[categorized list]

## Step 5 — Register
[how arrived vs usual + adjustment taken]

---
**Current state (one line):** …
**Pick up:** …
```

Then respond to the user. Do not start implementation unless directed.

---

## Rules

- MCP tools at every step where available. Read/Grep/shell only when MCP confirmed unavailable or for transcript paths MCP does not index.
- Postgres down is **not** a hard stop for cold recovery (unlike boot). Note it in Step 4 if relevant to the active thread.
- Compact summaries only — no full diffs, no full handoff dump.
- No hardcoded agent names — use `<agent>`, `[user]`, env vars, or parameters.
- If handoff is stale (> 2h): note it in Step 4; prefer transcript closing exchange for calibration.
- Native tools missing → substitute index (Step 0). Never abort at Step 1.

---

## Failure modes

| Failure | Response |
|---------|----------|
| Native tools missing | Switch to substitute index — not "can't execute" |
| Handoff stale (>2h) | Note staleness; prefer transcript closing exchange |
| Handoff vs git/gh conflict | Flag in Step 4; one external verification |
| No handoff exists | Step 4 gap: "continuity not documented" |
| Multiple parallel threads | Step 2 lists all; Step 5 does not assume one |

---

## Why CLI runtimes need this adapter

claude.ai holds conversation context as a platform primitive — `recent_chats` and `conversation_search` index it directly.

Claude Code and Cursor are stateless at session open. Willow's handoffs, transcript JSONL, cross-runtime hooks, and MCP search functions act as a **multi-index substitute** when native tools are absent.

The compensation layer (handoffs, hooks, transcripts) is what makes CLI cold recovery work. Strip it and CLI runtimes only have the current message — unless `/boot` runs.

---

## Stack placement

```
User opens session
    ↓
Hook injects: [CROSS-RUNTIME] + corrections
    ↓
User: "keep working" OR agent detects cold start
    ↓
/cold-recovery  (5 steps, runtime branch)
    ↓
User picks thread
    ↓
Optional: /boot if infra work needed
    ↓
Optional: /startup if anchor stale or boot degraded
```

---

## Recovery escalation

| Condition | Next skill |
|-----------|------------|
| Continuity restored, ready to work | Proceed on chosen thread |
| Infrastructure question | `/boot` |
| Anchor missing/stale, deeper continuity needed | `/startup` |
| Session end, structured handoff needed | `/shutdown` (handoff write is step 2) |
