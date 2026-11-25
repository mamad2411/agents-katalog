---
name: doc-harness
description: "Document-based project control that lets any AI agent or human resume work from files alone — no external memory needed. Use whenever the user wants to structure a long-running project, track progress across sessions, recover state after context loss, coordinate multiple agents, audit documentation health, or stop forgetting what was done last session. Triggers include '/doc-harness init' and '/doc-harness check' (slash commands) and phrases like 'help me set up this project', 'I keep losing track', 'my agent forgets between sessions', 'organize my project docs', 'audit this project', 'what did we do last time'."
argument-hint: "init [project-name] [description] | check | sync [--auto] | flush [--auto] | recall [query] | resume [--auto]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
license: MIT
---

# Doc Harness — Document-Based Project Control

Doc Harness keeps a project resumable purely from files: a brand-new agent, after any context break, reads the entry and takes over correctly.

It maintains, per project:

- **CLAUDE.md** — single authoritative entry: AGENT IDENTITY LOCK + stable anchor (framework anchor, iron rules, bottom-line principles) + operational rules.
- **AGENTS.md** — thin pointer to CLAUDE.md (never a stale copy).
- **events.log** — append-only event log: the single source of both history and current state.
- **CURRENT_STATUS.md** — a **generated projection** of `events.log` (`## NOW` + work surface + dead ends); never hand-edited.
- **FILE_INDEX.md** — file catalog; unregistered files are a red item.
- **DOC_HARNESS_SPEC.md** — optional reference copy of the specification.

Optional: `PHILOSOPHY.md` (bottom-line principles), `PARKING_LOT.md`, `RUNBOOK.md`, and inter-project `inbox/`/`outbox/` (plus an optional `MAIL_LEDGER.md`).

Core principle: **handoff over writing** — a new agent must be able to take over correctly from files alone. State changes are one `record` command; the deterministic toolbelt (`tools/`) verifies the document system's integrity.

## Invoking it (agent-agnostic)

The commands below describe **outcomes**, not a proprietary feature. How you invoke them depends on the agent you are using:

| Agent | How to invoke |
|-------|---------------|
| Claude Code | `/doc-harness check` (plugin slash command) |
| Kimi CLI | `/skill:doc-harness` loads this skill; then ask in natural language ("check this project's doc health") |
| Any other agent | natural language — "resume this project", "flush the doc state", "why did we choose X?" |

Nothing in this skill depends on an agent-specific feature: it is Markdown, plus an optional PowerShell toolbelt.

## Commands

### `/doc-harness init [project-name] [description]`

Create the files for a new project (clean init or mid-project adoption).
**→ See [init.md](init.md).**

### `/doc-harness check`

Audit health: projection freshness (now_refreshed vs events.log), unregistered files (red), entry uniqueness, `events.log` well-formedness, inbox, ops-rules version, identity lock, stale conclusions (`conclusion_until`), provenance class (`class=root|decision|reported`); then reflect on the anchor and bottom-line principles.
**→ See [check.md](check.md).**

### `/doc-harness sync [--auto]`

Repair drift: register files, append any missing state events to `events.log`, re-project `CURRENT_STATUS`, inbox housekeeping. `interactive` (default) asks before state changes; `auto` executes safe fixes.
**→ See [sync.md](sync.md).**

### `/doc-harness flush [--auto]`

Emergency save before compaction/session end: run sync, then **mandatorily** inventory context, write/register extracted items, verify a fresh arrival can find them, and **append the state events + re-project** last.
**→ See [flush.md](flush.md).**

### `/doc-harness recall [query]`

Retrieve information: Layer 0 stable anchor → Layer 1 `## NOW`/work surface → Layer 2 `events.log` (history) → Layer 3 FILE_INDEX → Layer 4 files. Read-only, source-cited. Mechanical grep via `tools/search.ps1`.
**→ See [recall.md](recall.md).**

### `/doc-harness resume [--auto]`

Structured, verifiable takeover: identity → stable anchor → current state from `events.log` (verified fresh) → read-first list → dead-end ledger; then a Recovery Report + 5-question verification + proceed/wait decision. If context is empty or the user says "resume", run this.
**→ See [resume.md](resume.md).**

### `/doc-harness` (no arguments)

Inspect the directory: all core files → suggest `check`; none → suggest `init`; partial → suggest `init` mid-project mode. Then show this help.

## Deterministic Toolbelt (`tools/`)

Plain PowerShell, tool-agnostic. The key entry is `record.ps1` (one-step state change: append event + re-project + conformance). Others: `project.ps1`, `search.ps1`, `conformance.ps1`, `now-verify`, `encoding-guard`, `unregistered`, `dead-pointer`, `cite-check`, `stale-check`, `recurrence`, `nested-git-guard`, `stale-writer-guard`, `batch-register`, `telemetry`, and the mail family (`mail-daemon`, `mail-send`, `mail-poll`, `mail-ledger`).

**Where it lives**: the toolbelt ships **inside this skill folder** (`tools/`, so any install — plugin
marketplace, `cp -r`, or a Kimi CLI copy — carries it), and the repository keeps the canonical copy at
its root. Run it with `-ProjectRoot <your project>`:

```powershell
powershell -File <this skill folder>/tools/record.ps1 -ProjectRoot C:\path\to\your\project -Verb close -Text "T3 evidence=docs/t3.md class=root"
```

It is still **optional**, and it is worth knowing exactly what weakens without it: (a) the guards that
turn drift into a red signal are gone, and (b) the projection has to be written by hand instead of
generated — the one thing v2 exists to avoid.

## Reference Documents

- [init.md](init.md) · [check.md](check.md) · [sync.md](sync.md) · [flush.md](flush.md) · [recall.md](recall.md) · [resume.md](resume.md) · [operational_rules.md](operational_rules.md) · [spec.md](spec.md) (authoritative).
