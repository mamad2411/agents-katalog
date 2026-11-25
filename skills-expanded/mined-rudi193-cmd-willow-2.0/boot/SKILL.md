---
name: boot
description: Willow 2.0 primary boot gate — reads contract, establishes context, checks fleet, loads continuity, persona, corrections, and stack before first response.
---
@markdownai

# /boot

> **Primary boot gate.** Run before producing any response to the user. A greeting, short message, or casual opening is not an exception — boot first.
>
> **Exceptions (narrow — only these two; the agent does not classify a turn as exempt on its own judgment):**
> - User is in a physical, mental, or personal emergency — respond immediately, boot after.
> - User explicitly says to skip it ("sandbox", "load without context", "no startup", or equivalent) — acknowledge and proceed without boot.

---

## Pre-session (fires automatically — no action needed)

These run before your first turn via hooks:

| Hook | What it does |
|---|---|
| **SessionStart** | Hardware scan · willow_status · jeles registration · dispatch subscribe · heartbeat · corpus corrections seeded from memory feedback files · stack snapshot read from SOIL · anchor written to `$WILLOW_HOME/session_anchor_{agent}_{project}.json` (or `session_anchor_{agent}.json` when project is unknown) |
| **prompt_submit (turn 1)** | Persona picker injected · boot guard injected · dispatch inbox injected |

---

## Config mode

`link_fleet_home` (or `bash setup.sh`) prints the active tier:

| Mode | When | Boot behavior |
|------|------|---------------|
| `private-config` | `~/github/.willow/willow.md` present | Full fleet: KB, handoffs, Grove |
| `public-fallback` | No private willow-config | Contract + skills + MCP template only |
| `degraded` | MCP or Postgres unreachable after boot starts | Continue with local contract |

In **public-fallback**: KB search, handoffs, and Grove are optional — not hard prerequisites.
In **private-config**: Postgres down remains a hard stop (step 3).

---

## Boot phases

Boot runs in **three phases**. The PreToolUse hook enforces them:

| Phase | Sentinel | Tools unlocked |
|-------|----------|----------------|
| **1 — Persona** | `willow-persona-done-{agent}-{session}.flag` | Read `boot.md`, `willow.md`, `personas/*.md`, `skills/*-boot.md`; Write persona sentinel only |
| **2 — Fleet boot** | *(persona sentinel must exist)* | **All MCP / Kart** + Read/Grep/Glob; shell and repo writes still blocked |
| **3 — Done** | `willow-boot-done-{agent}-{session}.flag` | Everything |

> **`{agent}` = fleet identity** (`WILLOW_AGENT_NAME` / `.willow/active-agent`) — never the persona.
> Persona is voice only; SOIL, handoffs, ledger, and sentinels key off the fleet id.

> **Digest fast path (warm boot).** Read `fast_path: yes|no` on the `[DIGEST]` block —
> **not** the `generated:` timestamp (always session-fresh; self-referential). When
> `fast_path: yes`, skip step 7 (handoff_latest), step 13 (stack snapshot), and
> `kb_startup_continuity` in step 14. When `fast_path: no`, run those cold-boot steps.

---

## Phase 1 — Persona (before MCP)

**1. Persona picker**
The hook injects the picker on turn 1. Render it visibly. User confirms with a number, name, or **`continue`** (keeps active persona). On confirm the hook writes the **persona-done** sentinel automatically.

**2. Persona boot overlay**
Read `willow/fylgja/skills/{persona}-boot.md` when it exists (voice/posture only).

**3. Boot guide**
Read this file (`boot.md`) for the full checklist.

**If `[PERSONA-GATE]` is in context:** show only the picker; wait for confirm — do not call MCP yet.

---

## Phase 2 — Fleet boot (MCP; persona sentinel required)

**4. Contract**
`mai_read_file("willow.md")` — fleet contract. Fallback: Read the raw file.

**5. Local context** *(compact)*
Fleet agent · repo root · branch · dirty-file counts · one-line diff note. No full patches.

**6. Fleet health** *(parallel with 7–9)*
`willow_status(app_id=<agent>)` — Postgres, SOIL, Ollama. **Postgres down = hard stop** in private-config.

**7. Continuity** *(cold boot only — skip on digest fast path)*
`handoff_latest(app_id=<agent>, workspace=<repo root>)` — project-scoped only.

**8. Grove inbox** *(parallel)*
`grove_get_history` on agent channel · dispatch inbox file if present.

**9. KB topic** *(parallel)*
`willow_find(scope=kb, query=<topic from user message>)` — strip filler; search the noun.

**9b. Dream gate** *(optional boot-report line)*
`dream_check(app_id=<agent>)` — one line if due.

**9c. KB tone modes** *(optional)* — Direct / Bridge / Sideways / Story seed / One-liner when surfacing KB hits.

**10. Corrections + preferences**
`soil_list(collection="corpus/corrections")` and `corpus/preferences`.

**11. Open initiatives**
`soil_list({agent}/overseer)` → `status != "closed"`.

**12. Ledger** *(mandatory)*
`ledger_read(project=<agent>, limit=3)`.

**13. Stack snapshot** *(cold boot only — skip on digest fast path)*
SOIL `{agent}/stack/current` — fleet id, not persona.

