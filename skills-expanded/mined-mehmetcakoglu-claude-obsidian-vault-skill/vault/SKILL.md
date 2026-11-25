---
name: vault
description: |
  Hybrid knowledge vault system (Obsidian-compatible markdown wikis) that archives Claude Code sessions, architectural decisions, bugs, domain concepts, entities, and reusable patterns. Two vaults coexist: a global vault (`~/Global Claude Vault/`) for cross-project knowledge and per-project vaults (`<project>/docs/vault/`) for project-specific knowledge. Implements the LLM-Wiki pattern (RAW → WIKI ← SCHEMA) with INGEST / QUERY / LINT operations — the LLM maintains a persistent, cumulative artifact that grows smarter with every session.

  Use this skill whenever the user:
  - Asks about past work, prior decisions, earlier bugs, or previous sessions ("what did we decide about X", "have we seen this bug before", "why did we go with Y")
  - Wants to persist context for the future ("remember this", "save this", "archive this", "don't forget", "add to the vault", "ingest it")
  - References the vault or archive explicitly ("vault", "wiki", "knowledge base", "archive")
  - Sets up a new project that should have a vault ("initialize vault", "/vault:init")
  - Asks to scan or ingest Claude Code sessions (`~/.claude/projects/*/*.jsonl`)
  - Reports a bug, makes an architectural decision, or discovers a reusable pattern worth recording
  - Wants cross-session continuity (remembering what was decided days or weeks ago)

  Proactively suggests recording when the user makes a decision, fixes a bug, or establishes a pattern that would be useful later. Uses the `/vault:init`, `/vault:scan`, `/vault:ingest`, and `/vault:batch-ingest` slash commands when they match cleanly, but performs ingest/query/lint operations directly when the user's request doesn't map to a command.
---

# Vault Skill — Hybrid Knowledge Archive

## System architecture

Two vaults coexist:

| Vault | Location | Content |
|---|---|---|
| **Global** | `~/Global Claude Vault/` (configurable via `$CLAUDE_VAULT`) | Cross-project knowledge: Claude Code patterns, general workflows, domain-agnostic lessons, personal preferences |
| **Project** | `<project-root>/docs/vault/` | Project-specific knowledge: domain rules, architectural decisions, bugs, entities, feature history |