**14. KB continuity + registry orientation** *(cold boot only for kb_startup_continuity)*
`kb_startup_continuity(app_id=<agent>)` when no fresh digest.

| File | What it contains |
|---|---|
| `willow/fylgja/skills/mcp-first.md` | **MCP before grep/Bash** — login, manifest, operator voice sources |
| `sap/mcp_registry.json` | MCP tools by domain |
| `willow/fylgja/powers/registry.json` | Named powers |
| `docs/INDEX.md` | Doc router |

**15. Flag triage**
`soil_list({agent}/flags, filter={"flag_state": "open"})` — max 5.

---

## Phase 3 — Close (write boot-done)

**16. Boot report + final sentinel**

Render persona picker (confirmed state), then compact status lines:

- **Fleet:** Postgres · Ollama · manifests
- **Branch:** branch · dirty summary
- **Threads:** count — top item
- **Corrections:** count loaded
- **Next:** next_bite ≤120 chars

Then write the **boot-done** sentinel: `Write` to the exact path from `[BOOT]` / PreToolUse messages (`/tmp/willow-boot-done-{agent}-{session}.flag`, content `booted`).

Then respond to the user.

---

## Rules

- **Phase order is enforced:** persona → MCP boot → boot-done sentinel.
- MCP in phase 2; Kart for shell until boot-done.
- Postgres down = hard stop in **private-config** only. Public-fallback may continue degraded.

- Grove unavailable = degraded, not fatal. Continue.
- Never report "postgres unknown" without probing first (phase 2 fleet step).
- Compact summaries only — no full diffs, no full handoff content.
- Persona picker and `[PERSONA-IDENTITY]` banner must be visible in the boot response — hook injection is system-only. Never imply persona switch changed fleet agent id.
- No hardcoded names or paths — use `[user]`, `[agent]`, env vars, or parameters.
- If anchor missing or stale (> 2h): run /startup after for deeper recovery.
- Open the **git repo root** for IDE folder scoping (not a parent like `~/github/`).
- Handoff/DB timestamps are **UTC**; `[CLOCK]` in hooks states local offset.

## Handoff authoring — v2 schema

Write session handoffs to `$WILLOW_HOME/handoffs/{agent}/` — **not** `docs/handoffs/` (that directory contains old-format files and will produce the wrong schema). Artifact templates: `docs/templates/README.md`.

Filename pattern: `session_handoff-{date}{letter}_{agent}.md` (e.g. `session_handoff-2026-05-26d_hanuman.md`).

```markdown
---
agent: {agent}
date: {YYYY-MM-DD}
session: {YYYY-MM-DD}{letter}
runtime: claude-code
format: v2
---

# HANDOFF: {one-line title}

## What I Now Understand

{One paragraph summary — what changed this session, what was resolved, what was discovered.}

## Open Threads

- **[label]** — description. Fix_path or next action ≤150 chars.

## What We Agreed On

- Bullet list of decisions, commitments, constraints that carry forward.

## 17 Questions

Q1: {open question — something unresolved that the next session should know about}
Q2: {open question}
...
Q16: {open question}
Q17: {next single bite — one sentence, no preamble}

## Agent Notes for Human

- {reminders, to-do's, stated unfinished tasks, patterns surfaced — max 17 lines}

## Human Notes to Agent

- {leave empty at close; the operator writes here afterward — handoff_latest reads it live from the file at next boot}

## Machine block for handoff_rebuild / kb_ingest

```json
{"summary": "", "open_threads": [], "agreements": [], "key_actions": [], "next_steps": [], "tools_used": [], "signals": {}}
```
```

**Required:** `format: v2` and `session:` in frontmatter. Without them `handoff_latest` will not surface this file.
**Required:** Section headers must match exactly — `## What I Now Understand`, `## Open Threads`, `## What We Agreed On`, `## 17 Questions`, `## Agent Notes for Human`, `## Human Notes to Agent`, `## Machine block …`.
**Required:** Q17 line must be `Q17: <text>` — no question mark in the key, colon-delimited, no preamble. Q17 is always "What is the next single bite?" answered.
**Convention:** Q1-Q16 are open questions for the next session — things unresolved, decisions pending, gates not yet crossed. Write as many as are genuinely open (pad to 17 only if needed). Q17 is always the next action.

After writing, run `handoff_rebuild(app_id={agent})` then verify with `handoff_latest(app_id={agent}, workspace=<repo root>)`.

---

## Recovery

If continuity is the bottleneck (pick up where we left off, no fleet gate): run `/cold-recovery` — see `willow/fylgja/skills/cold-recovery.md`.

If boot is degraded or the anchor is stale: run `/startup`. That skill handles anchor recovery, KB continuity, ledger check, and flag triage at depth.

## Claude Code registration

`Skill(skill='boot')` resolves via the Fylgja plugin layout:

- `willow/fylgja/skills/.claude-plugin/plugin.json`
- `willow/fylgja/skills/commands/boot.md` → symlink to `boot.md`

Re-wire after pull: `./willow.sh agents install <agent> --ide claude` then `/reload-plugins` in Claude Code if skills still show unknown.