Both use the LLM-Wiki pattern (Obsidian-compatible markdown, YAML frontmatter, `[[wiki-link]]` cross-refs). This pattern was introduced by **Selma Kocabıyık** in the [knowledge-pipeline](https://github.com/selmakcby/knowledge-pipeline) repository; this skill adapts it to Claude Code with auto-scanning and hybrid scoping.

**Constitution files (schema):**
- Global: `~/Global Claude Vault/CLAUDE.md`
- Project: `<project-root>/docs/vault/CLAUDE.md`

Always read the relevant `CLAUDE.md` before operating on a vault — the schema lives there and may have evolved since this skill was installed.

## Slash command surface

| Command | Purpose |
|---|---|
| `/vault:init` | Bootstrap a new project's vault skeleton (run once per project) |
| `/vault:scan` | Scan `~/.claude/projects/*/*.jsonl` and update the pending-ingest queue |
| `/vault:ingest` | Process the next pending session into the appropriate vault following LLM-Wiki INGEST rules |
| `/vault:batch-ingest [N]` | Process up to N pending sessions in one run (default 5, `all` for the full queue); stops early if context window approaches capacity |

A `SessionStart` hook runs `vault-context.py` **synchronously** on every new session. It scans the queue, auto-creates a project entity if one doesn't exist, then injects the vault index + project entity + recent sessions into Claude's context as a `system-reminder`. This means Claude already has relevant decisions and lessons loaded before the first user message — manual `/vault:scan` is rarely needed.

If `auto_ingest=true` is set in `~/Global Claude Vault/vault-config.json`, the hook also instructs Claude to drain the pending queue automatically at session start (respecting `auto_ingest_max_per_session`).

**Session registry**: `~/Global Claude Vault/state/ingested.txt` — shared between both vaults. After any ingest (global or project) the session ID is appended here so the scan never proposes it again.

## Which vault? (routing rule)

When the user asks to record something, pick the target vault using:

| Content | Target |
|---|---|
| Project-specific domain knowledge, architecture, bug, entity | **Project** (`docs/vault/`) |
| Project stack-specific preference or pattern | **Project** |
| Cross-project Claude Code pattern (hooks, skills, MCP) | **Global** (`~/Global Claude Vault/`) |
| General git, CI, testing, or tooling workflow | **Global** |
| Personal style, role preferences, collaboration defaults | **Global** |
| Confidential / NDA material | **Neither** (out of scope) |

When in doubt, read both vaults' `CLAUDE.md` "Scope" / "Out of scope" sections.

## Workflows

### INGEST (source → pages)

When importing a session, PR, bug report, or decision source into a vault:

1. Parse the source. For large JSONL files, use a sandbox execution tool (`ctx_execute`, `ctx_execute_file`, or a local python helper) — never read multi-megabyte transcripts into the model's context.
2. Present a 5–7 bullet summary to the user; wait for approval.
3. After approval, write pages in the appropriate directories:
   - `sources/sessions/YYYY-MM-DD-<slug>.md` (always, for session ingests)
   - `decisions/YYYY-MM-DD-<slug>.md` (for architectural decisions)
   - `bugs/<slug>.md` (for bug + fix pairs; project vault)
   - `entities/<slug>.md` (for new or changed entities)
   - `concepts/<slug>.md` (for new domain concepts)
   - `lessons/<slug>.md` (global vault; root cause + prevention)
4. Update `index.md` and `log.md`.
5. Append the session ID to `~/Global Claude Vault/state/ingested.txt`.
6. Commit with the `docs(vault):` prefix.

**Atomicity rule**: one decision = one page; one bug = one page. Do not merge.

### QUERY (question → answer)

When the user asks a question (even when not explicitly about the vault):

1. Read the relevant `index.md` (global, project, or both).
2. Open the linked pages (sources, entities, decisions, concepts, lessons, bugs).
3. Synthesize the answer with source citations (`[[sources/...]]`).
4. If the synthesis is novel, file it back as `syntheses/YYYY-MM-DD-<slug>.md`.
5. Log filed-back queries in `log.md`.

### LINT (health check)

When the user invokes `/vault:lint` or asks "check the vault":
- Orphan pages (no inbound links)
- Stale claims (60+ days `active` contradicting newer sources)
- Missing concepts (referenced in 3+ pages, no page of their own)
- One-way links (A→B but not B→A)
- Code reference drift (`related_code` paths that no longer exist)
- Duplicate entities

Produce a report at `syntheses/lint-YYYY-MM-DD.md` and log it.

## Hard rules (inviolable)

1. **`raw/` is immutable**. Source files never change; symlinks preferred, JSONLs gitignored.
2. **No sourceless claims**. Every page has a `source` frontmatter field and a `## Sources` section.
3. **No deletions**. Outdated pages move to `archive/` — git history already preserves them.
4. **Contradictions are visible**. Conflicting sources trigger a `## CONFLICT` section that survives even after resolution (mark `## RESOLVED (YYYY-MM-DD)` instead).
5. **`index.md` is updated on every ingest/lint**. It is the search surface at small-to-medium scale.
6. **File names are kebab-case ASCII**. No spaces, no non-ASCII characters — transliterate as needed.
7. **Security**: API keys, tokens, passwords, production IPs, database credentials are **never** written to any vault page. Use placeholders like `stored in env`, `redacted`, etc.
8. **Commit policy**: vault commits use the `docs(vault):` prefix so they can be filtered in PR review.
9. **Cross-vault purity**: project-specific knowledge does not live in the global vault, and vice versa. Link across instead of duplicating.
10. **Vault language**: the vault owner picks a single primary language and stays consistent across pages; technical terms may remain English in non-English vaults.

## Page format (all types)

```markdown
---
title: Page title
tags: [tag1, tag2]
source: "sources/sessions/YYYY-MM-DD-<slug>.md"
date: YYYY-MM-DD
status: draft | active | archived
related_code: "path/to/file.py:line_range"  # optional, project vault
session_size: "30M, 3451 messages"          # only for sources/sessions/
---

# Page title

Body. Every non-trivial claim points to a source (`[[sources/...]]` or external URL).

## Sources
- [[sources/sessions/...]]

## Related
- [[entities/...]]
- [[concepts/...]]
```

### Sections by page type

- **sources/sessions/** — Purpose · What happened · Files touched · Decisions · Bugs/fixes · Open questions
- **decisions/** — Context · Decision · Alternatives · Rationale · Affected code · Consequences
- **bugs/** — Symptoms · Reproduction · Root cause · Fix (commit hash) · Regression test · Prevention
- **entities/** — Definition · Responsibility · Related files · Relationships · Key decisions
- **concepts/** — Definition · Rule/formula · Examples · Related entities · Rationale
- **lessons/** (global) — Symptoms · Root cause · Fix · Prevention

## Behavior heuristics

### When to proactively suggest recording
- The user reaches a decision ("let's go with X") → offer `decisions/`
- A bug is diagnosed and fixed → offer `bugs/` (with fix commit hash)
- A domain concept crystallizes ("so taksit means…") → offer `concepts/`
- A long session is about to be compacted → offer to queue it for ingest

### When to stay silent
- One-shot trivial questions (no durable knowledge to capture)
- Exploratory code reading with no decisions made
- User has explicitly said "don't log this" or similar

### When to consult the vault
- **At session start**: vault context is auto-injected via `SessionStart` hook — read the `<vault-context>` block in the system prompt before answering any coding question
- User uses temporal cues ("earlier", "last week", "that decision") → check `index.md` first
- A bug is reported → search `bugs/` and `lessons/` for similar
- A project-specific question → project vault first, global vault fallback
- A cross-project question → global vault first
- Before starting a coding task → check `decisions/` and `lessons/` for relevant context

## Related tooling

- `~/Global Claude Vault/scripts/vault-context.py` — synchronous SessionStart hook: scans queue, auto-creates project entity, injects vault context into session
- `~/Global Claude Vault/scripts/scan-sessions.py` — JSONL scanner; writes sorted pending queue (cross-platform Python)
- `*.sh` / `*.ps1` wrappers — thin callers for Unix and Windows PowerShell respectively
- `~/.claude/commands/vault/{init,scan,ingest}.md` — slash command definitions
- `~/Global Claude Vault/state/ingested.txt` — shared session ID registry (global + all project vaults)
- `~/.claude/settings.json` `SessionStart` hook — runs `vault-context.py` synchronously on every new conversation

## Out of scope (use other mechanisms instead)

- **Runtime instructions** ("always use sonnet 4.6") → `~/.claude/CLAUDE.md`, not the vault
- **Ephemeral conversation state** → `TodoWrite`, plan mode, or memory files
- **Short lookup pointers** → `~/.claude/projects/.../memory/MEMORY.md`
- **Confidential / NDA content** → does not belong in any shared vault

## One-line summary

When a decision, bug, or concept surfaces, write an **atomic page** to the **right vault** (global or project), cite every claim, update `index.md` and `log.md`, then commit with `docs(vault):`.

## Credits

- **LLM-Wiki pattern** — introduced by [Selma Kocabıyık](https://github.com/selmakcby) in [knowledge-pipeline](https://github.com/selmakcby/knowledge-pipeline). This skill reuses her RAW→WIKI←SCHEMA architecture and the INGEST / QUERY / LINT operations.
- **Claude Code packaging** — slash commands, auto-scan, hybrid global+project scoping, session registry by [Mehmet Çakoğlu](https://github.com/mehmetcakoglu) in [claude-obsidian-vault-skill](https://github.com/mehmetcakoglu/claude-obsidian-vault-skill).
